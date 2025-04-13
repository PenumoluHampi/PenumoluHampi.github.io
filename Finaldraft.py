from tkinter import *
import tkinter as tk
import sys
import pandas as pd
import xlrd
from openpyxl import *
import psycopg2

LARGE_FONT= ("Verdana", 12)

class AnalysingLevelOfEnglish(tk.Tk):

    def __init__(self, *args, **kwargs):
       
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.title("AnalysingLevelOfEnglish")
        self.geometry("1500x1500")
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.connection = None
        self.cursor = None
        self.connect_to_db()
       
        for F in (Welcome, Signin, Signup , Login , Startexam , Exam  , Score , Improve , Thankyou):

            frame = F(container, self)

            self.frames[F] = frame
           
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Welcome)
       
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
    def connect_to_db(self):
        try:
            # Connect to your PostgreSQL database
            self.connection = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='student',
                host='localhost',  # e.g., 'localhost'
                port='5432'   # e.g., '5432'
            )
            self.cursor = self.connection.cursor()
            print("Database connection successful")
        except Exception as e:
            print("Error connecting to database:", e)
            
    def fetch_users(self):
        try:
            query = "SELECT * FROM Users"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows  # Return the fetched rows
        except Exception as e:
            print("Error fetching users:", e)
            return []

    def close_db(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed")

    def __del__(self):
        self.close_db()  # Ensure the database connection is closed when the app is closed


       
class Welcome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="          ",font=LARGE_FONT)
        label.pack(pady=200,padx=200)
       
        button = tk.Button(self, text="WELCOME",height=2,width=25,fg="blue",font=('arial',16,'bold'),command=lambda: controller.show_frame(Signin))
        button.pack()


       
class Signin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
             
        label = tk.Label(self, text="          ", font=LARGE_FONT)
        label.pack(pady=100,padx=100)

        label1 = tk.Label(self, text="new user",fg="blue",font=LARGE_FONT)
        label1.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="SIGN UP",height=2,width=25,fg="blue",font=('arial',16,'bold'),command=lambda: controller.show_frame(Signup))
        button1.pack()
        

        label2 = tk.Label(self, text="or existing user",fg="blue", font=LARGE_FONT)
        label2.pack(pady=20,padx=20)
       
        button2 = tk.Button(self, text="LOG IN",height=2,width=25,fg="blue",font=('arial',16,'bold'),command=lambda: controller.show_frame(Login))
        button2.pack()
        

class Signup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label2 = tk.Label(self, text="Enter your details", font=LARGE_FONT)
        label2.pack(pady=13, padx=13)

        self.name_label = tk.Label(self, text="Name:", fg="blue", font=('arial', 13, 'bold'))
        self.name_label.pack(pady=5)

        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        self.mobile_label = tk.Label(self, text="Mobile Number:", fg="blue", font=('arial', 13, 'bold'))
        self.mobile_label.pack(pady=5)

        self.mobile_entry = tk.Entry(self)
        self.mobile_entry.pack(pady=5)

        self.email_label = tk.Label(self, text="Email ID:", fg="blue", font=('arial', 13, 'bold'))
        self.email_label.pack(pady=5)

        self.email_entry = tk.Entry(self)
        self.email_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:", fg="blue", font=('arial', 13, 'bold'))
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self, show="*")  # Hide the password input
        self.password_entry.pack(pady=5)

        signup_button = tk.Button(self, text="Sign Up", height=2, width=25, fg="blue", font=('arial', 13, 'bold'),
                                   command=self.sign_up)
        signup_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", height=2, width=25, fg="blue", font=('arial', 13, 'bold'),
                                command=lambda: controller.show_frame(Signin))
        back_button.pack(pady=10)

        self.controller = controller  # Store controller reference

    def sign_up(self):
        print('Entered Sign up')
        name = self.name_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        try:
            query = "INSERT INTO Users (name, mobile, email, password) VALUES (%s, %s, %s, %s)"
            # Use the controller to access the cursor and connection
            self.controller.cursor.execute(query, (name, mobile, email, password))
            self.controller.connection.commit()
            print("User signed up successfully")
            self.controller.show_frame(Startexam)
        except Exception as e:
            print("Error during signup:", e)

        print(f"Name: {name}, Mobile: {mobile}, Email: {email}, Password: {password}")

