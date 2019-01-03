#===============IMPORT PACKAGES=========================================================================================
from tkinter import *
from tkinter import ttk
import datetime
import smtplib
from matplotlib import pyplot as plt
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql
from matplotlib import style
style.use('ggplot')
from itertools import chain
#================IMAGES=================================================================================================
image1 = 'library.png'
image2 = 'image2.png'
image3 = 'finance.png'
global conn1, conn


#===========================MAIN WINDOW=================================================================================
class menu:

    def __init__(self):
        self.root = Tk()
        self.root.title('Menu')
        conn1 = pymysql.connect("localhost", "root", "root", "librarystore")
        conn = conn1.cursor()
        conn.execute('''create table if not exists book_info
        (ID INT NOT NULL PRIMARY KEY ,
        TITLE VARCHAR(100),
        AUTHOR VARCHAR(100),
        GENRE VARCHAR(100) ,
        COPIES INT NOT NULL);''')
        conn1.commit()
        conn.execute('''create table if not exists book_issued
        (BOOK_NAME VARCHAR(100),
        STUDENT_ID VARCHAR(100),
        ISSUE_DATE DATE ,
        RETURN_DATE DATE ,
        PRIMARY KEY (BOOK_NAME,STUDENT_ID));''')
        conn1.commit()
        conn.execute('''create table if not exists Student_details(
                LIBRARYID VARCHAR(100),
                STUDENT_NAME VARCHAR(100),
                ADDRESS VARCHAR(100) ,
                ROLL_NO VARCHAR(100),
                DEPARTMENT VARCHAR(100),
                CLASS VARCHAR(100),
                EMAIL_ID VARCHAR(100),
                PRIMARY KEY (LIBRARYID));''')

        conn1.commit()
        conn.execute('''create table if not exists Fine_paid(
                LIBRARY_ID VARCHAR(100),
                BOOK_NAME VARCHAR(100),
                FINE_BOOK INT NOT NULL);''')
        conn1.commit()
        conn.execute(''' create table if not exists book_issued_report(
                Book_name VARCHAR(100),
                Copies INT);''')
        conn1.commit()
        conn.execute(''' create table if not exists fine_per_book_report(
                        Book_name1 VARCHAR(100),
                        Amount INT);''')
        conn1.commit()
        conn.execute(''' create table if not exists fine_per_student_report(
                        library_no VARCHAR(100),
                        Book_Amount INT);''')
        conn1.commit()
        conn.close()
        self.a = self.canvases(image1)
        l1 = Button(self.a, text='BOOK DATA', font='Papyrus 22 bold', fg='Yellow', bg='Black', width=19, padx=10,
                    borderwidth=0, command=self.book).place(x=100, y=300)

        l2 = Button(self.a, text='STUDENT DATA', font='Papyrus 22 bold', fg='Yellow', bg='Black', width=19, padx=10,
                    borderwidth=0, command=self.student).place(x=100, y=400)

        l3 = Button(self.a, text='REPORT', font='Papyrus 22 bold', fg='Yellow', bg='Black', width=19, padx=10,
                    borderwidth=0, command=self.report_fun).place(x=100, y=500)

        l4 = Button(self.a, text='LOGOUT', font='Papyrus 22 bold', fg='Yellow', bg='Black', width=19, padx=10,
                    borderwidth=0, command=self.logout_fun).place(x=100, y=600)

        self.root.mainloop()

    def logout_fun(self):
        self.root.destroy()
#==================================PLACING IMAGES=======================================================================
    def canvases(self, images):
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        photo = Image.open(images)
        photo1 = photo.resize((w, h), Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(photo1)

        self.canvas = Canvas(self.root, width='%d' % w, height='%d' % h)
        self.canvas.grid(row=0, column=0)
        self.canvas.grid_propagate(0)
        self.canvas.create_image(0, 0, anchor=NW, image=photo2)
        self.canvas.image = photo2
        return self.canvas
#==============================BOOK FUNCTION============================================================================
    def book(self):
        self.a.destroy()
        self.a = self.canvases(image2)
        l1 = Button(self.a, text='Add Books', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.addbook).place(x=12, y=100)
        l2 = Button(self.a, text='Search Books', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.search).place(x=12, y=200)

        l4 = Button(self.a, text='All Books', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.all).place(x=12, y=300)
        l4 = Button(self.a, text='<< Main Menu', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.mainmenu).place(x=12, y=500)

#===================BOOK DETAILS GUI====================================================================================
    def addbook(self):
        self.aid = StringVar()
        self.aauthor = StringVar()
        self.aname = StringVar()
        self.acopies = IntVar()
        self.agenre = StringVar()
        self.f1 = Frame(self.a, height=500, width=650, bg='black')
        self.f1.place(x=500, y=100)
        l1 = Label(self.f1, text='Book ID : ', font='Papyrus 12 bold', fg='Orange', bg='Black', pady=1).place(x=50,
                                                                                                              y=50)
        e1 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aid).place(x=180, y=50)
        l2 = Label(self.f1, text='Book-Name : ', font='Papyrus 12 bold', fg='Orange', bg='Black', pady=1). \
            place(x=50, y=100)
        e2 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aname).place(x=180, y=100)
        l3 = Label(self.f1, text='Author : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50,
                                                                                                             y=150)
        e3 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aauthor).place(x=180, y=150)
        l4 = Label(self.f1, text='Genre : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50, y=200)
        e2 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.agenre).place(x=180, y=200)
        l4 = Label(self.f1, text='Copies : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50,
                                                                                                             y=250)
        e2 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.acopies).place(x=180, y=250)
        self.f1.grid_propagate(0)
        b1 = Button(self.f1, text='Add', font='Papyrus 10 bold', fg='black', bg='orange', width=15, bd=3,
                    command=self.adddata).place(x=150, y=400)

        b2 = Button(self.f1, text='Back', font='Papyrus 10 bold', fg='black', bg='orange', width=15, bd=3,
                    command=self.rm).place(x=350, y=400)

