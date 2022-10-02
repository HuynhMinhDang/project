import tkinter as tk
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from tkinter import BOTTOM, LEFT, TOP, messagebox
import sqlite3
from tkinter.ttk import Frame, Label, Entry, Style, Button


# root = tk.Tk()

# canvas = tk.Canvas(root, width=600, height=300)
# canvas.grid(columnspan = 3, rowspan=3)

# # logo
# # logo = Image.open('dang2.jpg')
# # logo =  ImageTk.PhotoImage(logo)
# # logo_label = tk.Label(image=logo)
# # logo_label.image = logo
# # logo_label.grid(column=1, row=0)

# # instruction
# instruction = tk.Label(root, text="THIS IS REFLASH TOOL CREATE BY HUYNH MINH DANG", font="Raleway")
# instruction.grid(columnspan=3,column=0,row=1)

# def open_file():
#     # print("is this working??")
#     browse_text.set("loading...")
#     file = askopenfile(parent = root, mode = 'rb', title="Choose a file", filetype=[("Pdf file", ".pdf")])
#     if file:
#         print("file was sucessfuly loaded")
#         read_pdf = PyPDF2.PdfFileReader(file)
#         page = read_pdf.getPage(0)
#         page_content = page.extractText()
#         # print(page_content)
        
#         # text box
#         text_box = tk.Text(root, height=10, width=50, padx=15,pady=15)
#         text_box.insert(1.0, page_content)
#         text_box.tag_configure("center", 1.0, "end")
#         text_box.grid(column=1,row=3)
        
#         browse_text.set("Browse")


# # browse button
# browse_text = tk.StringVar()
# browse_btn = tk.Button(root, textvariable=browse_text, command=lambda:open_file(), font="Raleway", bg="#20bebe", fg="white", width=15)
# browse_text.set("Browse")
# browse_btn.grid(column=1,row=2)

# canvas = tk.Canvas(root, width=600, height=250)
# canvas.grid(columnspan = 3)

# Create window object

# messagebox.showinfo("RFlash tool","Thanks for using me")
a  =  "a"

def populate_list():
    print('Populate')

def add_item():
    print('Add')
    Base_SW_Name = Base_SW_entry.get()
    Ticket_BaseSW_Name = Ticket_BaseSW_entry.get()
    Latest_SW_Name = Latest_SW_entry.get()
    Ticket_latestSW_Name = Ticket_Latest_SW_entry.get()
    print(Base_SW_Name)
    print(Ticket_BaseSW_Name)
    print(Latest_SW_Name)
    print(Ticket_latestSW_Name)
    if Base_SW_Name == a:
        print("dung")

def remove_item():
    print('Remove')
    

def update_item():
    print('Update')

def clear_item():
    print('Clear')


app = tk.Tk()
# tk.title('Welcome')

window_width = 700
window_height = 350
app.title('Reflash Tool')
# app.geometry('700x350')
app.geometry("%dx%d" % (window_width, window_height))
# app.pack(fill=BOTH, expand=True)

# Part Base SW 
# Base_SW_text = tk.StringVar()
# Base_SW_label = tk.Label(app, text = 'Base SW Name', font = ('bold',14), pady = 20)
# Base_SW_label .grid(row = 0, column = 0)
# Base_SW_entry = tk.Entry(app, textvariable = Base_SW_text)
# Base_SW_entry.grid(row = 0, column = 1)

# button = Button(app, text='Geeks')
# button.pack(side = LEFT , pady=5)
# # button.grid(row = 0, column =0, padx = 10, pady =30)

# button1 = Button(app, text='Geeks')
# button1.pack(side= Literal['left','top'], pady=5)


frame = Frame(app)
frame.pack()


# bottomframe = Frame(app)
# bottomframe.pack(side = BOTTOM)

redbutton = Button(frame, text="Red")
redbutton.pack(side=LEFT, padx= 50, pady = 10)

greenbutton = Button(frame, text="green")
greenbutton.pack(side=LEFT)

