import copy
import itertools
import os
import random
from time import sleep
import ipaddress

from netaddr import IPNetwork

# subnet mask: 24

def get_network_addr(ip_address, subnet_mask="255.255.255.0"):
    ip = ipaddress.ip_interface(f"{ip_address}/{subnet_mask}")
    network_ip = ip.network.network_address
    return str(network_ip)

def check_subnet(ip1,ip2):
    """Checks If IP Exists In That Subnet."""
    # 225 = Broadcast Address, 0 = Network Address
    subnet = "255.255.0.0"
    if IPNetwork("{}/{}".format(ip1,subnet)) == IPNetwork("{}/{}".format(ip2,subnet)):
        return True
    return False

class packet:
    def __init__(self,num,src_name,dest_name,src_port,dest_port,dest_mac_addr=None,src_mac_addr=None,dest_ip_addr=None,src_ip_addr=None,data=None):
        self.num=num
        self.src_name=src_name
        self.dest_name=dest_name
        self.src_port=src_port
        self.dest_port=dest_port
        self.dest_mac_addr=dest_mac_addr
        self.src_mac_addr=src_mac_addr
        self.dest_ip_addr=dest_ip_addr
        self.src_ip_addr=src_ip_addr
        self.data=data
        '''print("packet structure: ",end="")
        print("dest mac_addr: ",self.dest_mac_addr," ","src mac_addr: ",self.src_mac_addr,end=" ")
        print("dest ip_addr: ",self.dest_ip_addr," ","src ip_addr: ",self.src_ip_addr,end=" ")
        print("Data: ",data)'''


class ARP:
    arp_cache = {}

    @staticmethod
    def add_entry( ip_address, mac_address):
        ARP.arp_cache[ip_address] = mac_address

    @staticmethod
    def lookup(ip_address):
        if ip_address in ARP.arp_cache:
            return ARP.arp_cache[ip_address]
        else:
            return None

    @staticmethod
    def send_arp_request(src_ip, dest_ip):
        print(f"Sending ARP request from {src_ip} to resolve {dest_ip}...")
        sleep(1)
        print("Received ARP response:")
        mac_addr = ARP.lookup(dest_ip)
        if mac_addr:
            print(f"IP: {dest_ip}, MAC: {mac_addr}")
        else:
            print(f"No MAC address found for IP: {dest_ip}")

def ftp_protocol(src_device,dest_device,file_name):
    file1 = open(file_name, "r")
    data = file1.readline()
    file1.close()
    src_device.setFile(os.path.join("C:\\Users\\Lenovo\\Desktop\\network simulator\\submission 1\\temp\\", file_name),data)
    src_device.send_file(dest_device)
    dest_device.process_file_data()



