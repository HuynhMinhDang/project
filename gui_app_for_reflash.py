from re import S, X
from telnetlib import SE
from tkinter import BOTTOM, CENTER, NW, SW, W, ttk
import tkinter.ttk
from struct import pack
import tkinter as tk
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from tkinter import LEFT, messagebox
import sqlite3
from tkinter.font import Font

from matplotlib.ft2font import HORIZONTAL


a = "a"



# def populate_list():
#     print('Populate')


# def run_item():
#     print('Add')
#     Base_SW_Name = Base_SW_entry.get()
#     Ticket_BaseSW_Name = Ticket_BaseSW_entry.get()
#     Latest_SW_Name = Latest_SW_entry.get()
#     Ticket_latestSW_Name = Ticket_Latest_SW_entry.get()
#     print(Base_SW_Name)
#     print(Ticket_BaseSW_Name)
#     print(Latest_SW_Name)
#     print(Ticket_latestSW_Name)
#     if Base_SW_Name == a:
#         print("dung")


# def remove_item():
#     print('Remove')


# def update_item():
#     print('Update')


# def clear_item():
#     print('Clear')


# app = tk.Tk()

# app.title('Reflash Tool')
# # app.iconbitmap('background_img.jpg')
# app.geometry('700x420')



# # logo
# logo = Image.open('background_img.jpg')
# logo = ImageTk.PhotoImage(logo)
# logo_label = tk.Label(image=logo)
# logo_label.place(x=0, y=0, relwidth = 1, relheight= 1)
# logo_label.image = logo
# logo_label.grid(column=0, row=0)

# Creat canvas

# canvas = tk.Canvas(app, width=700, height=420)
# # canvas.grid(columnspan = 0, rowspan=0)
# canvas.pack(fill= 'both', expand = True)
# canvas.create_image(0,0, image = logo, anchor = 'nw')

# # instruction
# instruction = tk.Label(app, text="THIS IS REFLASH TOOL CREATE BY HUYNH MINH DANG", font="Raleway")
# # instruction.grid(columnspan=3,column=0,row=1)

# # # Part Base SW
# Base_SW_text = tk.StringVar()
# # Base_SW_label = tk.Label(app, text='Base SW Name', font=('bold', 14), bg="#20bebe", fg="white", pady=20)
# Base_SW_label = canvas.create_text(80, 50, text='Base SW Name', font=('bold', 14), fill="Black")
# # Base_SW_label_window = canvas.create_window(10, 10, anchor="nw", window = Base_SW_label)
# # Base_SW_label .grid(row=0, column=0)
# Base_SW_entry = tk.Entry(app, textvariable = Base_SW_text, font = 'large_font')
# # Base_SW_entry.place(width=200, height=50)
# Base_SW_entry_window = canvas.create_window(10, 70, anchor="nw", window = Base_SW_entry)
# # Base_SW_entry.grid(row=0, column=1)


# # # Ticket_BaseSW
# Ticket_BaseSW_text = tk.StringVar()
# # Ticket_BaseSW_label = tk.Label(app, text='Ticket_BaseSW Name', font=('bold', 14), bg="#20bebe", fg="white", pady=20)
# Ticket_BaseSW_label = canvas.create_text(400, 50, text='Ticket BaseSW Name', font=('bold', 14), fill="Black")
# # Ticket_BaseSW_label .grid(row=0, column=2)
# # Ticket_BaseSW_entry = tk.Entry(app, textvariable=Ticket_BaseSW_text)
# Ticket_BaseSW_entry = tk.Entry(app, textvariable = Ticket_BaseSW_text, font='large_font')
# Ticket_BaseSW_entry_window = canvas.create_window(300, 70, anchor="nw", window=Ticket_BaseSW_entry)
# # Ticket_BaseSW_entry.grid(row=0, column=3)

# # # Part Latest SW
# Latest_SW_text = tk.StringVar()
# # Latest_SW_label = tk.Label(app, text='Latest SW Name', font=('bold', 14), bg="#20bebe", fg="white", pady=20)
# Latest_SW_label = canvas.create_text(80, 130, text='Latest SW Name', font=('bold', 14), fill="Black")
# # Latest_SW_label .grid(row=1, column=0)
# # Latest_SW_entry = tk.Entry(app, textvariable=Latest_SW_text)
# Latest_SW_entry = tk.Entry(app, textvariable = Latest_SW_text, font='large_font')
# Latest_SW_entry_window = canvas.create_window(10, 150, anchor="nw", window=Latest_SW_entry)
# Latest_SW_entry.grid(row=1, column=1)

