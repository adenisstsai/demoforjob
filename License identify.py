import time
from datetime import datetime
import os
import sys
import tkinter
import psutil

from ntplib import NTPClient
import msvcrt
from key_generator.key_generator import generate
from PyQt5.QtWidgets import QApplication, QMessageBox

def KeyGernator(): #密碼鎖
    c = NTPClient() 
    response = c.request('pool.ntp.org') 
    ts = response.tx_time 
    Key_date = time.strftime('%Y%m%d%H',time.localtime(ts)) 
    key = generate(seed = int(Key_date)+19831024+19910508)
    Key_seed = key.get_key()
    def pwd_input():    
        chars = []   
        while True:  
            try:  
                newChar = msvcrt.getch().decode(encoding="utf-8")  
            except:  
                return input("你很可能不是在cmd命令行下運行，密碼輸入將不能隱藏:")  
            if newChar in '\r\n': # 如果是換行，則輸入結束               
                break   
            elif newChar == '\b': # 如果是退格，則刪除密碼末尾一位並且刪除一個星號   
                if chars:    
                    del chars[-1]   
                    msvcrt.putch('\b'.encode(encoding='utf-8')) # 光標回退一格  
                    msvcrt.putch(' '.encode(encoding='utf-8')) # 輸出一個空格覆蓋原來的星號  
                    msvcrt.putch('\b'.encode(encoding='utf-8')) # 光標回退一格準備接受新的輸入                   
            else:  
                chars.append(newChar)  
                msvcrt.putch('*'.encode(encoding='utf-8')) # 顯示為星號  
        return (''.join(chars) )  

    filepath = "C:\key\key"
    if os.path.isfile(filepath):
        print("已通過驗證!")
    else:
        print("Please input your password:")
        pwd = pwd_input()  
        print("\nyour password is:{0}".format(pwd))
        if pwd == key.get_key():
            os.mkdir("C:\key")
            root = tkinter.Tk()
            root.withdraw()
            f = open('C:\key\key', 'a')
            f.write('已通過驗證!')
            print("Successfully!")
        else:
            os._exit(0)

def ExprationDate(): #程式期限
    c = NTPClient() 
    response = c.request('pool.ntp.org') 
    ts = response.tx_time 
    now_yea = time.strftime('%Y',time.localtime(ts))
    now_mon = time.strftime('%m',time.localtime(ts))
    now_day = time.strftime('%d',time.localtime(ts))
    expected_time = datetime(2022,3,20)

    app = QApplication(sys.argv)
    if datetime(int(now_yea),int(now_mon),int(now_day)) >= expected_time:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("提示")
        msg_box.setText("程式已經到期，請重新諮詢!")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.addButton("確定", QMessageBox.YesRole)
        msg_box.exec()
        os._exit(0)

def SingleWin(): #防多開
    pid = read_pid()
    #print pid
    pid = int(pid)
    if pid:
        running_pid = psutil.pids()
        if pid in running_pid:
            app = QApplication(sys.argv)
            msg_box =QMessageBox()
            msg_box.setWindowTitle("請勿多開")
            msg_box.setText("程式禁止多開 即將關閉!")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.addButton("確定", QMessageBox.YesRole)
            msg_box.exec()
            os._exit(0)
        else:
            write_pid()
    else:
        write_pid()

def write_pid():
    pid = os.getpid()
    fp = open("C:\key\pid",'w')
    fp.write(str(pid))
    fp.close()

def read_pid():
    if os.path.exists("C:\key\pid"):
        fp = open("C:\key\pid",'r')
        pid = fp.read()
        fp.close()
        return pid
    else:
        return False

if __name__ == '__main__':
    KeyGernator()
    ExprationDate()
    SingleWin()
    time.sleep(3600)