class Enddevice:
    endDevice_dict ={}
    i=1
    token_device=""
    def __init__(self,name,mac_addr,ip_addr,gateway):
        self.name=name
        self.token=False
        if Enddevice.i==1:
            self.token=True
            Enddevice.token_device=name
            Enddevice.i=2
        print(f"\n{name} End Device with mac address {mac_addr}.\n")
        ARP.add_entry(ip_addr,mac_addr)
        sleep(1)
        Enddevice.endDevice_dict[name]=self
        self.mac_addr=mac_addr
        self.gateway=gateway
        self.ip_addr=ip_addr
        self.switch_hub=None
        self.mem={
            80:""
        }
        self.last_received_frame_num=-1

    def getClass(self):
        return "enddevice"

    @staticmethod
    def getToken(name):
        if name==Enddevice.token_device:
            print(name," already has access")
        else:
            dev_list = list(Enddevice.endDevice_dict.values())
            index = dev_list.index(Enddevice.getObjectWithName(Enddevice.token_device))
            cycle_range = itertools.cycle(range(len(dev_list)))
            for i in cycle_range:
                if i>=index:
                    if(dev_list[i].name==name):
                        print(dev_list[i].name," has got token now , you can send")
                        Enddevice.token_device=dev_list[i].name
                        break
                    print(dev_list[i].name," has got token now")
                    Enddevice.token_device=dev_list[i].name
                    sleep(2)
                if i==len(dev_list)-1:
                    index=0
    @staticmethod
    def getObjectWithName(name):
        if name in Enddevice.endDevice_dict.keys():
            return Enddevice.endDevice_dict[name]
        return None
    
    def program(self):
        while True:
            print("Programs:")
            print("1.) send ARP request")
            print("2.) Implemet FTP protocol ") 
            print("3.) exit")
            ch=int(input("Enter your choice: "))
            print("--------------------------------------------")
            if ch==1:
                print("\n ARP Request")
                dest_device=Enddevice.getObjectWithName(input("Enter device name: "))
                ARP.send_arp_request(self.ip_addr,dest_device.ip_addr)
            elif ch==2:
                print()
                dest_device=input("Enter Destination Device: ")
                fileName=input("Enter File Name(with extension like .txt): ")
                dest_device=Enddevice.getObjectWithName(dest_device)
                if dest_device==False:
                    print("no such device exist in network")
                ftp_protocol(self,dest_device,fileName)
            else:
                break
            print("--------------------------------------------")
    
    
    def setFile(self,fileName,fileData):
        self.mem[80]=fileName+"||"+fileData

    def send_file(self,dest_device):
        self.send_data(self.mem[80],dest_device,80)

    def process_file_data(self):

        dict = self.mem[80].split('||')
        file1 = open(dict[0], "w")
        file1.write(dict[1])
        file1.close()

    def send_data(self,data,dest_device,port_no):
        dataitr = iter(data)
        x=30
        outputList = [data[y-x:y] for y in range(x, len(data)+x,x)]
        frames=[]
        i=1
        for f in outputList:
            #print(f)
            frames.append([packet(num=i,data=f,src_name=self.name,dest_name=dest_device.name,src_mac_addr=self.mac_addr,dest_mac_addr=dest_device.mac_addr,src_ip_addr=self.ip_addr,src_port=port_no,dest_port=port_no,dest_ip_addr=dest_device.ip_addr),len(outputList)])
            i+=1
        
        self.forward(dest_device.ip_addr,frames)

    def forward(self,dest_ip_addr,frames):
        self.send_frame_gbn(self.switch_hub,frames)
        if self.switch_hub.getClass()=="hub":
            self.switch_hub.receive(self)

        if not check_subnet(self.ip_addr,dest_ip_addr) and self.switch_hub.getClass()=="switch":
            self.switch_hub.receive(gateway=True)
        else:
            self.switch_hub.receive(gateway=False)
        

    def send_frame_gbn(self,device,frames): # go_back_n protocol # frames is list of packets
        print("-----------------------------------------------")
        print("Sending frames to ",device.name,"from device ",self.name," using gbn protocol")
        window_size=3
        print("\nWindow size is set to 3\n")
        win_start=0
        while win_start<len(frames):
            lock=False
            for i in range(win_start,min(win_start+window_size,len(frames))):    
                res=device.receive_frame_gbn(frames[i])
                if(res=="resend" ): # it means frame lost or ack lost
                    print("frame no",frames[i][0].num,"lost\n")
                    if(lock==False):
                        win_start=i
                        lock=True
                elif(res=="reject"):
                    print("frame ",i+1,"reject because one of the previous frame has not reached\n\n")    
                elif(res=="ACK"):
                    print("ACK received for frame number ",i+1 ,"\n\n")
                    win_start = i+1
                sleep(4)
        print("-----------------------------------------------")

        
    def receive_frame_gbn(self,frame:list[packet,int]):
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>75):
            sleep(4)
            print("Timed out. Send again\n")
            return "resend"      
        
        destination_mac_address, src_mac_address = frame[0].dest_mac_addr,frame[0].src_mac_addr
        
        if(destination_mac_address!=self.mac_addr):
            return False
        
        data, frame_num, port_no = frame[0].data, frame[0].num, frame[0].dest_port
        
        if(self.last_received_frame_num!=-1 and self.last_received_frame_num+1!=frame_num):
            return "reject"
        
        if(self.last_received_frame_num==-1 and frame_num>1):
            return "reject"
        
        print("Frame", frame_num,"Data received from device ",frame[0].src_name," mac_address "f"{src_mac_address} to device ",frame[0].dest_name," mac_address "f"{destination_mac_address}")
        
        self.last_received_frame_num = frame[0].num
        if(frame[0].num==1):
            self.mem[port_no]+=data

        elif(frame[0].num < frame[1]):
            self.mem[port_no]+=data
            
        else:
            self.mem[port_no]+=data
            #print("\nTotal Data received from mac_address "f"{src_mac_address} to mac_address "f"{destination_mac_address} is",self.mem[-1],"\n")
            print('Transmission completed')
            self.last_received_frame_num=-1

        return "ACK"
    
    def send_frame_stop_and_wait(self,device): # stop_and_wait protocol
        print("-----------------------------------------------")
        print("Sending frames to ",device.name,"from device ",self.name," using stop and wait protocol")
        frames=self.mem
        for frame in frames:
            print("Sending frame ",frame[0].num,":\n")
            
            res=device.receive_frame_stop_and_wait(frame)
            
            while(res=="resend"): # it will break when it will send ACK or false
                print("Resending frame ",frame[0].num,":\n")
                res=device.receive_frame_stop_and_wait(frame)
            
            if res==False:
                print("frame not for mac_address "f"{device.mac_address}\n")
                return
            
            if(res=="ACK"):
                print("ACK reveived\n")    
                sleep(1)
        print("-----------------------------------------------")
        
    def receive_frame_stop_and_wait(self,frame:list[packet,int]):    
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>75):
            sleep(4)
            print("Timed out. Send again\n")
            return "resend"      
        
        destination_mac_address, src_mac_address = frame[0].dest_mac_addr,frame[0].src_mac_addr
        
        if(destination_mac_address!=self.mac_address):
            return False
        
        data=frame[0].data

        print("Frame", frame[0].num," data received from mac address "f"{src_mac_address} to mac address "f"{destination_mac_address} is",data,"\n")
        
        if(frame[0].num==1 and frame[0].num==frame[1]):
            self.mem.append(data)
            print("\nTotal Data received from mac address "f"{src_mac_address} to mac address "f"{destination_mac_address} is",self.mem[-1],"\n")
            print('Transmission completed')
        
        if(frame[0].num==1):
            self.mem.append(data)
        elif(frame[0].num < frame[1]):
            self.mem[-1]+=data
        else:
            self.mem[-1]+=data
            print("\nTotal Data received from mac_address "f"{src_mac_address} to mac_address "f"{destination_mac_address} is",self.mem[-1],"\n")
            print('Transmission completed')
        
        return "ACK"
    
