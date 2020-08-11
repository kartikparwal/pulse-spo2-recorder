import time
import sys
import os
import pandas as pd
import tkinter
from tkinter import *
import tkinter.messagebox as tkMessageBox
import mysql.connector
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
import mplcursors
import PySimpleGUI as sg
from ing_theme_matplotlib import mpl_style
root = Tk(className=' AutocompleteEntry demo')
root.title("Pulse recorder")
width = 640
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
# root.resizable(0, 0)
OPTIONS = ["None","John","Roy","Robin"]              #Add more names in the same format
def Database():
    global conn, cursor
    conn = mysql.connector.connect(user='root', password='YourPassword',host='localhost',database='YourDatabase')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `pulse_record` ( name TEXT, datet DATETIME, pul INT, SpO2 INT)")

def Database2():
    global conn, cursor
    conn = mysql.connector.connect(user='root', password='YourPassword',host='localhost',database='YourDatabase')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `theme` ( p_theme TEXT)")

def theme_selection():
    Database2()
    cursor.execute("SELECT p_theme FROM theme WHERE user = 'jsk'")
    themesec = cursor.fetchone()
    theme = themesec[0]
    if theme == "light":
        light_theme()
    elif theme == "dark":
        black_theme()
    else:
        root.destroy()

NAME = StringVar()
PULSE = IntVar()
SPO = IntVar()
DNAME = StringVar()
variable = StringVar(root)

tkinter_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']

