#!/usr/bin/python3
import mysql.connector as my
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import math
import smtplib
from email.message import EmailMessage
import re
import json
# mydb=my.connect(host="bymxtndvmouso8un19j4-mysql.services.clever-cloud.com",user="unahlfqupvacftvn",passwd="GVr7R7SWz5rdR2vpzvFx",database="bymxtndvmouso8un19j4")
mydb=my.connect(host="localhost",user="root",passwd="iiits123",database="tippu")
mycursor = mydb.cursor()
with open('/home/student/Music/Projects/Project2/img/questions.json', encoding="utf8") as f:
    data = json.load(f)

# convert the dictionary in lists of questions and answers_choice 
questions = [v for v in data[0].values()]
answers_choice = [v for v in data[1].values()]

answers = [1,1,1,1,3,1,0,1,3,3] 

user_answer = []

indexes = []
win2=' '
win3=' '
root=' '
sent_otp=' '
parameter=1
ques = 1

def verify(email,user,pswd):
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	if(re.fullmatch(regex, email)):
		print("Valid Email")
		OTP=""
		digits="0123456789"
		for i in range(6):
			OTP+=digits[math.floor(random.random()*10)]
		message = "Your one time password is "+OTP
		details(message,email,OTP,user,pswd)
		global sent_otp
		sent_otp=OTP
	else:
		messagebox.showinfo("warning","enter valid details")
#-------------------------------------------create account window--------------------------------------#
def window3():
	win3=tk.Toplevel(win)
	win3.title("CREATE ACCOUNT")
	heading = Label(win3,bg="magenta",fg="black",width="500",height="500").pack(fill="x")
	label = Label(win3,text="successfully sent email").pack()
	frame = tk.Frame(win3,width=490,height=500,highlightbackground="pink", highlightthickness=10)
	frame.pack(expand=True)
	win3.geometry('550x420')
	win3.resizable(False,False)
	user = StringVar()
	pswd = StringVar()
	otp = StringVar()
	user_field = Label(win3,text="Username:",fg="purple",bg="white")
	pass_field = Label(win3,text="password:",fg="purple",bg="white")
	otp_field = Label(win3,text="OTP:",fg="purple",bg="white")
	email_field = Label(win3,text="Email:",fg="purple",bg="white")
	user_field.place(x=100,y=130)
	pass_field.place(x=100,y=190)
	email_field.place(x=100,y=250)
	otp_field.place(x=100,y=310)
	user_entry = Entry(win3,width=20,fg="black",bg="white")
	pass_entry = Entry(win3,width=20)
	email_entry= Entry(win3,width=30,fg="black",bg="white")
	otp_entry = Entry(win3,width=20,fg="black",bg="white")
	user_entry.place(x=100,y=160)
	pass_entry.place(x=100,y=220)
	email_entry.place(x=100,y=280)
	otp_entry.place(x=100,y=340)
	def clickedd():
		user = user_entry.get()
		pswd = pass_entry.get()
		otp = otp_entry.get()
		email = email_entry.get()
		sent_otp=verify(email,user,pswd)
	def submit(sent_otp):
		user = user_entry.get()
		pswd = pass_entry.get()
		otp = otp_entry.get()
		instance=0
		print(user)
		print(pswd)
		print(otp)
		print("sent_otp="+sent_otp)
		sqll(user,pswd,sent_otp,otp,instance)

	bt = Button(win3,text="SUBMIT",bg="red",fg="orange",command=lambda:submit(sent_otp))
	bt2 = Button(win3,text="Click For OTP",bg="red",height=1,fg="orange",command=clickedd)
	bt.place(x=100,y=370)
	bt2.place(x=370,y=280)