class hub:
    hub_link={}
    hub_router_link={}
    def __init__(self,name,mac_addr):
        self.mac_addr=mac_addr
        self.name=name
        print(f"\n{name} Switch Device with mac address {mac_addr}.\n")
        sleep(1)
        self.last_received_frame_num=-1
        self.mem=[]
        self.port_link={}
        self.port=0
        hub.hub_link[self]=[]

    def getClass(self):
        return "hub"
    
    def receive(self,send_device):
        print("\nReceived by hub ",self.name,"\n")
        self.froward(send_device)
        self.mem=[]
            
            
    def forward(self,send_device):
        print("\nReceived by hub ",self.name,"\n")
        for device in self.port_link.keys():
            if device != send_device:
                self.send_frame_gbn(device)
        
    def link(self,device,ip_addr=None):
        if device.getClass() == "router":
            hub.hub_router_link[self]=[ip_addr,device]
        elif device.getClass() == "enddevice":
            hub.hub_link[self].append(device)
            device.switch_hub=self

        self.port_link[device]=self.port
        self.port+=1
    
    
    def receive_frame_gbn(self,frame):
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>75):
            sleep(4)
            print("Timed out. Send again\n")
            return "resend"      
         
        frame_num =  frame[0].num
        if(self.last_received_frame_num!=-1 and self.last_received_frame_num+1!=frame_num):
            return "reject"
        if(self.last_received_frame_num==-1 and frame_num>1):
            return "reject"
        
        self.last_received_frame_num=frame[0].num
        if(frame[0].num==1):
            self.mem.append(frame)
        elif(frame[0].num<frame[1]):
            self.mem.append(frame)    
        else:
            self.mem.append(frame)
            print("Transmission to switch completed")
            #self.forward()
            #self.mem=[]
            self.last_received_frame_num=-1
        return "ACK"

    def send_frame_gbn(self,device): # go_back_n protocol
        print("-----------------------------------------------")
        print("Sending frames to ",device.name,"from device ",self.name," using gbn protocol")
        frames=self.mem
        window_size=3
        print("\nWindow size is set to 3\n")
        win_start=0
        while win_start<len(frames):
            lock=False
            for i in range(win_start,min(win_start+window_size,len(frames))):    
                res=device.receive_frame_gbn(frames[i])
                if(res=="resend" ): # it means frame lost or ack lost
                    print("frame no",frames[i][0].num,"lost\n")
                    if(lock==False):
                        win_start=i
                        lock=True
                if res==False:
                    print("frame not for mac_address "f"{device.mac_addr}\n")
                    return
                elif(res=="reject"):
                    print("frame ",i+1,"reject because one of the previous frame has not reached\n\n")    
                elif(res=="ACK"):
                    print("ACK received for frame number ",i+1 ,"\n\n")
                    win_start = i+1
                sleep(1)
        print("-----------------------------------------------")
        if device.getClass()=="switch":
            device.forward()
        if device.getClass()=="router":
            device.receive()

    def send_frame_stop_and_wait(self,device): # stop_and_wait protocol
        print("-----------------------------------------------")
        print("Sending frames to ",device.name,"from device ",self.name," using stop and wait protocol")
        frames=self.mem
        for frame in frames:
            print("Sending frame ",frame[0].num,":\n")
            
            res=device.receive_frame_stop_and_wait(frame)
            
            while(res=="resend"): # it will break when it will send ACK or false
                print("Resending frame ",frame[0].num,":\n")
                res=device.receive_frame_stop_and_wait(frame)
            
            if res==False:
                print("frame not for mac_address "f"{device.mac_address}\n")
                return
            
            if(res=="ACK"):
                print("ACK reveived\n")    
                sleep(1)
        print("-----------------------------------------------")
        if device.getClass()=="switch":
            device.forward()
        if device.getClass()=="router":
            device.receive()
    
    def receive_frame_stop_and_wait(self,frame:list[packet,int]):    
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>75):
            sleep(4)
            print("Timed out. Send again\n")
            return "resend"      
        
        if(frame[0].num==1 and frame[0].num==frame[1]):
            self.mem.append(frame)
            print('Transmission completed')
        
        if(frame[0].num==1):
            self.mem.append(frame)
        elif(frame[0].num < frame[1]):
            self.mem.append(frame)
        else:
            self.mem.append(frame)
            print('Transmission completed')
        
        return "ACK"
    
