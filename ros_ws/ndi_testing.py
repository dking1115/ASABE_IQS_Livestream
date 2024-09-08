import sys
import numpy as np
import NDIlib as ndi
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

class NDIStreamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set up the UI
        self.setWindowTitle("NDI Stream Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel("Waiting for NDI stream...", self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize NDI
        if not ndi.initialize():
            print("Failed to initialize NDI.")
            sys.exit(1)

        self.ndi_recv = self.initialize_ndi_receiver()

        # Timer to update frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)  # Update every 30ms

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
        t, video_data, audio_data, _ = ndi.recv_capture_v2(self.ndi_recv, 5000)
        if t!=ndi.FRAME_TYPE_AUDIO:
            print(t)
        if t == ndi.FRAME_TYPE_NONE:
            print('No data received.')
            return

        if t == ndi.FRAME_TYPE_VIDEO:
            print(f'Video data received: {video_data.xres}x{video_data.yres}')
            
            self.display_frame(video_data)
            print("Displayed")
            ndi.recv_free_video_v2(self.ndi_recv, video_data)
            
            

    def display_frame(self, video_frame):
        # Convert NDI frame data to numpy array
        width, height = video_frame.xres, video_frame.yres
        video_data = np.copy(np.frombuffer(video_frame.data, dtype=np.uint8))
        video_data = video_data.reshape((height, width, 4))  # BGRX format
        print("Converted")
        # Convert the numpy array to QImage
        qimg = QImage(video_data, width, height, QImage.Format_RGB32)

        # Display in QLabel
        #self.label.setPixmap(QPixmap.fromImage(qimg))
        print("Mapped")

    def closeEvent(self, event):
        # Clean up NDI resources
        ndi.recv_destroy(self.ndi_recv)
        ndi.destroy()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = NDIStreamWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
