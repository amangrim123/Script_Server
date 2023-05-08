import csv
from logging import exception
#from msilib.schema import File
import multiprocessing
from pathlib import Path
import subprocess
import shlex
import os
from datetime import datetime
import shutil
from multiprocessing.pool import ThreadPool
import sys
import mysql.connector
import pandas as pd
import requests
import time
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium import webdriver
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv




def call_proc(cmd):
    print("Inside call_proc - %s" % cmd)
    """ This runs in a separate thread. """
    #subprocess.call(shlex.split(cmd))  # This will block until cmd finishes
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (out, err)

def send_output_email(send_result):
    print(send_result)
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "aman.grimbyte@gmail.com"
    receiver_emails = ["rachit@grimbyte.com"]
    #receiver_email = "rachit@grimbyte.com, rajan@grimbyte.com"
    Password = "vpplugamxnyyzlui"
    
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    
    # storing the senders email address  
    msg['From'] = smtp_server
    
    # storing the receivers email address 
    
    # storing the subject 
    msg['Subject'] = "domain file"
    
    # string to store the body of the mail
    body = "Output file"
    
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # open the file to be sent 
    attachment = open(send_result, "rb")
    
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    
    # encode into base64
    encoders.encode_base64(p)

    filename = current_date + "_Key_to_url.csv"
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    # attach the instance 'p' to instance 'msg'
    # msg.attach(p)
    
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, Password)

        for receiver_email in receiver_emails:
            msg['To'] = receiver_email
            msg.attach(p)
            text = msg.as_string()
            # # sending the mail
            server.sendmail(smtp_server,receiver_email, text)
            print(f"successfully send output file on email to {receiver_email}")
            time.sleep(5)
        
        # terminating the session
        server.quit()

def upload_to_db(all_results):
    mydb = mysql.connector.connect(
            host="3.140.57.116",
            user="wp_raj1",
            password="rajPassword95$",
            database="Nikhil_Work"
        )

    with open(all_results,'r') as qq:
        out_qq = qq.read()

    mycursor = mydb.cursor()

    ssl = "INSERT into Output_Data (Date, Outpu_Result) VALUE (%s,%s)"  

    current_date_db = datetime.now().strftime("%d/%m/%y")

    val = (current_date_db,out_qq)

    mycursor.execute(ssl,val)

    mydb.commit()

    # return send_output_email(all_results) ######### send email ##########


def Merge_results(directory, summary_file_path,result_f,all_result,Path_Slash):
    print("the  resullf = ",result_f)
    time.sleep(10)

    print("Inside Merge_results function")
    directory_sub = os.listdir(directory)
    lista =[]
    for next_csv in directory_sub:
        if next_csv.startswith("key"):
            if os.stat(directory+Path_Slash+next_csv).st_size != 0:
                dataset = pd.read_csv(directory+Path_Slash+next_csv)
                data = dataset.loc[ :, 'Found_Dns']
                newlist = [x for x in data if pd.isnull(x) == False]
                print(newlist)
                lista.append(newlist)
            else:
                print("Output file Emply") 
        else:
            print("not file")          
    with open(summary_file_path,'w') as f:
        reader=csv.writer(f)
        reader.writerows(lista)

    with open(summary_file_path,"r") as ff:
        rrr =ff.read() 

    dd = rrr.split(",")

    listab = []

    for hh in dd:
        listab.append(hh)
    listab = list(set(listab))
    result_sub = os.listdir(result_f)
    if len(result_sub) == 0:
        with open(all_result, 'w',encoding='utf-8') as ff:            
            ff.writelines(i+"\n" for i in listab)
    else:        
        result_sub_last = result_sub[-1]

        if result_sub_last == current_date+"news_silo.csv":
            with open(result_f+Path_Slash+result_sub_last,mode='a',newline='') as ff:
                ff.writelines(i+"\n" for i in listab)
        else:
            with open(all_result, 'w',encoding='utf-8') as ff:            
                ff.writelines(i+"\n" for i in listab)

    return upload_to_db(all_result)    #add data in data base      


