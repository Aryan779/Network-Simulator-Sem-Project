from network_simulator import EndDevice,hub



def send_data(access_device,data,destination_device,hub_device): # destination_device: which device will receive the data
    frames = access_device.create_frame(data,destination_device)
    access_device.send_bits_hub(frames,hub_device)


#test case 3
print("\n\n -->test case 3: n number of end devices connected to hub \n\n")
h1 = hub(102)
'''
d1 = EndDevice(1)
d2 = EndDevice(2)
d3 = EndDevice(3)
d4 = EndDevice(4)
d5 = EndDevice(5)
'''
n=5 #num of devies connected to hub
devices=[EndDevice(1), EndDevice(2), EndDevice(3), EndDevice(4), EndDevice(5)]
for i in range(0,n):
    h1.connect_device(devices[i])
    devices[i].connect_with_hub(h1)

token=0 # token is always frist device assumed

while True:
    
    print("Enter the device number to send data to hub",0,"-",n-1,": ")
    destination = int(input())

    # validity of the node
    if destination < 0 or destination >= n:
        print("Invalid device number. Please try again.")
        continue

    if token==destination:
        print("Token is already assigned. Proceed ahead")
    elif token < destination:
        print("End Device", token, " with mac address ",devices[token].mac_address,"Has access \n")
        print("------Passing the Token ")
        for i in range(1,n):
            #endDevices[i] = t
            print("End Device ", i+token, "with mac address ",devices[i+token].mac_address,"Has access \n")

            if destination == i+token:
                print("----------------------------Access granted-----------------------------------")
                print("End Device ",destination,"with mac address ",devices[i+token].mac_address," is sending")
                token=destination
                print("E\nnter the device number that will receive data that was send to hub",0,"-",n-1,": ")
                receiving_device = int(input())
                if(token==receiving_device):
                    raise Exception("sender and receiver device are same") 
                print("\n Enter data you want to send: ")
                data = input()
                print('\n')
                send_data(devices[token],data,devices[receiving_device],h1)
                break
            if i != destination:
                print("------Passing the Token ")
    else:
        print("End Device ", token, "Has access ")
        print("------Passing the Token ")
        for i in range(1,n):
            #endDevices[i] = token
            print("End Device ", token-i, "Has access now")

            if destination == token-i:
                print("----------------------------Access granted-----------------------------------")
                token=destination
                break
            if i != destination:
                print("------Passing the Token ")




'''
frames = d1.create_frame(data,d5)
d1.send_bits_hub(frames,h1,opt1)
'''