#---------------------------------------------forgot password window-----------------------------------#
def window2():
	
	win3=tk.Toplevel(win)
	win3.title("FORGOT PASSWORD")
	heading = Label(win3,bg="magenta",fg="black",width="500",height="500").pack(fill="x")
	label = Label(win3,text="successfully sent email").pack()
	frame = tk.Frame(win3,width=490,height=500,highlightbackground="pink", highlightthickness=10)
	frame.pack(expand=True)
	win3.geometry('550x420')
	win3.resizable(False,False)
	user = StringVar()
	pswd = StringVar()
	otp = StringVar()
	user_field = Label(win3,text="Username:",fg="purple",bg="white")
	pass_field = Label(win3,text="password:",fg="purple",bg="white")
	otp_field = Label(win3,text="OTP:",fg="purple",bg="white")
	email_field = Label(win3,text="Email:",fg="purple",bg="white")
	user_field.place(x=100,y=130)
	pass_field.place(x=100,y=190)
	email_field.place(x=100,y=250)
	otp_field.place(x=100,y=310)
	user_entry = Entry(win3,width=20,fg="black",bg="white")
	pass_entry = Entry(win3,width=20)
	email_entry= Entry(win3,width=30,fg="black",bg="white")
	otp_entry = Entry(win3,width=20,fg="black",bg="white")
	user_entry.place(x=100,y=160)
	pass_entry.place(x=100,y=220)
	email_entry.place(x=100,y=280)
	otp_entry.place(x=100,y=340)
	def clickedd():
		user = user_entry.get()
		pswd = pass_entry.get()
		otp = otp_entry.get()
		email = email_entry.get()
		sent_otp=verify(email,user,pswd)
	def submit(sent_otp):
		user = user_entry.get()
		pswd = pass_entry.get()
		otp = otp_entry.get()
		instance=1
		print(user)
		print(pswd)
		print(otp)
		print("sent_otp="+sent_otp)
		sqll(user,pswd,sent_otp,otp,instance)

	bt = Button(win3,text="SUBMIT",bg="red",fg="orange",command=lambda:submit(sent_otp))
	bt2 = Button(win3,text="Click For OTP",bg="red",height=1,fg="orange",command=clickedd)
	bt.place(x=100,y=370)
	bt2.place(x=370,y=280)

#--------------------------Code to Send Mail----------------------------------------------#
def details(message,email,OTP,user,pswd):
	try:
		to=email
		msg = EmailMessage()
		msg.set_content(message)
		msg['Subject'] = 'Regarding internship'
		msg['From'] = "project444350@gmail.com"
		msg['To'] = to
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.login("project444350@gmail.com", "dcbtdpmtlpdpfrdq")
		server.send_message(msg)
		print("successfully send mail to "+to)
		# validation(user,pswd,otp)
		messagebox.showinfo("SHOWINFO","Sent Email successfully to "+to)
	except:
		messagebox.showinfo("Warning","Check your internet connectivity")
#--------------------------SQL CODE----------------------------------------------#
def sqll(user,pswd,sent_otp,otp,instance):
		print(user)
		print(pswd)
		print(otp)
		print("sent_otp="+sent_otp)
		if(otp==sent_otp and instance==1):
			sql = "UPDATE tippu.tippus SET password = %s WHERE username = %s"
			val = (pswd,user)
			mycursor.execute(sql,val)
			mydb.commit()
			messagebox.showinfo("SUCESS","Your password Updated")
		elif(otp==sent_otp and instance==0):
			sql =("INSERT INTO tippu.tippus (username,password) VALUES (%s,%s)")
			val = (user,pswd)
			mycursor.execute(sql,val)
			mydb.commit()
			messagebox.showinfo('Loginedd..!',"Welcome "+user)
			# user_entry.delete(0,END)
			# pass_entry.delete(0,END)

		else:
			messagebox.showinfo("FAILURE","PLEASE ENTER VALID OTP")
		
#------------------------------------------------------------------------------------------#

