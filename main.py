import serial
import serial.tools.list_ports

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




# with serial.Serial('COM4', 9600, timeout=1) as ser:
#    x = ser.read()          # read one byte
#    s = ser.read(10)        # read up to ten bytes (timeout)
#    line = ser.readline()   # read a '\n' terminated line
#    print(line)
