import tkinter as tk
from tkinter import Message, Text
import cv2
import os
import csv
import pandas as pd
import datetime
import time
import tkinter.font as font
# import pyrebase
# from firebase import firebase
# from google.cloud import storage
# from google.cloud.storage.blob import Blob

window = tk.Tk()
window.title("REFLASH TOOL 2022")
window.configure(background='black')
window.geometry('1280x670')

lbl = tk.Label(window, text="REFLASH GENERATE TESTCASE TOOL",
                bg="white", fg="black", width=50, height=3, font=('times', 30, 'italic bold'))
lbl.place(x=100, y=20)

lbl1 = tk.Label(window, text=" Insert the name of base SW", width=25,
                fg="black", bg="white", height=2, font=('times', 15, ' bold'))
lbl1.place(x=540, y=320)

# message = tk.Label(window, text="", fg="black", bg="white",
#                     activeforeground="green", width=35, height=7, font=('times', 15, ' bold '))
# message.place(x=470, y=400)

config = {
    "apiKey": "Enter here apiKey",
    "authDomain": "Enter here authDomain",
    "databaseURL": "Enter here databaseURL",
    "projectId": "Enter here projectId",
    "storageBucket": "Enter here storageBucket",
    "messagingSenderId": "Enter here messagingSenderId",
    "appId": "Enter here appId"
}

quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="black",
                    bg="white", width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
quitWindow.place(x=700, y=200)

quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="black",
                bg="white", width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
quitWindow.place(x=700, y=200)

lbl3 = tk.Label(window, text="DESIGN BY HUYNH MINH DANG",
                width=80, fg="white", bg="black", font=('times', 15, ' bold'))
lbl3.place(x=200, y=620)

window.mainloop()
