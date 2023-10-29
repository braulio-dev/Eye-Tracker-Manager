from tkinter import DISABLED

import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x500")
root.resizable(False, False)


def connect():
    print("Connect")


def calibrate():
    print("Calibrate")


def record():
    print("Record")


def stop():
    print("Stop")


frame = customtkinter.CTkFrame(root)
frame.pack(fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="CETYS Eye Tracker", font=("Roboto", 20), text_color="white")
label.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Connect", command=connect)
button.pack(pady=12, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="Calibrate", command=calibrate)
button2.pack(pady=12, padx=10)

button3 = customtkinter.CTkButton(master=frame, text="Record", command=record)
button3.pack(pady=12, padx=10)

button4 = customtkinter.CTkButton(master=frame, text="Stop", command=stop)
button4.pack(pady=12, padx=10)

# Place at the bottom left
quitButton = customtkinter.CTkButton(master=frame, text="Quit", command=root.quit, text_color="black", fg_color="#eb4d4b", hover_color="#ff7979")
quitButton.pack(pady=12, padx=10)
frame.update()
root.update()
quitButton.place(x=10, y=root.winfo_height() - button.winfo_height() - 10)

root.mainloop()
