#!/usr/bin/env python3
import requests
import datetime
import json
from prettytable import PrettyTable
import schedule
import time
from playsound import playsound
from notifypy import Notify

wavFile = "./1.wav"
def sendmessage(message1, current_time):
    notification = Notify()
    notification.title = message1
    notification.message = current_time
    playsound(wavFile)
    #notification.audio = wavFile
    notification.send()
    return



#table properties
x = PrettyTable()
x.field_names = ["Pincode", "Date", "Name", "Vaccine", "Age", "Fee", "Available"]

post_str = ["560001"]
age = 50
print_flag = 'Y'

base = datetime.datetime.today()
header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
date_str = ["23-05-2021"]

#print(date_str)
def job():
    prev_post = ""
    count = 0
    hold = ""
    x.clear_rows()
    for POST_CODE in post_str:
        #print(POST_CODE)
        curr_post = POST_CODE
        for INP_DATE in date_str:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(POST_CODE, INP_DATE)
            response = requests.get(URL, headers=header)
            #print(response)
            if response.ok:
                resp_json = response.json()
                #print(json.dumps(resp_json, indent = 1))
                flag = False
                if resp_json["centers"]:
                    #print("Available on: {}".format(INP_DATE))
                    if(print_flag=='y' or print_flag=='Y'):
                        for center in resp_json["centers"]:
                            for session in center["sessions"]:
                                if session["min_age_limit"] <= age:
                                    if session["available_capacity"] > 0:
                                        count += 1
                                        #populate rows of table:x
                                        l = []
                                        if(prev_post=="" or prev_post!=curr_post):
                                            l.append(POST_CODE)
                                            prev_post = curr_post
                                            hold+=POST_CODE+" , "
                                        else:
                                            l.append("")
                                        l.append(session["date"])
                                        str1 = center["name"] + " " + center["block_name"]
                                        l.append(str1)
                                        if(session["vaccine"] != ''):
                                            l.append(session["vaccine"])
                                        else:
                                            l.append("---")
                                        l.append(session["min_age_limit"])
                                        l.append(center["fee_type"])
                                        l.append(session["available_capacity"])

                                        x.add_row(l)
                else:
                    """print("No available slots on {}".format(INP_DATE))"""
    now = datetime.datetime.now()
    now = now.strftime("%H:%M:%S")
    if(count == 0):
        print("{}--{}  API:{}".format("No free slots", now, len(post_str)*len(date_str)))
    else:
        f = open("out.txt", "a")
        print(x)
        print("{}--{}  API:{}".format("Found free slots", now, len(post_str)*len(date_str)))
        print(x, file=f)
        print("{}--{}  API:{}".format("Found free slots", now, len(post_str)*len(date_str)), file=f)
        f.close()

    if(count > 0):
        mess = "FOUND vaccine : " + now
        sendmessage(mess, hold)

if __name__ == "__main__":
    print("Running .........")
    schedule.every().minute.at(":00").do(job)
    schedule.every().minute.at(":30").do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)