#=================================BACK BUTTON CLICK=====================================================================
    def rm(self):
        self.f1.destroy()

#===========================CALLING MAINMENU FUNCTION===================================================================
    def mainmenu(self):
        self.root.destroy()
        a = menu()

#==================ADDING BOOK DETAILS==================================================================================
    def adddata(self):
        a = self.aid.get()
        b = self.aname.get()
        c = self.aauthor.get()
        d = self.agenre.get()
        e = self.acopies.get()
        conn1 = pymysql.connect("localhost", "root", "root", "librarystore")
        conn = conn1.cursor()
        conn.execute("select * from book_info where  ID =%s ", (a))
        z = conn.fetchone()
        if z is None:
            if (a and b and c and d and e) == "":
                messagebox.showinfo("Error", "Fields cannot be empty.")
                return
            else:
                conn.execute("insert into book_info values (%s,%s,%s,%s,%s)",
                             (a, b, c, d, e))

                conn1.commit()
                messagebox.showinfo("Success", "Book added successfully")
                self.aid.set(" ")
                self.aname.set(" ")
                self.aauthor.set(" ")
                self.agenre.set(" ")
                self.acopies.set("0 ")
                return


        else:
            messagebox.showinfo("Error", "Book Id already present.")
            self.aid.set(" ")
            self.aname.set(" ")
            self.aauthor.set(" ")
            self.agenre.set(" ")
            self.acopies.set(" 0")
            conn.close()

            return

#========================SEARCHING GUI==================================================================================

    def search(self):
        self.sid = StringVar()
        self.f1 = Frame(self.a, height=500, width=650, bg='black')
        self.f1.place(x=500, y=100)
        l1 = Label(self.f1, text='Enter a Book-Name: ', font=('Papyrus 10 bold'), bd=2, fg='orange',
                   bg='black').place(x=20, y=40)
        e1 = Entry(self.f1, width=25, bd=5, bg='orange', fg='black', textvariable=self.sid).place(x=260, y=40)
        b1 = Button(self.f1, text='Search', bg='orange', font='Papyrus 10 bold', width=9, bd=2,
                    command=self.serch1).place(x=500, y=37)
        b1 = Button(self.f1, text='Back', bg='orange', font='Papyrus 10 bold', width=10, bd=2, command=self.rm).place(
            x=250, y=450)

    def create_tree(self, plc, lists):
        self.tree = ttk.Treeview(plc, height=13, column=(lists), show='headings')
        n = 0
        while n is not len(lists):
            self.tree.heading("#" + str(n + 1), text=lists[n])
            self.tree.column("" + lists[n], width=100)
            n = n + 1
        return self.tree

#=========================SEARCHING BOOK DETAILS FROM BOOK_INFO TABLE===================================================

    def serch1(self):
        k = self.sid.get()
        if k != "":
            self.list4 = ("BOOK ID", "Book-Name", "AUTHOR", "GENRE", "COPIES")
            self.trees = self.create_tree(self.f1, self.list4)
            self.trees.place(x=25, y=150)
            conn1 = pymysql.connect("localhost", "root", "root", "librarystore")
            conn = conn1.cursor()
            conn.execute("select * from book_info where  TITLE=%s  ",
                         (k.capitalize(),))
            a = conn.fetchall()
            if len(a) != 0:
                for row in a:
                    self.trees.insert("", END, values=row)
                conn1.commit()
                conn.close()
                self.trees.bind('<<TreeviewSelect>>')
                self.variable = StringVar(self.f1)
                self.variable.set("Select Action:")

                self.cm = ttk.Combobox(self.f1, textvariable=self.variable, state='readonly', font='Papyrus 15 bold',
                                       height=50, width=15, )
                self.cm.config(values=('Add Copies', 'Delete Copies', 'Delete Book'))

                self.cm.place(x=50, y=100)
                self.cm.pack_propagate(0)

                self.cm.bind("<<ComboboxSelected>>", self.combo)
                self.cm.selection_clear()
                return
            else:
                messagebox.showinfo("Error", "Data not found")
                return


        else:
            messagebox.showinfo("Error", "Search field cannot be empty.")
            return

    def combo(self, event):
        self.var_Selected = self.cm.current()
        if self.var_Selected == 0:
            self.copies(self.var_Selected)    # goto copies function line no -300
        elif self.var_Selected == 1:
            self.copies(self.var_Selected)      # goto copies function line no -300
        elif self.var_Selected == 2:
            self.deleteitem()        #goto deleteitem function lineno -269

