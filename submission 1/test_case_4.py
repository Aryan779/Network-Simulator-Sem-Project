from network_simulator import Switch,EndDevice
import time


print("--> test case 4 : switch connected to 5 devices")
print("\nChoose the option of flow control protocol fro device and switch same\n")
time.sleep(2)

devices=[EndDevice(1),EndDevice(2),EndDevice(3),EndDevice(4),EndDevice(5)]
s1=Switch(12)
for i in range(0,5):
    s1.connect_device(devices[i])
    time.sleep(1)


print("\nWhich Flow Control Protocol do you want to implement fro devices: ")
print("1.) Stop & wait ARQ")
print("2.) Go Back N ARQ")
opt1 = int(input("choose option(1 or 2): "))


while True:
    
    print("\nWhich device wants to send data (device from 0 to 4): ",end=" ")
    ind=int(input())

    data=input("\n what data you want to send: ")

    print("\nWhich device wants to receive data (device from 0 to 4): ",end=" ")
    ind1=int(input())

    if(ind==ind1):
        raise Exception("sender and receiver are same")
    
    frames=devices[ind].create_frame(data,devices[ind1])

    print("\n total frames created :",len(frames),"\n")
    if(opt1==1):
        devices[ind].send_frame_stop_and_wait(frames,s1)
    elif(opt1==2):
        devices[ind].send_frame_gbn(frames,s1)
    







