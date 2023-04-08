from network_simulator import EndDevice
import time

print("--> test Case 1 established connection betweeen two device and shown protcol implementation\n")

d1=EndDevice(1)
d2=EndDevice(2)
d3=EndDevice(3)
d1.connect_device(d2)
d2.connect_device(d1)

        
print("Which transmission do you want: ")
print("1.) d1 ---> d2")
print("2.) d2 ---> d1\n")

opt = int(input("choose option(1 or 2): "))
print("\nWhich Flow Control Protocol do you want to implement: ")
print("1.) Stop & wait ARQ")
print("2.) Go Back N ARQ")
opt1 = int(input("choose option(1 or 2): "))
data = input("Enter data you want to send: ")
print("\n")
if(opt==1):
    frames = d1.create_frame(data,d2)
    print("total frames created: ",len(frames),"\n\n")
    time.sleep(3)
    if opt1 is 1:
        print("\nImplementing Stop & Wait protocol\n")
        d1.send_frame_stop_and_wait(frames,d2)
    elif opt1 is 2:
        print("\nImplementing Go Back N protocol\n")
        d1.send_frame_gbn(frames,d2)


elif(opt==2):
    frames = d2.create_frame(data,d1)
    print("total frames created: ",len(frames),"\n\n")
    time.sleep(3)
    if opt1 is 1:
        print("\nImplementing Stop & Wait protocol\n")
        d2.send_frame_stop_and_wait(frames,d1)
    elif opt1 is 2:
        print("\nImplementing Go Back N protocol\n")
        d2.send_frame_gbn(frames,d1)

