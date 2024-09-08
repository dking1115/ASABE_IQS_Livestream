import serial
import sys
import time
import re
import socket
import threading
class camera():
    def __init__(self,com_port,ip_addr,port):
        if com_port:
            self.cam_ser=serial.Serial(com_port,38400,8,"N",1,.01)
            self.type=0
        self.address=1
        self.camera_ip=ip_addr
        self.pan_position=0
        self.responses=[]
        self.control_mode=0
        self.pan=0
        self.tilt=0
        self.zoom=0
        self.closed_pan_goal=0.0
        self.closed_tilt_goal=0.0
        self.closed_zoom_goal=0.0
        if ip_addr:
            self.setup_socket(ip_addr,port)
            self.type=1
            listener=threading.Thread(target=self.ip_listening_thread)
            listener.start()
        else:
            self.serial_listener_thread=threading.Thread(target=self.ser_listener)
            self.serial_listener_thread.start()
            pass
        
        self.pos_query()
        self.position_thread=threading.Thread(target=self.position_controller_thread)
        self.position_thread.start()
        

    
    def position_controller_thread(self):
        while True:
            if self.control_mode==2:
                self.position_controller(self.closed_pan_goal,self.closed_tilt_goal)
                ##print(self.closed_pan_goal)
                time.sleep(.01)

    def ser_listener(self):
        while True:
            data=self.cam_ser.read_until(b"ff")
            self.visca_recieve(data.hex())
    
    def ip_listening_thread(self):
        #self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server_socket.bind(('192.168.100.180', 54571))
        #self.server_socket.listen(1)
        #self.socket.listen(1)
        #print("starting loop")
        """while True:
            client_socket, client_address = self.server_socket.accept()
            #print(f"connection from {client_address}")
            if client_address==self.camera_ip:
                break
            client_socket.close()
        """
        #print("connected")
        while True:
            data=self.socket.recv(1024)
            ##print("rcv")
            #print(data.hex())
            self.visca_recieve(data.hex())
            if not data:
                break
        
    def visca_recieve(self,data):
        #print(data)
        try:
            if data[0]=="9" and data[1]=="0" and data[2]=="5" and data[3]=="0" and len(data)==22:
                pan_str=f"{data[5]}{data[7]}{data[9]}{data[11]}"
                pan=int(pan_str,16)
                #print(f"pan raw: {pan}")
                if pan & (1 << (len(pan_str) * 4 - 1)):
                    # Perform two's complement conversion
                    pan = pan - (1 << (len(pan_str) * 4))
                self.pan=pan/(2448/180)
                tilt_str=f"{data[13]}{data[15]}{data[17]}{data[18]}"
                tilt=int(tilt_str,16)
                if tilt & (1 << (len(tilt_str) * 4 - 1)):
                    # Perform two's complement conversion
                    tilt = tilt - (1 << (len(tilt_str) * 4))
                self.tilt=tilt/(1296/90)
                self.pan_position=self.pan
                ##print(f"Pos Pan:{self.pan} Tilt:{self.tilt}")
            elif data[0]=="9" and data[1]=="0" and data[2]=="5" and data[3]=="0" and len(data)==14:
                zoom_str=f"{data[5]}{data[7]}{data[9]}{data[11]}"
                zoom=int(zoom_str,16)
                zoom=100*zoom/16384
                ##print(f"zoom pos: {zoom}")
                self.zoom=zoom
        except Exception as E:
            #print(E)
            pass
        
        

    def zoom_query(self):
        self.send_cmd(f"8{self.address} 09 04 47 FF")


    def setup_socket(self,ip,port):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.socket.connect((ip, port))

    def send_cmd(self,cmd_str):
        #self.cam_ser.reset_input_buffer()
        if self.type==0:
            # if self.cam_ser.in_waiting > 0:
            #     additional_data = self.cam_ser.read(self.cam_ser.in_waiting)
            #     self.visca_recieve(additional_data.hex())
            # else:
            #     additional_data = None
            # ##print(cmd_str)
            command=bytes.fromhex(cmd_str)
            while True:
                if self.cam_ser.is_open:
                    self.cam_ser.write(command)
                    break
                
            # if self.cam_ser.in_waiting > 0:
            #     additional_data = self.cam_ser.read(self.cam_ser.in_waiting)
            #     self.visca_recieve(additional_data.hex())
            # else:
            #     additional_data = None
            # response=additional_data
            # return response

        if self.type==1:
            cmd_str=cmd_str.replace(" ", "")
            #cmd_str='8101043F0201FF'
            ##print(cmd_str)
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
        print(f"move {pan_speed}")
        pc=3
        if pan_speed>0:
            pc=2
        elif pan_speed<0:
            pc=1
        tc=3
        if tilt_speed>0:
            tc=1
        elif tilt_speed<0:
            tc=2
        pan_speed=abs(pan_speed)
        tilt_speed=abs(tilt_speed)


        command=f"8{self.address} 01 06 01 {format(pan_speed, '02x')} {format(tilt_speed, '02x')} 0{pc} 0{tc} FF"
        ##print(command)
        result=self.send_cmd(command)
        ##print(result)
    
    def abs_pos(self,pan_speed,pan_pos,tilt_pos):
        tilt_pos=tilt_pos*-1
        pan_pos_cmd=self.twos_comp(int(pan_pos*40103/170),20)
        tilt_pos_cmd=self.twos_comp(int(tilt_pos*21231/90),16)

        pan_pos_cmd=hex(pan_pos_cmd)[2:].zfill(5)
        tilt_pos_cmd=hex(tilt_pos_cmd)[2:].zfill(4)
        #print(f"pan: {pan_pos} tilt: {tilt_pos} pan: {pan_pos_cmd} tilt: {tilt_pos_cmd}")

        pan_pos_cmd=list(pan_pos_cmd)
        tilt_pos_cmd=list(tilt_pos_cmd)

        tilt_speed=10
        command=f"8{self.address} 01 06 02 {format(pan_speed, '02x')} {format(tilt_speed, '02x')} 0{pan_pos_cmd[0]} 0{pan_pos_cmd[1]} 0{pan_pos_cmd[2]} 0{pan_pos_cmd[3]} 0{tilt_pos_cmd[0]} 0{tilt_pos_cmd[1]} 0{tilt_pos_cmd[2]} 0{tilt_pos_cmd[3]} FF"
        #81 01 06 02 VV WW 0Y 0Y 0Y 0Y 0Z 0Z 0Z 0Z FF
        ##print(command)
        self.send_cmd(command)
    
    def zoom_pos(self,zoom_pos_cmd):
        """Zoom to specfic level."""
        ##input zoom 1-100 float

        zoom=int(zoom_pos_cmd*(16384/100))
        ##print(zoom)
        zoom=list(hex(zoom)[2:].zfill(4))
        command=f"8{self.address} 01 04 47 0{zoom[0]} 0{zoom[1]} 0{zoom[2]} 0{zoom[3]} FF"
        self.send_cmd(command)
    
    def position_controller(self,pan_goal,tilt_goal):
        self.pos_query()
        self.zoom_query()
        pan_cmd=min(max(int((pan_goal-self.pan_position)*1),-18),18)
        tilt_cmd=min(max(int((tilt_goal-self.tilt)*.5),-18),18)
        ##print(f"goals: pan:{pan_goal} tilt:{tilt_goal}")
        # #print(f"cmds pan:{pan_cmd} tilt:{tilt_cmd} goals: pan:{pan_goal} tilt:{tilt_goal} pan:{self.pan_position} tilt:{self.tilt}" )
        self.move(pan_cmd,tilt_cmd)
        
        #self.zoom_pos(self.closed_zoom_goal)

        dz=self.closed_zoom_goal-self.zoom
        # #print(dz)
        if abs(dz) < 10:
            self.zoom_speed(0)
        else:
            command=dz
            self.zoom_speed(int(max(-7,min(7,command))))
        ##print(f"Pan:{self.pan} tilt:{self.tilt} cmds: pan:{pan_cmd} tilt:{tilt_cmd}")
        

    def zoom_speed(self,speed):
        if speed ==0:
            zc=0
        elif speed>0:
            zc=2
        else:
            zc=3
        
        command=f"8{self.address} 01 04 07 {zc}{abs(speed)} FF"
        #print(abs(speed))
        self.send_cmd(command)

    def image_flip(self,on):
        command=f"8{self.address} 01 04 66 0{3-on} FF"
        self.send_cmd(command)

    def set_gain(self,value):
        ##value 1-12
        value=hex(value)[2:]
        command=f"8{self.address} 01 04 4C 00 00 00 0{value} FF"
        self.send_cmd(command)

    def set_white_balance(self,value):
        #value 0-5
        command=f"8{self.address} 01 04 35 0{value} FF"
        self.send_cmd(command)
    
    def pos_query(self):
        
        command=f"8{self.address} 09 06 12 FF"
        self.send_cmd(command)
        ##print(result)
        """"matches=re.findall(r'\\x([a-fA-F0-9]+)',str(result))
        if len(matches)>6:
            pan_nums=matches[1][1]+matches[2][1]+matches[3][1]+matches[4][1]+matches[5][1]
        else:
            return
        pan_value=int(pan_nums,20)
        ##print(pan_value)
        ##print(pan_nums)
        ##print(matches)
        """
    def parse(self,data):

        matches=re.findall(r'\\x([a-fA-S0-9]+)',str(data))
        start=0
        responses=[]
        for i in range(len(matches)):
            if matches[i]=='ff':
                responses.append(matches[start:i+1])
                start=i+1
        ##print(responses)
        for response in responses:
            if response[0]=='90P' and len(response)>6:
                try:
                    #print(response)
                    pan_nums=response[1][1]+response[2][1]+response[3][1]+response[4][1]+response[5][1]
                    num=int(pan_nums,16)
                    if num & (1 << (len(pan_nums) * 4 - 1)):
                        num -= 1 << len(pan_nums) * 4
                    self.pan_position=num
                    ##print(self.pan_position)
                except:
                    pass
        self.responses=responses
        ##print(responses)
    def exposure_set(self):
        command=f"8{self.address} 01 04 39 00 FF"
        
        self.send_cmd(command)


    def focus_mode_set(self):
        command=f"8{self.address} 01 04 38 02 FF"
        self.send_cmd(command)
    
        

        

