from network_simulator import EndDevice,Switch,hub
import matplotlib.pyplot as plt
import networkx as nx

# create an empty graph
G = nx.Graph()

# add nodes to the graph
G.add_node('End Device\n mac=1')
G.add_node('End Device\n mac=2')
G.add_node('End Device\n mac=3')
G.add_node('End Device\n mac=4')
G.add_node('End Device\n mac=5')
G.add_node('Hub\n mac=101')
G.add_node('Hub\n mac=102')
G.add_node('Switch\n mac=201')
G.add_node('End Device\n mac=10')
G.add_node('End Device\n mac=9')
G.add_node('End Device\n mac=8')
G.add_node('End Device\n mac=7')
G.add_node('End Device\n mac=6')

# add edges to connect the nodes
G.add_edge('End Device\n mac=1', 'Hub\n mac=101')
G.add_edge('End Device\n mac=2', 'Hub\n mac=101')
G.add_edge('End Device\n mac=3', 'Hub\n mac=101')
G.add_edge('End Device\n mac=4', 'Hub\n mac=101')
G.add_edge('End Device\n mac=5', 'Hub\n mac=101')
G.add_edge('Switch\n mac=201', 'Hub\n mac=101')
G.add_edge('Switch\n mac=201', 'Hub\n mac=102')

G.add_edge('End Device\n mac=6', 'Hub\n mac=102')
G.add_edge('End Device\n mac=7', 'Hub\n mac=102')
G.add_edge('End Device\n mac=8', 'Hub\n mac=102')
G.add_edge('End Device\n mac=9', 'Hub\n mac=102')
G.add_edge('End Device\n mac=10', 'Hub\n mac=102')

# draw the graph
pos = {'Hub\n mac=101': (10, 0), 'Switch\n mac=201': (20, 0), 'Hub\n mac=102': (30, 0),'End Device\n mac=1':(10,7),'End Device\n mac=2':(14,-7),'End Device\n mac=5':(6,-7),'End Device\n mac=3':(6,4),'End Device\n mac=4':(14,4),'End Device\n mac=6':(30,7),'End Device\n mac=7':(34,-7),'End Device\n mac=8':(26,-7),'End Device\n mac=9':(26,4),'End Device\n mac=10':(34,4)}

plt.title("test case 5\n")
nx.draw(G,pos, with_labels=True, node_color='lightblue',node_size=2500)
plt.show()
#--------------------------------------------------------------------------------------------------------------

print("--> test case 5: two star toppolgy each connected with a hub and two hubs connected to switch")
h1=hub(101)
h2=hub(102)

devices1=[EndDevice(1),EndDevice(2),EndDevice(3),EndDevice(4),EndDevice(5)]
devcies1_mac=[device.mac_address for device in devices1]
devices2=[EndDevice(6),EndDevice(7),EndDevice(8),EndDevice(9),EndDevice(10)]
devcies2_mac=[device.mac_address for device in devices2]

for i in range(0,5):
    h1.connect_device(devices1[i])
    h2.connect_device(devices2[i])
    
s1=Switch(201)
s1.connect_with_hub(h1)
h1.connect_with_switch(s1)
s1.connect_with_hub(h2)
h2.connect_with_switch(s1)

while True:
    hubDevice=None

    print("\nWhich device wants to send data (mac address from 1 to 10): ",end=" ") 
    ind=int(input())


    data=input("\n what data you want to send: ")

    print("\nWhich device wants to receive data (mac address from 1 to 10): ",end=" ")
    ind1=int(input())

    if(ind in devcies1_mac):
        ind=devcies1_mac.index(ind)
        device1=devices1[ind]
        hubDevice=h1
    elif(ind in devcies1_mac):
        ind=devcies2_mac.index(ind)
        device1=devices2[ind]
        hubDevice=h2

    if(ind1 in devcies1_mac):
        ind1=devcies1_mac.index(ind1)
        device2=devices1[ind1]
    elif(ind1 in devcies1_mac):
        ind1=devcies2_mac.index(ind1)
        device2=devices2[ind1]




    frames=device1.create_frame("aryan",device2)
    print("\nTotal frames created ",len(frames),"\n")
    device1.send_bits_hub(frames,hubDevice)
    print("\nTotal transmission completed\n")
    print("\nTotal data received by device with mac address",device2.mac_address,"is",device2.mem_stack[-1],"\n\n")
