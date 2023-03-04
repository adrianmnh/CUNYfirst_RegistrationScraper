"""Created by Adrian Miguel Noa, please don't sue me"""
# pip install selenium

import time
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def printScreen(*s):
    print("\33[2J")
    print("\033[%d;%dH" % (0, 0))
    string=format("Course", ">20s") + format("Section", ">15s") + format("Enrolled", ">15s")+"\n"
    count=0
    while count<len(s):
        string+=f'{s[count]:>20d}' + f'{65:>15.1f}' + f'{s[count+1]:>15s}' + "\n"
        count+=2
    string+="\n\n"
    print(string)

def printWelcome():
    clear()
    print("\r\r\t\t____    __    ____  _______  __        ______   ______   .___  ___.  _______") 
    print("\t\t\   \  /  \  /   / |   ____||  |      /      | /  __  \  |   \/   | |   ____|") 
    print("\t\t \   \/    \/   /  |  |__   |  |     |  ,----'|  |  |  | |  \  /  | |  |__   ") 
    print("\t\t  \            /   |   __|  |  |     |  |     |  |  |  | |  |\/|  | |   __|  ") 
    print("\t\t   \    /\    /    |  |____ |  `----.|  `----.|  `--'  | |  |  |  | |  |____ ") 
    print("\t\t    \__/  \__/     |_______||_______| \______| \______/  |__|  |__| |_______|\n\t")
    msg("\tWelcome! You're minutes away from automating CUNYFirst course registration!")
    msg("\t\t\t\t\t\t\t\tWritten by Adrian Noa")
    time.sleep(10)
    clear()
    submitUserInfo()
    
def submitUserInfo():
    q=input("\tWill you enter your username and password(\"1\") or use a JSON key-file?(\"2\")? (1/2)\t")
##    q="2"
    clear()
    if q=="1":
        cred=typeInfo()
    elif q=="2":
        cred=loadJSON()
    else:
        done()
    msg(f'Please wait....\n\t', 2)
    clear()
    mode=chooseMode()
    courses=getCodes()
    main(mode, cred, courses)

def chooseMode():
    msg("Adding courses allows you to register for courses in your current cart")
    msg("Swapping courses allows you to swap a class you're currently enrolled with another in cart")
    q=input("\tChoose a mode: ADD(\"1\") or SWAP(\"1\") a class? (1/2)\t")
##    q="1"
    clear()
    if q=="1":
        return 'CART'
    elif q=="2":
        return 'SWAP'
    done()
    
    
def loadJSON():
    import json
    import os
    clear()
    msg("Please enter your CUNYFirst login credentials into keys.json file:")
    msg("File is located in current project folder\n")
    q=input("\tWhen done press Enter...")
##    q=""
    if q=='' or d=='':
        if os.path.exists('keys.json'):
            with open("keys.json") as file:
                keys=json.load(file)
                cred=keys["user"],keys["pword"],keys["userid"]
                return cred
        else:
            msg("The file \"keys.json\" does not exists...")
            time.sleep(3)
            msg("Moving to input credentials...")
            time.sleep(3)
            return typeInfo()
    else:
        print("\tInvalid input, exiting...")
        done()

def resetPointer():
    print("\033[%d;%dH" %(4,0))

def typeInfo():
    clear()
    user=ask("Please enter CUNYFirst login: ")
    clear()
    pword=ask("Please enter password: ")
    clear()
    userid=ask("Please enter 8-digit CUNY ID: ")
    clear()
    q=ask("Save to keys.json?: (Y/N)\t")
    clear()
    if q=='y' or q=='Y':
        out=open('keys.json','w')
        msg("Saving....")
        json="{\n\t\"user\":\""+user+"\",\n"+"\t\"pword\":\""+pword+"\",\n\t\"userid\":\""+userid+"\"\n}"
        print(json)
        time.sleep(7)
        out.write(json)
        out.close()
    cred=(user,pword,userid)
    return cred

def main(mode, cred, courses):
    
    PATH = "drivers/geckodriver.exe"
    ffox = Service(PATH)
    driv = webdriver.Firefox(service=ffox)

    #driver = webdriver.Chrome(service=service)
    ##driver.set_window_size(450, 650)
    #driver.get("https://home.cunyfirst.cuny.edu/")

    url='https://cssa.cunyfirst.cuny.edu/psc/cnycsprd/EMPLOYEE/CAMP/c/SA_LEARNER_SERVICES.SSR_SSENRL_'+mode+'.GBL?Page=SSR_SSENRL_'+mode+'&Action=A&ACAD_CAREER=UGRD&EMPLID='+cred[2]+'&ENRL_REQUEST_ID=&INSTITUTION=QNS01&STRM=1226'
    driv.get(url)
    ##driver.execute_script("document.body.style.zoom='50%'")

    username = driv.find_element(By.ID, "CUNYfirstUsernameH")
    username.clear()
    username.send_keys(cred[0])
    password = driv.find_element(By.ID, "CUNYfirstPassword").send_keys(cred[1])
    driv.find_element(By.XPATH, '//*[@id="submit"]').click()
    time.sleep(0)
##    if mode=='CART':
##        addClass(status, driver, url)

    tuples=[]
    tuples=getTuples(driv, courses)
