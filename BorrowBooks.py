#Borrow Books

# -*- coding: utf-8 -*-
__author__="pengzhen3"

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from datetime import datetime,timedelta
import smtplib
import configparser
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='BorrowBooks.log',
                filemode='w')

class BookInfo(object):
    def __init__(self,book_name,borrow_date):
        self.__book_name = book_name
        self.__borrow_date = borrow_date
    
    def get_name(self):
        return self.__book_name
        
    def get_date(self):
        return self.__borrow_date
    

config=configparser.ConfigParser()
#读取配置文件
config.read("BookConfig.ini")

mail_to = config.get("EmailConfig","mail_to")
mail_host = config.get("EmailConfig","mail_host")
mail_user = config.get("EmailConfig","mail_user")
mail_pass = config.get("EmailConfig","mail_pass")

#mail_postfix="hikvision.com.cn"  #发件箱的后缀
mailto_list=mail_to.split(",")
keep_time = config.get("GeneralConfig","keep_time")

#后缀名
mail_suffix = mail_host[mail_host.find(".")+1:]

book_info_list=[]

#读取图书信息,
for x in range(10000):
    sectionname = "BookBorrow"+str(x)
    if not config.has_section(sectionname):
        break
    else:
        #temp_name = config.get(sectionname,"book_name")
        #temp_data = config.get(sectionname,"borrow_date")
        temp_info = BookInfo(config.get(sectionname,"book_name"),\
            config.get(sectionname,"borrow_date"))
        book_info_list.append(temp_info)
        

def send_mail(to_list,sub,content):  
    me ="From:"+"<"+mail_user+"@"+mail_suffix+">"
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()  
        server.set_debuglevel(1)
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.quit()  
        return True  
    except Exception as e:  
        print("Exception:",e)  
        return False
        
def send_rule():
    if len(mailto_list) == 0:
        logging.error('receiver email address is empty!!!')
        return False   
    if len(book_info_list) == 0:
        logging.error('book info is empty')
        return False
    
    bRet = True
    
    #判断是否超期
    for book_info in book_info_list:
        temp_date = datetime.strptime(book_info.get_date(), '%Y-%m-%d')+timedelta(days=int(keep_time))
        temp_delta = temp_date-datetime.now() 
        temp_days = getattr(temp_delta,'days')
        if temp_days >=3:
            continue
        elif temp_days>0 and temp_days<3:
            content = "你好，"+mail_user+"你的图书【"+book_info.get_name()+\
                "】将于"+str(temp_days)+"天后到期！！！\n"+"借书日期："+book_info.get_date()
        elif temp_days==0:
            content = "你好，"+mail_user+"你的图书【"+book_info.get_name()+\
                "】将于今天到期！！！\n 借书日期："+book_info.get_date() 
        else:
            content = "你好，"+mail_user+"你的图书【"+book_info.get_name()+\
                "】已超期"+str(temp_days*(-1)) +"天！！！\n 借书日期："+book_info.get_date()
        
        if not send_mail(mailto_list,"【借书提醒】",content):
            logging.error('send_mail fail ')
            bRet = False
  
    return bRet

if __name__ == '__main__':  
    if send_rule():  
        print("执行成功")  
    else:  
        print("执行失败")