class AutocompleteEntry(tkinter.Entry):
    """
    Subclass of tkinter.Entry that features autocompletion.
    To enable autocompletion use set_completion_list(list) to define 
    a list of possible strings to hit.
    To cycle through hits use down and up arrow keys.
    """

    def set_completion_list(self, completion_list):
        self._completion_list = completion_list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)               

    def autocomplete(self, delta=0):
        """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
        if delta: # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tkinter.END)
        else: # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.startswith(self.get().lower()):
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits=_hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0,tkinter.END)
            self.insert(0,self._hits[self._hit_index])
            self.select_range(self.position,tkinter.END)
                        
    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tkinter.INSERT), tkinter.END) 
            self.position = self.index(tkinter.END)
        if event.keysym == "Left":
            if self.position < self.index(tkinter.END): # delete the selection
                self.delete(self.position, tkinter.END)
            else:
                self.position = self.position-1 # delete one character
                self.delete(self.position, tkinter.END)
        if event.keysym == "Right":
            self.position = self.index(tkinter.END) # go to end (no selection)
        if event.keysym == "Down":
            self.autocomplete(1) # cycle to next hit
        if event.keysym == "Up":
            self.autocomplete(-1) # cycle to previous hit
        # perform normal autocomplete if event is a single key or an umlaut
        if len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
            self.autocomplete()

def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()

def bl_cheaker():
    Database2()
    cursor.execute("SELECT p_theme FROM theme WHERE user = 'jsk'")
    themesec = cursor.fetchone()
    theme = themesec[0]
    if theme == "dark":
        tkMessageBox.showinfo("Pulse Recorder","Theme already set to dark.")
    elif theme == "light":
        ans = tkMessageBox.askquestion("Pulse Recorder","To change theme, app needs to be restarted. All unsaved data will be deleted. Are you sure!")
        if ans == 'yes':
            cursor.execute("UPDATE theme SET p_theme = 'dark' WHERE user = 'jsk'")
            conn.commit()
            tkMessageBox.showinfo("Pulse Recorder","Please restart app to apply changes.")
            root.destroy()
        else:
            pass
    else:
        root.destroy()

def lt_cheaker():
    Database2()
    cursor.execute("SELECT p_theme FROM theme WHERE user = 'jsk'")
    themesec = cursor.fetchone()
    theme = themesec[0]
    if theme == "light":
        tkMessageBox.showinfo("Pulse Recorder","Theme already set to light.")
    elif theme == "dark":
        ans = tkMessageBox.askquestion("Pulse Recorder","To change theme, app needs to be restarted. All unsaved data will be deleted. Are you sure!")
        if ans == 'yes':
            cursor.execute("UPDATE theme SET p_theme = 'light' WHERE user = 'jsk'")
            conn.commit()
            tkMessageBox.showinfo("Pulse Recorder","Please restart app to apply changes.")
            root.destroy()
        else:
            pass
    else:
        root.destroy()

def light_theme():
    root.configure(background='grey90')
    menubar = Menu(root, background='#FFFFFF', foreground='black', activebackground='#FFFFFF', activeforeground='black')
    filemenu = Menu(menubar, tearoff=0, background='#FFFFFF', foreground='black', activebackground='#FFFFFF', activeforeground='black')
    thememenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=Exit)
    thememenu.add_command(label="Light Mode", command = lt_cheaker)
    thememenu.add_command(label="Dark Mode", command = bl_cheaker)
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Theme", menu=thememenu)
    root.config(menu=menubar)
    def good():
        NAME.set("")
        PULSE.set(0)
        SPO.set(0)
        RecordFrame.destroy()
        Fetch_alldata()
        
    def back():
        NAME.set("")
        UpdateFrame.destroy()
        Fetch_alldata()

    def treetohome2():
        NAME.set("")
        FetchdFrame2.destroy()
        test(test_list)

    def treetohome3():
        NAME.set("")
        FetchdFrame3.destroy()
        Fetch_alldata()

    def graph_data():
        a = variable.get()
        nam = a.title()
        Database()
        query = '''SELECT DATE_FORMAT(datet, "%%d-%%m-%%y") AS Date, pul AS Pulse, SpO2 AS SpO2 FROM `pulse_record` WHERE `name` = "%s";'''%str(a)
        df1 = pd.read_sql(query, conn, index_col= None)
        df = pd.DataFrame(df1)
        df = df.set_index(['Date'])
        df.plot(marker='o')
        mpl_style(dark=False)
        plt.xlabel("Date")
        plt.ylabel("Number")
        plt.title("%s"%nam)
        mplcursors.cursor()
        plt.show()

    def updateit():
        try:
            if NAME.get() == "" or PULSE.get() == "" or SPO.get() == "":
                tkMessageBox.showerror("Pulse Recorder","Please complete the given field.")
            else:
                a = NAME.get()
                e = time.strptime(a,"%d-%m-%Y %H:%M:%S")
                z = time.strftime("%Y-%m-%d %H:%M:%S",e)
                Database()
                cursor.execute("UPDATE pulse_record SET pul = %s WHERE datet = %s",(PULSE.get(), z, ))
                cursor.execute("UPDATE pulse_record SET SpO2 = %s WHERE datet = %s",(SPO.get(), z, ))
                conn.commit()
                tkMessageBox.showinfo("Pulse Recorder","Updated Successfully.")
                NAME.set("")
                SPO.set(0)
                PULSE.set(0)
        except Exception as e:
            tkMessageBox.showerror("Pulse Recorder","Please complete the given field with correct value.")

    def update():
        FetchdFrame2.destroy()
        global UpdateFrame
        UpdateFrame = Frame(root)
        root.title("Pulse Recorder (Update)")
        UpdateFrame.pack(side=TOP, pady=20)
        UpdateFrame.config(background="grey90")
        lbl_date = Label(UpdateFrame, text="Time:", font=('arial', 25), bd=18, bg="grey90")
        lbl_date.grid(row=1)
        lbl_nbpm = Label(UpdateFrame, text="SpO2:", font=('arial', 25), bd=18, bg="grey90")
        lbl_nbpm.grid(row=2)
        lbl_npulse = Label(UpdateFrame, text="Pulse:", font=('arial', 25), bd=18, bg="grey90")
        lbl_npulse.grid(row=3)
        lbl_upbutton = Button(UpdateFrame, text="Fetch Data", font=('arial', 12), width=25, command=good)
        lbl_upbutton.grid(row=0, columnspan=2)
        name = Entry(UpdateFrame, font=('arial', 20), textvariable=NAME, width=15)
        name.grid(row=1, column=1)
        bpm = Entry(UpdateFrame, font=('arial', 20), textvariable=SPO, width=15)
        bpm.grid(row=2, column=1)
        pulse = Entry(UpdateFrame, font=('arial', 20), textvariable=PULSE, width=15)
        pulse.grid(row=3, column=1)
        btn_Record = Button(UpdateFrame, text="Update It", font=('arial', 18), width=35, command=updateit)
        btn_Record.grid(row=5, columnspan=2, pady=20)
        lbl_button = Button(UpdateFrame, text="Back", font=('arial', 12), width=25, command=back)
        lbl_button.grid(row=0, columnspan=2)

    def Fetch_alldata():
        a = "Pulse Recorder (%s)"%None
        root.title(a)
        def FinalForm2():
            global FetchdFrame2
            FetchdFrame2 = Frame(root)
            FetchdFrame2.pack(side=TOP, pady=20)
            FetchdFrame2.config(background="grey90")
            def ok():
                def FinalForm3():
                    if variable.get() == "None":
                        pass
                    else:
                        FetchdFrame2.destroy()
                        global FetchdFrame3
                        FetchdFrame3 = Frame(root)
                        FetchdFrame3.pack(side=TOP, pady=20)
                        FetchdFrame3.config(background="grey90")
                        z = variable.get()
                        a = "Pulse Recorder (%s)"%z
                        root.title(a)
                        bckbutton = Button(FetchdFrame3, text="Back", font=('arial', 12), width=12, command=treetohome3)
                        bckbutton.pack(side=TOP, pady=10)
                        grfbutton = Button(FetchdFrame3, text="Graph", font=('arial', 12), width=12, command=graph_data)
                        grfbutton.pack(side=TOP, pady=10)
                        Database()
                        cursor.execute("SELECT datet FROM `pulse_record` WHERE `name` = %s", (variable.get(),))
                        results = cursor.fetchall()
                        cursor.execute("SELECT pul FROM `pulse_record` WHERE `name` = %s", (variable.get(),))
                        resul = cursor.fetchall()
                        cursor.execute("SELECT SpO2 FROM `pulse_record` WHERE `name` = %s", (variable.get(),))
                        res = cursor.fetchall()
                        tree = ttk.Treeview(FetchdFrame3, columns = (1,2,3), height = 400, show = "headings")
                        tree.pack(side = 'left')

                        tree.heading(1, text="Time")
                        tree.heading(2, text="Pulse")
                        tree.heading(3, text="SpO2")

                        tree.column(1, width = 200)
                        tree.column(2, width = 100, anchor="center")
                        tree.column(3, width = 100, anchor="center")

                        scroll = ttk.Scrollbar(FetchdFrame3, orient="vertical", command=tree.yview)
                        scroll.pack(side = 'right', fill = 'y')

                        tree.configure(yscrollcommand=scroll.set)
                        for jk in range(36500,0,-1):
                            try:
                                tree.insert('', 'end', values = (results[jk], resul[jk], res[jk]) )
                            except IndexError:
                                pass
                FinalForm3()
            bckbutton = Button(FetchdFrame2, text="Back", font=('arial', 12), width=25, command=treetohome2)
            bckbutton.pack(side=TOP, pady=10)
            chgbutton = Button(FetchdFrame2, text="Update", font=('arial', 12), width=25, command=update)
            chgbutton.pack(side=TOP, pady=5)
            variable.set(OPTIONS[0])
            s = Label(FetchdFrame2, text="Sort By Name", font=('arial', 12), bd=18, bg="grey90")
            s.pack()
            w = OptionMenu(FetchdFrame2,variable, *OPTIONS)
            w.pack()
            button = Button(FetchdFrame2, text="OK", font=('arial', 12), width=25, command=ok)
            button.pack(side=TOP, pady=10)
            Database()
            cursor.execute("SELECT name FROM `pulse_record`")
            result = cursor.fetchall()
            cursor.execute('''SELECT DATE_FORMAT(datet,"%d-%m-%y %H:%i:%S") FROM `pulse_record`''')
            results = cursor.fetchall()
            cursor.execute("SELECT pul FROM `pulse_record`")
            resul = cursor.fetchall()
            cursor.execute("SELECT SpO2 FROM `pulse_record`")
            res = cursor.fetchall()
            tree = ttk.Treeview(FetchdFrame2, columns = (1,2,3,4), height = 400, show = "headings")
            tree.pack(side = 'left')
            tree.heading(1, text="Name")
            tree.heading(2, text="Time")
            tree.heading(3, text="Pulse")
            tree.heading(4, text="SpO2")

            tree.column(1, width = 110)
            tree.column(2, width = 150)
            tree.column(3, width = 70, anchor="center")
            tree.column(4, width = 70, anchor="center")

            scroll = ttk.Scrollbar(FetchdFrame2, orient="vertical", command=tree.yview)
            scroll.pack(side = 'right', fill = 'y')

            tree.configure(yscrollcommand=scroll.set)
            for jk in range(36500,-1,-1):
                try:
                    tree.insert('', 'end', values = (result[jk], results[jk], resul[jk], res[jk]) )
                except IndexError:
                    pass
        FinalForm2()

    def test(test_list):
        global RecordFrame
        RecordFrame = Frame(root)
        root.title("Pulse Recorder")
        RecordFrame.pack(side=TOP, pady=80)
        RecordFrame.configure(bg="grey90")
        lbl_name = Label(RecordFrame, text="Name:", font=('arial', 25), bd=18, bg="grey90")
        lbl_name.grid(row=1)
        lbl_bpm = Label(RecordFrame, text="SpO2:", font=('arial', 25), bd=18, bg="grey90")
        lbl_bpm.grid(row=2)
        lbl_pulse = Label(RecordFrame, text="Pulse:", font=('arial', 25), bd=18, bg="grey90")
        lbl_pulse.grid(row=3)
        lbl_button = Button(RecordFrame, text="Fetch Data", font=('arial', 12), width=25, command=good)
        lbl_button.grid(row=0, columnspan=2)
        name = AutocompleteEntry(RecordFrame, font=('arial', 20), textvariable=NAME, width=15)
        name.grid(row=1, column=1)
        name.set_completion_list(test_list)
        bpm = Entry(RecordFrame, font=('arial', 20), textvariable=SPO, width=15)
        bpm.grid(row=2, column=1)
        pulse = Entry(RecordFrame, font=('arial', 20), textvariable=PULSE, width=15)
        pulse.grid(row=3, column=1)
        style1 = ttk.Style()
        style1.configure('C.TButton', font = 
                        ('Comic Sans MS', 18, 'bold'), 
                                borderwidth = '4')
        style1.map("C.TButton",
            foreground=[('pressed', 'green'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'blue'), ('active', 'white')]
            )
        btn_Record = ttk.Button(RecordFrame, text="Record It!", width=23, style="C.TButton",command=Record)
        btn_Record.grid(row=5, columnspan=2, pady=20)

    def Record():
        a = NAME.get()
        try:
            if NAME.get() == "" or PULSE.get() == "" or SPO.get() == "":
                tkMessageBox.showerror("Pulse Recorder","Please complete the given field.")
            else:
                if a.isalpha():
                    testlist = ['John','Roy','Robin']         #Add more names in the same format
                    if a in testlist:
                        ptime = time.strftime("%Y/%m/%d %H:%M:%S")
                        Database()
                        cursor.execute("INSERT INTO pulse_record (datet , name , pul , SpO2) VALUES(%s , %s , %s , %s)",(ptime, NAME.get(), PULSE.get(), SPO.get(), ))
                        conn.commit()
                        tkMessageBox.showinfo("Pulse Recorder","Recorded Successfully.")
                        NAME.set("")
                        SPO.set(0)
                        PULSE.set(0)
                    else:
                        tkMessageBox.showerror("Pulse Recorder","Name not registered.")
                else:
                    tkMessageBox.showerror("Pulse Recorder","Please complete the given field with correct value.")
        except Exception as e:
            tkMessageBox.showerror("Pulse Recorder","Please complete the given field with correct value.")
    test(test_list)

#--------------------------------------------Black Theme-----------------------------------------------------------
def black_theme():
    root.configure(background='#484848')
    menubar = Menu(root, background='#696969', foreground='#FFFFFF', activebackground='#696969', activeforeground='#FFFFFF')
    filemenu = Menu(menubar, tearoff=0, background='#696969', foreground='#FFFFFF', activebackground='#696969', activeforeground='#FFFFFF')
    thememenu = Menu(menubar, tearoff=0, background='#696969', foreground='#FFFFFF', activebackground='#696969', activeforeground='#FFFFFF')
    filemenu.add_command(label="Exit", command=Exit)
    thememenu.add_command(label="Light Mode", command=lt_cheaker)
    thememenu.add_command(label="Dark Mode", command=bl_cheaker)
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Theme", menu=thememenu)
    root.config(menu=menubar)
    def goodbl():
        NAME.set("")
        PULSE.set(0)
        SPO.set(0)
        RecordFramebl.destroy()
        Fetch_alldatabl()

    def backbl():
        NAME.set("")
        UpdateFramebl.destroy()
        Fetch_alldatabl()

    def treetohome2bl():
        NAME.set("")
        FetchdFrame2bl.destroy()
        testbl(test_list)

    def treetohome3bl():
        NAME.set("")
        FetchdFrame3bl.destroy()
        Fetch_alldatabl()

    def graph_databl():
        a = variable.get()
        nam = a.title()
        Database()
        query = '''SELECT DATE_FORMAT(datet, "%%d-%%m-%%y") AS Date, pul AS Pulse, SpO2 AS SpO2 FROM `pulse_record` WHERE `name` = "%s";'''%str(a)
        df1 = pd.read_sql(query, conn, index_col= None)
        df = pd.DataFrame(df1)
        df = df.set_index(['Date'])
        df.plot(marker='o')
        mpl_style(dark=True)
        ax = plt.gca()
        ax.set_facecolor('#A9A9A9')
        plt.xlabel("Date")
        plt.ylabel("Number")
        plt.title("%s"%nam)
        mplcursors.cursor()
        plt.show()

    def updateitbl():
        try:
            if NAME.get() == "" or PULSE.get() == "" or SPO.get() == "":
                tkMessageBox.showerror("Pulse Recorder","Please complete the given field.")
            else:
                a = NAME.get()
                e = time.strptime(a,"%d-%m-%Y %H:%M:%S")
                z = time.strftime("%Y-%m-%d %H:%M:%S",e)
                print(z)
                Database()
                cursor.execute("UPDATE pulse_record SET pul = %s WHERE datet = %s",(PULSE.get(), z, ))
                cursor.execute("UPDATE pulse_record SET SpO2 = %s WHERE datet = %s",(SPO.get(), z, ))
                conn.commit()
                tkMessageBox.showinfo("Pulse Recorder","Updated Successfully.")
                NAME.set("")
                SPO.set(0)
                PULSE.set(0)
        except Exception as e:
            tkMessageBox.showerror("Pulse Recorder","Please complete the given field with correct value.")

    def updatebl():
        FetchdFrame2bl.destroy()
        global UpdateFramebl
        UpdateFramebl = Frame(root)
        UpdateFramebl.config(background='#484848')
        root.title("Pulse Recorder (Update)")
        UpdateFramebl.pack(side=TOP, pady=20)
        lbl_date = Label(UpdateFramebl, text="Time:", font=('arial', 25), bd=18, bg="#484848", fg="white")
        lbl_date.grid(row=1)
        lbl_nbpm = Label(UpdateFramebl, text="SpO2:", font=('arial', 25), bd=18, bg="#484848", fg="white")
        lbl_nbpm.grid(row=2)
        lbl_npulse = Label(UpdateFramebl, text="Pulse:", font=('arial', 25), bd=18, bg="#484848", fg="white")
        lbl_npulse.grid(row=3)
        lbl_upbutton = Button(UpdateFramebl, text="Fetch Data", font=('arial', 12), width=25, bg="grey", fg="white", command=goodbl)
        lbl_upbutton.grid(row=0, columnspan=2)
        name = Entry(UpdateFramebl, font=('arial', 20), textvariable=NAME, width=15, bg="grey", fg="white")
        name.grid(row=1, column=1)
        bpm = Entry(UpdateFramebl, font=('arial', 20), textvariable=SPO, width=15, bg="grey", fg="white")
        bpm.grid(row=2, column=1)
        pulse = Entry(UpdateFramebl, font=('arial', 20), textvariable=PULSE, width=15, bg="grey", fg="white")
        pulse.grid(row=3, column=1)
        btn_Record = Button(UpdateFramebl, text="Update It", font=('arial', 18), width=35, command=updateitbl, bg="grey", fg="white")
        btn_Record.grid(row=5, columnspan=2, pady=20)
        lbl_button = Button(UpdateFramebl, text="Back", font=('arial', 12), width=25, command=backbl, bg="grey", fg="white")
        lbl_button.grid(row=0, columnspan=2)

    def Fetch_alldatabl():
        a = "Pulse Recorder (%s)"%None
        root.title(a)
        def FinalForm2bl():
            global FetchdFrame2bl
            FetchdFrame2bl = Frame(root)
            FetchdFrame2bl.pack(side=TOP, pady=20)
            FetchdFrame2bl.config(background="#484848")
            def okbl():
                def FinalForm3bl():
                    if variable.get() == "None":
                        pass
                    else:
                        FetchdFrame2bl.destroy()
                        global FetchdFrame3bl
                        FetchdFrame3bl = Frame(root)
                        FetchdFrame3bl.pack(side=TOP, pady=20)
                        FetchdFrame3bl.config(background="#484848")
                        z = variable.get()
                        a = "Pulse Recorder (%s)"%z
                        root.title(a)
                        bckbutton = Button(FetchdFrame3bl, text="Back", font=('arial', 12), width=12, bg="grey", fg="white", command=treetohome3bl)
                        bckbutton.pack(side=TOP, pady=10)
                        grfbutton = Button(FetchdFrame3bl, text="Graph", font=('arial', 12), width=12, bg="grey", fg="white", command=graph_databl)
                        grfbutton.pack(side=TOP, pady=10)
                        Database()
                        cursor.execute("SELECT datet FROM `pulse_record` WHERE `name` = %s", (variable.get(),))
                        results = cursor.fetchall()
                        cursor.execute("SELECT pul FROM `pulse_record` WHERE `name` = %s", (variable.get(),))
                        resul = cursor.fetchall()
                        cursor.execute("SELECT SpO2 FROM `pulse_record` WHERE `name` = %s", (variable.get(),))
                        res = cursor.fetchall()
                        style = ttk.Style(root)
                        # set ttk theme to "clam" which support the fieldbackground option
                        style.theme_use("clam")
                        style.configure("Treeview", background="#696969", 
                            fieldbackground="#696969", foreground="white")
                        tree = ttk.Treeview(FetchdFrame3bl, columns = (1,2,3), height = 400, show = "headings")
                        tree.pack(side = 'left')

                        tree.heading(1, text="Time")
                        tree.heading(2, text="Pulse")
                        tree.heading(3, text="SpO2")

                        tree.column(1, width = 200)
                        tree.column(2, width = 100, anchor="center")
                        tree.column(3, width = 100, anchor="center")

                        scroll = ttk.Scrollbar(FetchdFrame3bl, orient="vertical", command=tree.yview)
                        scroll.pack(side = 'right', fill = 'y')

                        tree.configure(yscrollcommand=scroll.set)
                        for jk in range(36500,-1,-1):
                            try:
                                tree.insert('', 'end', values = (results[jk], resul[jk], res[jk]) )
                            except IndexError:
                                pass
                FinalForm3bl()
            bckbutton = Button(FetchdFrame2bl, text="Back", font=('arial', 12), width=25, bg="grey", fg="white", command=treetohome2bl)
            bckbutton.pack(side=TOP, pady=10)
            chgbutton = Button(FetchdFrame2bl, text="Update", font=('arial', 12), width=25, bg="grey", fg="white", command=updatebl)
            chgbutton.pack(side=TOP, pady=5)
            variable.set(OPTIONS[0])
            s = Label(FetchdFrame2bl, text="Sort By Name", font=('arial', 12), bd=18, bg="#484848", fg="white")
            s.pack()
            w = OptionMenu(FetchdFrame2bl,variable, *OPTIONS)
            # w["menu"].config(background='#484848', foreground='#FFFFFF', activebackground='#696969', activeforeground='#FFFFFF')
            w.pack()
            button = Button(FetchdFrame2bl, text="OK", font=('arial', 12), width=25, bg="grey", fg="white", command=okbl)
            button.pack(side=TOP, pady=10)
            Database()
            cursor.execute("SELECT name FROM `pulse_record`")
            result = cursor.fetchall()
            cursor.execute('''SELECT DATE_FORMAT(datet,"%d-%m-%y %H:%i:%S") FROM `pulse_record`''')
            results = cursor.fetchall()
            cursor.execute("SELECT pul FROM `pulse_record`")
            resul = cursor.fetchall()
            cursor.execute("SELECT SpO2 FROM `pulse_record`")
            res = cursor.fetchall()
            style = ttk.Style(root)
            # set ttk theme to "clam" which support the fieldbackground option
            style.theme_use("clam")
            style.configure("Treeview", background="", 
                fieldbackground="#696969", foreground="white")
            tree = ttk.Treeview(FetchdFrame2bl, columns = (1,2,3,4), height = 400, show = "headings")
            tree.pack(side = 'left')
            tree.heading(1, text="Name")
            tree.heading(2, text="Time")
            tree.heading(3, text="Pulse")
            tree.heading(4, text="SpO2")

            tree.column(1, width = 110)
            tree.column(2, width = 150)
            tree.column(3, width = 70, anchor="center")
            tree.column(4, width = 70, anchor="center")

            scroll = ttk.Scrollbar(FetchdFrame2bl, orient="vertical", command=tree.yview)
            scroll.pack(side = 'right', fill = 'y')

            tree.configure(yscrollcommand=scroll.set)
            for jk in range(36500,-1,-1):
                try:
                    tree.insert('', 'end', values = (result[jk], results[jk], resul[jk], res[jk]) )
                except IndexError:
                    pass
        FinalForm2bl()

    def testbl(test_list):
        global RecordFramebl
        RecordFramebl = Frame(root)
        root.title("Pulse Recorder")
        RecordFramebl.pack(side=TOP, pady=80)
        RecordFramebl.config(background="#484848")
        def on_entry_click(event):
            """function that gets called whenever name is clicked"""
            if name.get() == 'Your name':
                name.delete(0, "end") # delete all the text in the name
                name.insert(0, '') #Insert blank for user input
                name.config(fg = 'white')

        def on_focusout(event):
            if name.get() == '':
                name.insert(0, 'Your name')
                name.config(fg = 'white')

        lbl_name = Label(RecordFramebl, text="Name:", font=('arial', 25), bd=18, bg="#484848", fg="white")
        lbl_name.grid(row=1)
        lbl_bpm = Label(RecordFramebl, text="SpO2:", font=('arial', 25), bd=18, bg="#484848", fg="white")
        lbl_bpm.grid(row=2)
        lbl_pulse = Label(RecordFramebl, text="Pulse:", font=('arial', 25), bd=18, bg="#484848", fg="white")
        lbl_pulse.grid(row=3)
        lbl_button = Button(RecordFramebl, text="Fetch Data", font=('arial', 12), width=25, bg="grey", fg="white", command=goodbl)
        lbl_button.grid(row=0, columnspan=2)
        name = AutocompleteEntry(RecordFramebl, font=('arial', 20), textvariable=NAME, width=15, bg="grey", fg="white")
        name.grid(row=1, column=1)
        name.insert(0, 'Your name')
        name.bind('<FocusIn>', on_entry_click)
        name.bind('<FocusOut>', on_focusout)
        name.set_completion_list(test_list)
        bpm = Entry(RecordFramebl, font=('arial', 20), textvariable=SPO, width=15, bg="grey", fg="white")
        bpm.grid(row=2, column=1)
        pulse = Entry(RecordFramebl, font=('arial', 20), textvariable=PULSE, width=15, bg="grey", fg="white")
        pulse.grid(row=3, column=1)
        style1 = ttk.Style()
        style1.configure('C.TButton', font = 
                        ('Comic Sans MS', 18, 'bold'), 
                                borderwidth = '4')
        style1.map("C.TButton",
            foreground=[('pressed', 'green'), ('active', 'black')],
            background=[('pressed', '!disabled', '#484848'), ('active', '#696969')]
            )
        btn_Record = ttk.Button(RecordFramebl, text="Record It", style="C.TButton", width=35, command=Recordbl)
        btn_Record.grid(row=5, columnspan=2, pady=20)

    def Recordbl():
        a = NAME.get()
        try:
            if NAME.get() == "" or PULSE.get() == "" or SPO.get() == "":
                tkMessageBox.showerror("Pulse Recorder","Please complete the given field.")
            else:
                if a.isalpha():
                    testlist = ['John','Roy','Robin']           #Add more names in the same format
                    if a in testlist:
                        ptime = time.strftime("%Y/%m/%d %H:%M:%S")
                        Database()
                        cursor.execute("INSERT INTO pulse_record (datet , name , pul , SpO2) VALUES(%s , %s , %s , %s)",(ptime, NAME.get(), PULSE.get(), SPO.get(), ))
                        conn.commit()
                        tkMessageBox.showinfo("Pulse Recorder","Recorded Successfully.")
                        NAME.set("")
                        SPO.set(0)
                        PULSE.set(0)
                    else:
                        tkMessageBox.showerror("Pulse Recorder","Name not registered.")
                else:
                    tkMessageBox.showerror("Pulse Recorder","Please complete the given field with correct value.", background='#696969', foreground='#FFFFFF', activebackground='#696969', activeforeground='#FFFFFF')
        except Exception as e:
            tkMessageBox.showerror("Pulse Recorder","Please complete the given field with correct value.", background='#696969', foreground='#FFFFFF', activebackground='#696969', activeforeground='#FFFFFF')
    testbl(test_list)   

if __name__ == '__main__':
    test_list = (u'John', u'Roy', u'Robin')         #Add more names in the same format
    theme_selection()
    root.mainloop()