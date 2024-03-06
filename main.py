import time
from tkinter import filedialog as fd
import threading
import ttkbootstrap as tb

from serial import Serial
import serial.tools.list_ports


# initial Config for Tkinter and ttkbootstrap
root = tb.Window(themename="darkly")
root.title("DIY CNC Control Panel")
root.geometry('800x600')

# Variables
port: Serial  # Serial Port which will be connected
portname: str or None = None  # Name of the port which will be used

streaming: bool = False  # Flag to check if file is streaming
speed: float = 0.001
gcode: list = []  # list of commands in the gcode file
i: int = 0  # keeps count of the index


def allPorts() -> list:
    """
    :return: A list of all the ports that are available at the moment
    """

    ports = serial.tools.list_ports.comports() # Puts all the available ports in a Variable
    all_ports: list = [] # Stores all the available Ports

    if len(ports) > 0:
        for port_name in ports:
            all_ports.append(port_name.name)
        return all_ports


def checkPortCon():
    """
    This Fuction Sets the Portname (ex: COM4) ,
    Starts the serial port,
    Checks if it is runnin
    """
    global portname, port

    portname = ports_dropdown.get() # Gets the Currently selected item in ports_dropdown variable

    print(portname)
    if portname == 'No Ports Connected':
        ports_label.config(text="No Ports Selected")
        return
    else:
        port = Serial(portname, 9600, timeout=1)
        if port.is_open:
            ports_label.config(text="Connected")
        else:
            ports_label.config(text="Unable to connect")


def testing():
    """
    This Function tests if the Serial device is running
    :return:
    """
    if not port.is_open:
        port.open()

    test_instructions = [b"M300 S30\n",
                         b"M300 S50\n",
                         b"G21/G90/G1 X10  F3500\n",
                         b"G21/G90/G1 Y10 F3500\n",
                         b"G21/G90/G1 Y-10 F3500\n",
                         b"G21/G90/G1 X-10 F3500\n"]
    # Iterates over the testing instructions
    for inst in test_instructions:
        port.write(inst)
        time.sleep(1)


def fileSelector():
    """
    Gives a prompt to open a gcode file and gets the path to that file
    initiates gcode file
    :return:
    """

    global streaming, gcode, port

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
    else:
        print(f"User Selected: {filename}")
        gcode = [comms for comms in open(filename, 'r')]
        if len(gcode) <= 0:
            return
        else:
            gcode_button.state(["disabled"])
            print("Starting Streaming")
            streaming = True
            print("Staring Serial Event")
            run_send_gcode(filename, port)
            gcode_button.state(["!disabled"])


def send_gcode(filename, port):
    if not port.isOpen():
        print('Starting Serial Port at ')
        port.open()

    if not streaming:
        return

    try:
        # Discard the first three lines from the serial port
        for _ in range(3):
            port.readline()

        # Open G-code file
        with open(filename, 'r') as file:
            command_terminal_text.config(text=f'Running {filename.split("/")[-1]}')
            # Read each line from the file
            if streaming:
                for idx, line in enumerate(file, start=1):
                    # Send the G-code line through serial port
                    port.write(line.encode())
                    sent = f"Sent: {line.strip()}"

                    # Wait for response containing "ok"
                    response = b""
                    while b"ok" not in response:
                        chunk = port.read(port.in_waiting or 1)
                        if chunk:
                            response += chunk

                    response = f"Response: {response.decode().strip()}"
                    command_terminal.config(text=f'{sent} \n {response}')
                    gcode_progress = int(idx * (100 / (len([i for i in open(filename, 'r')]))))
                    if gcode_progress < 100:
                        progress_label.config(text=f"Progress {gcode_progress} %")
                        progress.config(value=gcode_progress)
                        gcode_button.config(bootstyle='success')
                    else:
                        progress_label.config(text=f"Idle")
                        progress.config(value=0)
                        command_terminal.config(text=f'idle')
                        command_terminal_text.config(text='Run a gcode to start')
                        gcode_button.config(bootstyle='light outline')



    except FileNotFoundError:
        print("File not found:", filename)
    except serial.SerialException as e:
        print("Serial communication error:", e)
    finally:
        # Close serial port
        print("Closing Port")
        port.close()
        print(port.isOpen())


def run_send_gcode(filename, port):
    thread = threading.Thread(target=send_gcode, args=(filename, port))
    thread.start()
    return thread


# Main Divs
left_side = tb.Frame()
left_side.pack(side='left')

right_side = tb.Label()
right_side.pack(side='right')

bottom_side = tb.Label()
bottom_side.pack(side='bottom')

# ------------- Port Selection and Connections ----------------
Main_menu = tb.Frame(left_side)
Main_menu.pack(ipadx=10)

ports_label = tb.Label(Main_menu, text="Select Port from the box below", font=('Terminal', 14), bootstyle='danger')
ports_label.pack(pady=10)

ports = ['No Ports Selected']


def update_ports():
    if allPorts():
        ports = allPorts()
    else:
        ports = ['No Ports Available']
    ports_dropdown.config(values=ports)
    ports_dropdown.after(1000, update_ports)


# Port selection panel
ports_dropdown = tb.Combobox(Main_menu, bootstyle="info", values=ports)
ports_dropdown.pack(padx=15,side="left")
ports_dropdown.current(0)

update_ports()

port_connect = tb.Button(Main_menu, text="connect", command=checkPortCon, bootstyle='info')
port_connect.pack(side='left')
# ------------- Port Selection and Connections ----------------

# ------------- Testing ----------------
test_menu = tb.Label(left_side)
test_menu.pack(pady=30)

test_label = tb.Label(test_menu, text='Test the machine', font=('Terminal', 18), bootstyle='danger')
test_label.pack(pady=10)

test_button = tb.Button(test_menu, text='Start', bootstyle='primary', command=testing)
test_button.pack(fill='x')

# ------------- Testing ----------------

# ------------- Gcode Running ----------------
gcode_menu = tb.Label(left_side)
gcode_menu.pack(pady=30)

gcode_label = tb.Label(gcode_menu, text='Run Gcode', font=('Terminal', 18), bootstyle='danger')
gcode_label.pack(pady=20)

gcode_button = tb.Button(gcode_menu, text='Open File', bootstyle='light outline', command=fileSelector)
gcode_button.pack(pady=15, fill='x')

# ------------- Gcode Running ----------------
# _____________ Command Panel ______________
command_menu = tb.Button(right_side)
command_menu.pack(ipadx=150, padx=20, pady=20, ipady=20)

termina_menu = tb.Label(command_menu)
termina_menu.pack(pady=40, padx=10, ipady=50, ipadx=130)

command_terminal = tb.Label(termina_menu, text='Idle', bootstyle='success', font=('Terminal', 12))
command_terminal.pack(pady=20)

command_terminal_text = tb.Label(termina_menu, text='Run a gcode to start now', bootstyle='danger',
                                 font=('Terminal', 11))
command_terminal_text.pack(pady=20, side='bottom')
# _____________ Command Panel _____________


# ------------- Progress ----------------
progress_section = tb.Label(right_side)
progress_section.pack(padx=25, ipadx=170)

progress_label = tb.Label(progress_section, text='Idle', font=('Terminal', 18), bootstyle='danger')
progress_label.pack(pady=20)

# progress = tb.Floodgauge(progress_section, length=0, bootstyle='danger', mode='determinate')
# progress.pack(padx=20,side='right')

progress = tb.Progressbar(progress_section, bootstyle='success striped', maximum=100, mode='determinate', length=300)
progress.pack(ipadx=5, ipady=5, padx=5, pady=5)
# ------------- Progress ----------------


root.mainloop()
