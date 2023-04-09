from network_simulator import EndDevice

print("--> test case: 2 token passing in token ring topology\n")
'''
    d1 <------> d2
     \\         /
      \\       /
       \\     /
        \\    /          
           d3

'''
devices=[EndDevice(1,0),EndDevice(2,1),EndDevice(3,2),EndDevice(4,3),EndDevice(5,4)]
#d1=EndDevice(1,sequence=0)
#d2=EndDevice(2,sequence=1)
#d3=EndDevice(3,sequence=2)
#d4=EndDevice(4,sequence=3)
#d5=EndDevice(5,sequence=4)

#forming ring topology of nodes = 5
n=5
for i in range(0,n):
    if i < n-1:
        devices[i].connect_device(devices[i+1])
        devices[i+1].connect_device(devices[i])
    elif i==n-1:
        devices[i].connect_device(devices[0])
        devices[0].connect_device(devices[i])

token = 0 # always token will start from first device (index = 0 ) assumed
while True:
    # user to choose a node or device to send the token to
    destination = int(input("Enter the node number to send the token to (0-4): "))

    # validity of the node
    if destination < 0 or destination >= n:
        print("Invalid node or device number. Please try again.")
        continue

    # Check if the chosen node is the current node holding the token
    if token==destination:
        print("Token is already assigned. Proceed ahead")
    elif token < destination:
        print("End Device", token, "Has access ")
        print("------Passing the Token ")
        for i in range(1,n):
            #endDevices[i] = t
            print("End Device ", i+token, "Has access now")

            if destination == i+token:
                print("----------------------------Access granted-----------------------------------")
                print("End Device ",destination," is sending")
                token=destination
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