bluebutton = Button(frame, text="Blue")
bluebutton.pack(side=LEFT)
frame2 = Frame(app)
frame2.pack()

blackbutton = Button(frame2, text="Black")
blackbutton.pack(side=LEFT)


# button1.pack(side = TOP , pady=5)
# button1.grid(row = 0, column =1, padx = 10, pady =30)
# button2 = Button(app, text='Geeks')
# # button.pack(side = TOP , pady=5)
# button2.grid(row = 0, column =2, padx = 10, pady =30)
# button3 = Button(app, text='Geeks')
# # button.pack(side = TOP , pady=5)
# button3.grid(row = 0, column =3, padx = 10, pady =30)

# # Ticket_BaseSW
# Ticket_BaseSW_text = tk.StringVar()
# Ticket_BaseSW_label = tk.Label(app, text = 'Ticket_BaseSW Name', font = ('bold',14), pady = 20)
# Ticket_BaseSW_label .grid(row = 0, column = 2)
# Ticket_BaseSW_entry = tk.Entry(app, textvariable = Ticket_BaseSW_text)
# Ticket_BaseSW_entry.grid(row = 0, column = 3)

# # Part Latest SW
# Latest_SW_text = tk.StringVar()
# Latest_SW_label = tk.Label(app, text = 'Latest SW Name', font = ('bold',14))
# Latest_SW_label .grid(row = 1, column = 0)
# Latest_SW_entry = tk.Entry(app, textvariable = Latest_SW_text)
# Latest_SW_entry.grid(row = 1, column = 1)

# # Ticket_Latest_SW
# Ticket_Latest_SW_text = tk.StringVar()
# Ticket_Latest_SW_label = tk.Label(app, text = 'Ticket_Latest_SW Name', font = ('bold',14))
# Ticket_Latest_SW_label .grid(row = 1, column = 2)
# Ticket_Latest_SW_entry = tk.Entry(app, textvariable = Ticket_Latest_SW_text)
# Ticket_Latest_SW_entry.grid(row = 1, column = 3)

# # Part List (Listbox)
# parts_list = tk.Listbox(app, height=8,width=50, border = 0)
# parts_list.grid(row = 3, column = 0, columnspan = 3, rowspan = 6, pady = 20, padx = 20)

# # Create scrollbar
# scrollbar = tk.Scrollbar(app)
# scrollbar.grid(row=3,column=3)

# # Buttons
# add_btn = tk.Button(app, text = 'Add Part', width = 12, command = add_item)
# add_btn.grid(row=2, column = 0, pady = 20)

# remove_btn = tk.Button(app, text = 'Remove Part', width = 12, command = remove_item)
# remove_btn.grid(row=2, column = 1)

# update_btn = tk.Button(app, text = 'Update Part', width = 12, command = update_item)
# update_btn.grid(row=2, column = 2)

# clear_btn = tk.Button(app, text = 'Clear Part', width = 12, command = clear_item)
# clear_btn.grid(row=2, column = 3)

# # def func():#function of the button
# #     tkinter.messagebox.showinfo("Greetings","Hello! Welcome to PythonGeeks.")
    
# # btn=Button(win,text="Click Me", width=10,height=5,command=func)
# # btn.place(x=200,y=30)

# # Set scroll to listbox
# parts_list.configure(yscrollcommand=scrollbar.set)
# scrollbar.configure(command=parts_list.yview)
# # def resizer(e):
#     # global logo1, resize_logo, new_logo, instruction
#     # logo1 = Image.open('background_img.jpg')
#     # resize_logo = logo1.resize((e.width, e.height), Image.ANTIALIAS)
#     # new_logo = ImageTk.PhotoImage(resize_logo)
#     # canvas.create_image(0, 0, image=new_logo, anchor='nw')

#     # print(e.width)
#     # size  = e.width /10
#     # instruction = tk.Label(app, text="Welcome to ReFlash tool create by dev Huynh Minh Dang", font=("helvetica", int(size)))


# # Populate data
# populate_list()



# Start program
app.mainloop()



# root.mainloop()