# # Ticket_Latest_SW
# Ticket_Latest_SW_text = tk.StringVar()
# # Ticket_Latest_SW_label = tk.Label(app, text='Ticket_Latest_SW Name', font=('bold', 14), bg="#20bebe", fg="white", pady=20)
# Ticket_Latest_SW_label = canvas.create_text(400, 130, text='Ticket Latest SW Name', font=('bold', 14), fill="Black")
# # Ticket_Latest_SW_label .grid(row=1, column=2)
# # Ticket_Latest_SW_entry = tk.Entry(app, textvariable=Ticket_Latest_SW_text)
# Ticket_Latest_SW_entry = tk.Entry(app, textvariable = Ticket_Latest_SW_text, font='large_font')
# Ticket_Latest_SW_entry_window = canvas.create_window(300, 150, anchor="nw", window=Ticket_Latest_SW_entry)
# Ticket_Latest_SW_entry.grid(row=1, column=3)

# # Part List (Listbox)
# parts_list = tk.Listbox(app, height=8, width=50,border=0, bg="#20bebe", fg="white")
# parts_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# # Create scrollbar
# scrollbar = tk.Scrollbar(app)
# scrollbar.grid(row=3, column=3)

# # Buttons
# run_btn = tk.Button(app, text='RUN', width=14, command = run_item)
# run_btn_window = canvas.create_window(390, 190, anchor = "nw", window = run_btn)
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

# Populate data
# populate_list()


# frame = Frame(app)
# frame.pack()


# # bottomframe = Frame(app)
# # bottomframe.pack(side = BOTTOM)

# redbutton = Button(frame, text="Red")
# redbutton.pack(side=LEFT, padx=50, pady=10)

# greenbutton = Button(frame, text="green")
# greenbutton.pack(side=LEFT)

# bluebutton = Button(frame, text="Blue")
# bluebutton.pack(side=LEFT)
# frame2 = Frame(app)
# frame2.pack()

# blackbutton = Button(frame2, text="Black")
# blackbutton.pack(side=LEFT)
# app = tk.Tk()
# app.title('Reflash Tool')
# window_width = 700
# window_height = 420
# app.geometry('700x420')
# app.geometry("%dx%d" % (window_width, window_height))


# logo
# logo = Image.open('image/background_img.jpg')
# logo = ImageTk.PhotoImage(logo)

# # Creat canvas

# canvas = tk.Canvas(app, width=700, height=420)

# canvas.pack(fill='both', expand=True)
# canvas.create_image(0, 0, image=logo, anchor='nw')


# my_label = tk.Label(app, image=logo)
# my_label.place(x= 0, y = 0, relwidth = 1, relheight = 1)


# Input_path_text = tk.StringVar()
# Input_path_label = tk.Label(app, text='Input path', font=('bold', 14), fg = 'black')
# Input_path_label.place(x=0, y=0)


# Input_path_entry = tk.Entry(app, textvariable=Input_path_text, font='large_font', width=50)
# Input_path_entry_window = canvas.create_window(10, 70, anchor="nw", window=Input_path_entry)






# Reconfigure our rows and columns for grid



# Input_path_label = tk.Label(app, text='Input path', font=('bold', 14))
# Input_path_label.grid(column=0,row=0)
# app.columnconfigure(0, weight=1)
# app.rowconfigure(0, weight=1)

# Input_path_text1 = tk.StringVar()
# Input_path_label1 = tk.Label(app, text='Output path', font=('bold', 14), fg='black')
# Input_path_label1.grid(column=1, row=0)
# app.columnconfigure(0, weight=1)
# app.rowconfigure(0, weight=1)
# Input_path_text2 = tk.StringVar()
# Input_path_label2 = tk.Label(app, text='Output path2222', font=('bold', 14), fg='black')
# Input_path_label2.grid(column=1, row=0)
# app.columnconfigure(0, weight=1)
# app.rowconfigure(0, weight=1)
# Input_path_label3 = tk.Label(app, text='entry', font=('bold', 14))
# Input_path_label3.grid(column=1, row=1)


# app = tk.Tk()
# app.title('Reflash Tool')
# app.geometry('700x420')
# app.update()

# app.resizable(True, True)

# my_sizegrip = ttk.Sizegrip(app)

# # logo
# logo = Image.open('image/background_img.jpg')
# logo = ImageTk.PhotoImage(logo)

# canvas = tk.Canvas(app, width=700, height=420)

# canvas.create_image(0, 0, image=logo, anchor='nw')

# back ground image

