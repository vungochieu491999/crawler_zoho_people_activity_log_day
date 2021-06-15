import time
import os
import codecs
from datetime import date
from selenium import webdriver
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Class Log execute write log
class Log:

    # Calling Constructor
    def __init__(self, file_name, logs):
        self.file_name = file_name
        self.logs = logs

    def info(self):
        #open the file for write operation
        file = codecs.open(ROOT_DIR + '/crawler_zoho_people/zoho_activity_logs/' + self.file_name, "a", "utf-8")
        for row in self.logs:                 
            file.write(row.find_element_by_class_name('tline').text + " : " + row.find_element_by_tag_name('div').text + "\n")
        file.close()
            
            

# Class ZohoPeople execute with zoho people
class ZohoPeople:
      
    # Calling Constructor 
    def __init__(self, link_sign_in, link_activity, login_id, password):
        self.login_id = login_id
        self.password = password
        self.link_sign_in = link_sign_in
        self.link_activity = link_activity
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\hieuvn\Downloads\chromedriver.exe")
         
    # Function get all log active by today
    def get_zoho_log_activity(self):
        self.driver.get(self.link_sign_in)

        self.driver.find_element_by_xpath('//*[@id="login_id"]').send_keys(self.login_id)
        self.driver.find_element_by_xpath('//*[@id="nextbtn"]').click()

        time.sleep(2)

        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="nextbtn"]').click()

        time.sleep(1)
        self.driver.get(self.link_activity)

        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="ZPaclog_filter_date_options"]/select/option[4]').click()

        self.driver.find_element_by_xpath('//*[@id="ZPActLogsearch"]').click()
        time.sleep(3)

        log_details   = self.driver.find_elements_by_class_name('event')

        page = 1
        limit = 24
        while True:
            log_details   = self.driver.find_elements_by_class_name('event')
            if len(log_details) < page * limit:
                break

            for index in range(len(log_details)):
                if index < limit:
                    self.driver.execute_script("arguments[0].scrollIntoView();", log_details[index]);
                elif index - page * limit  < limit and index - page * limit > 0 or index < limit:

                    self.driver.execute_script("arguments[0].scrollIntoView();", log_details[index]);
            page = page + 1
            time.sleep(3)

        return log_details

    def close(self):
        self.driver.close()

def main():

    link_sign_in  ="https://accounts.zoho.com/signin?servicename=zohopeople&signupurl=https://www.zoho.com/people/signup.html"
    sub_domain    = "******"
    link_activity ="https://people.zoho.com/" + sub_domain + "/zp#admin/dataadministration/activityLog"

    login_id = "******@smartosc.com"
    password = "password"

    file_name    = 'zh-activity-logs-'+ str(date.today()) +'.log'

    zh_people    = ZohoPeople(link_sign_in, link_activity, login_id, password)

    logs         = zh_people.get_zoho_log_activity()

    log          = Log(file_name, logs)

    log.info()

    zh_people.close()
    
main()