class switch:
    switch_link={}
    switch_router_link={}
    def __init__(self,name,mac_addr):
        self.mac_addr=mac_addr
        self.name=name
        print(f"\n{name} Switch Device with mac address {mac_addr}.\n")
        sleep(1)
        self.last_received_frame_num=-1
        self.mem=[]
        self.addr_table={}
        switch.switch_link[self]=[]

        self.dev_tabel={}
        self.port=1
        self.port_link={}

    def getClass(self):
        return "switch"
    
    def receive(self,gateway=False):
        print("\nReceived by switch ",self.name,"\n")
        if gateway:
            router=switch.switch_router_link[self][1]
            self.send_frame_gbn(router)
        else:
            self.forward()
            

    def forward(self):
        if len(self.addr_table.keys())==0:
            self.addr_learn()
            self.forward()
        else:
            dest_mac_addr=self.mem[0][0].dest_mac_addr
            if dest_mac_addr in self.addr_table.keys():
                port = self.addr_table[dest_mac_addr]
                dest_device=None
                for device,assc_port in self.port_link.items():
                    if assc_port==port:
                        dest_device=device
                        break
                self.send_frame_gbn(dest_device)
                #print("Packet arrived at the destination switch Device",dest_device.name," with mac addr ",dest_device.mac_addr)

    def link(self,device,ip_addr=None):
        if device.getClass() == "router":
            switch.switch_router_link[self]=[ip_addr,device]
        elif device.getClass() == "enddevice":
            switch.switch_link[self].append(device)
            device.switch_hub=self

        self.port_link[device]=self.port
        self.port+=1
    
    def getTable(self,learning_switch=None)->dict:
        if(len(self.addr_table.values())==0 and learning_switch!=None):
            self.addr_learn(lDevice=learning_switch)
            table=self.addr_table
            self.addr_table={}
            return table
        return self.addr_table
    
    def addr_learn(self,lDevice=None):
        if lDevice==None:
            print("\nDestination MAC not found, flooding packet to all ports\n")
            print("Address Learning starts\n")
        for device in self.port_link.keys():
            if device.getClass() == "enddevice":
                self.addr_table[device.mac_addr]=self.port_link[device]

            elif device.getClass() == "hub" and lDevice!=device:
                hub_queue=[device]
                port=self.port_link[device]
                
                while len(hub_queue) > 0:
                    dev = hub_queue.pop(0)
                    for d in hub.hub_link[dev]:
                        if d.getClass() == "enddevice":
                            self.addr_table[d.mac_addr] = port
                        elif d.getClass() == "switch" and d!=self:
                            switch_table=device.getTable(learning_switch=self)
                            for device1 in switch_table.keys():
                                self.addr_table[device1]=port
                        elif d.getClass() == "hub":
                            hub_queue.append(d)

            elif device.getClass() == "switch" and lDevice!=device:
                switch_table=device.getTable(learning_switch=self)
                for device1 in switch_table.keys():
                    self.addr_table[device1]=self.port_link[device]
    
    def receive_frame_gbn(self,frame):
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>75):
            sleep(4)
            print("Timed out. Send again\n")
            return "resend"       
        frame_num =  frame[0].num
        if(self.last_received_frame_num!=-1 and self.last_received_frame_num+1!=frame_num):
            return "reject"
        if(self.last_received_frame_num==-1 and frame_num>1):
            return "reject"

        self.last_received_frame_num=frame[0].num
        if(frame[0].num==1):
            self.mem.append(frame)
        elif(frame[0].num<frame[1]):
            self.mem.append(frame)    
        else:
            self.mem.append(frame)
            print("Transmission to switch completed")
            #self.mem=[]
            self.last_received_frame_num=-1
        return "ACK"

    def send_frame_gbn(self,device): # go_back_n protocol
        print("-----------------------------------------------")
        print("Sending frames to ",device.name,"from device ",self.name," using gbn protocol")
        frames=self.mem
        window_size=3
        print("\nWindow size is set to 3\n")
        win_start=0
        while win_start<len(frames):
            lock=False
            for i in range(win_start,min(win_start+window_size,len(frames))):    
                res=device.receive_frame_gbn(frames[i])
                if(res=="resend" ): # it means frame lost or ack lost
                    print("frame no",frames[i][0].num,"lost\n")
                    if(lock==False):
                        win_start=i
                        lock=True
                elif(res=="reject"):
                    print("frame ",i+1,"reject because one of the previous frame has not reached\n\n")    
                elif(res=="ACK"):
                    print("ACK received for frame number ",i+1 ,"\n\n")
                    win_start = i+1
                sleep(1)
        print("-----------------------------------------------")
        if device.getClass()=="hub":
            device.forward(self)
        elif device.getClass()=="switch":
            device.forward()
        elif device.getClass()=="router":
            device.receive()

    def send_frame_stop_and_wait(self,device): # stop_and_wait protocol
        print("-----------------------------------------------")
        print("Sending frames to ",device.name,"from device ",self.name," using stop and wait protocol")
        frames=self.mem
        for frame in frames:
            print("Sending frame ",frame[0].num,":\n")
            
            res=device.receive_frame_stop_and_wait(frame)
            
            while(res=="resend"): # it will break when it will send ACK or false
                print("Resending frame ",frame[0].num,":\n")
                res=device.receive_frame_stop_and_wait(frame)
            
            if(res=="ACK"):
                print("ACK reveived\n")    
                sleep(1)
        print("-----------------------------------------------")
        if device.getClass()=="hub":
            device.forward(self)
        elif device.getClass()=="switch":
            device.forward()
        elif device.getClass()=="router":
            device.receive()
    
    def receive_frame_stop_and_wait(self,frame:list[packet,int]):    
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>75):
            sleep(4)
            print("Timed out. Send again\n")
            return "resend"      
        
        if(frame[0].num==1 and frame[0].num==frame[1]):
            self.mem.append(frame)
            print('Transmission to switch completed')
        
        if(frame[0].num==1):
            self.mem.append(frame)
        elif(frame[0].num < frame[1]):
            self.mem.append(frame)
        else:
            self.mem.append(frame)
            print('Transmission to switch completed')
        
        return "ACK"