# background_img = Image.open("./image/background_img.jpg")
# background_img = background_img.resize((app.winfo_width(), app.winfo_height()), Image.ANTIALIAS)
# background_tkimg = ImageTk.PhotoImage(background_img)

# Creat canvas

# canvas = tk.Canvas(app, highlightthickness= 0)
# canvas.pack(expand = True, fill = 'both')
# canvas.create_image(0, 0, image = background_tkimg, anchor='nw')

# app.update()
# canvas_height = canvas.winfo_height()
# canvas_width = canvas.winfo_width()

# title_label = canvas.create_text(
#     (canvas_width//2), (canvas_height//2) - 25, fill="white", text="TITLE")
# button1 = tk.Button(canvas, text="button 1")
# button2 = tk.Button(canvas, text="button 2")
# button3 = tk.Button(canvas, text="button 3")

# canvas.create_window((canvas_width//2) - 75,(canvas_height//2) + 25, window=button1)
# canvas.create_window((canvas_width//2), (canvas_height//2) + 25, window=button2)
# canvas.create_window((canvas_width//2) + 75,(canvas_height//2) + 25, window=button3)

# frame_all = tk.(canvas)

# app.resizable(True,True)
# my_sizegrip = ttk.Sizegrip(app)
# my_sizegrip.pack(side="right", anchor=SW)

app = tk.Tk()
app.title('Reflash Tool')
app.geometry('700x420')
# app.update()

frameall = tk.Frame(app)
frame1 = tk.Frame(frameall)
frame2 = tk.Frame(frameall)
frame3 = tk.Frame(frameall)
frame4 = tk.Frame(frameall)
frame5 = tk.Frame(frameall)



Input_path_text = tk.StringVar()
Input_path_label = tk.Label(frame1, text='Input path', font=('bold', 14), bg="#20bebe", fg="black").grid(row=0, column=0, sticky='w')
Input_path_entry = tk.Entry(frame1, textvariable=Input_path_text,font='large_font', width=55).grid(row=1, column=0, sticky='w')

Output_path_text = tk.StringVar()
Output_path_label = tk.Label(frame1, text='Output path', font=('bold', 14), bg="#20bebe", fg="black").grid(row=2, column=0, sticky='w')
Output_path_entry = tk.Entry(frame1, textvariable=Output_path_text,font='large_font', width=55).grid(row=3, column=0, sticky='w')

# browse button
browse_input_path_text = tk.StringVar()
browse_btn_input_path = tk.Button(frame1, textvariable=browse_input_path_text, command=lambda: None, font="Raleway", width=7, height=1).grid(row=1, column=1, pady=5, padx=10)
browse_input_path_text.set("Browse")


# browse button save file
browse_output_path_text = tk.StringVar()
browse_btn_output_path = tk.Button(frame1, textvariable=browse_output_path_text, command=lambda: None,font="bold", width=7, height=1).grid(row=3, column=1, pady=5, padx=10)
browse_output_path_text.set("Browse")

frame1.pack()

# Run program Buttons
run_btn_text = tk.StringVar()
run_btn = tk.Button(frame2, textvariable=run_btn_text, command=None, font="bold", width=15).grid(row=0, column=0, pady=20)
run_btn_text.set("RUN")

frame2.pack()




# progress bar
bar = ttk.Progressbar(frame3, orient='horizontal', length=585, mode='determinate').grid(row=0, column=0, columnspan=1, sticky='w')

frame3.pack()

percent = tk.StringVar()
percentLabel = tk.Label(frame4, textvariable=percent, font=('bold', 14), bg="#20bebe", fg="black").grid(row=0, column=0)
percent.set("100%")

frame4.pack()

Programing_counter_text = tk.StringVar()
Programing_counter_label = tk.Label(frame5, text='Programing_counter_step', font=('bold', 14), bg="#20bebe", fg="black").grid(row=0, column=0, padx=30, pady=10, sticky='w')
Programing_counter = tk.Spinbox(frame5, from_=0, to=10, width=10, font=Font(family='Helvetica', size=15)).grid(row=1, column=0, padx=30)

Programing_Attempt_counter_text = tk.StringVar()
Programing_Attempt_counter_label = tk.Label(frame5, text='Programing_Attempt_counter_step', font=('bold', 14), bg="#20bebe", fg="black").grid(row=0, column=1, padx=30, pady=10, sticky='w')
Programing_Attempt_counter = tk.Spinbox(frame5, from_=0, to=10, width=10, font=Font(family='Helvetica', size=15)).grid(row=1, column=1, padx=30)

frame5.pack()