##    for i in tuples:
##        msg(str(i))

    reloadUntilAvailable(driv,url,courses,tuples)

    done()

def getTuples(driv, courses):
    clear()
    msg("Courses to scrape for:")
    print("\t", end='')
    print(courses)
    print()
    try:
        table = WebDriverWait(driv,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ACE_$ICField257"]')))
        content = table.find_elements(By.CLASS_NAME, 'PSHYPERLINK')
    except:
        msg("Unable to log in with user credentials...")
        done()
        
    content=content[::2]
    for i in range(len(content)):
        content[i]=int(content[i].text.split()[2].strip("()"))
    msg("Courses in CART:")
    print("\t", end='')
    if len(content)==0:
        print("CUNYFirst cart is empty...")
        done()
    print(content)
    print()

    t=[]
    for i in range(len(courses)):
        for j in range(len(content)):
            if courses[i]==content[j]:
                a=(courses[i],i,j)
                t.append(a)

    msg("Cross-referenced desired courses that are currently in cart:")
    for i in t:
        print(f'\t[ CourseID: {i[0]} -- Entry# {i[1]} -- OnlineCARTindex: {i[2]} ]' , sep= ",", end="\n")
    msg("\n", 6)
    
    return t

def reloadUntilAvailable(driv, url, courses, tuples):
    from random import randint
    while len(tuples)>0:
##        reloadUntilOpen(driv, url, tuples)
        for i in range(len(tuples)):
            driv.get(url)
            s=f'//*[@id="win0divDERIVED_REGFRM1_SSR_STATUS_LONG${str(tuples[i][2])}"]/div/img'
            try:
                status=WebDriverWait(driv,10).until(EC.presence_of_element_located((By.XPATH, s)))
                imgsrc=status.get_attribute("src")
##            msg(f'{i} - {tuples[i]} : {imgsrc}')
                t=str(i)
            except:
                done()
            if "OPEN" in imgsrc:
                submit = WebDriverWait(driv,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="DERIVED_REGFRM1_LINK_ADD_ENRL$82$"]')))
                submit.click()
                time.sleep(1)
                submit = WebDriverWait(driv,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="DERIVED_REGFRM1_SSR_PB_SUBMIT"]')))
                submit.click()
                time.sleep(2)
                x2=f'//*[@id="win0divDERIVED_REGFRM1_SS_MESSAGE_LONG${t}"]/div'
                x2=WebDriverWait(driv,10).until(EC.presence_of_element_located((By.XPATH, x2))).text
                x1=f'//*[@id="win0divDERIVED_REGFRM1_SSR_STATUS_LONG${t}"]/div/img'
                x1=WebDriverWait(driv,10).until(EC.presence_of_element_located((By.XPATH, x1))).get_attribute("src")
##                print(x1)
##                print(x2)
                time.sleep(4)                ##x1 is the image source, x2 is the message
                if ("SUCCESS" in x1) and ("Success" in x2):
##                if "Message:" in x2:
                    printSuccess(str(tuples[i][0]))
                    driv.get(url)
                    clear()
                    msg("Checking if there are courses left to enroll in")
                    tuples=getTuples(driv, courses)
                    time.sleep(8)
                    continue

                else:
                    continue
        r=randint(1,15)
        delline(f'\t...Waiting {r} seconds to reload page...')
        time.sleep(r)        

def done():
    msg("Exiting program....\n\n",2)
    exit()
    
#printScreen(331,"YEEES", 381,"NOOO")
def ask(s):
    clear()
    query="\t"+s+"\t"
    q=input(query)
    return q

def getCodes():
    x=[]
    a=ask("How many courses do you want to enroll in?")
##    a=3
    if int(a)>0:
        for i in range(int(a)):
            x.append(reqCode())
        return x
    else:
        done()

def reqCode():
##    if i==0:
##        return 11112
##    if i==1:
##        return 46476
    a=ask("What is the 4,5-digit course ID?")
    b=ask(f'Is {a} the correct course ID? (Y/N)\t')
    if b=='y' or b=='Y' or b=="":
        try:
            a=int(a)
        except:
            done()
        msg(f'Adding {a} to list of courses...',2)
        return a
    else:
        reqCode()
##    return 46481

def msg(*a):
    print("\t"+a[0])
    if len(a)==2:
        time.sleep(a[1])

def delline(s):
    print("                                                           ", end='\r')
    print(s, end="\r")

def clear():
    import os
    print(os.name)
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    resetPointer()

def printSuccess(a):
    clear()
    msg(" _____ _   _ _____  _____  _____ _____ _____ _ ")
    msg("/  ___| | | /  __ \/  __ \|  ___/  ___/  ___| |")
    msg("\ `--.| | | | /  \/| /  \/| |__ \ `--.\ `--.| |")
    msg(" `--. \ | | | |    | |    |  __| `--. \`--. \ |")
    msg("/\__/ / |_| | \__/\| \__/\| |___/\__/ /\__/ /_|")
    msg("\____/ \___/ \____/ \____/\____/\____/\____/(_)\n")
    msg(f'SUCCESS! You\'re now enrolled on course id: {a}')
    time.sleep(10)


def driver():
    clear()
    printWelcome()

 # clear the screen
##print("\33[1A") # move the cursor up one line

##
if __name__ == "__main__":
    driver()
