import tkinter as Tk
import ctypes
import time
from pynput.keyboard import Key, Listener
import json
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import os
from winotify import Notification,audio
import locale
from googletrans import Translator

#-----------Translated sentences-----------
dist = locale.getdefaultlocale()
translator = Translator()
text_menu = translator.translate('Quit', src='en', dest=dist[0][:2])
text_pave = translator.translate('Number pad', src='en', dest=dist[0][:2])
text_maj = translator.translate('Uppercase', src='en', dest=dist[0][:2])
text_defil = translator.translate('Scrolling', src='en', dest=dist[0][:2])
title_text = translator.translate(' is in service', src='en', dest=dist[0][:2])
notif_result = translator.translate(' is running in the background. \nTo close the application, you just have to just make a right click on the icon in the taskbar.', src='en', dest=dist[0][:2])

#-----------App launch notification-----------
toast = Notification(app_id="Indicator Lock",
                     title="Indicator Lock "+title_text.text,
                     msg="Indicator Lock "+notif_result.text,
                     icon=os.path.join(os.path.dirname(os.path.abspath(__file__)),"caps-lock.ico"))
toast.set_audio(audio.Reminder, loop=False)
toast.show()


#-----------Configuration of the root window----------------
root = Tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width = 350
app_height = 40
x = (screen_width / 2) - (app_width / 2)
y = 0
root.title("Indicator Lock")

root.attributes("-alpha", 0)
root.configure(background='Black')

root.attributes("-topmost", True)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
Text = Tk.Label(root, text="")

#-----------Variables----------------
n = 0
h = 1
j = 1
pave = 0
maj = 0
defil = 0




def init():
    global pave, maj, defil
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    VK_NUMLOCK = 0x90
    VK_SCROLL = 0x91
    maj = hllDll.GetKeyState(VK_CAPITAL)
    pave = hllDll.GetKeyState(VK_NUMLOCK)
    defil = hllDll.GetKeyState(VK_SCROLL)

    indic(pave, maj, defil)


#-----------System shutdown function----------------
def stopthis():
    icon.stop()
    root.quit()
    os._exit(1)


#-----------Configuration of the icon in the taskbar----------------
image = Image.open("caps-lock.ico")

menu = pystray.Menu(item(text_menu.text, stopthis))
icon = pystray.Icon("name", image, "Indicator Lock", menu)
icon.run_detached()


def update_window(n):   #manages root transparency
    root.attributes("-alpha", n)


def show(key):      #Detects num, shift and scroll keys
    if key == Key.caps_lock:

        CAPSLOCK_STATE(maj,pave,defil)
    elif key == Key.num_lock:

        NUMLOCK_STATE(maj,pave,defil)
    elif key == Key.scroll_lock:

        SCROLLOCK_STATE(maj,pave,defil)



def NUMLOCK_STATE(maj,pave,defil):#manages the state of the numeric keypad and returns it
    hllDll = ctypes.WinDLL("User32.dll")
    VK_NUMLOCK = 0x90
    b = hllDll.GetKeyState(VK_NUMLOCK)

    if b == 65409:
        pave = 1
    else:
        pave = 0
    indic(pave, maj, defil)

    texte(b, text_pave.text)


def CAPSLOCK_STATE(maj, pave, defil):#manages the status of capital letters and returns it
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    a = hllDll.GetKeyState(VK_CAPITAL)

    if a == 65409:
        maj = 1
    else:
        maj = 0
    indic(pave, maj,defil)
    texte(a, text_maj.text)


def SCROLLOCK_STATE(maj,pave,defil):#manages the state of the scroll and returns it
    hllDll = ctypes.WinDLL("User32.dll")
    VK_SCROLL = 0x91
    c = hllDll.GetKeyState(VK_SCROLL)

    if c == 65409:
        defil = 1
    else:
        defil = 0

    indic(pave, maj,defil)
    texte(c, text_defil.text)



def affichage(x):#do the fade in and fade out

    if x == 0:
        update_window(0.6)
        time.sleep(0.03)
        update_window(0.4)
        time.sleep(0.03)
        update_window(0.2)
        time.sleep(0.03)
        update_window(0)
    if x == 1:
        update_window(0.8)



def texte(p, t):#user display of key status
    if p == 65409:
        Text.config(background="Black", foreground="Lime", text=t+" activée 😉", font=("Tahoma", 15))
    else:
        Text.config(background="Black", foreground="Red", text=t+" désactivée 😡", font=("Tahoma", 15))

    affichage(1)
    progressbar()


def progressbar():#root display timer
    global h
    global timer
    try:
        root.after_cancel(timer)
        progressbar()
    except:

        timer = root.after(1500,lambda:affichage(0))




#-----------Coordinates of aroot and reuse----------------
data ={
    'w':((screen_width * 84) / 85) - (app_width / 2),
    'z':(screen_height * 11) / 12
}

try:
    with open('coord.txt') as coordonnee:
        data = json.load(coordonnee)
except:
    pass


#-----------Configuration of the aroot window----------------
aroot = Tk.Toplevel(root)
w = int(data['w'])
z = int(data['z'])
aroot.overrideredirect(1)
aroot.wm_attributes("-topmost",True)
aroot.wm_attributes("-transparentcolor", "black")
aroot.configure(background='black')
aroot.geometry(f'{app_width}x{app_height}+{int(w)}+{int(z)}')
c = Tk.Canvas(aroot, bg="black", highlightthickness=0)
c.pack()


def indic(n, m,s):          #manages the appearance of lights and their modification
    x1,y1,x2,y2 = 14,10,24,20

    num,maj,scroll = c.create_oval(x1, y1, x2, y2, fill="black"),c.create_oval(x1 + 15, y1, x2 + 15, y2, fill="black"),c.create_oval(x1 + 30, y1, x2 + 30, y2, fill="black")

    if n == 1:
        c.itemconfig(num,fill="lime")
    else:
        c.itemconfig(num,fill="red")
    if m == 1:
        c.itemconfig(maj,fill="lime")
    else:
        c.itemconfig(maj,fill="red")
    if s == 1:
        c.itemconfig(scroll, fill="lime")
    else:
        c.itemconfig(scroll, fill="red")




#gère le déplacement de aroot
lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    global coord
    w,z = event.x - lastClickX + aroot.winfo_x(), event.y - lastClickY + aroot.winfo_y()
    aroot.geometry("+%s+%s" % (w,z))
    coord = {
        'w':w,
        'z':z
    }


def savecoord(event):           #Enregistrement des coordonnées
    with open('coord.txt','w') as coordonnee:
        json.dump(coord, coordonnee)

init()
#-----------Détecte les touches et les souris à tout moment et les .pack----------------
listener = Listener(on_press=show)
listener.start()
Text.pack()
aroot.bind('<Button-1>', SaveLastClickPos)
aroot.bind('<B1-Motion>', Dragging)
aroot.bind('<ButtonRelease-1>', savecoord)
root.overrideredirect(1)
root.mainloop()
