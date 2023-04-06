import time
import random
class switch:
    def __init__(self,mac_address):
        print("\nCreated a Hub device with mac_address ",mac_address,"\n")
        self.mac_address=mac_address
        self.num_of_ports=10
        self.connected=0
        self.devices = []

    def connect_device(self,device):
        if(self.num_of_ports>0):
            self.connected+=1
            self.devices.append(device)
            device.connect_with_hub(self)
            self.num_of_ports-=1
        else:
            print("Number of ports limit reached. No connection would take place")

    def transmit_bits(self,bits,device): 
        if device in self.devices:
            device.receive_bits(bits)
    
    def receive_bits(self,bits,device): # here device parameter will tell from which device the bits came
        self.transmit_bits(bits,[element for element in self.devices if element != device]) 
    
class hub:
    def __init__(self,mac_address):
        print("\nCreated a Hub device with mac_address ",mac_address,"\n")
        self.mac_address=mac_address
        self.num_of_ports=10
        self.connected=0
        self.devices = []
    
    def connect_device(self,device):
        if(self.num_of_ports>0):
            self.connected+=1
            self.devices.append(device)
            device.connect_with_hub(self)
            self.num_of_ports-=1
        else:
            print("Number of ports limit reached. No connection would take place")
    
    def transmit_bits(self,bits,deviceList): 
        for device in deviceList:
            device.receive_bits(bits)
    
    def receive_bits(self,bits,device): # here device parameter will tell from which device the bits came
        self.transmit_bits(bits,[element for element in self.devices if element != device]) 

class EndDevice:
    def __init__(self, mac_address):
        print("\n Created a End device with mac_address ",mac_address,"\n")
        self.mac_address = mac_address
        self.max_devices=5
        self.connected_devices=[]
        self.hub=[]
        self.mem_stack=[]
        self.token=None
    
    

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
            print("mac_address "f"{self.mac_address} has connected to mac_address "f"{device.mac_address}")
        else:
            print("mac_address "f"{self.mac_address} has reached its max devices connection limit. No connection can happen.")
    
    def connect_with_hub(self,hubDevice):
        if(self.max_devices>0):
            self.hub.append(hubDevice)
            self.max_devices-=1
            print("mac_address "f"{self.mac_address} has connected to hub with mac_address "f"{hubDevice.mac_address}")
        else:
            print("mac_address "f"{self.mac_address} has reached its max devices connection limit. No connection can happen.")

    def return_connected_devices(self):
        return self.connected_devices
            
    #physical layer
    def send_bits(self, frame,device,probabError):
        if(probabError>70):
            time.sleep(5)
            print("Timed out. Send again")
            return "resend"
        bits = self.convert_frame_to_bits(frame)    
        device.receive_bits(bits)

    def send_bits_hub(self,frame,hubDevice):
        bits = self.convert_frame_to_bits(frame)
        hubDevice.receive_bits(bits,self)    
                
    def receive_bits(self, bits):
        frame=self.convert_bits_to_frame(bits)
        res=self.receive_frame(frame)
        if res is False: 
            print("frame not for mac_address "f"{self.mac_address}")
        
        
    #data link layer
    def create_frame(self,data,destination_device):
        print("Creating frames with a total data: ",data," which is been sending from mac_address "f"{self.mac_address} to {destination_device.mac_address}")
        #frame=[destination_device.mac_address, self.mac_address, data]
        max_frame_size = 5 # 
        frames = [data[i:i+max_frame_size] for i in range(0, len(data), max_frame_size)]
        n=len(frames)
        for i in range(0,n):
            frames[i]=[destination_device.mac_address,self.mac_address,frames[i],i+1,n]
        return frames

    def receive_frame(self,frame):
        
        destination_mac_address, src_mac_address, data = frame[0],frame[1],frame[2]
        if(destination_mac_address!=self.mac_address):
            return False
        print("Frame Data received from mac_address "f"{src_mac_address} to mac_address "f"{destination_mac_address} is",data)
        if(frame[3]==1):
            self.mem_stack.append(data)
        elif(frame[3]<frame[4]):
            self.mem_stack[-1]+=data
        else:
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
 

print("\n\n Use 1 to 100 mac_address for end_device & 101 to 150 for hub & 151 to 200 for bridge & & 201 to 250 for switch \n\n")

'''
d1=EndDevice(1)
d2=EndDevice(2)
d3=EndDevice(3)
d4=EndDevice(3)

d1.connect_device(d2)
d1.connect_device(d3)
d1.connect_device(d4)
d2.connect_device(d1)
d3.connect_device(d1)

'''
        
print("\n --> test case 1\n\n")
d1=EndDevice(1)
d2=EndDevice(2)
d3=EndDevice(3)
d1.connect_device(d2) 
d2.connect_device(d1)       
print("\n\n")

print("Which transmission do you want: ")
print("1.) d1 ---> d2")
print("2.) d2 ---> d1")
where = int(input("choose option(1 or 2): "))
data = input("Enter data you want to sned: ")
if(where==1):
    frames = d1.create_frame(data,d2)
    sequence_number = 0
    window_start = 0
    window_end = 0
    window_size = 4
    timeout = 5
    framesList=[]
    for frame in frames:
        framesList.append((sequence_number,sequence_number))
        sequence_number+=1
    #packets = [(0, 'Packet 0'), (1, 'Packet 1'), (2, 'Packet 2'), (3, 'Packet 3'), (4, 'Packet 4')]
    ack_received = False

    # Send initial window of packets
    while window_start < window_size:
        if(window_start>=len(framesList)):
            break
        frame = framesList[window_start]
        print(f'Sending Frame {frame[0]}')
        d1.send_bits(frame[1],d2)
        # Simulate network delay and packet loss
        time.sleep(0.5)
        temp=random.random()
        if  temp < 0.2:
            print(f'Frame {frame[0]} lost\n\n')
        else:
            # Simulate network delay
            time.sleep(0.5)
            print(f'Frame {frame[0]} received\n\n')
            window_start += 1

    # Start the timer
    start_time = time.time()

    # Wait for ACKs
    while not ack_received:
        # Check for timeout
        if time.time() - start_time > timeout:
            print('Timeout, resending window')
            window_start = window_start - (window_end - window_start)  # Slide window back
            window_end = window_start + window_size - 1
            for i in range(window_start, window_end + 1):
                packet = framesList[i]
                print(f'Resending Frame {frame[0]}')
                d1.send_bits(frame[1],d2)
                # Simulate network delay and packet loss
                time.sleep(0.5)
                if random.random() < 0.2:
                    print(f'Frame {frame[0]} lost')
                else:
                    # Simulate network delay
                    time.sleep(0.5)
                    print(f'Frame {frame[0]} received')
        else:
            # Simulate network delay
            time.sleep(0.5)
            # Check for ACK
            if random.random() < 0.2:
                print('ACK lost')
            else:
                print('ACK received')
                sequence_number += window_size
                window_start = window_end + 1
                window_end = window_start + window_size - 1
                # Check for end of transmission
                if window_start >= len(framesList):
                    ack_received = True


