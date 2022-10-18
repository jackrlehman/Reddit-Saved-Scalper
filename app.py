from concurrent.futures import thread
from operator import truediv
import threading
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException     
import urllib
import datetime
import os
import threading

class Wait:
    def wait_to_be_clickable_and_click(elementTag : str, elementType: By, waitType: int):
        WebDriverWait(driver, waitType).until(EC.element_to_be_clickable((elementType, elementTag)))
        driver.find_element(elementType, elementTag).click()

    def wait_to_be_clickable_and_send_keys(keys : str, elementTag : str, elementType: By, waitType: int):
        WebDriverWait(driver, waitType).until(EC.element_to_be_clickable((elementType, elementTag)))
        driver.find_element(elementType, elementTag).send_keys(keys)

    def wait_to_check_presence_and_click(elementTag : str, elementType: By, waitType: int):
        try:
            WebDriverWait(driver, waitType).until(EC.presence_of_element_located((elementType, elementTag)))
            driver.find_element(elementType, elementTag).click()
        except Exception:
            return False
        return True

    def check_exists_and_click(elementTag : str, elementType: By):
        try:
            driver.find_element(elementType, elementTag).click()
        except Exception:
            return False
        return True

    def check_exists(elementTag : str, elementType: By):
        try:
            driver.find_element(elementType, elementTag)
        except Exception:
            return False
        return True

class Login:
    __XPATH_loginPopupBtn = "/html/body/div[1]/div/div[2]/div[1]/header/div/div[2]/div/div[1]/a[1]"
    __XPATH_loginFormIframe = "/html/body/div[1]/div/div[2]/div[3]/div/div/iframe"
    __ID_usernameField = "loginUsername"
    __ID_passwordField = "loginPassword"
    __XPATH_loginFormBtn = "/html/body/div/main/div[1]/div/div/form/fieldset[4]/button"
    __XPATH_loginConfirmation = "/html/body/div[1]/div/div[2]/div[3]/div/div/div[1]"
    __expectedLoginConfirmationString = "logged in"
    __XPATH_interestsPopupCloseBtn = "/html/body/div[1]/div/div[2]/div[4]/div/div/div/header/div/div[2]/button/i"

    def __init__(self, username : str, password : str):
        self.username = username
        self.password = password

    def perform_login(self):
        try:
            Wait.wait_to_be_clickable_and_click(self.__XPATH_loginPopupBtn, By.XPATH, shortWait)
            WebDriverWait(driver, shortWait).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, self.__XPATH_loginFormIframe)))
            Wait.wait_to_be_clickable_and_send_keys(self.username, self.__ID_usernameField, By.ID, shortWait)
            Wait.wait_to_be_clickable_and_send_keys(self.password, self.__ID_passwordField, By.ID, shortWait)
            Wait.wait_to_be_clickable_and_click(self.__XPATH_loginFormBtn, By.XPATH, shortWait)
            WebDriverWait(driver, mediumWait).until(EC.text_to_be_present_in_element((By.XPATH, self.__XPATH_loginConfirmation), self.__expectedLoginConfirmationString))  
            Wait.wait_to_check_presence_and_click(self.__XPATH_interestsPopupCloseBtn,By.XPATH,mediumWait) #Reddit "interests" popup          
            driver.get('https://www.reddit.com/user/{0}/saved/'.format(self.username))
            print("Login Successful")
        except Exception:
            print("Login Failed")
            raise Exception("Login Failed")

class Reload:
    def reload_to_saved(self):
        driver.get('https://www.reddit.com/user/{0}/saved/'.format(self.username))
        print("Reload Successful")
        Saved(unsavePostAfterDownload).begin()

