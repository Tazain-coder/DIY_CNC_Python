import serial
import serial.tools.list_ports
import keyboard

streaming: bool = False
speed: float = 0.001
gcode: str
i: int = 0


def allPorts() -> dict:
    ports = serial.tools.list_ports.comports()
    all_ports: dict = {}
    if len(ports) > 0:
        for idx,port in enumerate(ports):

            all_ports[idx] = port.name
        return all_ports

    else:
        print('No Ports Found or device not connected')

def openSerialPorts(portname:str = None):
    if portname == None:
        print("No ports Were Selected")
    else:
        print(f"Opening Serial port in : {portname}")
        ser = serial.Serial(portname, 9600,timeout=1)
        return ser
def getfilepath():
    pass
def streamGcode():
    if not streaming:
        return

ser = openSerialPorts(allPorts()[0])


while True:
    try:
        if keyboard.is_pressed('2'):
            ser.write(b"M300 S30\n")
        if keyboard.is_pressed('5'):
            ser.write(b"M300 S50\n")
        if keyboard.is_pressed('a'):
            ser.write(b"G21/G90/G1 X-10  F3500\n")
        if keyboard.is_pressed('d'):
            ser.write(b"G21/G90/G1 X10 F3500\n")
        if keyboard.is_pressed('w'):
            ser.write(b"G21/G90/G1 Y10 F3500\n")
        if keyboard.is_pressed('s'):
            ser.write(b"G21/G90/G1 Y-10 F3500\n")
        if keyboard.is_pressed('g') and not streaming:
            streaming=True
            streamGcode()
            streaming=False


        if keyboard.is_pressed('x'):
            break

    except:
        break


ser.close()

