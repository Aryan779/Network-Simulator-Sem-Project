import time
import random

class Switch:
    def __init__(self,mac_address):
        self.mac_address=mac_address
        print("\nCreated a Switch device with mac_address ",mac_address,"\n")
        self.mac_table = {}
        self.num_of_Ports=10
        self.connected=0
        self.connected_devices=[]
        self.hub=[]
        self.port=1
        print("\nWhich Flow Control Protocol do you want to implement in Switch: ")
        print("1.) Stop & wait ARQ")
        print("2.) Go Back N ARQ")
        self.opt1 = int(input("choose option(1 or 2): "))
        print()
        self.frames=[]
        self.last_received_frame_num=-1
    
    def connect_with_hub(self,hubDevice):
        if(self.connected<=self.num_of_Ports):
            self.connected+=1
            print("Switch device with mac address ",self.mac_address," to hub device with mac address ",hubDevice.mac_address,"\n")
            time.sleep(1)
            self.hub.append(hubDevice)
        else:
            print("Number of ports in Switch limit reached. No connection would take place")

    def connect_device(self,device):
        if(self.connected<=self.num_of_Ports):
            self.connected+=1
            print("Switch device with mac address ",self.mac_address," to End Device with mac address ",device.mac_address,"\n")
            time.sleep(1)
            self.connected_devices.append(device)
            device.connect_with_switch(self)
        else:
            print("Number of ports in Switch limit reached. No connection would take place")

    def receive_bits_hub(self,bits,hubDevice):
        frame=self.convert_bits_to_frame(bits)
        print("Switch with mac address",self.mac_address,"Received frame",frame[3]," in form of bits from hub with mac address ",hubDevice.mac_address,"\n")
        if(frame[3]==1 and frame[3]!=frame[4]):
            self.frames.append(frame)
        elif(frame[3]<frame[4]):
            self.frames.append(frame)
        else:
            self.frames.append(frame)
            print('Transmission completed from hub')
            self.transmit()
            self.frames=[]

    def transmit(self):
        dest_device_mac=self.frames[0][0]
        devices=list(self.mac_table.keys())
        mac_addr_list=[device.mac_address for device in devices ]

        if len(self.connected_devices)==self.port-1 and dest_device_mac not in mac_addr_list:
            print("\nThere is no device with mac address",dest_device_mac," in any path of switch")
            print("Frames all rejected\n")
            return
        
        if dest_device_mac in mac_addr_list:
            #source_device=devices[mac_addr_list.index(source_device_mac)]
            # Send the packet to the appropriate port
            dest_device=devices[mac_addr_list.index(dest_device_mac)]
            if type(self.mac_table[dest_device]) is list:
                port=self.mac_table[dest_device][0]
                print(f"Frame sent from port {port}")
                if(type(self.mac_table[dest_device][1]) is hub):
                    h=self.mac_table[dest_device]
                    hubDevice=h[1]
                    for frame in self.frames:
                        bits=self.convert_frame_to_bits(frame)
                        hubDevice.receive_bits(bits,self)
            else:
                port = self.mac_table[dest_device]
                print(f"Frame sent from port {port}")
                if(self.opt1==2):
                    self.send_frame_gbn(self.frames,dest_device)
                if(self.opt1==1):
                    self.send_frame_stop_and_wait(self.frames,dest_device)

        else:
            # Flood the packet to all ports except the source
            print("Destination MAC not found, flooding packet to all ports\n")
            
            self.learn_address()
            
            devices=list(self.mac_table.keys())
            mac_addr_list=[device.mac_address for device in devices ]
            if dest_device_mac in mac_addr_list:
                print("\nThere is no device with mac address",dest_device_mac," in any path of switch")
                print("Frames all rejected\n")
                return
            dest_device=devices[mac_addr_list.index(dest_device_mac)]
            time.sleep(1)
            if type(self.mac_table[dest_device]) is list:
                port=self.mac_table[dest_device][0]
                print(f"Frame sent from port {port}")
                if(type(self.mac_table[dest_device][1]) is hub):
                    h=self.mac_table[dest_device][1]
                    for frame in self.frames:
                        bits=self.convert_frame_to_bits(frame)
                        h.receive_bits(bits,self)
            else:
                port = self.mac_table[dest_device]
                print(f"Frame sent from port {port}")
                if(self.opt1==2):
                    self.send_frame_gbn(self.frames,dest_device)
                if(self.opt1==1):
                    self.send_frame_stop_and_wait(self.frames,dest_device)

    def send_frame_gbn(self,frames,device): # go_back_n protocol
        window_size=3
        print("\nWindow size is set to 3\n")
        win_start=0
        while win_start<len(frames):
            lock=False
            for i in range(win_start,min(win_start+window_size,len(frames))):
                res=self.send_bits_gbn(frames[i],device)
                if(res=="resend" ): # it means frame lost or ack lost
                    print("frame no",frames[i][3],"lost\n")
                    if(lock==False):
                        win_start=i
                        lock=True
                elif(res=="reject"):
                    print("frame ",i+1,"reject because one of the previous frame has not reached\n\n")    
                elif(res=="ACK"):
                    print("ACK received for frame number ",i+1 ,"\n\n")
                    win_start=i +1
                time.sleep(4)
            
    def receive_frame_gbn(self,frame):       
        frame_num =  frame[3]
        if(self.last_received_frame_num!=-1 and self.last_received_frame_num+1!=frame_num):
            return "reject"
        if(self.last_received_frame_num==-1 and frame_num>1):
            return "reject"
        
        self.last_received_frame_num=frame[3]
        if(frame[3]==1):
            self.frames.append(frame)
        elif(frame[3]<frame[4]):
            self.frames.append(frame)    
        else:
            self.frames.append(frame)
            print("Transmission to switch completed")
            self.transmit()
            self.frames=[]
            self.last_received_frame_num=(-1)

        return "ACK"
    
    def send_frame_stop_and_wait(self,frames,device): # stop_and_wait protocol
        for frame in frames:
            print("Sneding frame ",frame[3],":\n")
            res=self.send_bits_stop_and_wait(frame,device)
            while(res=="resend"): # it will break when it will send ACK or false
                print("Resending frame ",frame[3],":\n")
                res=self.send_bits_stop_and_wait(frame,device)
            if res==False:
                    print("frame not for mac_address "f"{device.mac_address}\n")
                    return
            if(res=="ACK"):
                print("ACK reveived\n")    
            time.sleep(2)
    
    def receive_frame_stop_and_wait(self,frame):
        
        if(frame[3]==1 and frame[3]==frame[4]):
            self.frames.append(frame)
        if(frame[3]==1):
            self.frames.append(frame)
        elif(frame[3]<frame[4]):
            self.frames.append(frame)
        elif(frame[3]==frame[4]):
            self.frames.append(frame)
            print("Transmission to switch completed")
            self.transmit()
            self.frames=[]
            self.last_received_frame_num=(-1)

        return "ACK"
    
    def send_bits_stop_and_wait(self, frame,device):
        bits = self.convert_frame_to_bits(frame)    
        return device.receive_bits_stop_and_wait(bits)
    
    def send_bits_gbn(self, frame,device):
        bits = self.convert_frame_to_bits(frame)    
        return device.receive_bits_gbn(bits)


    def receive_bits_stop_and_wait(self, bits):
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>80):
            time.sleep(3)
            print("Timed out. Send again\n")
            return "resend"
        frame=self.convert_bits_to_frame(bits)
        res=self.receive_frame_stop_and_wait(frame)
        return res
    
    def receive_bits_gbn(self, bits):
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>80):
            time.sleep(3)
            print("Timed out. Send again\n")
            return "resend"
        frame=self.convert_bits_to_frame(bits)
        res=self.receive_frame_gbn(frame)
        return res
    
    


    def learn_address(self):
        for device in self.connected_devices:
            if device not in self.mac_table.keys():
                self.mac_table[device] = self.port
                self.port += 1
        for hub in self.hub:
            for device in hub.devices:
                if device not in self.mac_table.keys():
                    self.mac_table[device] = [self.port,hub]
            self.port += 1

    def convert_frame_to_bits(self,frame):
        binary_repr = [format(i, 'b') if isinstance(i, int) else ''.join(format(ord(c), '08b') for c in i) for i in frame]
        bits = ' '.join(binary_repr)
        return bits

    def convert_bits_to_frame(self,bits):
        frame=[]
        bits = bits.split()
        frame.append(int(bits[0],2))
        frame.append(int(bits[1],2))
        bit_groups = [bits[2][i:i+8] for i in range(0, len(bits[2]), 8)]
        s = ''.join(chr(int(group, 2)) for group in bit_groups)
        frame.append(s)
        frame.append(int(bits[3],2))
        frame.append(int(bits[4],2))
        return frame
    
