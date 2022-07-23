t import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# from PyWhatsapp import send_unsaved_contact_message

try:
    import autoit
except ModuleNotFoundError:
    pass
import time
import datetime
import os
import argparse
import platform

s=Service(r"C:\Users\Rahul\Desktop\ffff\chromedriver_win32\chromedriver.exe")
driver="undefined"
message=None
wait=None
flag=None
doc_filename=None
docChoice=None
x=None

#This function basically takes the input message from the user and stores the mssg in the list
def input_message():
    # Declaring the global variables that we use in this function
    global message
    print(
        "Enter the message and use the symbol '~' to end the message:\nFor example: Hi, this is a test message~\n\nYour message: ")
    message = []
    done = False

    while not done:
        temp = input()
        if len(temp) != 0 and temp[-1] == "~":
            done = True
            message.append(temp[:-1])
        else:
            message.append(temp)
    message = "\n".join(message)
    print(message)

# This function basically sends the mssg that was previously stored in the "message" list to the specified contact
def send_message(target):
    global message, wait, driver,flag
    try:
        x_arg = '//span[contains(@title,' + target + ')]'  
        ct = 0
        while ct != 5:
            try:
                group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                group_title.click()
                break
            except Exception as e:
                print("Retry Send Message Exception", e)
                ct += 1
                time.sleep(3)
        
        # Finding the input message box by using the following X-PATH
        input_box=driver.find_element(by=By.XPATH, value="//*[@title='Type a message']")

        for ch in message:
            if ch == "\n":
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                    Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfully")
        time.sleep(1)
        flag=True
    except NoSuchElementException as e:
        flag=True
        print("send message exception: ", e)
    return schedule.CancelJob

# This function basically sends the mssg that was previously stored in the "message" list to the specified contact number
def send_unsaved_contact_message(i):
    global message,flag
    # Opening chat of the unsaved contact number using the below mentioned link in the chrome browser
    try:
        link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(i)
        driver.get(link)
    except:
        print("Unable to find the number,please check and retry\n")
    time.sleep(10)
    try:
        alert_obj = driver.switch_to.alert
        time.sleep(2)
        alert_obj.accept() 
        time.sleep(5)
    except:
        print("No alert message")
    print("Sending message to", i)
    try:
        time.sleep(10)
        driver.implicitly_wait(10)

        # Finding the input message box by using the following X-PATH
        input_box=driver.find_element(by=By.XPATH, value="//*[@title='Type a message']")
        for ch in message:
            if ch == "\n":
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                    Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfully")
        flag=True
    except Exception as e:
        print("Failed to send message exception: ", e)
        flag=True
    return schedule.CancelJob

#This function basically deals to schedule a mssg,to wait till the scheduled function is completed
def scheduler():
    global flag
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
            if(flag):
                 return
        except:
            return 

# This function basically used to send an attachment along with a given message to saved/unsaved contact number
def send_attachment(target):
    global x,message,flag

    # If our choice is to send to saved contact number
    if(x==1):
        try:
            x_arg = '//span[contains(@title,' + target + ')]'  
            ct = 0
            while ct != 5:
                try:
                    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                    group_title.click()
                    break
                except Exception as e:
                    print("Retry Send Message Exception", e)
                    ct += 1
                    time.sleep(3)
        except:
            print("Unable to detect the target")

    # If our choice is to send to unsaved contact number    
    elif(x==2):
        link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(target)
        driver.get(link)
        time.sleep(10)
        try:
            alert_obj = driver.switch_to.alert
            time.sleep(2)
            alert_obj.accept() 
            time.sleep(5)
        except:
            print("No alert message")
        print("Sending message to", target)
    time.sleep(10)
    try:
        # Searching and clicking the clip button by using the below mentioned X-PATH
        clipButton = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span')
        clipButton.click()
    except:
        traceback.print_exc()
    time.sleep(1)

    try:
        # Searching and clicking the media button by using the below mentioned X-PATH
        mediaButton = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/span')
        mediaButton.click()
    except:
        traceback.print_exc()
    time.sleep(3)
    hour = datetime.datetime.now().hour

    # After 5am and before 11am scheduled this
    if (hour >= 5 and hour <= 11):
        image_path = os.getcwd() + "\\Media\\" + 'goodmorning.jpg'

    # After 9pm and before 11pm schedule this
    elif (hour >= 21 and hour <= 23):
        image_path = os.getcwd() + "\\Media\\" + 'goodnight.jpg'

    # At any other time schedule this
    else:  
        image_path = os.getcwd() + "\\Media\\" + 'howareyou.jpg'

    # once file explorer opens,We use the below lines to search for the given file path and open the given file into the whatsapp
    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", image_path)
    autoit.control_click("Open", "Button1")

    time.sleep(3)
    try:
        # print("Send the caption for the attachment")
        # Finding the input element by using the following X-PATH
        input_element=driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                    Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_element.send_keys(ch)
        input_element.send_keys(Keys.ENTER)
        print("Message sent successfully\n")
        time.sleep(1)
        flag=True
    except:
        flag=True
        print("Error")
    
    print("Attachment sent successfully\n")

