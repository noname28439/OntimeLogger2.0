from pynput import keyboard
from pynput import mouse as mse
import os
import subprocess
from threading import Thread
import time
import pynput as lelek
from pynput.mouse import Controller as mouse
from pynput.mouse import Button
from pynput.keyboard import Key
import datetime
import sys
import webbrowser
import random
import os.path
import json
import win32gui
import win32con
import win32api
import win32process
import pywintypes

def list_to_string(list):
    string = ""
    for c in list:
        string += c
    return string

LOG_FILE_PATH = "./TimeLogs"

is_afk = False
afk_timeout = 0
afk_set_to = 30
inGame = False


counter_list = {}



def calculate_current_file_name():
    date = datetime.datetime.now()
    day = str(date.day)
    month = str(date.month)
    year = str(date.year)

    return LOG_FILE_PATH+"/date@"+year+"-"+month+"-"+day+".json"


def check_file_exists():
    if not os.path.isfile(calculate_current_file_name()):
        cf = open(calculate_current_file_name(), "w+")
        cf.close()
        print("File just created, because it didn't exist!")


def file_save():
    global counter_list
    check_file_exists()
    with open(calculate_current_file_name(), "w") as file:
        json.dump(counter_list, file)

def file_load():
    global counter_list
    if os.path.isfile(calculate_current_file_name()):
        with open(calculate_current_file_name(), "r") as file:
            data = json.load(file)
            counter_list = data

file_load()

def listmanagement_add_time(id, time):
    if id in counter_list:
        counter_list[id][0] = counter_list[id][0]+time

def listmanagement_set_name(id, window_name):
    counter_list[id][1] = window_name

def listmanagement_add_process(id, window_name):
    counter_list[id] = [1, window_name]

def get_current_active_window_path():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _,pid = win32process.GetWindowThreadProcessId(hwnd)
        hndl = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, pid)
        path = win32process.GetModuleFileNameEx(hndl, 0)
        return path
    except pywintypes.error:
        print("<--ERROR-->")
        return None


def main_thread():
    global afk_timeout, on_sec, off_sec, is_afk, inGame
    while True:
        time.sleep(1)
        if inGame:
            afk_timeout = afk_set_to

        current_active_window_name = str(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        current_active_window_id = win32gui.GetForegroundWindow()
        current_active_window_path = get_current_active_window_path()

        if not "OFF-TIME" in counter_list:
            listmanagement_add_process("OFF-TIME", "offlineTimes")

        if current_active_window_path in counter_list:
            listmanagement_set_name(current_active_window_path, current_active_window_name)

        if afk_timeout>0:
            is_afk=False
            if not current_active_window_path in counter_list:
                listmanagement_add_process(current_active_window_path, current_active_window_name)
            else:
                listmanagement_add_time(current_active_window_path, 1)
            afk_timeout -= 1
        else:
            if not is_afk:                  #Wenn er noch nicht AFK war, dann ist er seit exakt 30 Sek. AFK und diese 30 Sek. werden abgezogen
                listmanagement_add_time("OFF-TIME", afk_set_to)
                listmanagement_add_time(current_active_window_path, -afk_set_to)
            is_afk = True
            listmanagement_add_time("OFF-TIME", 1)


        print("afk: "+str(afk_timeout))
        print("List: "+str(counter_list))

        #print("[ON_SEC: "+str(on_sec)+" MIN: "+str(round((on_sec/60),2))+" HOUR: "+str(round((on_sec/60/60),2))+""+" || afkTimeout: "+str(afk_timeout)+"]", end="\n")
        #print("[OFF_SEC: " + str(off_sec) + " MIN: " + str(round((off_sec / 60),2)) + " HOUR: " + str(round((off_sec / 60 / 60),2)) + "" + " || afkTimeout: " + str(afk_timeout) + "]", end="\n")


def writerThread():
    global on_sec, off_sec, year, month, day
    while True:
        time.sleep(10)
        file_save()
        file_load()



fbt = Thread(target=main_thread)
fbt.daemon = True
fbt.start()
wt = Thread(target=writerThread)
wt.daemon = True
wt.start()




#recognize KeyInteraction
if __name__  == "__main__":

    pressed = []

    controller = keyboard.Controller()

    def on_press(key):
        global afk_timeout
        afk_timeout = afk_set_to
        key = str(key).replace("'","")
        if(not key in pressed):
            pressed.append(key)

    def on_release(key):
        key = str(key).replace("'", "")
        if (key in pressed):
            pressed.remove(key)


    def mouse_move(x, y):
        global afk_timeout
        afk_timeout = afk_set_to
        #print("moved to",str(x), " " , str(y))


    def key_on():
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def mouse_on():
        with mse.Listener(on_move=mouse_move) as ml:
            ml.join()


    kt = Thread(target=key_on)
    kt.daemon = True
    kt.start()
    km = Thread(target=mouse_on)
    km.daemon = True
    km.start()


    try:
        while True:
            cons_recv = input("")
            if cons_recv == "inGame":
                inGame = not inGame
                print("INGAME: "+str(inGame))
    except KeyboardInterrupt:
        with open(LOG_FILE_PATH+"/date@" + year + "-" + month + "-" + day + ".txt", "w") as file:
            file.write(str(on_sec)+"\n"+str(off_sec))
        print("Stopping...")
        quit()

    print("run_out")
