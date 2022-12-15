import serial.tools.list_ports
import serial

from tkinter import *
from tkinter import ttk

import threading, time

import pygame 

root = Tk()
root.title("Driver")


ports = serial.tools.list_ports.comports(include_links=False)
languages_var = Variable(value=ports)

state = StringVar()
state.set('Не подключенно')

s = serial.Serial()


def handle_click():
    global state, connect_port, s

    try:
        s = serial.Serial(port=connect_port, baudrate=115200,write_timeout=1, timeout=3)
    except:
        s.close()
        state.set("Не удалось подключится")
    else:
        s.flushInput()
        s.flushOutput()
        s.write(str.encode("START\n"))
        data = s.readline(200)
        print(data)
        if len(data) != 0:
            state.set("Подключенно")
        else:
            state.set("Устройство не отвечает")

button_rigth = False
button_left  = False

button_down = False
button_up  = False

m = 0
rigth = 39
up = 38
down = 40
left = 37

def down(e):
    global m
    if m == 0:
        if e.keycode == left:
            s.write(str.encode("XLEFT\n"))
            print("dgdfg")
        if e.keycode == rigth:
            s.write(str.encode("XRIGTH\n"))
            print("dgdfg")

        if e.keycode == up:
            s.write(str.encode("YUP\n"))
            print("dgdfg")
        if e.keycode == down:
            s.write(str.encode("YDOWN\n"))
            print("dgdfg")
        m = 1

def up(e):
    global m
    if m == 1:
        if e.keycode == left:
            s.write(str.encode("XSTOP\n"))
            print("dgdfg")
        if e.keycode == rigth:
            s.write(str.encode("XSTOP\n"))
            print("dgdfg")

        if e.keycode == up:
            s.write(str.encode("YSTOP\n"))
            print("dgdfg")
        if e.keycode == down:
            s.write(str.encode("YSTOP\n"))
            print("dgdfg")        
        m = 0


def handle_update():
    global ports, languages_var
    ports = serial.tools.list_ports.comports(include_links=False)
    languages_var = Variable(value=ports)
    languages_listbox.delete(0, END)  #clear listbox
    for filename in ports: #populate listbox again
        languages_listbox.insert(END, filename)

def selected(event):
    global connect_port
    selected_indices = languages_listbox.curselection()
    selected_langs = ",".join([languages_listbox.get(i) for i in selected_indices])
    selected_langs = selected_langs[:selected_langs.find(" ")]
    connect_port = selected_langs



frame3 = ttk.Frame(master=root, width=100, height=100,)
frame3.pack(fill=Y, side=LEFT)

state_label = ttk.Label(master = frame3, text="Состояние:")
state_label.pack(anchor=NW, fill=Y, padx=5, pady=5)

current_state_label = ttk.Label(master = frame3, textvariable=state)
current_state_label.pack(anchor=NW, fill=Y, padx=5, pady=5)

languages_listbox = Listbox(master = frame3, listvariable=languages_var, selectmode=EXTENDED)
languages_listbox.pack(anchor=NW, fill=X, padx=5, pady=5)
languages_listbox.bind("<<ListboxSelect>>", selected)

connect_button = ttk.Button(frame3, text="Подключится", command=handle_click)
connect_button.pack(anchor=NW, fill=X, padx=5, pady=5)

update_button = ttk.Button(frame3, text="Обновить", command=handle_update)
update_button.pack(anchor=NW, fill=X, padx=5, pady=5)





root.bind('<KeyPress>', down)
root.bind('<KeyRelease>', up)



root.mainloop()