# ======== here is rebooting =====
def fuct_for_reboot():
    chrome_options = Options()  
    chrome_options.headless = True

    a ="dev\chromedriver.exe"
    driver = webdriver.Chrome(a,chrome_options=chrome_options)  # Path to where I installed the web driver
    driver.get("http://192.168.1.1/")
    time.sleep(0.2) # Let the user actually see something!

    search_box = driver.find_element("name", "Frm_Username").send_keys('user')
    search_box = driver.find_element("name","Frm_Password").send_keys('user')

    search_box = driver.find_element('id',"LoginId").click()
    time.sleep(0.5)
    # search_box = driver.find_element(by = By.XPATH,value='//*[@id="mgrAndDiag"]').click()
    button1 = driver.find_element("id","mgrAndDiag")
    button1.click()

    time.sleep(0.2)
    button2 = driver.find_element("id","devMgr")
    button2.click()

    time.sleep(0.2)
    button2 = driver.find_element("id","Btn_restart")
    button2.click()

    time.sleep(0.2)
    button2 = driver.find_element("id","confirmOK")
    button2.click()

    time.sleep(5)
    driver.minimize_window()

    time.sleep(120) # Let the user actually see something!
    driver.quit()
    return print("======Wifi has rebooted successfully ====")


def GetInput_fromUrl(url, output_file_path):
    print("Inside GetInput_fromUrl")

    #Output_file_path = os.path.join(outputfolder, File_name)
    with open(output_file_path, 'wb') as out_file:
        content = requests.get(url, stream=True).content
        out_file.write(content)

    return True


def Clean_InputFile(input_file_path, column_name):
    print("Inside Clean_InputFile")
    try:
        if '.csv' in input_file_path :
            temp = pd.read_csv(input_file_path)
        elif ('.xlsx' in input_file_path) or ('.xls' in input_file_path):
            temp = pd.read_excel(input_file_path)
        else:
            print("Unsupported input file path passed")
            return False
        
        temp = temp.drop(temp.columns[temp.columns != column_name], axis=1)
        temp.to_csv(input_file_path, header=False, index=False)

        return True

    except exception as e:
        return False