#=================================DELETE A PARTICULAR BOOK GUI==========================================================
    def deleteitem(self):
        try:
            self.curItem = self.trees.focus()

            self.c1 = self.trees.item(self.curItem, "values")[1]
            b1 = Button(self.f1, text='Update', font='Papyrus 10 bold', width=9, bd=3, command=self.delete2).place(
                x=500, y=97)

        except:
            messagebox.showinfo("Empty", "Please select something.")
            return

#================================DELETE A PARTICULAR BOOK===============================================================
    def delete2(self):
        conn1 = pymysql.connect("localhost", "root", "root", "librarystore")
        conn = conn1.cursor()
        conn.execute("select * from book_issued where BOOK_NAME=%s", (self.c1,))
        ab = conn.fetchone()
        print(ab)
        if ab is None:
            conn.execute("DELETE FROM book_info where TITLE=%s", (self.c1,))
            conn1.commit()
            messagebox.showinfo("Successful", "Book Deleted sucessfully.")
            self.trees.delete(self.curItem)
            return
        else:
            messagebox.showinfo("Error", "Book is Issued.\nBook cannot be deleted.")
            return
            conn.close()

#========================================BOOK COPIES GUI================================================================
    def copies(self, varr):
        try:
            curItem = self.trees.focus()
            self.c1 = self.trees.item(curItem, "values")[1]
            self.c2 = self.trees.item(curItem, "values")[4]
            self.scop = IntVar()
            self.e5 = Entry(self.f1, width=20, textvariable=self.scop)
            self.e5.place(x=310, y=100)
            if varr == 0:  # copies add function
                b5 = Button(self.f1, text='Update', font='Papyrus 10 bold', bg='orange', fg='black', width=9, bd=3,
                            command=self.copiesadd).place(x=500, y=97)
            if varr == 1:  # copies delete function
                b6 = Button(self.f1, text='Update', font='Papyrus 10 bold', bg='orange', fg='black', width=9, bd=3,
                            command=self.copiesdelete).place(x=500, y=97)
            return
        except:
            messagebox.showinfo("Empty", "Please select a book.")
            return

#======================================ADD BOOK COPIES==================================================================
    def copiesadd(self):
        no = self.e5.get()
        if int(no) >= 0:

            conn1 = pymysql.connect("localhost", "root", "root", "librarystore")
            conn = conn1.cursor()
            conn.execute("update book_info set COPIES=COPIES+%s where TITLE=%s", (no, self.c1,))
            conn1.commit()

            messagebox.showinfo("Updated", "Copies added sucessfully.")
            self.serch1()
            conn.close()
            return
        else:
            messagebox.showinfo("Error", "No. of copies cannot be negative.")
            return

