# -*- coding: UTF-8 -*-

import os
import time
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global html
global strScanTime 
global strTodayDate 
global strYesterdayDate


def time_to_go():
    now = int(time.strftime("%H", time.localtime(time.time())))
    while(True):
        if now>1:
            time.sleep(600)
            now = int(time.strftime("%H", time.localtime(time.time())))
            continue
        else:
            scanner('target.list')
            compare()
            sendmail()
            now = int(time.strftime("%H", time.localtime(time.time())))
            if now<1:
                time.sleep(3601)
                now = int(time.strftime("%H", time.localtime(time.time())))
            

def scanner(ip_addr_file):
    global html
    global strScanTime 
    global strTodayDate 
    global strYesterdayDate
    html=''
    strTodayDate = time.strftime("%Y%m%d", time.localtime(time.time()))
    strYesterdayDate = strTime = time.strftime("%Y%m%d", time.localtime(time.time()-60*60*24))
    os.system('sudo /usr/local/masscan/bin/masscan -p0-65535 -iL '+ip_addr_file+' --rate 800 -oJ '+strTodayDate+'.json')
    strScanTime = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))  
    print(ip_addr_file+' scan finished at '+strScanTime)
    
    
def compare():
    global html
    global strScanTime 
    global strTodayDate 
    global strYesterdayDate
    result_today=strTodayDate+'.json'
    result_yesterday=strYesterdayDate+'.json'
    
    today_data=[]
    yesterday_data=[]
    html += strTodayDate + '\n'
    html += '\n ip and open ports: \n'
    try:
        with open(result_today,'r',encoding='utf8')as fp:
            json_data = json.load(fp)
            for element in json_data:
                ip=element['ip']
                port=str(element['ports'][0]['port'])
                html += ip + '\t' + port+'\n'
                today_data.append({'ip': ip, 'port': port})
        with open(result_yesterday,'r',encoding='utf8')as fp:
            json_data = json.load(fp)
            for element in json_data:
                ip=element['ip']
                port=str(element['ports'][0]['port'])
                yesterday_data.append({'ip': ip, 'port': port})    
    except:
        html=''
        print('cannot get masscan result\n')
        return
    
    html += '\n new ip and ports: \n'
    for td in today_data:
        flag = 0
        for yd in yesterday_data:
            if td['ip'] == yd['ip'] and td['port'] == yd['port']:
                    flag = 1
                    break
        if flag == 0:
            html += td['ip']+ '\t' +td['port']+'\n'
            
    html += '\n closed ip and ports: \n'
    for yd in yesterday_data:
        flag = 0
        for td in today_data:
            if td['ip'] == yd['ip'] and td['port'] == yd['port']:
                    flag = 1
                    break
        if flag == 0:
            html += yd['ip']+ '\t' +yd['port']+'\n'
            
    print(html)

    
def sendmail():
    global html
    if html == '':
        return
    
    
    sender="dalbert@163.com"
    receiver=["15901037215@163.com", "411496687@qq.com", "617261336@qq.com","ouyangxin@pbc.gov.cn"]
    #receiver=["15901037215@163.com"]
    
    text=MIMEText(html,'plain','utf-8')
    message=MIMEMultipart('mixed')
    message['From']='Cactus-Monitor'
    message['To']=';'.join(receiver)
    message['Cc']=sender
    message['Subject']='IP and Port Daily Monitor'
    message.attach(text)
    smtp=smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login('dalbert@163.com','Dong130417')
    receiver.append(sender)
    smtp.sendmail(sender,';'.join(receiver),message.as_string())
    smtp.quit()
    print("mail done \n")
    
    
if __name__=="__main__":
    time_to_go()