class Saved:
    __XPATH_tableItem = "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[{0}]"
    __XPATH_postContent = "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[{0}]/div/a"
    __XPATH_postContentAlt1 = "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[5]/div[3]/div[1]/div/a"
    __XPATH_postContentAlt2 = "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[5]/div[3]/div[1]/div/a"
    __XPATH_postContentAlt3 = "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[5]/div/a"
    __postContentStandardValue = 5
    __XPATH_postContentArray = "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[5]/div[1]/div/div[1]/ul/li[{0}]/figure/a"
    __XPATH_postContentArrayAlt = "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[5]/div[3]/div/div[1]/div/div[1]/ul/li[{0}]/figure/a"
    __postContentArrayStandardValue = 1
    __XPATH_delUser1 = "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[{0}]/div/div/div[2]/div/div[2]/div[2]/div[2]/span[2]"
    __XPATH_delUser2 = "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[{0}]/div/div/div/div/div[2]/div/div[2]/div[2]/div[2]/span[2]"
    __XPATH_unsaveBtn = "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[{0}]/div/div/div[2]/div/div[2]/div[3]/div[3]/div[3]/button"  
    __XPATH_unsaveBtnAlt1 = "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[{0}]/div/div/div/div/div[2]/div/div[2]/div[3]/div[3]/div[3]/button"                            
    __XPATH_unsaveBtnAlt2 = "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[{0}]/div/div/div/div/div[2]/div/div[2]/div[3]/div[3]/div[2]/button"
    __XPATH_unsaveBtnAlt3 = "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[{0}]/div/div/div[2]/div/div[2]/div[3]/div[3]/div[2]/button"
    __XPATH_postContentCloseBtn = "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[1]/div/div[2]/button"
    __iterator = 0
    __path = ""
    __downloadCnt = 0
    def __init__(self, unsaveAfterDownload):
        self.unsaveAfterDownload = unsaveAfterDownload

    def begin(self):
        self.__path = os.getcwd() + "\Reddit Media\\" 
        print("Download folder location: " + self.__path)
        if(os.path.exists(self.__path) == False):
            os.mkdir(self.__path) #Create folder
        self.find_media()
    
    def find_media(self):  
        done = False
        exceptionOccured = False
        reAttemptedAtIterator = 0
        while(done == False):
            try:
                exceptionOccured = False
                if(Wait.wait_to_check_presence_and_click(self.__XPATH_tableItem.format(self.__iterator + 1),By.XPATH,longWait)) == True:                    
                    self.__iterator += 1
                    src = "";  
                    i = 0; j = 0; 
                    contentFound = False; possibleContentArray = False #Content arrays are reddit media posts with multiple media per post              
                    while(contentFound == False): #Sort through possible locations of href to image
                        try:
                            if(possibleContentArray == True):
                                try:
                                    src = driver.find_element(By.XPATH, self.__XPATH_postContentArray.format(self.__postContentArrayStandardValue + j)).get_attribute('href')
                                except:
                                    src = driver.find_element(By.XPATH, self.__XPATH_postContentArrayAlt.format(self.__postContentArrayStandardValue + j)).get_attribute('href')
                                if(".gif" in src):
                                    print("Unsupported Filetype: .gif")
                                    raise Exception("Unsupported Filetype.")
                                self.download_media_setup(src)
                                j += 1
                            else:
                                try:
                                    src = driver.find_element(By.XPATH, self.__XPATH_postContent.format(self.__postContentStandardValue + i)).get_attribute('href')
                                except:
                                    try:
                                        src = driver.find_element(By.XPATH, self.__XPATH_postContentAlt1).get_attribute('href')
                                    except:
                                        try:
                                            src = driver.find_element(By.XPATH, self.__XPATH_postContentAlt2).get_attribute('href')
                                        except:
                                            src = driver.find_element(By.XPATH, self.__XPATH_postContentAlt3).get_attribute('href')
                                if('flair' in src): #Flair was percieved to be content source, keep looking.
                                    i += 1
                                    if(i > 20): #If webpage loads inproperly...
                                        raise Exception("Element could not be located due to a most likely broken page") 
                                    continue
                                if(".gif" in src):
                                    print("Unsupported Filetype: .gif")
                                    raise Exception("Unsupported Filetype.")
                                self.download_media_setup(src)
                                contentFound = True
                        except NoSuchElementException:
                            if(possibleContentArray == True and j != 0):
                                contentFound = True
                            elif(possibleContentArray == False):
                                i += 1 
                                if(i > 10): 
                                    possibleContentArray = True
                            else:
                                raise Exception("Content not found")
                else:
                    
                    if(reAttemptedAtIterator + 3 > self.__iterator and reAttemptedAtIterator != 0): #There has been a recent reattempt, and it has failed. Exit.
                        print("End of Saved table reached")
                        done = True
                    else: #Reattempt the latest attempt
                        reAttemptedAtIterator = self.__iterator
                        print("End of table may have been reached at grid record #" + str(self.__iterator)+".")
                    
            except Exception:
                exceptionOccured = True
                print("Unsupported media at grid record #" + str(self.__iterator) +". Skipping record")   
            finally:
                self.exit_found_media(exceptionOccured)

    def exit_found_media(self, exceptionOccured):
        Wait.wait_to_check_presence_and_click(self.__XPATH_postContentCloseBtn,By.XPATH,longWait) # Check if content close button can be found, and if so, click it.
        if(self.unsaveAfterDownload):
            if(self.__iterator != 1):
                # If a dialog popup is on screen, a secondary click is required. Only time dialog would be present is to say post unsaved. Since we have 4 possible buttons we click, we check 4 times.
                Wait.check_exists_and_click(self.__XPATH_postContentCloseBtn,By.XPATH) 
                Wait.check_exists_and_click(self.__XPATH_postContentCloseBtn,By.XPATH) 
                Wait.check_exists_and_click(self.__XPATH_postContentCloseBtn,By.XPATH) 
                Wait.check_exists_and_click(self.__XPATH_postContentCloseBtn,By.XPATH) 
            if(not exceptionOccured):
                resolved = False
                if(Wait.check_exists(self.__XPATH_delUser1.format(self.__iterator), By.XPATH)): #Deleted users have UI elements shifted
                    if("u/[deleted]" in (driver.find_element(By.XPATH,self.__XPATH_delUser1.format(self.__iterator)).text)):
                        Wait.check_exists_and_click(self.__XPATH_unsaveBtnAlt3.format(self.__iterator),By.XPATH)
                        resolved = True
                elif(Wait.check_exists(self.__XPATH_delUser2.format(self.__iterator), By.XPATH)): #Deleted users have UI elements shifted
                    if("u/[deleted]" in (driver.find_element(By.XPATH,self.__XPATH_delUser2.format(self.__iterator)).text)):
                        Wait.check_exists_and_click(self.__XPATH_unsaveBtnAlt2.format(self.__iterator),By.XPATH)
                        resolved = True
                if(not resolved): #It can be anyone of these as they can also represent seperate buttons than unsave, so might as well just click them all.
                    Wait.check_exists_and_click(self.__XPATH_unsaveBtn.format(self.__iterator),By.XPATH)
                    Wait.check_exists_and_click(self.__XPATH_unsaveBtnAlt1.format(self.__iterator),By.XPATH)
                    Wait.check_exists_and_click(self.__XPATH_unsaveBtnAlt2.format(self.__iterator),By.XPATH)
                    Wait.check_exists_and_click(self.__XPATH_unsaveBtnAlt3.format(self.__iterator),By.XPATH)
                print("Downloaded all media from grid record #" + str(self.__iterator))   
 

    def download_media_setup(self, src):
        self.__downloadCnt += 1
        threading.Thread(target=self.download_media, args=(src, self.__downloadCnt,)).start()

    def download_media(self, src : str, cnt: int):
        fileName = datetime.datetime.now().strftime('%m-%d-%Y %H-%M-%S-%f')[:-3] + ' ' + str(cnt) + '.' + src.split('.')[-1].split('?')[0]  
        urllib.request.urlretrieve(src, self.__path + fileName)
        if(cnt % 10 == 0):
            print("Total items downloaded: {0}".format(cnt))