#===============================================DELETE BOOK COPIES======================================================
    def copiesdelete(self):
        no1 = self.e5.get()
        if int(no1) >= 0:
            if int(no1) <= int(self.c2):
                conn = pymysql.connect("localhost", "root", "root", "librarystore")
                conn1 = conn.cursor()
                conn1.execute("update book_info set COPIES=COPIES-%s where TITLE=%s", (no1, self.c1,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Updated", "Deleted sucessfully")
                self.serch1()
                return
            else:
                messagebox.showinfo("Maximum", "No. of copies to delete exceed available copies.")
                return

        else:
            messagebox.showinfo("Error", "No. of copies cannot be negative.")
            return

#===================================SEARCHING ALL  BOOKS GUI============================================================
    def all(self):
        self.f1 = Frame(self.a, height=500, width=650, bg='black')
        self.f1.place(x=500, y=100)
        b1 = Button(self.f1, text='Back', bg='orange', fg='black', width=10, bd=3, command=self.rm).place(x=250, y=400)
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        self.list3 = ("BOOK ID", "TITLE", "AUTHOR", "GENRE", "COPIES")
        self.treess = self.create_tree(self.f1, self.list3)
        self.treess.place(x=25, y=50)
        conn1.execute("select * from book_info order by ID")
        g = conn1.fetchall()
        if len(g) != 0:
            for row in g:
                self.treess.insert('', END, values=row)
        conn.commit()
        conn1.close()

#======================STUDENT GUI======================================================================================

    def student(self):
        self.a.destroy()
        self.a = self.canvases(image2)
        l1 = Button(self.a, text='Issue book', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.issue).place(x=12, y=100)
        l2 = Button(self.a, text='Return Book', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.returnn).place(x=12, y=200)
        l3 = Button(self.a, text='Student Activity', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.activity).place(x=12, y=300)
        l4 = Button(self.a, text='<< Main Menu', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.mainmenu).place(x=20, y=600)
        l5 = Button(self.a, text='Student Details', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.Studentfun).place(x=12, y=400)

#==================================BOOK ISSUE GUI=======================================================================
    def issue(self):
        self.aname = StringVar()
        self.astudentt = StringVar()
        self.f1 = Frame(self.a, height=550, width=500, bg='black')
        self.f1.place(x=500, y=100)
        l1 = Label(self.f1, text='Book-Name : ', font='papyrus 15 bold', bg='black', fg='orange').place(x=50, y=100)
        e1 = Entry(self.f1, width=25, bd=4, bg='orange', textvariable=self.aname).place(x=200, y=100)
        l2 = Label(self.f1, text='Library-Id : ', font='papyrus 15 bold', bg='black', fg='orange').place(x=50, y=150)
        e2 = Entry(self.f1, width=25, bd=4, bg='orange', textvariable=self.astudentt).place(x=200, y=150)
        b1 = Button(self.f1, text='Back', font='Papyrus 10 bold', fg='black', bg='orange', width=10, bd=3,
                    command=self.rm).place(x=50, y=250)
        b2 = Button(self.f1, text='Issue', font='Papyrus 10 bold', fg='black', bg='orange', width=10, bd=3,
                    command=self.issuedbook).place(x=200, y=250)

#========================ISSUE A BOOK===================================================================================
    def issuedbook(self):
        suuedate = datetime.date.today()
        rd = datetime.date.today() + datetime.timedelta(7)
        bookname = self.aname.get()
        Liid = self.astudentt.get()
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        conn2 = conn.cursor()
        conn3 = conn.cursor()
        conn1.execute("select TITLE,COPIES from book_info where TITLE=%s", bookname)
        conn2.execute("select * from Student_details where LIBRARYID=%s", Liid)
        conn3.execute("select * from book_issued where BOOK_NAME=%s AND STUDENT_ID= %s ", (bookname, Liid))
        cn = conn3.fetchone()
        bn = conn2.fetchone()
        an = conn1.fetchone()
        if (bookname and Liid != ""):  # liid is library card no of student
            if an is not None:
                if an[1] > 0:
                    if bn is not None:
                        if cn is None:
                            conn1.execute("insert into book_issued values (%s,%s,%s,%s)",
                                          (bookname, Liid, suuedate, rd))

                            conn.commit()

                            conn1.execute("update book_info set COPIES=COPIES-1 where TITLE=%s", (bookname,))
                            conn.commit()
                            conn1.execute("select EMAIL_ID from Student_details where LIBRARYID =%s ", Liid)
                            em = conn1.fetchone()
                            book=self.aname.get()
                            conn1.execute("select * from book_issued_report where Book_name=%s",(book))
                            book_re=conn1.fetchone()
                            if book_re is None:
                                cop=1
                                conn1.execute("insert into book_issued_report values(%s,%s)",
                                              (book,cop))
                                conn.commit()
                            else:
                                conn1.execute("update book_issued_report set Copies=Copies+1 where Book_name=%s",(book))
                                conn.commit()
                            conn1.close()
                            messagebox.showinfo("Updated", "Book Issued sucessfully.")
                            sender = 'sender mail-id'
                            receivers = [em]
                            account = 'sender mail-id'
                            password = 'senders mail-id password'

                            message = '''From: From Person <your_email>
                                To: To Person <their_email>
                                Subject: SMTP e-mail test

                                Book Issued Succesfully.
                                Return Your Book in 7 Days or Fine
                                1 Rs  Per Day After 7 Days.
                                Thank You
                                '''

                            try:
                                smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
                                smtpObj.ehlo()
                                smtpObj.starttls()
                                smtpObj.login(account, password)
                                smtpObj.sendmail(sender, receivers, message)
                                print("Successfully sent email")

                            except:
                                print("Error: unable to send email")

                            self.aname.set(" ")
                            self.astudentt.set(" ")

                            return
                        else:
                            messagebox.showinfo("Error", "Book Already Issued.")
                            self.aname.set(" ")
                            self.astudentt.set(" ")
                            return
                    else:
                        messagebox.showinfo("Error", " ID_number Not Avalaible.")
                        self.aname.set(" ")
                        self.astudentt.set(" ")
                        return
                else:
                    messagebox.showinfo("Unavailable", "Book unavailable.\nThere are 0 copies of the book.")
                    self.aname.set(" ")
                    self.astudentt.set(" ")

                    return
            else:
                messagebox.showinfo("Error", "Book Not Available.")
                self.aname.set(" ")
                self.astudentt.set(" ")
                return
        else:
            messagebox.showinfo("Error", "Fields cannot be blank.")
            self.aname.set(" ")
            self.astudentt.set(" ")
            return

#====================STUDENT DETAILS GUI================================================================================

    def Studentfun(self):
        self.aid1 = StringVar()
        self.aname1 = StringVar()
        self.aaddress1 = StringVar()
        self.arollno1 = StringVar()
        self.adept1 = StringVar()
        self.aclass1 = StringVar()
        self.aemail1 = StringVar()

        self.f1 = Frame(self.a, height=500, width=650, bg='black')
        self.f1.place(x=500, y=100)
        l1 = Label(self.f1, text='Student-Name : ', font='Papyrus 12 bold', fg='Orange', bg='Black', pady=1).place(x=50,
                                                                                                                   y=50)
        e1 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aname1).place(x=200, y=50)
        l2 = Label(self.f1, text='Library-cardid : ', font='Papyrus 12 bold', fg='Orange', bg='Black', pady=1). \
            place(x=50, y=100)
        e2 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aid1).place(x=200, y=100)
        l3 = Label(self.f1, text='Roll-No : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50,
                                                                                                              y=150)
        e3 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.arollno1).place(x=200, y=150)
        l4 = Label(self.f1, text='Department : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1). \
            place(x=50, y=200)
        e4 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.adept1).place(x=200, y=200)
        l5 = Label(self.f1, text='Class : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50,
                                                                                                            y=250)
        e5 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aclass1).place(x=200, y=250)
        l6 = Label(self.f1, text='Address : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50,
                                                                                                              y=300)
        e6 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aaddress1).place(x=200, y=300)

        l7 = Label(self.f1, text='Email-Id : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50,
                                                                                                               y=350)
        e7 = Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aemail1).place(x=200, y=350)

        self.f1.grid_propagate(0)
        b1 = Button(self.f1, text='Add', font='Papyrus 10 bold', fg='black', bg='orange', width=15, bd=3,
                    command=self.addstu).place(x=150, y=400)
        b2 = Button(self.f1, text='Back', font='Papyrus 10 bold', fg='black', bg='orange', width=15, bd=3,
                    command=self.rm).place(x=350, y=400)

