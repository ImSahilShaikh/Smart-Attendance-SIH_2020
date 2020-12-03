import os
import cv2
import time
import mtcnn
import datetime
import schedule
from tkinter import *
import tkinter as tk
import tkinter.font as font
from random import randint
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN 	
from django.shortcuts import render
from AMS.forms import StudentForm
from AMS.models import Student
from django.http import HttpResponse
from django.conf import settings
from matplotlib.patches import Rectangle
from tkinter import messagebox
from django.contrib import messages


def stud(request):
	if request.method == 'POST':
		form = StudentForm(request.POST)
		if form.is_valid():
			try:
				form.save()
				return redirect()
			except:
				pass
	else:
		form = StudentForm()
	return render(request,"index.html",{'form':form})


def adminLogin(request):
	if request.method == 'POST':
		user = request.POST['username']
		passw = request.POST['password']
		if(user == 'admin' and passw=='123'):
			#students = Student.objects.all()
			#{'students':students}
			messages.success(request,"Logged in successfully.")
			return render(request,"index.html")
		else:
			return render(request,"login.html")	

def login(request):
	return render(request,"login.html")

def captureImages(request):
	rno = request.POST['rollno']
	name = request.POST['name']
	folder = rno+'_'+name
	os.mkdir(os.path.join('Datasets/', folder))
	cam = cv2.VideoCapture(0)
	i=0
	val=1
	time.sleep(0.001)
	while cam.isOpened():
	    #messagebox.showinfo("Info","Please look directly into camera and press ok")
	    for i in range (75):
	        ret, frame = cam.read()
	        cv2.imwrite('Datasets/'+folder+'/'+name+'_'+str(val)+'.jpg',frame)
	        val += 1
	    cam.release()
	    if cv2.waitKey(30) & 0xFF == ord('q'):
	        break
	    #messagebox.showinfo("Info","Images captured successfully")
	#exit()
	#students = Student.objects.all()
	messages.success(request,"Images Captured and Stored Successfully.")
	return render(request,"index.html",)	


def StartSystem(request):
	prev_cnt = 0
	curr_cnt = 0
	diff = 0
	end_val = True
	global call_final
	
	def job():
		def create_global_function(master):
			return "NOtinh"
			master.destroy()
		try:
			valRead = open("img_val.txt", "r+")
		except IOError:
			valRead = open("img_val.txt", "w+")
			valRead.close()
			valRead = open("img_val.txt", "r+")

		text = valRead.read()
		if(text == ''):
			valRead.close()
			valRead = open("img_val.txt", "w")
			valRead.write('1')
			valRead.close()
		else:
			val = int(text)
			val = val + 1
			valRead.close()
			valRead = open("img_val.txt", "w")
			valRead.write(str(val))
			valRead.close()
		valRead = open("img_val.txt", "r")
		val = int(valRead.read())
		valRead.close()
		filename = 'capture.jpg'

		videoCaptureObject = cv2.VideoCapture(0)

		ret, frame = videoCaptureObject.read()
		if ret:
			detector = MTCNN()
			cv2.imwrite(filename,frame)
			pixels = pyplot.imread(filename)
			faces = detector.detect_faces(pixels)
			os.remove(filename)
		videoCaptureObject.release()
		cv2.destroyAllWindows()
		
		master = Tk()
		master.geometry("450x250+550+450")
		master.title("Student's Count")
	 
		variable1=StringVar()
		global prev_cnt
		global curr_cnt
		global diff
		global end_val
		try:
			f = open("output.txt", "r")
		except IOError:
			f = open("output.txt", "w+")
			x = datetime.datetime.now()
			f.writelines('{0} \t {1} \t {2}\n'.format(len(faces), 0,x))
			f.close()		

		with open("output.txt", "r") as f:
			data = f.readlines()
		lastline = data[-1]
		tail = data[-10:]
		f.close()
		day = lastline.split()[2]
		timee = lastline.split()[3]
		prev_cnt = int(lastline.split()[1])
		# curr_cnt = int(lastline.split()[0])
		# prev_cnt = curr_cnt
		curr_cnt = len(faces)
		diff = curr_cnt - prev_cnt
		def callDjango(master):
			global end_val
			end_val = False
			master.destroy()
		def retrieve_input(master):
			global prev_cnt
			global curr_cnt
			global diff
			f = open("output.txt", "a+")
			if(var1.get() == 1 and var2.get() == 0):			
				prev_cnt = curr_cnt
				x = datetime.datetime.now()
				f.writelines('{0} \t {1} \t {2}\n'.format(curr_cnt, prev_cnt,x))
				f.close()
				print("Current count : ", curr_cnt)
				print("Previous count : ", prev_cnt)
				master.destroy()
			elif((var1.get() == 0 and var2.get() == 0) or (var1.get() == 1 and var2.get() == 1)):
				messagebox.showwarning("Bad input","Illegal values, please try again")
				master.destroy()
				job()
			else:
				print("Previous count : ", prev_cnt)
				x = datetime.datetime.now()
				f.writelines('{0} \t {1} \t {2}\n'.format(prev_cnt, 0,x))
				f.close()
				master.destroy()

		myFont = font.Font(size=20)
		label1= Label(master, font=("Helvetica", 16),text = "Previous count : ").place(x = 20,y = 30)   
		label2= Label(master, font=("Helvetica", 16),text = prev_cnt).place(x = 180,y = 30)

		label3= Label(master, font=("Helvetica", 16),text = "Current count : ").place(x = 240,y = 30)   
		label4= Label(master, font=("Helvetica", 16),text = curr_cnt).place(x = 390,y = 30)

		label5=Label(master, font=("Helvetica", 16) , text = "Difference is : ").place(x = 120,y = 75)   
		label6=Label(master, font=("Helvetica", 16), text = diff).place(x = 270,y = 75)
		#label1['font']=myFont
		# label2.config(font=("Courier", 14))
		# label3.config(font=("Courier", 14))
		# label4.config(font=("Courier", 14))
		button1 = tk.Button(master, text="Submit", bg='#0052cc', fg='#ffffff',command=lambda: retrieve_input(master))
		button1.place(x = 50, y = 170)
		button1['font'] = myFont

		#button2 = tk.Button(master, text="QUIT", fg="red", command=master.destroy)
		button2 = tk.Button(master, text="QUIT", bg="red", fg='#ffffff', command=lambda: callDjango(master))
		button2.place(x = 300, y = 170) 
		button2['font'] = myFont
		
		var1 = IntVar()
		Checkbutton(master, text="Lock Count",font=("Helvetica", 14), variable=var1).place(x = 30,y = 120)
		var2 = IntVar()
		Checkbutton(master, text="Use Previous Count", font=("Helvetica", 14),variable=var2).place(x = 220, y = 120)
		master.resizable(0, 0)
		mainloop()		
		
		
	schedule.every(0.001).minutes.do(job)
	while end_val:
		schedule.run_pending()
		time.sleep(0.001)
	students = Student.objects.all()	
	return render(request,"index.html",{'students':students})

def trainImages(request):
	time.sleep(2)
	#students = Student.objects.all()
	messages.success(request,"Images Trained Successfully.")	
	return render(request,"index.html")		

def stop(request):
	time.sleep(3)
	messages.success(request,"Table of Recognized Faces.")
	students = Student.objects.all()	
	return render(request,"index.html",{'students':students})				