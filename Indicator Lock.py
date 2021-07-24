import tkinter as Tk
import threading
import ctypes
import time
from pynput.keyboard import Key, Listener
from tkinter import font
from tkinter import ttk

root = Tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width = 350
app_height = 50
x=(screen_width/2)-(app_width/2)
y=(screen_height/2)-(app_height/2)



root.attributes("-alpha",0)
root.configure(background='black')
root.attributes("-topmost", True)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
Text=Tk.Label(root, text ="Erreur appelle Amir ou redémarre l'ordi")
Text.config(background = "Black",foreground="white")
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
Text=Tk.Label(root, text ="Error, reboot the program")
Text.config(background = "Black",foreground="white")
s = ttk.Style()
s.theme_use('winnative')
s.configure("colors.Horizontal.TProgressbar", foreground='black', background='black')
myprogress = ttk.Progressbar(root,style="colors.Horizontal.TProgressbar", orient = Tk.HORIZONTAL, length=350, mode='determinate')

h=0
n=0

def update_window(n):
    root.attributes("-alpha", n)
        

def show(key):
  
    if key==Key.caps_lock:
        print("Hello World")
        CAPSLOCK_STATE()  

def CAPSLOCK_STATE():

    hllDll = ctypes.WinDLL ("User32.dll")
    VK_CAPITAL = 0x14
    a = hllDll.GetKeyState(VK_CAPITAL)
    texte(a)

def affichage(x):
    if x==0:
        update_window(0.6)
        time.sleep(0.03)
        update_window(0.4)
        time.sleep(0.03)
        update_window(0.2)
        time.sleep(0.03)
        update_window(0)
        
    if x==1:       
        update_window(0.8)

def texte(a):
    if a==65409:
        Text.config(background = "Black",foreground="white",text="Majuscule activée", font=("Comic Sans MS",15))
    else:
        Text.config(background = "Black",foreground="gray",text="Majuscule désactivée",font=("Comic Sans MS",15))
    affichage(1)
    timer()


def progressbar():
    global h
    myprogress['value']=h
    j=h
    h=j+1
    root.update_idletasks()
    myprogress['value']=h
    if h>100:
        affichage(0)
        h=0
    else:
        timer()
def timer():
    t=threading.Timer(0.000001,progressbar)
    t.start()
    
    




listener=Listener(on_press = show)   
listener.start()

Text.pack()
myprogress.pack()  
root.overrideredirect(1)
root.mainloop()


    