class router:
    router_dict={}
    link_dict={}
    def __init__(self,name,mac_addr,ip_addr=None):
        self.name=name
        self.mac_addr=mac_addr
        print(f"{name} router Device with mac address {mac_addr}.\n")
        self.ip_addr=[]
        self.last_received_frame_num=-1
        self.mem=[]
        if ip_addr!=None:
            self.ip_addr.append(ip_addr)
        self.route_table={}
        self.send_table={}
        router.router_dict[get_network_addr(ip_addr)]=self
        self.max_connect=10

    def getClass(self):
        return "router"

    '''def addNetwork(self,ip_addr):
        self.ip_addr.append(ip_addr)
        router.router_dict[ip_addr]=self'''

    def setRouteTable(self):
        route_table={}
        print("Static routing for router ",self.name,": ")
        while True:
            destination=input("Enter destination ip: ")
            nextHop=input("Enter next hop: ")
            route_table[get_network_addr(destination)]=get_network_addr(nextHop)
            exit=input("Enter x for exit: ")
            if exit=='x':
                break
        self.route_table=route_table
        self.printTable()
        sleep(1)
    
    def printTable(self):
        print("--------------------------------------")
        print("Route table of ",self.name,": ")
        print("Destination | Next Hop")
        for key,value in self.route_table.items():
            print(key,end=" | ")
            print(value)
        print("--------------------------------------")

    def getRouteTable(self):
        return self.route_table
    
    def rip_protocol(self):
        self.BellmanFord()

    def link(self,l_router,ip_addr,w):
        router.link_dict[get_network_addr(ip_addr)]=[l_router,self,w]
    
    #rip routing protocol
    def BellmanFord(self):
        distance = {}
        prev_node = {}

        for u, v,w in router.link_dict.values():
                distance[u]=float("Inf")
                distance[v]=float("Inf")

        prev_node=copy.copy(distance)

        for i in prev_node.keys():
            prev_node[i]=None
        
        distance[self] = 0

        for u, v, weight in router.link_dict.values():
            if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    prev_node[v] = u
            elif distance[v] != float('inf') and distance[v] + weight < distance[u]:
                    distance[u] = distance[v] + weight
                    prev_node[u] = v

        table = {}
        for dest in distance.keys():
            if dest != self:
                path = []
                curr = dest
                while curr is not None:
                    path.append(curr)
                    curr = prev_node[curr]
                path.reverse()
                next_node = None if len(path) == 1 else path[1]
                table[dest] = next_node
        
        self.send_table=table

        for key1,value1 in table.items():
            ip=""
            for key,value in router.link_dict.items():
                if value[0]==self and value[1]==value1:
                    ip=key
                elif value[1]==self and value[0]==value1:
                    ip=key
            table[key1]=ip
        table1={}
        for key,value in table.items():
            for ip in key.ip_addr:
                table1[get_network_addr(ip)]=get_network_addr(value)
        
        self.route_table=table1
        self.printTable()
        sleep(1)

    def receive(self,frames=None):
        if frames!=None:
            self.mem=frames
        
        dest = get_network_addr(self.mem[0][0].dest_ip_addr)
        #src = get_network_addr(self.mem[0][0].src_ip_addr)
        #if dest not in self.route_table.keys():
        #    return
        
        dest_rt = router.getObject(dest)

        #print("\nRouting Start: \n")

        if self.mac_addr!=dest_rt.mac_addr:
            print("Reached router ",self.name)
            rt_table=self.getRouteTable()
            src=rt_table[dest]
            if src in router.link_dict.keys():
                print("Passing through link: ",src)
                l,r,w = router.link_dict[get_network_addr(src)]
                if l!=self:
                    l.receive(frames=self.mem)
                elif r!=self:
                    r.receive(frames=self.mem)
        else:
            print("\nReached the destination router ",dest_rt.name,"and the network",dest,"\n")
            self.forward_in_net(self.mem)
        
            

    def forward_in_net(self,frames):
        self.mem=frames
        # forwarding to switch
        for switch_dev,[link_ip,rt_dev] in switch.switch_router_link.items():
            if link_ip == self.ip_addr[0]:
                print("\nForwarding to Switch ",switch_dev.name," with mac_address ",switch_dev.mac_addr,"\n")
                self.send_frame_gbn(switch_dev)
                return
        
        # forwarding to shub 
        for hub_dev,[link_ip,rt_dev] in hub.hub_router_link.items():
            if link_ip == self.ip_addr[0]:
                print("\nForwarding to hub ",hub_dev.name," with mac_address ",hub_dev.mac_addr,"\n")
                self.send_frame_gbn(hub_dev)
                return
                #switch_dev.forward(packet)

    def receive_frame_gbn(self,frame):
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>75):
            sleep(4)
            print("Timed out. Send again\n")
            return "resend"       
        frame_num =  frame[0].num
        if(self.last_received_frame_num!=-1 and self.last_received_frame_num+1!=frame_num):
            return "reject"
        if(self.last_received_frame_num==-1 and frame_num>1):
            return "reject"

        self.last_received_frame_num=frame[0].num
        if(frame[0].num==1):
            self.mem.append(frame)
        elif(frame[0].num<frame[1]):
            self.mem.append(frame)    
        else:
            self.mem.append(frame)
            print("Transmission to switch completed")
            #self.forward()
            #self.mem=[]
            self.last_received_frame_num=-1
        return "ACK"

    def send_frame_gbn(self,device): # go_back_n protocol
        print("-----------------------------------------------")
        print("Sending frames to ",device.name,"from device ",self.name," using gbn protocol")
        frames=self.mem
        window_size=3
        print("\nWindow size is set to 3\n")
        win_start=0
        while win_start<len(frames):
            lock=False
            for i in range(win_start,min(win_start+window_size,len(frames))):    
                res=device.receive_frame_gbn(frames[i])
                if(res=="resend" ): # it means frame lost or ack lost
                    print("frame no",frames[i][0].num,"lost\n")
                    if(lock==False):
                        win_start=i
                        lock=True
                elif(res=="reject"):
                    print("frame ",i+1,"reject because one of the previous frame has not reached\n\n")    
                elif(res=="ACK"):
                    print("ACK received for frame number ",i+1 ,"\n\n")
                    win_start = i+1
                sleep(1)
        print("-----------------------------------------------")
        if device.getClass()=="switch":
            device.forward()
        elif device.getClass()=="hub":
            device.forward(self)

    def send_frame_stop_and_wait(self,device): # stop_and_wait protocol
        print("-----------------------------------------------")
        print("Sending frames to ",device.name,"from device ",self.name," using stop and wait protocol")
        frames=self.mem
        for frame in frames:
            print("Sending frame ",frame[0].num,":\n")
            
            res=device.receive_frame_stop_and_wait(frame)
            
            while(res=="resend"): # it will break when it will send ACK or false
                print("frame no",frame[0].num,"lost\n")
                print("Resending frame ",frame[0].num,":\n")
                res=device.receive_frame_stop_and_wait(frame)
            
            if(res=="ACK"):
                print("ACK reveived\n")    
                sleep(1)
        print("-----------------------------------------------")
        if device.getClass()=="switch":
            device.forward()
        elif device.getClass()=="hub":
            device.forward(self)
    
    def receive_frame_stop_and_wait(self,frame:list[packet,int]):    
        probabError=random.uniform(0,1)
        probabError*=(100)    
        if(probabError>75):
            sleep(4)
            print("Timed out. Send again\n")
            return "resend"      
        
        if(frame[0].num==1 and frame[0].num==frame[1]):
            self.mem.append(frame)
            print('Transmission to switch completed')
        
        if(frame[0].num==1):
            self.mem.append(frame)
        elif(frame[0].num < frame[1]):
            self.mem.append(frame)
        else:
            self.mem.append(frame)
            print('Transmission to switch completed')
        
        return "ACK"
    
    @staticmethod
    def getRouter(rt,link_ip_addr):
        if link_ip_addr in router.link_dict.keys():
            for rt1 in router.link_dict[link_ip_addr]:
                if rt!=rt1:
                    return  rt1
        return False
    
    @staticmethod
    def getObject(ip_addr):
        #net_addr=get_network_addr(ip_addr)
        if ip_addr in router.router_dict.keys():
            return  router.router_dict[ip_addr]
        return False

def generate_mac_address():
    """Grants A MAC Address To Each Of The Device"""
    mac = [str(random.randint(0xB,0x63)) for x in range(3)]
    return ("11:11:11:"+":".join(mac))



