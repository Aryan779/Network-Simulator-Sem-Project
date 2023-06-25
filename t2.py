from rip_routing import router
from rip_routing import Enddevice
from rip_routing import switch
from rip_routing import hub
from rip_routing import generate_mac_address


def main():
    print("\n Test Case 2 with RIP protocol\n")

    r1=router("r1",generate_mac_address(),"70.0.0.1")
    r2=router("r2",generate_mac_address(),"50.0.0.1")
    r3=router("r3",generate_mac_address(),"60.0.0.1")
    r4=router("r4",generate_mac_address(),"80.0.0.1")

    r1.link(r2,"90.0.0.0",1)
    r2.link(r3,"91.0.0.0",1)
    r4.link(r3,"92.0.0.0",1)
    r4.link(r1,"93.0.0.0",1)
    r4.link(r2,"94.0.0.0",1)


    s1=switch("s1",generate_mac_address())
    s2=switch("s2",generate_mac_address())
    s3=switch("s3",generate_mac_address())
    h1=hub("h1",generate_mac_address())
    

    s1.link(r1,"70.0.0.1")
    s2.link(r2,"50.0.0.1")
    s3.link(r3,"60.0.0.1")
    h1.link(r4,"80.0.0.1")

    d1=Enddevice("d1",generate_mac_address(),"70.0.0.2","70.0.0.1")
    d2=Enddevice("d2",generate_mac_address(),"50.0.0.2","50.0.0.1")
    d3=Enddevice("d3",generate_mac_address(),"60.0.0.2","60.0.0.1")
    d4=Enddevice("d4",generate_mac_address(),"80.0.0.2","80.0.0.1")

    
    s1.link(d1)
    s2.link(d2)
    s3.link(d3)
    h1.link(d4)

    r1.rip_protocol()
    r2.rip_protocol()
    r3.rip_protocol()
    r4.rip_protocol()


    while True:
        device_name=input("Enter device name(d1,d2,d3,d4): ")
        device = Enddevice.getObjectWithName(device_name)
        Enddevice.getToken(device_name)
        device.program()

main()