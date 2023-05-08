import csv 
import smtplib
import mysql.connector
from smtplib import SMTPException
from email.mime.text import MIMEText
import re
from datetime import datetime
#from random import randint
#from time import sleep
from numpy import random
from time import sleep
import os
import sys
#msg = MIMEText("EmailOperator testing email.")

def Send_Email_p():
  All_arguments = sys.argv
  Subject_f = open(Subject_path,'r')
  Subject_file = Subject_f.read()
  Subject_f.close()

  fp = open(Messages_path, mode='r',encoding='UTF-8')
  msg = MIMEText(fp.read())
  fp.close()

  msg['Subject'] = Subject_file
  msg['From'] = "Ranjan Khurana <{}>".format(All_arguments[4])

  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  #server.login('thegamingdial@gmail.com', 'ykmixikasujjvbno')
  try:
    server.login(All_arguments[4], All_arguments)
  except:
    print("====== Please check Email and password =======") 
    sys.exit(1)
  email_d = open(Emails_path, mode='r',encoding='UTF-8') 
  email_data = email_d.readlines()
  ############# add here csv file #################
  email_pattern= re.compile("^.+@.+\..+$")
  i=0
  ff = open("Sent_emails.csv","w")
  for row in email_data:
    row = row.replace("\n",'')
    i=i+1
    if( email_pattern.search(row) ):
      del msg['To']
      msg['To'] = row
      print("i is",i)
      try:
        if (i/40).is_integer():
          server.quit()
          server = smtplib.SMTP('smtp.gmail.com:587')
          server.starttls()
          server.login(All_arguments[4], All_arguments[5])
          print("smtp logged in again")
        #sleep(randint(3,8))
        server.sendmail('test@gmail.com', [row], msg.as_string())
        sleeptime = random.uniform(40, 120)
        print("sleeping for:", sleeptime, "seconds")
        sleep(sleeptime)
        print("sleeping is over")
        ffa = open("Sent_emails.csv","a")
        ffa.write(str(row)+"\n")
        ffa.close()
        print("Sent Email to ",row)
      except Exception as e:
        print ("An error occured.",e)
  server.quit()

def Geting_Data():
    All_arguments = sys.argv
    arg_f = open(All_arguments[1],'r')
    arg_fa = arg_f.read()
    arg_f.close()
    Email_f = open(Emails_path,'w')
    Email_f.write(arg_fa)
    Email_f.close()
    arg_f = open(All_arguments[3],'r')
    arg_fa = arg_f.read()
    arg_f.close() 
    message_f = open(Messages_path,'w')
    message_f.write(arg_f)
    message_f.close()
    Subject_f = open(Subject_path,'w')
    Subject_f.write(All_arguments[2])
    Subject_f.close()

if "__main__"==__name__:
    ################# Path Section ###############
    print("======= The Script Proper Running =====")
    Script_Path = os.path.dirname(__file__)
    if "\\" in Script_Path:
      Path_Slash = '\\'
    else:
      Path_Slash = "/"  
    Input_Folder = os.path.join(Script_Path,'Input')
    if not os.path.exists(Input_Folder):
      os.mkdir(Input_Folder)
    Messages_path = os.path.join(Input_Folder,"Messages_.txt")
    Emails_path = os.path.join(Input_Folder,"Emails_list.csv")
    Subject_path = os.path.join(Input_Folder,"Subject_text.txt")
    user_Email = os.path.join(Input_Folder,"user_e.txt")
    user_pass = os.path.join(Input_Folder,"user_pass.txt")
    Geting_Data()
    Send_Email_p()