if __name__=="__main__":
    #cam=camera(None,"192.168.1.220",1259)
    #cam.move(-18,0)
    #time.sleep(10)
    cam=camera("/dev/ttyUSB0",None,None)
    speeds=[]
    i=18
    #cam.cam_ser.reset_input_buffer()
    #time.sleep(1)
    #cam.move(-18,0)
    #time.sleep(10)
    #print("Starting")
    #cam.move(1,1)
    """while abs(i)<=18:
        start=time.time()
        cam.responses=[]
        while len(cam.responses)<4 or time.time()-start<5:
            cam.move(i,0)
            time.sleep(.01)
        end=time.time()
        speeds.append(360/(end-start))
        #print(speeds)
        i=int((abs(i)-1)*-1*(i/abs(i)))
        #print(i)
        #cam.pos_query()
        #time.sleep(.1)
        #cam.abs_pos(18,18,90,-30)S
        #cam.zoom_pos(0)
        #cam.image_flip(0)
        #cam.set_gain(0)
        #cam.set_white_balance(0)
        #cam.abs_pos(18,18,10,0.0)
        time.sleep(1)
    #print(speeds)
    """
    #cam.abs_pos(18,0,0)

    #cam.zoom_pos(0)
    #cam.zoom_speed(0)
    cam.move(8,8)
    while True:
        cam.pos_query()
        ##print(cam.pan_position)
    #cam.zoom_pos(60)
    #time.sleep(1)
    #cam.move(-6,6)
    # cam.pos_query()
    # time.sleep(1)
    # #print(cam.pan_position)
    # while True:
    #     cam.position_controller(0.0,0.0)
    #     time.sleep(.5)
    # for i in range(0,100):
    #     cam.pos_query()
    #     #print(cam.pan)
    #     cam.abs_pos(18,i/10.0,0)
    #     time.sleep(.03)
    #cam.zoom_pos(100)
    #cam.abs_pos(18,180,10)
    time.sleep(2)

    #cam.position_controller(0,0)
    #cam.control_mode=2
    #cam.abs_pos(7,-10,10)
    #cam.move(10,0)
    # while True:
    #     for i in range(-1800,1800):
    #         cam.closed_pan_goal=i/10
    #         cam.closed_zoom_goal=(((i/10)/360)+.5)*100
    #         #cam.closed_zoom_goal=20
    #         time.sleep(.1)
    #         #cam.abs_pos(12,i,0)
    
    #cam.closed_pan_goal=80
    #cam.closed_zoom_goal=(((0/10)/360)+.5)*100
    # while True:
    #     for i in range(0,18):
    #         cam.move(-1*i,-1*i)
    #         time.sleep(.1)
    #         #print("loop")
    # #cam.zoom(-7)
    #cam.exposure_set()
    #cam.focus_mode_set()
        
        

        

    #cam.cam_ser.close()