class hub:
    def __init__(self,mac_address):
        print("\nCreated a Hub device with mac_address ",mac_address,"\n")
        self.mac_address=mac_address
        self.num_of_ports=10
        self.connected=0
        self.devices = []
        self.switch=[]
    
    def connect_with_switch(self,switchDevice):
        if(self.num_of_ports>0):
            self.connected+=1
            print("Hub device with mac address ",self.mac_address," to Switch device with mac address ",switchDevice.mac_address,"\n")
            time.sleep(1)
            self.switch.append(switchDevice)
            self.num_of_ports-=1
        else:
            print("Number of ports in Hub limit reached. No connection would take place")

    def connect_device(self,device):
        if(self.num_of_ports>0):
            self.connected+=1
            self.devices.append(device)
            print("Hub device with mac address ",self.mac_address," to End device with mac address ",device.mac_address,"\n")
            time.sleep(1)
            device.connect_with_hub(self)
            self.num_of_ports-=1
        else:
            print("Number of ports limit reached. No connection would take place")
    
    def transmit_bits(self,bits,deviceList): 
        for device in deviceList:
                print("Hub transmiting the bits to device with mac address",device.mac_address,"\n")
                device.receive_bits_hub(bits,self)
                time.sleep(2)
                #switch.receive_bits_hub

    def transmit_bits_switch(self,bits,switchList): 
        for switch in switchList:
            print("Hub transmiting the bits to switch with mac address",switch.mac_address,"\n")
            switch.receive_bits_hub(bits,self)
            time.sleep(2)
            
    def receive_bits(self,bits,device): # here device parameter will tell from which device the bits came
        if(len(self.devices)>0):
            self.transmit_bits(bits,[element for element in self.devices if element != device]) 
        if(len(self.switch)>0):
            self.transmit_bits_switch(bits,[element for element in self.switch if element != device])

