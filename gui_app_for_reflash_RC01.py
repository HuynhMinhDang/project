from struct import pack
import tkinter as tk
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from tkinter import HORIZONTAL, messagebox
from tkinter import ttk
import tkinter.ttk
import sqlite3
import time


a = "a"

def progress():
    tasks = 10
    x = 0
    while(x<tasks):
        time.sleep(1)
        bar['value'] += 10
        x+=1
        percent.set(str((x/tasks)*100)+"%")
        app.update_idletasks()

def populate_list():
    print('Populate')


def run_item():
    print('Add')
    run_btn_text.set("Loading...")
    Base_SW_Name = Base_SW_entry.get()
    Ticket_BaseSW_Name = Ticket_BaseSW_entry.get()
    Latest_SW_Name = Latest_SW_entry.get()
    Ticket_latestSW_Name = Ticket_Latest_SW_entry.get()
    if Base_SW_Name == "":
        messagebox.showwarning("WARNING", "BaseSW name is invalid")
    print(Base_SW_Name)
    print(Ticket_BaseSW_Name)
    print(Latest_SW_Name)
    print(Ticket_latestSW_Name)
    progress()
    run_btn_text.set("DONE")
    tkinter.messagebox.showinfo("GREAT!", "Test case RFlash tool created successfully")
    if Base_SW_Name == a:
        print("dung")


def remove_item():
    print('Remove')


def update_item():
    print('Update')


def clear_item():
    print('Clear')


app = tk.Tk()

app.title('Reflash Tool')
# app.iconbitmap('background_img.jpg')
app.geometry('700x420')


# logo
logo = Image.open('background_img.jpg')
logo = ImageTk.PhotoImage(logo)
# logo_label = tk.Label(image=logo)
# logo_label.place(x=0, y=0, relwidth = 1, relheight= 1)
# logo_label.image = logo
# logo_label.grid(column=0, row=0)

# Creat canvas

canvas = tk.Canvas(app, width=700, height=420)
# canvas.grid(columnspan = 0, rowspan=0)
canvas.pack(fill='both', expand=True)
canvas.create_image(0, 0, image=logo, anchor='nw')

# instruction
instruction = tk.Label(app, text="THIS IS REFLASH TOOL CREATE BY HUYNH MINH DANG", font="Raleway")
Base_SW_entry_window = canvas.create_window(130, 390, anchor="nw", window=instruction)
# instruction = canvas.create_text(340, 390, text='THIS IS REFLASH TOOL CREATE BY HUYNH MINH DANG', font=('bold', 14), fill="White")
# instruction.grid(columnspan=3,column=0,row=1)

# # Part Base SW
Base_SW_text = tk.StringVar()
# Base_SW_label = tk.Label(app, text='Base SW Name', font=('bold', 14), bg="#20bebe", fg="white", pady=20)
Base_SW_label = canvas.create_text(80, 50, text='Base SW Name', font=('bold', 14), fill="Black")
# Base_SW_label_window = canvas.create_window(10, 10, anchor="nw", window = Base_SW_label)
# Base_SW_label .grid(row=0, column=0)
Base_SW_entry = tk.Entry(app, textvariable=Base_SW_text, font='large_font')
# Base_SW_entry.place(width=200, height=50)
Base_SW_entry_window = canvas.create_window(10, 70, anchor="nw", window=Base_SW_entry)
# Base_SW_entry.grid(row=0, column=1)


# # Ticket_BaseSW
Ticket_BaseSW_text = tk.StringVar()
# Ticket_BaseSW_label = tk.Label(app, text='Ticket_BaseSW Name', font=('bold', 14), bg="#20bebe", fg="white", pady=20)
Ticket_BaseSW_label = canvas.create_text(
    400, 50, text='Ticket BaseSW', font=('bold', 14), fill="Black")
# Ticket_BaseSW_label .grid(row=0, column=2)
# Ticket_BaseSW_entry = tk.Entry(app, textvariable=Ticket_BaseSW_text)
Ticket_BaseSW_entry = tk.Entry(
    app, textvariable=Ticket_BaseSW_text, font='large_font')