class Login(tk.Frame):
    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
       
        label2 = tk.Label(self, text="          ", font=LARGE_FONT)
        label2.pack(pady=130,padx=130)
       
        button = tk.Button(self, text="Enter your details!!!",height=2,width=25,fg="blue",font=('arial',13,'bold'))
        button.pack()
       
        label = tk.Label(self, text="Mail ID ",fg="blue", font=('arial',13,'bold'))
        label.pack(pady=13,padx=13)

        textBox=tk.Text(self, height=3, width=30)
        textBox.pack()
       
        self.password = tk.Label(self, text="Password:",fg="blue", font=('arial',13,'bold'))
        self.password.pack(pady=20,padx=20)

        self.textBox=tk.Text(self, height=3, width=30)
        self.textBox.pack()
        
        button1 = tk.Button(self, text="Enter into exam ->",height=2,width=25,fg="blue",font=('arial',13,'bold'),command=lambda: controller.show_frame(Startexam))
        button1.pack()
       
        label1 = tk.Label(self, text="or", font=LARGE_FONT)
        label1.pack(pady=13,padx=13)

        button2 = tk.Button(self, text="Back",height=2,width=25,fg="blue",font=('arial',13,'bold'),command=lambda: controller.show_frame(Signin))
        button2.pack()
        
    def log_in(self):
        print('Entered Login')
        name = self.textBox.get("1.0", tk.END).strip() # Get the name from the text box
        mobile = self.textBox.get("1.0", tk.END).strip()
        email = self.textBox.get("1.0", tk.END).strip()
        password = self.textBox.get("1.0", tk.END).strip()
        # Get other inputs similarly...

        try:
            # Insert user data into the database
            query = "INSERT INTO Users (name, mobile, email, password) VALUES (%s, %s, %s, %s)"
            self.parent.cursor.execute(query, (name, mobile, email, password))
            self.parent.connection.commit()  # Commit the transaction
            print("User signed up successfully")
            # Optionally show a message or transition to another frame
        except Exception as e:
            print("Error during signup:", e)