# The below function is used to log out from the whatsapp 
def log_out():
    # try:
    # /html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/div/span
    # /html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[4]/div[1]
    driver.find_element(by=By.XPATH,value="/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/div").click()
    time.sleep(5)
    driver.find_element(by=By.XPATH,value="/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[3]/span/div/ul/li[4]/div[1]").click()
    # except:
    #     print("Unable to log out from the whatsapp\n") 

# This function typically used to send the files 
def send_files():
    global doc_filename
    try:
        clipButton = driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span')
        clipButton.click()
    except:
        print("Unable to find the clipbutton\n")
    time.sleep(1)

    # To send a Document(PDF, Word file, PPT)
    if doc_filename.split('.')[1]=='pdf'or doc_filename.split('.')[1]=='docx'or doc_filename.split('.')[1]=='pptx' :
        try:
            docButton = driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[4]/button')
            docButton.click()
        except:
            traceback.print_exc()

    # This makes sure that gifs, images can be imported through documents folder and they display
    # properly in whatsapp web.
    else:
        try: 
            docButton = driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button')
            docButton.click()
        except:
            traceback.print_exc()
    time.sleep(1)
    docPath = os.getcwd() + "\\Documents\\" + doc_filename
    try:
        autoit.control_focus("Open", "Edit1")
    except :
        traceback.print_exc()
    autoit.control_set_text("Open", "Edit1", docPath)
    autoit.control_click("Open", "Button1")

    time.sleep(3)

    # Finding and clicking the whatsapp send button by using the below xpath
    try:
        whatsapp_send_button = driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div')
        whatsapp_send_button.click()
    except:
        print("Unable to find the whatsapp send button\n")
    print('File sent successfully\n')

if __name__ == "__main__":
    while True:

        # Create two lists to store the saved and unsaved contact details
        Contact=[]
        unsaved_Contacts=[]

        # Enter your choice 1 or 2 or 3
        print("PLEASE CHOOSE ONE OF THE OPTIONS:\n")
        print("1.Message to Saved Contact number\n")
        print("2.Message to Unsaved Contact number\n")
        print("3.Quit the program\n")

        x = int(input("Enter your choice(1 or 2 or 3):"))
        print()

        if(x==1 or x==2):
            print("Do you want to schedule your message(YES/NO):\n")
            sc=input()
            k=input("Do you want to send ATTACHMENTS(YES/NO)\n")
            docChoice = input("Would you file to send a Document file(YES/NO): \n")
            if (docChoice == "YES"):
                # Note the document file should be present in the Document Folder
                doc_filename = input("Enter the Document file name you want to send: ")
        
        # storing saved contacts in contact list
        if x == 1:
            n = int(input('Enter number of Contacts to add(count)->'))
            print()
            for i in range(0, n):
                inp = str(input("Enter contact name(text)->"))
                inp = '"' + inp + '"'
                Contact.append(inp)

        # storing unsaved contacts in unsaved contact list
        elif x == 2:
            n = int(input('Enter number of unsaved Contacts to add(count)->'))
            print()
            for i in range(0, n):
                # Example use: 919899123456, Don't use: +919899123456
                # Reference : https://faq.whatsapp.com/en/android/26000030/
                inp = str(input(
                    "Enter unsaved contact number with country code(interger):\n\nValid input: 91943xxxxx12\nInvalid input: +91943xxxxx12\n\n"))
                # print (inp)
                unsaved_Contacts.append(inp)

        # Signing out of whatsapp and closing the browser
        else:
            log_out()
            driver.close()
            print("Logged out successfully\n")
            break

        if(driver=="undefined"):
            # To open whatsapp via chrome browser
            driver=webdriver.Chrome(service=s)
            driver.get("https://web.whatsapp.com/")
            driver.maximize_window()

            # Waiting till we idenify the QR code in the chrome browser
            try: