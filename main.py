import serial

streaming:bool = False
speed:float = 0.001
gcode:str
i:int = 0

portname:str = None

def openSerialPorts():
   if portname == None:
      return
# void
# openSerialPort()
# {
# if (portname == null)
# return;
# if (port != null) port.stop();
#
# port = new
# Serial(this, portname, 9600);
#
# port.bufferUntil('\n');
# }


with serial.Serial('COM4', 9600, timeout=1) as ser:
   x = ser.read()          # read one byte
   s = ser.read(10)        # read up to ten bytes (timeout)
   line = ser.readline()   # read a '\n' terminated line
   print(line)