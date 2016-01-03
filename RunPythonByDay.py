# -*- coding: utf-8 -*-
__author__="pengzhen3"

from BorrowBooks import send_rule
from datetime import datetime,timedelta
import configparser
import time


def doSendRule():
    bSendMail = False
    while not bSendMail :
        if send_rule():
            bSendMail = True
        time.sleep(3600)

    config=configparser.ConfigParser()
    config.read("BookConfig.ini")
    date_now = datetime.now()
    strTimenow = now.strftime('%Y-%m-%d %H:%M:%S')
    config.set("LastSendDate","send_date",strTimenow)


def RunEveryDay():

    strTimeold = ""
    config=configparser.ConfigParser()
    config.read("BookConfig.ini")

    while(True):
        if not config.has_section("LastSendDate"):
            doSendRule()

        else:
            strTimeold = config.get("LastSendDate","send_date")
            date_timeold = datetime.strptime(strTimeold, '%Y-%m-%d')
            temp_delta = date_now - date_timeold

            if temp_delta > 1:
                doSendRule()
        time.sleep(3600)

if __name__ == '__main__':
    RunEveryDay()