#--------------------------------------Exam Window--------------------------------------------------------------#
def window4():
	def gen():
	    global indexes
	    while(len(indexes) < 9):
	        x = random.randint(0,9)
	        if x in indexes:
	            continue
	        else:
	            indexes.append(x)
	def showresult(score):
	    lblQuestion.destroy()
	    r1.destroy()
	    r2.destroy()
	    r3.destroy()
	    r4.destroy()
	    labelimage = Label(
	        root,
	        background = "#ffffff",
	        border = 0,
	    )
	    labelimage.pack(pady=(50,30))
	    labelresulttext = Label(
	        root,
	        font = ("Consolas",20),
	        background = "#ffffff",
	    )
	    labelresulttext.pack()
	    if score >= 25:
	        img = PhotoImage(file="/home/student/Music/Projects/Project2/img/great1.png")
	        labelimage.configure(image=img)
	        labelimage.image = img
	        labelresulttext.configure(text="You Are Excellent !!")
	    elif (score >= 15 and score < 25):
	        img = PhotoImage(file="/home/student/Music/Projects/Project2/img/justOk.png")
	        labelimage.configure(image=img)
	        labelimage.image = img
	        labelresulttext.configure(text="You Can Be Better and try again !!")
	    else:
	        img = PhotoImage(file="/home/student/Music/Projects/Project2/img//bad.png")
	        labelimage.configure(image=img)
	        labelimage.image = img
	        labelresulttext.configure(text="You need to Work Hard !!")


	def calc():
	    global indexes,user_answer,answers
	    x = 0
	    score = 0
	    for i in indexes:
	        if user_answer[x] == answers[i]:
	            score = score + 5
	        x += 1
	    print(score)
	    showresult(score)


	
	def selected():
	    global radiovar,user_answer
	    global lblQuestion,r1,r2,r3,r4
	    global ques
	    x = radiovar.get()
	    user_answer.append(x)
	    radiovar.set(-1)
	    if ques < 9:
	        lblQuestion.config(text= questions[indexes[ques]])
	        r1['text'] = answers_choice[indexes[ques]][0]
	        r2['text'] = answers_choice[indexes[ques]][1]
	        r3['text'] = answers_choice[indexes[ques]][2]
	        r4['text'] = answers_choice[indexes[ques]][3]
	        ques += 1
	    else:
	        calc()
	def startquiz():
	    global lblQuestion,r1,r2,r3,r4
	    lblQuestion = Label(
	        root,
	        text = questions[indexes[0]],
	        font = ("Consolas", 16),
	        width = 500,
	        justify = "center",
	        wraplength = 400,
	        background = "#ffffff",
	    )
	    lblQuestion.pack(pady=(100,30))

	    global radiovar
	    radiovar = IntVar()
	    radiovar.set(-1)

	    r1 = Radiobutton(
	        root,
	        text = answers_choice[indexes[0]][0],
	        font = ("Times", 12),
	        value = 0,
	        variable = radiovar,
	        command = selected,
	        background = "#ffffff",
	    )
	    r1.pack(pady=5)

	    r2 = Radiobutton(
	        root,
	        text = answers_choice[indexes[0]][1],
	        font = ("Times", 12),
	        value = 1,
	        variable = radiovar,
	        command = selected,
	        background = "#ffffff",
	    )
	    r2.pack(pady=5)

	    r3 = Radiobutton(
	        root,
	        text = answers_choice[indexes[0]][2],
	        font = ("Times", 12),
	        value = 2,
	        variable = radiovar,
	        command = selected,
	        background = "#ffffff",
	    )
	    r3.pack(pady=5)

	    r4 = Radiobutton(
	        root,
	        text = answers_choice[indexes[0]][3],
	        font = ("Times", 12),
	        value = 3,
	        variable = radiovar,
	        command = selected,
	        background = "#ffffff",
	    )
	    r4.pack(pady=5)


	def startIspressed():
	    labelimage.destroy()
	    labeltext.destroy()
	    lblInstruction.destroy()
	    lblRules.destroy()
	    btnStart.destroy()
	    gen()
	    startquiz()



	root = tk.Toplevel(win) 
	root.title("Test@Online")
	root.geometry("1200x1200")
	root.config(background="#ffffff")
	root.resizable(0,0)


	img1 = PhotoImage(file="/home/student/Music/Projects/Project2/img/test.png")

	labelimage = Label(
	    root,
	    image = img1,
	    background = "#ffffff",
	)
	labelimage.pack(pady=(40,0))

	labeltext = Label(
	    root,
	    text = "TEST ONLINE✍️",
	    font = ("Comic sans MS",24,"bold"),
	    background = "#ffffff",
	)
	labeltext.pack(pady=(0,50))

	img2 = PhotoImage(file="/home/student/Music/Projects/Project2/img/start2.png")

	btnStart = Button(
	    root,
	    image = img2,
	    relief = FLAT,
	    border = 0,
	    command = startIspressed,
	)
	btnStart.pack()

	lblInstruction = Label(
	    root,
	    text = "Read The Rules And\nClick Start Once You Are ready",
	    background = "#ffffff",
	    font = ("Consolas",14),
	    justify = "center",
	)
	lblInstruction.pack(pady=(10,100))

	lblRules = Label(
	    root,
	    text = "This quiz contains 10 questions\nYou will get 20 seconds to solve a question\nOnce you select a radio button that will be a final choice\nhence think before you select",
	    width = 100,
	    font = ("Times",14),
	    background = "#000000",
	    foreground = "#FACA2F",
	)
	lblRules.pack()

	root.mainloop()