# frame.pack()
frameall.place(relx = 0.5, rely = 0.5, anchor = CENTER)


instruction = tk.Label(app, text="          Welcome to ReFlash tool create by dev Huynh Minh Dang", font=("helvetica", 14))
instruction_version = tk.Label(app, text="R1.1.2", font=("helvetica", 14))
instruction_version.pack(side="right", anchor='s')
instruction.pack(side="bottom",fill = 'both', anchor=CENTER)

# canvas.pack()
frameall.configure(background="#20bebe")
frame1.configure(background="#20bebe")
frame2.configure(background="#20bebe")
frame3.configure(background="#20bebe")
frame4.configure(background="#20bebe")
frame5.configure(background="#20bebe")
app.configure(background="#20bebe")



# qua xau khong sai co the chinh sua sau nay


# tk.Grid.rowconfigure(app, 0, weight=1)
# tk.Grid.rowconfigure(app, 1, weight=1)
# tk.Grid.rowconfigure(app, 2, weight=1)
# tk.Grid.rowconfigure(app, 3, weight=1)
# tk.Grid.rowconfigure(app, 4, weight=1)
# tk.Grid.rowconfigure(app, 5, weight=1)
# tk.Grid.rowconfigure(app, 6, weight=1)
# tk.Grid.rowconfigure(app, 7, weight=1)
# tk.Grid.rowconfigure(app, 8, weight=1)
# tk.Grid.columnconfigure(app, 0, weight=1)
# tk.Grid.columnconfigure(app, 1, weight=1)


# Input_path_text = tk.StringVar()
# Input_path_label = tk.Label(app, text='Input path', font=('bold', 14), bg="#20bebe", fg="black",).grid(row=0, column=0,  sticky='nsew')
# Input_path_entry = tk.Entry(app, textvariable=Input_path_text,font='large_font', width=51).grid(row=1, column=0, sticky='nsew')


# Output_path_text = tk.StringVar()
# Output_path_label = tk.Label(app, text='Output path', font=('bold', 14), bg="#20bebe", fg="black").grid(row=2, column=0,  sticky='nsew')
# Output_path_entry = tk.Entry(app, textvariable=Output_path_text, font='large_font', width=51).grid(row=3, column=0,  sticky='nsew')

# # browse button open file
# browse_input_path_text = tk.StringVar()
# browse_btn_input_path = tk.Button(app, textvariable=browse_input_path_text, command=lambda: None,
#                                   font="Raleway", width=7, height=1).grid(row=1, column=1, pady=5, padx=10, sticky='nsew')
# browse_input_path_text.set("Browse")

# # browse button save file
# browse_output_path_text = tk.StringVar()
# browse_btn_output_path = tk.Button(app, textvariable=browse_output_path_text, command=lambda: None,
#                                    font="bold", width=7, height=1).grid(row=3, column=1, pady=5, padx=10, sticky='nsew')
# browse_output_path_text.set("Browse")

# # Run program Buttons
# run_btn_text = tk.StringVar()
# run_btn = tk.Button(app, textvariable=run_btn_text, command=None,
#                     font="bold", width=15).grid(row=4, column=0, pady=20, sticky='nsew')
# run_btn_text.set("RUN")

# # progress bar
# bar = ttk.Progressbar(app, orient='horizontal', length=550,
#                       mode='determinate').grid(row=5, column=0, sticky='nsew')


# percent = tk.StringVar()
# percentLabel = tk.Label(app, textvariable=percent, font=(
#     'bold', 14), bg="#20bebe", fg="black").grid(row=6, column=0, sticky='nsew')
# percent.set("100%")

# Programing_couter_text = tk.StringVar()
# Programing_couter_label = tk.Label(app, text='Programing_couter_step', font=('bold', 14), bg="#20bebe", fg="black").grid(row=7, column=0, padx=30, pady=10, sticky='nsew')
# Programing_couter = tk.Spinbox(app, from_=0, to=10, width=10, font=Font(family='Helvetica', size=15)).grid(row=8, column=0, padx=30)

# Programing_Attemp_couter_text = tk.StringVar()
# Programing_Attemp_couter_label = tk.Label(app, text='Programing_Attemp_couter_step', font=('bold', 14), bg="#20bebe", fg="black").grid(row=7, column=1, padx=30, pady=10, sticky='nsew')
# Programing_Attemp_couter = tk.Spinbox(app, from_=0, to=10, width=10, font=Font(family='Helvetica', size=15)).grid(row=8, column=1, padx=30)


# app.configure(background="#20bebe")
# Start program
app.mainloop()


# root.mainloop()
