import sys
import numpy as np
import NDIlib as ndi
from PyQt5.QtCore import QTimer, Qt,pyqtSignal, QObject
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtQuick import QQuickImageProvider
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
import time

class NDIImageProvider(QQuickImageProvider):
    """Image Provider to serve frames to QML UI."""
    def __init__(self):
        super(NDIImageProvider, self).__init__(QQuickImageProvider.Image)
        self.image = QImage()

    def requestImage(self, id, size, requestedSize=None):
        print("Requested")
        print(f"Image: {self.image.byteCount()}")
        return self.image, self.image.size()

    def update_image(self, qimg):
        self.image = qimg

class FrameNotifier(QObject):
    # Signal to notify QML when a new frame is ready
    frameChanged = pyqtSignal()

class NDIStreamApp:
    def __init__(self):
        # Initialize the application and NDI
        self.app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine()

        # Set up NDI
        if not ndi.initialize():
            print("Failed to initialize NDI.")
            sys.exit(1)

        self.ndi_recv = self.initialize_ndi_receiver()

        self.notifier = FrameNotifier()

        # Set up QML Image Provider for passing NDI frames
        self.image_provider = NDIImageProvider()
        self.engine.addImageProvider("ndiImageProvider", self.image_provider)
        self.engine.rootContext().setContextProperty("frameNotifier", self.notifier)
        # Timer to update frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)  # Update every 30ms

        

        # Load QML file
        self.engine.load('ndi_3.qml')
        if not self.engine.rootObjects():
            sys.exit(-1)

        

    def initialize_ndi_receiver(self):
        # Create NDI find object
        ndi_find = ndi.find_create_v2()

        if ndi_find is None:
            print("Failed to create NDI find object.")
            sys.exit(1)

        # Look for NDI sources
        sources = []
        while len(sources) == 0:
            print('Looking for NDI sources...')
            ndi.find_wait_for_sources(ndi_find, 1000)
            sources = ndi.find_get_current_sources(ndi_find)

        print(f"Found source: {sources[0].ndi_name}")

        # Create NDI receiver
        ndi_recv_create = ndi.RecvCreateV3()
        ndi_recv_create.color_format = ndi.RECV_COLOR_FORMAT_BGRX_BGRA
        ndi_recv = ndi.recv_create_v3(ndi_recv_create)

        if ndi_recv is None:
            print("Failed to create NDI receiver.")
            sys.exit(1)

        # Connect to the first source
        ndi.recv_connect(ndi_recv, sources[0])
        ndi.find_destroy(ndi_find)
        return ndi_recv

    def update_frame(self):
        t, video_data, _, _ = ndi.recv_capture_v2(self.ndi_recv, 5000)

        if t == ndi.FRAME_TYPE_NONE:
            print('No data received.')
            return

        if t == ndi.FRAME_TYPE_VIDEO:
            #print(f'Video data received: {video_data.xres}x{video_data.yres}')
            self.display_frame(video_data)
            ndi.recv_free_video_v2(self.ndi_recv, video_data)

    def display_frame(self, video_frame):
        # Convert NDI frame data to numpy array
        width, height = video_frame.xres, video_frame.yres
        video_data = np.copy(np.frombuffer(video_frame.data, dtype=np.uint8))
        video_data = video_data.reshape((height, width, 4))  # BGRX format

        # Convert the numpy array to QImage
        qimg = QImage(video_data, width, height, QImage.Format_RGB32)

        # Update the QML Image Provider with the new frame
        self.image_provider.update_image(qimg)

        self.notifier.frameChanged.emit()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    ndi_app = NDIStreamApp()
    ndi_app.run()
