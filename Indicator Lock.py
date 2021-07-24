import tkinter as Tk
import threading
import ctypes
import time

    

root = Tk.Tk()
"""root.withdraw()"""
root.attributes("-alpha",0)
root.configure(background='black')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

app_width = 350
app_height = 50

x=(screen_width/2)-(app_width/2)
y=(screen_height/2)-(app_height/2)


root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')



Text=Tk.Label(root, text ="Erreur appelle Amir ou redémarre l'ordi")
Text.config(background = "Black",foreground="white")


def disappear():
    root.attributes("-alpha", 0.8)
    time.sleep(0.03)
    root.attributes("-alpha", 0.6)
    time.sleep(0.03)
    root.attributes("-alpha", 0.4)
    time.sleep(0.03)
    root.attributes("-alpha", 0.2)
    time.sleep(0.03)
    root.attributes("-alpha", 0)
def appear():
    root.attributes("-alpha", 0)
    time.sleep(0.03)
    root.attributes("-alpha", 0.2)
    time.sleep(0.03)
    root.attributes("-alpha", 0.4)
    time.sleep(0.03)
    root.attributes("-alpha", 0.6)
    time.sleep(0.03)
    root.attributes("-alpha", 0.8)

def redir(event):
    
    CAPSLOCK_STATE()
    

def CAPSLOCK_STATE():

    hllDll = ctypes.WinDLL ("User32.dll")
    VK_CAPITAL = 0x14
    a = hllDll.GetKeyState(VK_CAPITAL)
    affichage(a)

def affichage(a):
    
    t=threading.Timer(1.5,disappear)
    appear()
    if a==65409:
        Text.config(background = "Black",foreground="white",text="Majuscule activé", font=("Comic Sans MS",15))
    else:
        Text.config(background = "Black",foreground="white",text="Majuscule désactivé",font=("Comic Sans MS",15))
    t.start()
    


        
root.bind('<Caps_Lock>', redir)
Text.pack()
root.overrideredirect(1)
root.mainloop()

