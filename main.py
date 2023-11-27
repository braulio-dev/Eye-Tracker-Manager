from tkinter import DISABLED
from tkinter.constants import NORMAL

import calibrar
import tobii_research as tr
import customtkinter
import ctypes
import time

# arreglar escala de resolucion
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # if your windows version >= 8.1
except:
    ctypes.windll.user32.SetProcessDPIAware()  # win 8.0 or less

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

tracker = None  # Guardar el eye tracker

root = customtkinter.CTk()
root.geometry("500x500")
root.resizable(False, False)
root.title("CETYS Eye Tracker")

cache = []

def connect():
    encontrados = tr.find_all_eyetrackers()
    global tracker
    tracker = encontrados[0]

    global num_serie
    num_serie.configure(text=f'Numero de Serie: {tracker.serial_number}')
    global button2
    button2.configure(state=NORMAL)


def calibrate():
    calibrar.calibrar(eyetracker=tracker)
    global button3
    button3.configure(state=NORMAL)
    global button4
    button4.configure(state=NORMAL)


def record():
    def gaze_data_callback(gaze_data):
        # Print gaze points of left and right eye
        print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
            gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
            gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))
        cache.append(gaze_data)

    tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    time.sleep(2)

def stop():
    tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA)
    global frame
    label = customtkinter.CTkLabel(master=frame,
                                   text="Guardando archivo...",
                                   font=("Roboto", 20),
                                   text_color="white")
    label.pack(pady=12, padx=10)

    # Save to csv
    with open('data.csv', 'w') as f:
        for item in cache:
            f.write("%s\n" % item)

    cache.clear()
    time.sleep(2)
    label.destroy()



frame = customtkinter.CTkFrame(root)
frame.pack(fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="CETYS Eye Tracker", font=("Roboto", 20), text_color="white")
label.pack(pady=12, padx=10)

num_serie = customtkinter.CTkLabel(master=frame,
                                   text="Dispostivo no conectado",
                                   font=("Roboto", 20),
                                   text_color="white")
num_serie.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Connect", command=connect)
button.pack(pady=12, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="Calibrate", command=calibrate)
button2.configure(state=DISABLED)
button2.pack(pady=12, padx=10)

button3 = customtkinter.CTkButton(master=frame, text="Record", command=record)
button3.configure(state=DISABLED)
button3.pack(pady=12, padx=10)

button4 = customtkinter.CTkButton(master=frame, text="Stop", command=stop)
button4.configure(state=DISABLED)
button4.pack(pady=12, padx=10)

# Place at the bottom left
quitButton = customtkinter.CTkButton(master=frame, text="Quit", command=root.quit, text_color="black",
                                     fg_color="#eb4d4b", hover_color="#ff7979")
quitButton.pack(pady=12, padx=10)
quitButton.place(x=10, y=460)

root.mainloop()