#==========================ADDING STUDENT DETAILS=======================================================================
    def addstu(self):
        a = self.aid1.get()
        b = self.aname1.get()
        c = self.aaddress1.get()
        d = self.arollno1.get()
        e = self.adept1.get()
        f = self.aclass1.get()
        g = self.aemail1.get()  # email id
        conn1 = pymysql.connect("localhost", "root", "root", "librarystore")
        conn = conn1.cursor()
        if (a and b and c and d and e and f and g) == "":
            messagebox.showinfo("Error", "Fields cannot be empty.")
            return
        else:

            email = self.aemail1.get()
            if re.match("\A(?P<name>[\w\-_]+)@(?P<domain>[\w\-_]+).(?P<toplevel>[\w]+)\Z", email, re.IGNORECASE):
                print('Yes')
                conn.execute("select * from Student_details where  LIBRARYID=%s ", a)
                x = conn.fetchone()
                if x is None:
                    conn.execute("insert into Student_details values (%s,%s,%s,%s,%s,%s,%s)",
                                 (a, b, c, d, e, f, g))

                    conn1.commit()
                    messagebox.showinfo("Success", "Student data added successfully")
                    self.aid1.set(" ")
                    self.aname1.set(" ")
                    self.aaddress1.set(" ")
                    self.arollno1.set(" ")
                    self.adept1.set(" ")
                    self.aclass1.set("")
                    self.aemail1.set("")
                    return
                else:
                    messagebox.showinfo("Error", "Student is already present.")
                    self.aid1.set(" ")
                    self.aname1.set(" ")
                    self.aaddress1.set(" ")
                    self.arollno1.set(" ")
                    self.adept1.set(" ")
                    self.aclass1.set("")
                    self.aemail1.set("")
                    return
                return
            else:
                messagebox.showinfo("Error", "INVALID EMAIL_ID")
                self.aemail1.set(" ")
                conn.close()

                return
            return

#======================RETURNING BOOK GUI===============================================================================

    def returnn(self):
        self.abookname = StringVar()
        self.astudentt5 = StringVar()
        self.f1 = Frame(self.a, height=550, width=500, bg='black')
        self.f1.place(x=500, y=100)
        l1 = Label(self.f1, text='Book-Name : ', font='papyrus 15 bold', fg='orange', bg='black').place(x=50, y=100)
        e1 = Entry(self.f1, width=25, bd=4, bg='orange', textvariable=self.abookname).place(x=220, y=100)
        l2 = Label(self.f1, text='Library-Id : ', font='papyrus 15 bold', fg='orange', bg='black').place(x=50, y=150)
        e2 = Entry(self.f1, width=25, bd=4, bg='orange', textvariable=self.astudentt5).place(x=220, y=150)
        b1 = Button(self.f1, text='Back', font='Papyrus 10 bold', bg='orange', fg='black', width=10, bd=3,
                    command=self.rm).place(x=50, y=250)
        b1 = Button(self.f1, text='Return', font='Papyrus 10 bold', bg='orange', fg='black', width=10, bd=3,
                    command=self.returnbook).place(x=200, y=250)
        self.f1.grid_propagate(0)