#----------------------------------MAIN WINDOW------------------------------------------#
win = tk.Tk()
win.title("TIPPU SULTHAN")
l1=Label(win,fg="white",bg="purple",width=10).pack(side="left",fill="y")
heading = Label(text="Log IN",bg="yellow",fg="black",font="20",width="20",height="2").pack(fill="x")
l1=Label(win,fg="white",bg="black").pack(side="bottom",fill="x")
frame = tk.Frame(win,width=490,height=500,highlightbackground="black", highlightthickness=10)
frame.pack(expand=True)
tk.Label(win,bg="black").pack(fill="x")
image = Image.open("/home/student/Desktop/user.jpeg")
resize_image = image.resize((120,120))
img = ImageTk.PhotoImage(resize_image)
frame1 = tk.Frame(win,width=130,height=130,highlightbackground="black", highlightthickness=10)
frame1.place(x=740,y=170)
label1 = Label(image=img)
# label1.image = img
label1.place(x=750,y=180)

win.geometry('1500x1500')
# win.resizable(False,False)
user = StringVar()
pswd = StringVar()
user_field = Label(text="Username:",fg="purple",bg="white")
pass_field = Label(text="password:",fg="purple",bg="white")
user_field.place(x=500,y=200)
pass_field.place(x=500,y=260)
user_entry = Entry(win,width=20,fg="black",bg="white")
pass_entry = Entry(win,width=20)
user_entry.place(x=500,y=230)
pass_entry.place(x=500,y=290)
def clickedd():
	user = user_entry.get()
	pswd = pass_entry.get()
	print(user)
	print(pswd)
	try:
		if(len(user)==0 or len(pswd)==0):
			messagebox.showinfo('MESSAGE',"NO filed should empty")
		else:
			sql = "SELECT * FROM tippu.tippus where username=%s and password=%s;"
			val = (user,pswd)
			mycursor.execute(sql,val)
			row = mycursor.fetchone()
			print(row)
			if row == None:
				messagebox.showinfo('MESSAGE',"You are not an user pls register..if you are a user pls reset your password")
			else:
				window4()
				
				# messagebox.showinfo('MESSAGE',"You are alredy an User brohhh....!")
			
	except:
		messagebox.showinfo('warning',"Please Enter valid details")
		user_entry.delete(0,END)
		pass_entry.delete(0,END)


bt = Button(win,text="SUBMIT",bg="red",fg="orange",command=clickedd)
bt2 = Button(win,text="FORGOT password",bg="red",fg="orange",command=lambda:window2(),width="20")
bt3 = Button(win,text="Create Account",bg="red",fg="orange",command=lambda:window3(),width="10")
bt.place(x=500,y=340)	
bt2.place(x=600,y=340)
bt3.place(x=790,y=340)
win.mainloop()
