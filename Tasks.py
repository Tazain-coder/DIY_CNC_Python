import time
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import cachetools
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import keyboard
import serial
import serial.tools.list_ports
from serial.serialutil import SerialException

# initial Confige for Tkinter and ttkbootstrap
root = tb.Window(themename="superhero")
root.title("test")
root.geometry('800x600')


def allPorts() -> list:
    """
    :return: A list of all the ports that are available at the moment
    """
    ports = serial.tools.list_ports.comports()
    all_ports: list = []
    if len(ports) > 0:
        for port in ports:
            all_ports.append(port.name)
        return all_ports


def checkPortCon():
    portname = ports_dropdown.get()
    print(portname)
    if portname == 'No Ports Connected':
        ports_label.config(text="No Ports Selected")
        return
    else:
        try:
            global ser
            ser = serial.Serial(portname, 9600, timeout=None)
            ser.read()
            ports_label.config(text="Connected")

        except SerialException as se:
            ports_label.config(text="No Ports Selected")


def testing():
    test_instructions = [b"M300 S30\n",
                         b"M300 S50\n",
                         b"G21/G90/G1 X10  F3500\n",
                         b"G21/G90/G1 Y10 F3500\n",
                         b"G21/G90/G1 Y-10 F3500\n",
                         b"G21/G90/G1 X-10 F3500\n"]

    for inst in test_instructions:
        ser.write(inst)
        time.sleep(1)


def fileSelector():
    filetypes = (
        ('Gcode files', '*.gcode'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a gcode file',
        initialdir='/',
        filetypes=filetypes)

    if not filename:
        print("selection was cancelled")




# ------------- Port Selection and Connections ----------------
ports_label = tb.Label(text="Select Port from the box below", font=('Terminal', 14), bootstyle='danger')
ports_label.pack(pady=10)

ports = ['No Ports Available']


def update_ports():
    if allPorts():
        ports = allPorts()
    else:
        ports = ['No Ports Available']
    ports_dropdown.config(values=ports)
    ports_dropdown.after(1000, update_ports)


ports_dropdown = tb.Combobox(root, bootstyle="success", values=ports)
ports_dropdown.pack(pady=15)
ports_dropdown.current(0)

update_ports()

port_connect = tb.Button(text="connect", command=checkPortCon, bootstyle='primary')
port_connect.pack(pady=20)
# ------------- Port Selection and Connections ----------------

# ------------- Testing ----------------
test_label = tb.Label(text='Test the machine')
test_label.pack(pady=30)

test_button = tb.Button(text='Start', bootstyle='primary', command=testing)
test_button.pack(pady=35)

# ------------- Testing ----------------

# ------------- Gcode Running ----------------
gcode_label = tb.Label(text='Run Gcode')
gcode_label.pack(pady=40)

gcode_button = tb.Button(text='Open File', bootstyle='primary', command=fileSelector)
gcode_button.pack(pady=45)

# ------------- Gcode Running ----------------
root.mainloop()
