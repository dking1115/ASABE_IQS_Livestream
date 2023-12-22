import serial
import sys
import time
import re
import socket

class camera():
    def __init__(self,com_port,ip_addr):
        if com_port:
            self.cam_ser=serial.Serial(com_port,38400,8,"N",1,.01)
            self.type=0
        self.address=1
        self.camera_ip=ip_addr
        self.pan_position=0
        self.responses=[]
        if ip_addr:
            self.setup_socket(ip_addr)
            self.type=1
        
    
    def ip_listening_thread(self):
        self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(1)
        while True:
            client_socket, client_address = self.server_socket.accept()
            if client_address==self.camera_ip:
                break
            client_socket.close()
        while True:
            data=client_socket.recv(1024)
            self.visca_recieve(data)
            if not data:
                break
        
    def visca_recieve(self,data):
        print(data)
        




    def setup_socket(self,ip,port):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.socket.connect((ip, port))

    def send_cmd(self,cmd_str):
        #self.cam_ser.reset_input_buffer()
        if self.type==0:
            if self.cam_ser.in_waiting > 0:
                additional_data = self.cam_ser.read(self.cam_ser.in_waiting)
                self.parse(additional_data)
            else:
                additional_data = None
            print(cmd_str)
            command=bytes.fromhex(cmd_str)
            self.cam_ser.write(command)
            if self.cam_ser.in_waiting > 0:
                additional_data = self.cam_ser.read(self.cam_ser.in_waiting)
                self.parse(additional_data)
            else:
                additional_data = None
            response=additional_data
            return response

        if self.type==1:
            data=bytes.fromhex(cmd_str)
            self.socket.send(data)
    
    def twos_comp(self,val, nbits):
        """Compute the 2's complement of int value val"""
        if val < 0:
            val = (1 << nbits) + val
        else:
            if (val & (1 << (nbits - 1))) != 0:
                # If sign bit is set.
                # compute negative value.
                val = val - (1 << nbits)
        return val

    def move(self,pan_speed,tilt_speed):
        pc=3
        if pan_speed>0:
            pc=2
        elif pan_speed<0:
            pc=1
        tc=3
        if tilt_speed>0:
            tc=2
        elif tilt_speed<0:
            tc=1
        pan_speed=abs(pan_speed)
        tilt_speed=abs(tilt_speed)


        command=f"8{self.address} 01 06 01 {format(pan_speed, '02x')} {format(tilt_speed, '02x')} 0{pc} 0{tc} FF"
        #print(command)
        result=self.send_cmd(command)
        #print(result)
    
    def abs_pos(self,pan_speed,tilt_speed,pan_pos,tilt_pos):
        tilt_pos=tilt_pos*-1
        pan_pos_cmd=self.twos_comp(int(pan_pos*40103/170),20)
        tilt_pos_cmd=self.twos_comp(int(tilt_pos*21231/90),16)

        pan_pos_cmd=hex(pan_pos_cmd)[2:].zfill(5)
        tilt_pos_cmd=hex(tilt_pos_cmd)[2:].zfill(4)
        print(f"pan: {pan_pos} tilt: {tilt_pos} pan: {pan_pos_cmd} tilt: {tilt_pos_cmd}")

        pan_pos_cmd=list(pan_pos_cmd)
        tilt_pos_cmd=list(tilt_pos_cmd)

        
        command=f"8{self.address} 01 06 02 {format(pan_speed, '02x')} 00 0{pan_pos_cmd[0]} 0{pan_pos_cmd[1]} 0{pan_pos_cmd[2]} 0{pan_pos_cmd[3]} 0{pan_pos_cmd[4]} 0{tilt_pos_cmd[0]} 0{tilt_pos_cmd[1]} 0{tilt_pos_cmd[2]} 0{tilt_pos_cmd[3]} FF"
        print(command)
        print(self.send_cmd(command))
    
    def zoom_pos(self,zoom_pos_cmd):
        """Zoom to specfic level."""
        ##input zoom 1-100 float

        zoom=int(zoom_pos_cmd*(16384/100))
        #print(zoom)
        zoom=list(hex(zoom)[2:].zfill(4))
        command=f"8{self.address} 01 04 47 0{zoom[0]} 0{zoom[1]} 0{zoom[2]} 0{zoom[3]} FF"
        print(self.send_cmd(command))
    
    def zoom(self,speed):
        
        if speed>0:
            zc=2
        else:
            zc=3

        command=f"8{self.address} 01 04 07 {zc}{abs(speed)} FF"
        print(self.send_cmd(command))

    def image_flip(self,on):
        command=f"8{self.address} 01 04 66 0{3-on} FF"
        print(self.send_cmd(command))

    def set_gain(self,value):
        ##value 1-12
        value=hex(value)[2:]
        command=f"8{self.address} 01 04 4C 00 00 00 0{value} FF"
        print(self.send_cmd(command))

    def set_white_balance(self,value):
        #value 0-5
        command=f"8{self.address} 01 04 35 0{value} FF"
        print(self.send_cmd(command))
    
    def pos_query(self):
        
        command=f"8{self.address} 09 06 12 FF"
        result=self.send_cmd(command)
        #print(result)
        matches=re.findall(r'\\x([a-fA-F0-9]+)',str(result))
        if len(matches)>6:
            pan_nums=matches[1][1]+matches[2][1]+matches[3][1]+matches[4][1]+matches[5][1]
        else:
            return
        pan_value=int(pan_nums,20)
        #print(pan_value)
        #print(pan_nums)
        #print(matches)
    
    def parse(self,data):

        matches=re.findall(r'\\x([a-fA-S0-9]+)',str(data))
        start=0
        responses=[]
        for i in range(len(matches)):
            if matches[i]=='ff':
                responses.append(matches[start:i+1])
                start=i+1
        #print(responses)
        for response in responses:
            if response[0]=='90P':
                print(response)
                pan_nums=response[1][1]+response[2][1]+response[3][1]+response[4][1]+response[5][1]
                self.pan_position=int(pan_nums,20)
                print(self.pan_position)
        self.responses=responses
        #print(responses)
    def exposure_set(self):
        command=f"8{self.address} 01 04 39 00 FF"
        
        self.send_cmd(command)


    def focus_mode_set(self):
        command=f"8{self.address} 01 04 38 02 FF"
        self.send_cmd(command)
    
        

        