#============================RETURN BOOK================================================================================
    def returnbook(self):
        crntdate = datetime.date.today()
        a = self.abookname.get()
        b = self.astudentt5.get()
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        conn2 = conn.cursor()
        conn1.execute("select * from book_issued where BOOK_NAME =%s and STUDENT_ID=%s",
                      (a, b,))
        d = conn1.fetchone()
        print(d)
        conn.commit()
        if a and b != " ":
            if d is not None:
                conn1.execute("select RETURN_DATE from book_issued where BOOK_NAME=%s AND STUDENT_ID=%s  ", (a, b))
                fh = conn1.fetchone()
                q = fh[0]
                conn.commit()
                if crntdate <= q:
                    conn1.execute("DELETE  FROM book_issued where BOOK_Name=%s and STUDENT_ID=%s",
                                  (a, b,))
                    conn.commit()
                    conn1.execute("update book_info set COPIES=COPIES+1 where TITLE=%s", (a,))
                    conn.commit()
                    conn1.execute("select EMAIL_ID from Student_details where LIBRARYID=%s", (b,))
                    em = conn1.fetchone()
                    conn.commit()
                    conn1.close()
                    messagebox.showinfo("Success", "Book Returned sucessfully.")
                    self.abookname.set(" ")
                    self.astudentt5.set(" ")
                    sender = 'senders mail-id'
                    receivers = [em]
                    account = 'senders mail-id'
                    password = 'senders mail-id password'

                    message = '''From: From Person <your_email>
                                               To: To Person <their_email>
                                               Subject:  Book Recieved

                                               Book Recieved Succesfully.
                                               Thank You For Returning In Time.
                                               Enjoy Your Day
                                               '''

                    try:
                        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
                        smtpObj.ehlo()
                        smtpObj.starttls()
                        smtpObj.login(account, password)
                        smtpObj.sendmail(sender, receivers, message)
                        print("Successfully sent email")

                    except:
                        print("Error: unable to send email")

                else:
                    self.fine = (crntdate - q)
                    self.amount = IntVar()
                    q=self.astudentt5.get()
                    conn = pymysql.connect("localhost", "root", "root", "librarystore")
                    conn1 = conn.cursor()
                    conn1.execute("select EMAIL_ID from Student_details where LIBRARYID=%s", q)
                    em = conn1.fetchone()
                    conn.commit()
                    sender ='senders mail-id'
                    receivers = [em]
                    account = 'senders mail-id'
                    password = 'senders mail-id password'
                    self.fine.days
                    message = '''From: From Person <your_email>
                                                           To: To Person <their_email>
                                                           Subject: Late Book Return Fees

                                                           Please Pay Below Amount
                                                           TO Return Book=self.fine.days

                                                           '''

                    try:
                        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
                        smtpObj.ehlo()
                        smtpObj.starttls()
                        smtpObj.login(account, password)
                        smtpObj.sendmail(sender, receivers, message,message1)
                        print("Successfully sent email")

                    except:
                        print("Error: unable to send email")

                    messagebox.showinfo("Error", "Please Enter amount to be paid")
                    self.f1 = Frame(self.a, height=550, width=600, bg='black')
                    self.f1.place(x=500, y=100)

                    l3 = Label(self.f1, text='Amount To Be paid: ', font='papyrus 15 bold', fg='orange', bg='black'). \
                        place(x=50, y=100)
                    e3 = Entry(self.f1, width=25, bd=4, bg='orange', textvariable=self.amount).place(x=350, y=100)

                    b1 = Button(self.f1, text='pay', font='Papyrus 10 bold', bg='orange', fg='black', width=10, bd=3,
                                command=self.payfun).place(x=350, y=350)
                    self.f1.grid_propagate(0)
                    print(self.fine.days)
            else:
                messagebox.showinfo("Error", "Data not found.")
                self.abookname.set(" ")
                self.astudentt5.set(" ")
                conn.commit()
                conn.close()
                return

        else:
            messagebox.showinfo("Error", "Feilds Cannot Be Blank")
            return

#======================FINE PAYMENT=====================================================================================

    def payfun(self):
        x = self.amount.get()
        y = self.fine.days
        q = self.astudentt5.get()
        r = self.abookname.get()
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        if x == 0:
            messagebox.showinfo ("Error", "Amount cannot be NULL ")
            return
        elif x != y:
            messagebox.showinfo("Error", "Enter a Correct Amount")
            self.amount.set(" ")
            return
        else:
            messagebox.showinfo("Error", "fine paid successfully")
            conn1.execute("insert into Fine_paid values (%s,%s,%s)", (q, r, y))
            conn.commit()
            conn1.execute("DELETE FROM book_issued where BOOK_Name=%s and STUDENT_ID=%s",
                          (r, q,))
            conn.commit()
            conn1.execute("update book_info set COPIES=COPIES+1 where TITLE=%s", (r))
            conn.commit()
            conn1.execute("select * from fine_per_book_report where Book_name1=%s ", (r,))
            fin = conn1.fetchone()
            print(fin)
            if fin is None:
                conn1.execute("insert into fine_per_book_report values (%s,%s)", (r, self.fine.days))
                conn.commit()
            else:
                conn1.execute("update fine_per_book_report set Amount=Amount+%s where Book_name1=%s",
                              (self.fine.days, r))
                conn.commit()
            conn1.execute("select * from fine_per_student_report where library_no=%s ",(q))
            fin1=conn1.fetchone()
            if fin1 is None:
                conn1.execute("insert into fine_per_student_report values (%s,%s)", (q, self.fine.days))
                conn.commit()
            else:
                conn1.execute("update fine_per_student_report set Book_Amount=Book_Amount+%s where library_no=%s",
                              (self.fine.days, q))
                conn.commit()

            conn.close()
            self.amount.set(" ")
            self.f1.destroy()