Ticket_BaseSW_entry_window = canvas.create_window(
    325, 70, anchor="nw", window=Ticket_BaseSW_entry)
# Ticket_BaseSW_entry.grid(row=0, column=3)

# # Part Latest SW
Latest_SW_text = tk.StringVar()
# Latest_SW_label = tk.Label(app, text='Latest SW Name', font=('bold', 14), bg="#20bebe", fg="white", pady=20)
Latest_SW_label = canvas.create_text(
    80, 130, text='Latest SW Name', font=('bold', 14), fill="Black")
# Latest_SW_label .grid(row=1, column=0)
# Latest_SW_entry = tk.Entry(app, textvariable=Latest_SW_text)
Latest_SW_entry = tk.Entry(app, textvariable=Latest_SW_text, font='large_font')
Latest_SW_entry_window = canvas.create_window(
    10, 150, anchor="nw", window=Latest_SW_entry)
# Latest_SW_entry.grid(row=1, column=1)

# # Ticket_Latest_SW
Ticket_Latest_SW_text = tk.StringVar()
# Ticket_Latest_SW_label = tk.Label(app, text='Ticket_Latest_SW Name', font=('bold', 14), bg="#20bebe", fg="white", pady=20)
Ticket_Latest_SW_label = canvas.create_text(
    400, 130, text='Ticket Latest SW', font=('bold', 14), fill="Black")
# Ticket_Latest_SW_label .grid(row=1, column=2)
# Ticket_Latest_SW_entry = tk.Entry(app, textvariable=Ticket_Latest_SW_text)
Ticket_Latest_SW_entry = tk.Entry(
    app, textvariable=Ticket_Latest_SW_text, font='large_font')
Ticket_Latest_SW_entry_window = canvas.create_window(
    325, 150, anchor="nw", window=Ticket_Latest_SW_entry)
# Ticket_Latest_SW_entry.grid(row=1, column=3)

# # Part List (Listbox)
# parts_list = tk.Listbox(app, height=8, width=50,border=0, bg="#20bebe", fg="white")
# parts_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# # Create scrollbar
# scrollbar = tk.Scrollbar(app)
# scrollbar.grid(row=3, column=3)


# # Buttons
run_btn_text = tk.StringVar()
run_btn = tk.Button(app, textvariable=run_btn_text, command=run_item,font="Raleway", width=15)
run_btn_text.set("RUN")
# run_btn.grid(column=1, row=2)
# run_btn = tk.Button(app, text='RUN', width=14, command=run_item)
run_btn_window = canvas.create_window(390, 190, anchor="nw", window=run_btn)
# add_btn.grid(row=2, column=0, pady=20)




# remove_btn = tk.Button(app, text='Remove Part', width=12, command=remove_item)
# remove_btn.grid(row=2, column=1)

# update_btn = tk.Button(app, text='Update Part', width=12, command=update_item)
# update_btn.grid(row=2, column=2)

# clear_btn = tk.Button(app, text='Clear Part', width=12, command=clear_item)
# clear_btn.grid(row=2, column=3)

# # def func():#function of the button
# #     tkinter.messagebox.showinfo("Greetings","Hello! Welcome to PythonGeeks.")

# # btn=Button(win,text="Click Me", width=10,height=5,command=func)
# # btn.place(x=200,y=30)

# # Set scroll to listbox
# parts_list.configure(yscrollcommand=scrollbar.set)
# scrollbar.configure(command=parts_list.yview)

# progress bar
bar = ttk.Progressbar(app, orient = HORIZONTAL, length = 600, mode = 'determinate')
bar_window = canvas.create_window(40, 250, anchor = "nw", window = bar)
# barpack(pady = 10)

percent = tk.StringVar() 
# percentLabel = tk.Label(app, textvariable = percent).pack()
percentLabel = tk.Label(app, textvariable=percent)
percentLabel_window = canvas.create_window(330, 300, anchor = "nw", window = percentLabel)


# Populate data
populate_list()


# Start program
app.mainloop()


# root.mainloop()