if __name__=="__main__":
    cam=camera("/dev/ttyUSB0")
    speeds=[]
    i=18
    #cam.cam_ser.reset_input_buffer()
    #time.sleep(1)
    #cam.move(-18,0)
    #time.sleep(10)
    print("Starting")
    """while abs(i)<=18:
        start=time.time()
        cam.responses=[]
        while len(cam.responses)<4 or time.time()-start<5:
            cam.move(i,0)
            time.sleep(.01)
        end=time.time()
        speeds.append(360/(end-start))
        print(speeds)
        i=int((abs(i)-1)*-1*(i/abs(i)))
        print(i)
        #cam.pos_query()
        #time.sleep(.1)
        #cam.abs_pos(18,18,90,-30)S
        #cam.zoom_pos(0)
        #cam.image_flip(0)
        #cam.set_gain(0)
        #cam.set_white_balance(0)
        #cam.abs_pos(18,18,10,0.0)
        time.sleep(1)
    print(speeds)
    """
    cam.abs_pos(18,18,0,-10)

    #cam.zoom_pos(0)
    #cam.zoom(-4)
    #cam.zoom_pos(60)
    #time.sleep(1)
    cam.abs_pos(18,18,-6,13)
    #cam.zoom(-7)
    #cam.exposure_set()
    #cam.focus_mode_set()
        
        

        

    cam.cam_ser.close()