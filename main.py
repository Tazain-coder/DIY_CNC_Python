import serial
import serial.tools.list_ports

streaming: bool = False
speed: float = 0.001
gcode: str
i: int = 0

portname: str = None


def port_select() -> list:
    ports = serial.tools.list_ports.comports()
    all_ports = []
    if len(ports) > 0:
        for port in ports:
            all_ports.append(port)
        return all_ports

    else:
        print('No Ports Found or device not connected')

"""
Add ways to work with ports

"""
port_select()


def openSerialPorts():
    if portname == None:
        return

# with serial.Serial('COM4', 9600, timeout=1) as ser:
#    x = ser.read()          # read one byte
#    s = ser.read(10)        # read up to ten bytes (timeout)
#    line = ser.readline()   # read a '\n' terminated line
#    print(line)