class Startexam(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
       
        label2 = tk.Label(self, text="          ", font=LARGE_FONT)
        label2.pack(pady=100,padx=100)

       
        button1 = tk.Button(self, text="Start Exam",height=2,width=25,fg="blue",font=('arial',16,'bold'),command=lambda: controller.show_frame(Exam))
        button1.pack()

        label = tk.Label(self, text="or", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button2 = tk.Button(self, text="Quit",height=2,width=25,fg="blue",font=('arial',16,'bold'),command=lambda: controller.show_frame(Thankyou))
        button2.pack()
   
class Exam(tk.Frame):


    def Split(self):
        sheet1 = pd.read_excel(r'Word Lists.xls')  
        wb = xlrd.open_workbook("Word Lists.xls")
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 0)
        a=[]
        b=[]
        c=[]
        wb1 = xlrd.open_workbook("Book1.xls")
        sheet1 = wb1.sheet_by_index(0)
        sheet1.cell_value(0, 0)
       
        wb2 = xlrd.open_workbook("Book2.xls")
        sheet2 = wb2.sheet_by_index(0)
        sheet2.cell_value(0, 0)

       
        for i in range(sheet.nrows):
            a.append(sheet.cell_value(i, 0))
            #print(a[i])
       
        for i in range(sheet1.nrows):
            b.append(sheet1.cell_value(i, 0))
            #print(b[i])
        for i in range(sheet2.nrows):
            c.append(sheet2.cell_value(i, 0))
            #print(c[i])
        self.list=self.text.get("1.0",tk.END)
        word_list = self.list.split()
        
        word_freq = [word_list.count(n) for n in word_list]
        sent_list=self.list.splitlines()
        oxf=[a.count(n) for n in a]
        gen=[b.count(n) for n in b]
        awlfreq=[c.count(n) for n in c]
        vowels=['a','e','i','o','u','y','A','E','I','O','U','Y']
        count_word_list=0
        for i in word_list:
            count_word_list=count_word_list+1
#        print(count_word_list)

        characters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        count_char_list=0
        char_list= [each for each in self.list if each in characters]
#        print(char_list)
        count_char_list=len(char_list)
        print('Total characters')
        print(count_char_list)

        count_sent_list=0
        for i in sent_list:
            count_sent_list=count_sent_list+1
        print('Total sentences')
        print(count_sent_list)
        
        syllable_list= [each for each in self.list if each in vowels]
        count_syllable_list=len(syllable_list)
#        print(count_syllable_list)

        ASL=count_word_list/count_sent_list
        print('Total ASL Words')

        print(ASL)
        
        ASW=count_syllable_list/count_word_list
        print('Total AWL Words')

        print(ASW)
        
        RE = 206.835 - (1.015 * ASL) - (84.6 * ASW)
        #Rule 6
        
        FKRA = (0.39 * ASL) + (11.8 * ASW) - 15.59
        #Rule 6
        
        part1=count_char_list/count_word_list
        part2=count_word_list/count_sent_list
        ARI= (4.71 * part1) + (0.5 * part2) - 21.43
        #Rule 6

    # Display the results
        print(f"Flesch Reading Ease: {RE}")
        print(f"Flesch-Kincaid Grade Level: {FKRA}")
        print(f"Automated Readability Index: {ARI}")

        if RE > 0 and RE <30:
            res = 'Very Low'
            print(res)
        elif RE > 30 and RE <80:
            res = 'Better'
            print(res)
        elif RE > 80 and RE <=100:
            res = 'Excellent'
            print(res)

        oxford=dict(zip(a, oxf))
        general=dict(zip(b, gen))
        awl=dict(zip(c, awlfreq))
        t=dict(zip(word_list, word_freq))
        
        p=q=r=p1=p2=0
        d1 = {key:t[key] for key in oxford if key in t}
        p=len(d1)

        d2 = {key:t[key] for key in general if key in t}
        q=len(d2)
        
        d3 = {key:t[key] for key in awl if key in t}
        r=len(d3)
        
        d5 = {key:d1[key] for key in d2 if key in d1}
        p1=len(d5)
        
        d4 = {key:d5[key] for key in d3 if key in d5}
        p2=len(d4)
        
        count=0
        if(p>q)or (p>r):
            count=p
        elif (q>p or q>r):
            count=q
        else:
            count=r
        #print(count)       
        def write(self,d1):
            k=0
            self.listbox.insert(END,'List1 Words')
            for key in d1:
                k+=1
                self.listbox.insert(END, '{}: {} - {}'.format(k,key, d1[key]))
        write(self,d1)
        
        def write1(self,d2):
            k=0
            self.listbox1.insert(END,'List2 Words')
            for key in d2:
                k+=1
                self.listbox1.insert(END, '{}: {} - {}'.format(k,key, d2[key]))
        write1(self,d2)
        
        def write2(self,d3):
            k=0
            self.listbox2.insert(END,'List3 Words')
            for key in d3:
                k+=1
                self.listbox2.insert(END, '{}: {} - {}'.format(k,key, d3[key]))
        write2(self,d3)
        
        def write3(self,d5):
            k=0
            self.listbox3.insert(END,'Common Words from list1 and list2')
            for key in d5:
                k+=1
                self.listbox3.insert(END, '{}: {} - {}'.format(k,key, d5[key]))
            self.listbox3.insert(END, res )
        write3(self,d5)

        
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label1 = tk.Label(self, text="          ", font=LARGE_FONT)
        label1.pack(pady=50,padx=50)
       
        label = tk.Label(self, text="Edit your text!!!",fg="green", font=('arial',16,'bold'))
        label.pack(pady=10,padx=10)

        self.text=tk.Text(self,height=30, width=45)
        self.text.pack(side=LEFT, expand=1)


        self.listbox3 = tk.Listbox(self,height=15, width=17)
        self.listbox3.pack(side=RIGHT)

        self.listbox2 = tk.Listbox(self,height=15, width=17)
        self.listbox2.pack(side=RIGHT)

        self.listbox1 = tk.Listbox(self,height=15, width=17)
        self.listbox1.pack(side=RIGHT)


        self.listbox = tk.Listbox(self,height=15, width=17)
        self.listbox.pack(side=RIGHT)
       

        label1 = tk.Label(self, text="          ", font=LARGE_FONT)
        label1.pack(pady=300,padx=300)

        self.buttonCal = tk.Button(self, text="Check",height=2,width=20,fg="blue",font=('arial',16,'bold'), command=self.Split)
        self.buttonCal.pack(side=LEFT)
       
        button2 = tk.Button(self, text="Submit",height=2,width=25,fg="blue",font=('arial',16,'bold'),command=lambda: controller.show_frame(Score))
        button2.pack(side=RIGHT)

       
           
class Score(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
       
        label = tk.Label(self, text="Thank you for taking the exam",fg="blue",font=('arial',16,'bold'))
        label.pack(pady=10,padx=10)
        
       
        button2 = tk.Button(self, text="next",height=2,width=25,fg="blue",font=('arial',16,'bold'),command=lambda: controller.show_frame(Improve))
        button2.pack()
           

class Improve(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Do you want to improve your level then enter into exam", fg="blue",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
       
        button1 = tk.Button(self, text="Start Exam",height=2,width=25,fg="blue",font=('arial',16,'bold'),command=lambda: controller.show_frame(Exam))
        button1.pack()

        label = tk.Label(self, text="or", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button2 = tk.Button(self, text="Quit",height=2,width=25,fg="blue",font=('arial',16,'bold'),command=lambda: controller.show_frame(Thankyou))
        button2.pack()

class Thankyou(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label1 = tk.Label(self, text="          ", font=LARGE_FONT)
        label1.pack(pady=50,padx=50)
       
       
        label = tk.Label(self, text="Thank you",fg="blue", font=('arial',25,'bold'))
        label.pack(pady=10,padx=10)
       
app = AnalysingLevelOfEnglish()
app.configure()
app.mainloop()