class EndDevice:
    def __init__(self, mac_address,sequence_no=None):
        print("\n Created a End device with mac_address ",mac_address,"\n")
        self.mac_address = mac_address
        self.max_devices=10
        self.connected_devices=[]
        self.hub=[]
        self.switch=[]
        self.sequence_no=None
        self.mem_stack=[]
        self.last_received_frame_num=-1
    

    #connection
    def isConnectionThere(self,device):
        if(device in self.connected_devices):
            print("\nyes, there is connection betwen mac_address "f"{self.mac_address} and other end device  mac_address "f"{device.mac_address}\n")
        elif(device in self.hub):
            print("\nyes, there is connection betwen mac_address "f"{self.mac_address} and  hub mac_address "f"{device.mac_address}\n")
        else:
            print("\nNo, there is not any connection betwen mac_address "f"{self.mac_address} and other device  mac_address "f"{device.mac_address}\n")
    
    def connect_device(self,device):
        if(self.max_devices>0):
            self.connected_devices.append(device)
            self.max_devices-=1
            print("\nmac_address "f"{self.mac_address} has connected to mac_address "f"{device.mac_address}\n")
        else:
            print("\nmac_address "f"{self.mac_address} has reached its max devices connection limit. No connection can happen.\n")
    
    def connect_with_hub(self,hubDevice):
        if(self.max_devices>0):
            self.hub.append(hubDevice)
            self.max_devices-=1
            print("mac_address "f"{self.mac_address} has connected to hub with mac_address "f"{hubDevice.mac_address}")
        else:
            print("mac_address "f"{self.mac_address} has reached its max devices connection limit. No connection can happen.")

    def connect_with_switch(self,switchDevice):
        if(self.max_devices>0):
            self.switch.append(switchDevice)
            self.max_devices-=1
            print("mac_address "f"{self.mac_address} has connected to Switch with mac_address "f"{switchDevice.mac_address}")
        else:
            print("mac_address "f"{self.mac_address} has reached its max devices connection limit. No connection can happen.")

    def return_connected_devices(self):
        return self.connected_devices
            
    #physical layer
    def send_bits_stop_and_wait(self, frame,device):
        bits = self.convert_frame_to_bits(frame)    
        return device.receive_bits_stop_and_wait(bits)
    
    def send_bits_gbn(self, frame,device):
        bits = self.convert_frame_to_bits(frame)    
        return device.receive_bits_gbn(bits)

    def send_bits_hub(self,frames,hubDevice):
        if(hubDevice not in self.hub):
            raise Exception("first connect with the hub device") 
        for frame in frames:
            print("Transmitting frame ",frame[3]," converted to bits to hub with mac address ",hubDevice.mac_address,"\n")
            bits = self.convert_frame_to_bits(frame)
            hubDevice.receive_bits(bits,self)    
            time.sleep(3)
    
    #def receive_bits_hub(self,bits,switchDevice):



    def receive_bits_hub(self,bits,hubDevice):
        frame=self.convert_bits_to_frame(bits)
        destination_mac_address, src_mac_address, data = frame[0],frame[1],frame[2]
        if(destination_mac_address!=self.mac_address):
            print("This frame is not for this device with mac address ",self.mac_address,"\n")
            return
        print("Received frame",frame[3]," with ",data," in form of bits from hub with mac address ",hubDevice.mac_address,"\n")
        if(frame[3]==1 and frame[3]!=frame[4]):
            self.mem_stack.append(data)

        elif(frame[3]<frame[4]):
            self.mem_stack[-1]+=data
        else:
            self.mem_stack[-1]+=data
            print("\nTotal Data received from mac_address "f"{src_mac_address} to mac_address "f"{destination_mac_address} is",self.mem_stack[-1],"\n")
            print('Transmission completed')


    def receive_bits_stop_and_wait(self, bits):
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>80):
            time.sleep(3)
            print("Timed out. Send again\n")
            return "resend"
        frame=self.convert_bits_to_frame(bits)
        res=self.receive_frame_stop_and_wait(frame)
        return res
    
    def receive_bits_gbn(self, bits):
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>80):
            time.sleep(3)
            print("Timed out. Send again\n")
            return "resend"
        frame=self.convert_bits_to_frame(bits)
        res=self.receive_frame_gbn(frame)
        return res
        
    #data link layer
    def create_frame(self,data,destination_device):
        print("Creating frames with a total data: '",data,"' which is been sending from mac_address "f"{self.mac_address} to {destination_device.mac_address}\n\n")
        time.sleep(3)
        #frame=[destination_device.mac_address, self.mac_address, data]
        max_frame_size = 3 # 
        frames = [data[i:i+max_frame_size] for i in range(0, len(data), max_frame_size)]
        n=len(frames)
        for i in range(0,n):
            frames[i]=[destination_device.mac_address,self.mac_address,frames[i],i+1,n]
        return frames

    def send_frame_gbn(self,frames,device): # go_back_n protocol
        window_size=3
        print("\nWindow size is set to 3\n")
        win_start=0
        while win_start<len(frames):
            lock=False
            for i in range(win_start,min(win_start+window_size,len(frames))):
                res=self.send_bits_gbn(frames[i],device)
                if(res=="resend" ): # it means frame lost or ack lost
                    print("frame no",frames[i][3],"lost\n")
                    if(lock==False):
                        win_start=i
                        lock=True
                elif(res=="reject"):
                    print("frame ",i+1,"reject because one of the previous frame has not reached\n\n")    
                elif(res=="ACK"):
                    print("ACK received for frame number ",i+1 ,"\n\n")
                    win_start=i +1
                elif res==False:
                    print("frame not for mac_address "f"{self.mac_address}")
                    return
                time.sleep(4)
            
    def receive_frame_gbn(self,frame):       
        destination_mac_address, src_mac_address, data, frame_num = frame[0],frame[1],frame[2], frame[3]
        if(self.last_received_frame_num!=-1 and self.last_received_frame_num+1!=frame_num):
            return "reject"
        if(self.last_received_frame_num==-1 and frame_num>1):
            return "reject"
        if(destination_mac_address!=self.mac_address):
            return False
        print("Frame", frame[3],"Data received from mac_address "f"{src_mac_address} to mac_address "f"{destination_mac_address} is",data)
        self.last_received_frame_num=frame[3]
        if(frame[3]==1):
            self.mem_stack.append(data)

        elif(frame[3]<frame[4]):
            self.mem_stack[-1]+=data
            
        else:
            self.mem_stack[-1]+=data
            print("\nTotal Data received from mac_address "f"{src_mac_address} to mac_address "f"{destination_mac_address} is",self.mem_stack[-1],"\n")
            print('Transmission completed')
            self.last_received_frame_num=-1
        
        return "ACK"
    
    def send_frame_stop_and_wait(self,frames,device): # stop_and_wait protocol
        for frame in frames:
            print("Sneding frame ",frame[3],":\n")
            res=self.send_bits_stop_and_wait(frame,device)
            while(res=="resend"): # it will break when it will send ACK or false
                print("Resending frame ",frame[3],":\n")
                res=self.send_bits_stop_and_wait(frame,device)
            if res==False:
                    print("frame not for mac_address "f"{device.mac_address}\n")
                    return
            if(res=="ACK"):
                print("ACK reveived\n")    
            time.sleep(2)
    
    def receive_frame_stop_and_wait(self,frame):
        
        destination_mac_address, src_mac_address, data = frame[0],frame[1],frame[2]
        if(destination_mac_address!=self.mac_address):
            print("This frame is not for this device with mac address ",self.mac_address,"\n\n")
            return False
        print("Frame", frame[3],"Data received from mac address "f"{src_mac_address} to mac address "f"{destination_mac_address} is",data,"\n")
        if(frame[3]==1 and frame[3]==frame[4]):
            self.mem_stack.append(data)
            print("\nTotal Data received from mac address "f"{src_mac_address} to mac address "f"{destination_mac_address} is",self.mem_stack[-1],"\n")
            print('Transmission completed')
        if(frame[3]==1):
            self.mem_stack.append(data)
        elif(frame[3]<frame[4]):
            self.mem_stack[-1]+=data
        elif(frame[3]==frame[4]):
            self.mem_stack[-1]+=data
            print("\nTotal Data received from mac_address "f"{src_mac_address} to mac_address "f"{destination_mac_address} is",self.mem_stack[-1],"\n")
            print('Transmission completed')
        
        return "ACK"
    
    #frame to bits & bits to frame
    def convert_frame_to_bits(self,frame):
        binary_repr = [format(i, 'b') if isinstance(i, int) else ''.join(format(ord(c), '08b') for c in i) for i in frame]
        bits = ' '.join(binary_repr)
        return bits

    def convert_bits_to_frame(self,bits):
        frame=[]
        bits = bits.split()
        frame.append(int(bits[0],2))
        frame.append(int(bits[1],2))
        bit_groups = [bits[2][i:i+8] for i in range(0, len(bits[2]), 8)]
        s = ''.join(chr(int(group, 2)) for group in bit_groups)
        frame.append(s)
        frame.append(int(bits[3],2))
        frame.append(int(bits[4],2))
        return frame
 
print("\n\n Used 1 to 100 mac_address for end_device & 101 to 150 for hub & 201 to 250 for switch \n\n")


    