#==================================STUDENT ACTIVITY GUI=================================================================
    def activity(self):
        self.aidd = StringVar()
        self.astudentt = StringVar()
        self.f1 = Frame(self.a, height=550, width=500, bg='black')
        self.f1.place(x=500, y=80)
        self.list2 = ("BOOK-Name", "LIBRARY ID", "ISSUE DATE", "RETURN DATE")
        self.trees = self.create_tree(self.f1, self.list2)
        self.trees.place(x=50, y=150)

        l1 = Label(self.f1, text='Book-Name/Library ID : ', font='Papyrus 15 bold', fg='Orange', bg='black').place(x=50,
                                                                                                                   y=30)
        e1 = Entry(self.f1, width=20, bd=4, bg='orange', textvariable=self.aidd).place(x=280, y=35)

        b1 = Button(self.f1, text='Back', bg='orange', font='Papyrus 10 bold', width=10, bd=3, command=self.rm).place(
            x=340, y=450)
        b2 = Button(self.f1, text='Search', bg='orange', font='Papyrus 10 bold', width=10, bd=3,
                    command=self.searchact).place(x=40, y=450)
        b3 = Button(self.f1, text='All', bg='orange', font='Papyrus 10 bold', width=10, bd=3,
                    command=self.searchall).place(x=190, y=450)
        self.f1.grid_propagate(0)

#========================SEARCH STUDENT ACTIVITY========================================================================
    def searchact(self):
        self.list2 = ("BOOK-Name", "LIBRARY ID", "ISSUE DATE", "RETURN DATE")
        self.trees = self.create_tree(self.f1, self.list2)
        self.trees.place(x=50, y=150)
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        bid = self.aidd.get()
        sid = self.aidd.get()
        if sid and bid is not None:
            conn1.execute("select * from book_issued where BOOK_Name=%s or STUDENT_ID=%s", (bid, sid,))
            d = conn1.fetchall()
            if len(d) != 0:
                for row in d:
                    self.trees.insert("", END, values=row)
                return
            else:
                messagebox.showinfo("Error", "Data not found.")
                conn.commit()
                return
        else:
            messagebox.showinfo("Error", "Fields cannot Blank")
            conn.close()
            return

#============================SEARCHING ALL STUDENT ACTIVITY=============================================================
    def searchall(self):
        self.list2 = ("BOOK-Name", "LIBRARY ID", "ISSUE DATE", "RETURN DATE")
        self.trees = self.create_tree(self.f1, self.list2)
        self.trees.place(x=50, y=150)
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        conn1.execute("select * from book_issued")
        d = conn1.fetchall()
        if d is not None:
            for row in d:
                self.trees.insert("", END, values=row)

            conn.commit()
            return
        else:
            messagebox.showinfo("Error", " Data not present")
            conn.close()
            return


#======================================REPORT GUI=======================================================================
    def report_fun(self):
        self.a = self.canvases(image2)
        l1 = Button(self.a, text='BOOKS AVAILABLE', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.cop).place(x=12, y=100)
        l2 = Button(self.a, text='BOOKS USED', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.book_used).place(x=12, y=200)
        l3 = Button(self.a, text='FINE PER BOOK', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.per_book).place(x=12, y=300)
        l4 = Button(self.a, text='<< Main Menu', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.mainmenu1).place(x=20, y=600)
        l5 = Button(self.a, text='FINE PER STUDENT', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10,
                    command=self.per_student).place(x=12, y=400)

#========================MAINMENU1======================================================================================
    def mainmenu1(self):
        self.root.destroy()
        a = menu()

#=================BOOKS AVAILABLE GRAPH=================================================================================
    def cop(self):
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        self.due=[]
        self.count =[]
        conn1.execute("select TITLE from book_info;")
        for var in conn1.fetchall():
            self.due.append(var)

        conn.commit()
        conn1.execute("select COPIES from book_info;")
        for var in conn1.fetchall():
            self.count.append(var)
        conn.commit()
        print(list(chain(*self.due)))
        print(list(chain(*self.count)))

        plt.bar(list(chain(*self.due)),list(chain(*self.count)),align='center',alpha=0.5)
        plt.title(' Book Available after Issued ')
        plt.ylabel('No-Of-Copies')
        plt.xlabel('Book-Name')
        plt.show()
        plt.close()
        conn.commit()
        conn1.close()

