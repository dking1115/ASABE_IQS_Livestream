import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String
from open_gopro import WiredGoPro,Params
from std_srvs.srv import Empty
import asyncio
import subprocess
from .connection_secrets import SERVER_IP,SERVER_PASSWORD,SERVER_USER
class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')  # Node name
        self.get_logger().info('Node is starting...')

        self.start_serv=self.create_service(Empty,"Start_Recording_GoPro",self.start_recording_callback)
        self.stop_serv=self.create_service(Empty,"Stop_Recording_GoPro",self.stop_recording_callback)
        self.footage_tf=self.create_service(Empty,"Transfer_Footage",self.footage_transfer_callback)
        asyncio.run(self.connect())
        #asyncio.run(self.start_recording())
        #time.sleep(10)
        #asyncio.run(self.stop_recording())

    async def connect(self):
        print("Connecting")
        self.gopro=WiredGoPro()
        await self.gopro.open()
        print("Connected")

    async def start_recording(self):
        await self.gopro.http_command.set_shutter(shutter=Params.Toggle(True))

    async def stop_recording(self):
        await self.gopro.http_command.set_shutter(shutter=Params.Toggle(False))

    async def footage_transfer(self):
        st=await self.gopro.http_command.get_last_captured_media()
        vid=await self.gopro.http_command.download_file(camera_file=f"{st.data}",local_file="media.mp4")
        subprocess.run(f"sshpass -p {SERVER_PASSWORD} scp media.mp4 {SERVER_USER}@{SERVER_USER}:~/",shell=True)
        
    def start_recording_callback(self,request,response):
        self.get_logger().info("Starting Recording")
        asyncio.run(self.start_recording())
        return response
    
    def stop_recording_callback(self,request,response):
        self.get_logger().info("Stopping Recording")
        asyncio.run(self.stop_recording())
        return response

    def footage_transfer_callback(self,request,response):
        self.get_logger().info("Starting Footage transfer")
        asyncio.run(self.footage_transfer())
        self.get_logger().info("Finished Footage transfer")
        return response
    
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