shortWait = 5; mediumWait = 10; longWait = 15

#TODO Apple and Google login. Headless option, ability to exit and close webdriver on exit
print("Welcome to Reddit Saved Scalper by jackrlehman. Last updated: 10/18/2022. The scalper will download all images from your reddit saved page. Please ensure you have Google Chrome installed on this device and do not interfere with the newly opened Chrome application.")
try:
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1}) # Pass the argument 1 to allow and 2 to block
    driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
    try:
        username = input("Enter Reddit Username: ")
        password = input("Enter Reddit Password: ")
        unsavePostAfterDownload = True

        isComplete = False
        while not isComplete:
            a = input("Would you like to unsave the post after download? (y/n): ")
            a = a.lower().strip()
            if(a == "y"):
                unsavePostAfterDownload = True
                isComplete = True
            elif (a == "n"):
                unsavePostAfterDownload = False
                isComplete = True
            else:
                print(a + " is not a valid input.")
        
        print("Process started. You will find a folder called 'Reddit Media' containing the downloaded contents in your base directory.")

        driver.get('https://www.reddit.com/')
        Login(username,password).perform_login()
        Saved(unsavePostAfterDownload).begin()
        print("All items downloaded")   
    except:
        print("An unresolvable issue occured. Application shutting down.")
    
    driver.close()

except:
    print("There was an issue regarding Google Chrome. Please ensure you have Google Chrome installed on this device.")


