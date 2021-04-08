import win32gui
import win32con
import win32api
import win32process
import time

while True:
    try:
        time.sleep(1)
        hwnd = win32gui.GetForegroundWindow()
        _,pid = win32process.GetWindowThreadProcessId(hwnd)
        hndl = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, pid)
        path = win32process.GetModuleFileNameEx(hndl, 0)
        print(path)
    except pywintypes.error:
        print("<--ERROR-->")