#=================BOOKS USED GRAPH======================================================================================
    def book_used(self):
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        self.due = []
        self.count = []
        conn1.execute("select Book_name from book_issued_report;")
        for var in conn1.fetchall():
            self.due.append(var)
        conn.commit()
        conn1.execute("select Copies from book_issued_report;")
        for var in conn1.fetchall():
            self.count.append(var)
        conn.commit()

        print(list(chain(*self.due)))
        print(list(chain(*self.count)))
        plt.bar(list(chain(*self.due)), list(chain(*self.count)), align='center', alpha=0.5)
        plt.title(' Books Mostly Issued ')
        plt.ylabel('No-Of-Copies')
        plt.xlabel('Book-Name')
        plt.show()
        plt.close()
        conn.commit()
        conn1.close()


#=======================PER BOOK FINE GRAPH=============================================================================

    def per_book(self):
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        self.due = []
        self.count = []
        conn1.execute("select Book_name1 from fine_per_book_report;")
        for var in conn1.fetchall():
            self.due.append(var)
        conn.commit()
        conn1.execute("select Amount from fine_per_book_report;")
        for var in conn1.fetchall():
            self.count.append(var)
        conn.commit()
        print(list(chain(*self.due)))
        print(list(chain(*self.count)))
        plt.bar(list(chain(*self.due)), list(chain(*self.count)), align='center', alpha=0.5)
        plt.title(' Fine Per Book ')
        plt.ylabel('Amount')
        plt.xlabel('Book-Name')
        plt.show()
        plt.close()
        conn.commit()
        conn1.close()

#==========================PER STUDENT FINE GFRAPH======================================================================
    def per_student(self):
        conn = pymysql.connect("localhost", "root", "root", "librarystore")
        conn1 = conn.cursor()
        self.due = []
        self.count = []
        conn1.execute("select library_no from fine_per_student_report;")
        for var in conn1.fetchall():
            self.due.append(var)
        conn.commit()
        conn1.execute("select Book_Amount from fine_per_student_report;")
        for var in conn1.fetchall():
            self.count.append(var)
        conn.commit()
        print(list(chain(*self.due)))
        print(list(chain(*self.count)))
        plt.bar(list(chain(*self.due)), list(chain(*self.count)), align='center', alpha=0.5,color='green')
        plt.title(' Fine Per Student ')
        plt.ylabel('Amount')
        plt.xlabel('Library Id')
        plt.show()
        plt.close()
        conn.commit()
        conn1.close()

#====================START==============================================================================================
def canvases(images, w, h):
    photo = Image.open(images)
    photo1 = photo.resize((w, h), Image.ANTIALIAS)
    photo2 = ImageTk.PhotoImage(photo1)

    canvas = Canvas(root1, width='%d' % w, height='%d' % h)
    canvas.grid(row=0, column=0)
    canvas.grid_propagate(0)
    canvas.create_image(0, 0, anchor=NW, image=photo2)
    canvas.image = photo2
    return canvas


root1 = Tk()
root1.title("LOGIN")

w = root1.winfo_screenwidth()
h = root1.winfo_screenheight()
canvas = canvases(image3, w, h)


#===========================DATABASE====================================================================================
def Database():
    global conn, cursor
    conn = pymysql.connect("localhost", "root", "root", "librarystore")
    cursor = conn.cursor()


#===========================ADMIN LOGIN=================================================================================
def Login(event=None):
    Database()

    if USERNAME.get() == "" or PASSWORD.get() == "":
        messagebox.showinfo("Error", "Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            root1.destroy()
            b = menu()
        else:
            messagebox.showinfo("Error", "Invalid username or password.")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()


#===============================VARIABLES===============================================================================
USERNAME = StringVar()
PASSWORD = StringVar()

#===============================LABELS==================================================================================
lbl_title = Label(canvas, text="ADMIN   LOGIN", font=('Papyrus', 30, 'bold',), bg='black', fg='orange')
lbl_title.place(x=500, y=100)
lbl_username = Label(canvas, text="Username:", font=('Papyrus', 15, 'bold'), bd=4, bg='black', fg='orange')
lbl_username.place(x=500, y=230)
lbl_password = Label(canvas, text="Password :", font=('Papyrus', 15, 'bold'), bd=3, bg='black', fg='orange')
lbl_password.place(x=500, y=330)
lbl_text = Label(canvas)
lbl_text.place(x=450, y=500)
lbl_text.grid_propagate(0)

#===============================ENTRY WIDGETS===========================================================================
username = Entry(canvas, textvariable=USERNAME, font=(14), bg='black', fg='orange', bd=6)
username.place(x=650, y=230, )
password = Entry(canvas, textvariable=PASSWORD, show="*", font=(14), bg='black', fg='orange', bd=6)
password.place(x=650, y=330)

#===============================BUTTON WIDGETS==========================================================================
btn_login = Button(canvas, text="LOGIN", font=('Papyrus 15 bold'), width=25, command=Login, bg='black', fg='orange')
btn_login.place(x=500, y=400)
btn_login.bind('<Return>', Login)
root1.mainloop()
#=======================================================================================================================