if __name__ == '__main__':

    ################### Sript path #################
    ScriptPath = os.path.dirname(os.path.abspath(__file__))
    ScriptName = os.path.basename(__file__).replace('.py','')

    print("1. Parent Script Initiating...")
    if '/' in ScriptPath:
        Path_Slash="/"
    else:
        Path_Slash="\\"


    # try:
    #     driver_path = sys.argv[1]
    # except:
    #     print("============ Please write command python3 main.py server or local ========= ")
    #     sys.exit()

    # if driver_path != 'server':
    #     dotenv_path = Path(ScriptPath + Path_Slash +'local.env')
    #     print(dotenv_path)
    #     load_dotenv(dotenv_path=dotenv_path)
    # else:
    #     dotenv_path = Path(ScriptPath + Path_Slash +'server.env')
    #     print(dotenv_path)
    #     load_dotenv(dotenv_path=dotenv_path)
        
    ############ Folder path from .env file ###########
    
    # BOOTSTRAP_Diractory_path = os.environ.get('dricatory_path')
    BOOTSTRAP_output_folder = os.path.join(ScriptPath,'output_folder')
    # print(BOOTSTRAP_output_folder)
    # BOOTSTRAP_output_folder_result = BOOTSTRAP_Diractory_path + os.environ.get('output_folder_result')
    # BOOTSTRAP_temp_folder = BOOTSTRAP_Diractory_path + os.environ.get('temp_folder')
    # BOOTSTRAP_log_folder = BOOTSTRAP_Diractory_path + os.environ.get('log_folder')
    # BOOTSTRAP_Source_file_path = BOOTSTRAP_Diractory_path + os.environ.get('Source_file_path')
    
    ########################### core Setting #######################

    BOOTSTRAP_Number_of_core = os.environ.get('Number_of_core')
    BOOTSTRAP_GoogleUrls_Count = os.environ.get('GoogleUrls_Count')
    BOOTSTRAP_Batch_size = os.environ.get('Batch_size')


    ########### Initializing Parent script ###########

    current_time = datetime.now().strftime("%d%m%y_%H%M%S")
    current_date = datetime.now().strftime("%d%m%y")

    Google_urls = ScriptPath + Path_Slash + 'GoogleUrls.csv'

    ############ Output Folder path ################

    output_folder = os.path.join(ScriptPath,'output')
    result_folder = os.path.join(ScriptPath,'Output_result')
    
    FlagFile_Path = ScriptPath + Path_Slash + "Flag_file.txt"
    output_sub_folder = output_folder + Path_Slash + "Output_" + current_time
    sub_result_f = result_folder + Path_Slash + current_date + "news_silo.csv"
    # output_file = ScriptName + "_output_" + current_time + "_XXX.csv"
    output_file = ScriptName + "_output_" + current_time + "_XXX.csv"
    output_file_path = output_sub_folder + Path_Slash + output_file
    summary_file = "Summary_" + current_time + ".csv"
    output_summary_file_path = output_sub_folder + Path_Slash +  summary_file
    ##################### All Path #######################
    #################### Input Folder ####################


    temp_folder = os.path.join(ScriptPath,'temp')


    #################### Log Folder path ###############

    log_folder = os.path.join(ScriptPath,'logs')

    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    log_sub_folder = log_folder + Path_Slash + "Log_" + current_time
    if not os.path.exists(log_sub_folder):
        os.mkdir(log_sub_folder)

    log_file = ScriptName + "_log_" + current_time + "_XXX.log"
    log_file_path = log_sub_folder + Path_Slash + log_file

    log_sub_folder = log_folder + Path_Slash + "Log_" + current_time
    if not os.path.exists(log_sub_folder):
        os.mkdir(log_sub_folder)

    ######## Settings ########
    
    Number_of_Scripts_to_run_parallel = 2
    Batch_size = 1

    GoogleUrls_Count = 1
  
    GoogleFile_Path = ScriptPath + Path_Slash + "GoogleUrls.csv"

    #testing on windows 10 machine with i7 cpu and mobile data Jio Rs.555 wala plan 
    
    '''
    PARSER = argparse.ArgumentParser()

    PARSER.add_argument('--csv', help="csv file path")
    PARSER.add_argument('--url', help="URL of csv file")
    PARSER.add_argument('--col', help="Column name to keep in csv file")
    PARSER.add_argument("-n", default=8, type=int, help="Number_of_Scripts_to_run_parallel")
    PARSER.add_argument("-b", default=16, type=int, help="Batch_size")
    PARSER.add_argument("-g", default=8, type=int, help="GoogleUrls_Count")

    args = PARSER.parse_args()
    
    csv_file_path = args.csv
    url = args.url
    column_name = args.col
    Number_of_Scripts_to_run_parallel = int(args.n)
    Batch_size = int(args.b)
    GoogleUrls_Count = int(args.g)
    ''' 
    try:
        check_argument = sys.argv
        print(check_argument)
        print(len(check_argument))
        if len(check_argument) > 1:
            file_argument = sys.argv[1]
            in_f = open(file_argument,'r')
            in_file = in_f.read()
            in_f.close()

        Source_folder = os.path.join(ScriptPath,'INPUT')
        source_file_path = os.path.join(Source_folder,"hello.png")
        Get_INput_f = open(source_file_path,'w')
        Get_INput_f.write(in_file)
        Get_INput_f.close()

    except:
        print(" ================= Opps! Your Source file Is Empaty! ================ ")  
        sys.exit()

    print(" get source_file = ",source_file_path)
    print("2. Settings configured :")
    print(" Number_of_Scripts_to_run_parallel - %s" % Number_of_Scripts_to_run_parallel)
    print(" Batch_size - %s" % Batch_size)
    print(" GoogleUrls_Count - %s" % GoogleUrls_Count)

    Flag_file = ScriptPath + Path_Slash + "Flag_file.txt"
    with open(Flag_file, 'r') as f:
        a = f.readline()
        if a =="True":
            a = True
        else:
            a = False   

    if a==True:
    
        ## Creating Temp folder for child scripts to pick their input query files
        print("5. Creating Temp folder for child scripts to pick their input query files")
        
        if os.path.exists(temp_folder):
            print(" Deleting 'temp' folder...")
            shutil.rmtree(temp_folder)
        

        print(" Creating new 'temp' folder...")
        os.mkdir(temp_folder)
        temp_file = temp_folder + Path_Slash + "Temp_" + current_time + "_XXX" + ".csv"


        ### Get Target DNS to search
        print("6. Get Target DNS to search from Source CSV file")
        TargetUrls = []
        # Temp_string = "inurl%3A"
        with open(source_file_path, mode='r',encoding= 'unicode_escape') as file:
            for line in file:
                TargetUrls.append(line.replace('"', '').replace(u'\ufeff', '').rstrip())
        

        ### Get Google URLs to search
        print("7. Fetching Google URLs to search")
        GoogleUrls = []
        with open(GoogleFile_Path, mode='r',encoding='UTF-8') as file:
            counter = 0
            for line in file:
                #if counter < GoogleUrls_Count:
                GoogleUrls.append(line.rstrip())       


        ###### Creating Batches ######
        print("8. Creating Batches with batch size - %s" % Batch_size)
        Batches=[]
        possible_word_seperators = ['.','-',':']
        possible_word_count = 0
        Batch = []

        for idx,i in enumerate(TargetUrls):
            current_word_count = 0

            for j in possible_word_seperators:
                current_word_count += i.count(j)
            
            current_word_count = current_word_count + 1
            possible_word_count += current_word_count

            if idx != (len(TargetUrls) - 1):
                if possible_word_count <= Batch_size:
                    Batch.append(i)
                else:
                    Batches.append(Batch)
                    Batch = []
                    possible_word_count = current_word_count
                    Batch.append(i)
            else:
                Batch.append(i)
                Batches.append(Batch)
            
        print(" Created %s different queries..." % len(Batches))
        
        '''
        start_urls = []
        for idx,i in enumerate(Batches):
            LL = idx % len(GoogleUrls)
            Query_Url = "https://www" + GoogleUrls[LL] + "/search?q=" + ("+OR+".join(i)) + "&tbm=nws"
            start_urls.append(Query_Url)


        Query_count = len(start_urls)
        if Query_count <= Number_of_Scripts_to_run_parallel:
            print("Number_of_Scripts_to_run_parallel is greater than equal to Total Query count..")
            print("Hence terminating the script...")
            sys.exit()
        '''
    if a==True:
        ###### Creating Temp files ######
        print("9. Creating Temporary Query Files..")
        GoogleUrls_index = 0
        first_result = int(input("Please Enter how many Page Result You Want Per Keyword: "))
        for i in range(1,Number_of_Scripts_to_run_parallel+1):
            temp_file_path = temp_file.replace('XXX', str(i))

            GoogleUrls_index +=1

            start_idx = int(len(Batches) * (i-1)/Number_of_Scripts_to_run_parallel)
            end_idx = int(len(Batches) * (i)/Number_of_Scripts_to_run_parallel)
            
            start_google = GoogleUrls_index*GoogleUrls_Count % len(GoogleUrls)
            end_google = (GoogleUrls_index+1)*GoogleUrls_Count % len(GoogleUrls)
            
            GoogleUrlsTemp = []
            
            GoogleUrlsTemp = GoogleUrls[start_google:end_google]

            # change google index 
            if end_google >= 190:
                GoogleUrls_index = 0
                
            Query_Url = []
            
            for idx,j in enumerate(Batches[start_idx:end_idx]):
                LL = (idx-1) % len(GoogleUrlsTemp)
                # Query_Url.append("https://www" + GoogleUrlsTemp[LL] + "/search?q=" + ("+OR+".join(j)))
                aa_query = ("https://www" + GoogleUrlsTemp[LL] + "/search?q=" + ("+OR+".join(j)))
                for i in range(first_result):
                    page_query = aa_query + f"&start={str(i)}0&gl=us" 
                    Query_Url.append(page_query)

            with open(temp_file_path, 'w',encoding='utf-8') as f:            
                f.writelines(i+"\n" for i in Query_Url)
            
            print(" Created '%s' file with '%s' queries..." % (temp_file_path, (end_idx - start_idx)))
    else:
        print("9a. Updating Temporary Query Files..")
        temp_file = temp_folder + Path_Slash + "Temp_" + current_time + "_XXX" + ".csv"
        entriesa = os.listdir(temp_folder)
        entries = os.listdir(output_folder)

        sub_output =entries[-1]

        sub_outfiles = os.listdir(output_folder+Path_Slash+sub_output)
        print(sub_outfiles[-1])

        lista =[]
        part = 0
        for aa in sub_outfiles:
            if aa.startswith('key_to_url'):
                if os.stat(output_folder+Path_Slash+sub_output+Path_Slash+aa).st_size !=0:
                    # output_folder+Path_Slash+sub_output+Path_Slash+aa
                    dataseta = pd.read_csv(output_folder+Path_Slash+sub_output+Path_Slash+aa)
                    # output_folder+Path_Slash+sub_output+Path_Slash+aa
                    count_row = pd.DataFrame(dataseta)
                    cc =  count_row.shape[0]
                    lista.append(cc)
                else:
                    print("OutFile is Empty")
                    lista.append(0)    

        #temp file here -----------------------

        print(lista)
        j = -1
        for bb in entriesa:
            part+=1
            j +=1
            nn = lista[j]
            dataset = pd.read_csv(temp_folder+Path_Slash+bb)
            dfa = pd.DataFrame(dataset)
            dfa.drop(dfa.index[1:nn], inplace=True)
            os.remove(temp_folder+Path_Slash+bb)
            dfa.to_csv(temp_folder+Path_Slash+bb,index=False)
            print("file upload")


    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    if not os.path.exists(output_sub_folder):
        os.mkdir(output_sub_folder)

    ###### Creating Sub process ######
    print("10. Creating Sub process...")
    pool = ThreadPool(multiprocessing.cpu_count())
    results = []
    for i in range(1,(Number_of_Scripts_to_run_parallel+1)):
        
        FEED_URI = "file:///%s" % (output_file_path.replace('XXX', str(i)))
        if a==True:
            temp=temp_file.replace('XXX', str(i))
        else:
            temp=temp_folder+Path_Slash+entriesa[i-1]
        
        attrib_arguments = " -a input_query_filepath='%s'" % temp
        attrib_arguments += " -s FEED_URI='%s'" % FEED_URI
        attrib_arguments += " -s LOG_FILE='%s'" % log_file_path.replace('XXX', str(i))

        print("Process %s command - %s" % (str(i), ("scrapy runspider '" + ScriptPath + Path_Slash + "Key_Child.py'" + attrib_arguments)))        
        
        #results.append(pool.apply_async(call_proc, ("scrapy runspider 'C:\\Users\\Jackie\\.virtualenvs\\BeautifulSoup_Project\\Proj4\\S4_v2_Child.py'" + attrib_arguments,)))
        results.append(pool.apply_async(call_proc, ("scrapy runspider '" + ScriptPath + Path_Slash + "Key_Child.py'" + attrib_arguments,)))

    # Close the pool and wait for each running task to complete
    pool.close()
    pool.join()
    for result in results:
        out, err = result.get()
        print("out: {} err: {}".format(out, err))
    
    # Summarising results k
    print("11. Summarising results at - %s" % output_summary_file_path)
    print(result_folder)
    Merge_results(output_sub_folder, output_summary_file_path, result_folder,sub_result_f,Path_Slash)

    print("The End")
    # temp_folder = BOOTSTRAP_temp_folder

    # entriesa = os.listdir(temp_folder)

    # for tt in entriesa:
    #     datasetaa = pd.read_csv(temp_folder+Path_Slash+tt)
    #     count_row = pd.DataFrame(datasetaa)
    #     ccc =  count_row.shape[0]
    #     if ccc < 3:
    #         with open(FlagFile_Path,'w') as files:
    #             files.write("True")
    #         print("Complete Namecheap File please change your file")    
    #     else:
    #         with open(FlagFile_Path,'w') as files:
    #             files.write("True")

    #fuct_for_reboot()
        
