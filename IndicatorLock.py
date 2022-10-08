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


#-----------Notification de lancement de l'appli-----------
toast = Notification(app_id="Indicator Lock",
                     title="Indicator Lock est en fonctionnement",
                     msg="Indicator Lock fonctionne en arrière-plan. Si vous souhaitez fermer l'application, elle se trouve dans la barre des tâches",
                     icon=os.path.join(os.path.dirname(os.path.abspath(__file__)),"caps-lock.ico"))
toast.set_audio(audio.Reminder, loop=False)
toast.show()


#-----------Configuration de la fenêtre root----------------
root = Tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width = 350
app_height = 40
x = (screen_width / 2) - (app_width / 2)
y = 0
root.title("CapsLock")

root.attributes("-alpha", 0)
root.configure(background='Black')

root.attributes("-topmost", True)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
Text = Tk.Label(root, text="")

#-----------Variables----------------
n = 0
h= 1
j =1
maj=0
pave=1
defil=0


#-----------Fonction d'arrêt du système----------------
def stopthis():
    icon.stop()
    root.quit()
    os._exit(1)


#-----------Configuration de l'icone dans la barre des tâches----------------
image = Image.open("caps-lock.ico")
menu = pystray.Menu(item("Quitter", stopthis))
icon = pystray.Icon("name", image, "CapsLock", menu)
icon.run_detached()


def update_window(n):   #gère la transparence du root
    root.attributes("-alpha", n)


def show(key):      #Détecte les touches num, maj et scroll
    if key == Key.caps_lock:

        CAPSLOCK_STATE(maj,pave,defil)
    elif key == Key.num_lock:

        NUMLOCK_STATE(maj,pave,defil)
    elif key == Key.scroll_lock:

        SCROLLOCK_STATE(maj,pave,defil)



def NUMLOCK_STATE(maj,pave,defil):          #gère l'état du pavé numérique et le renvoie
    hllDll = ctypes.WinDLL("User32.dll")
    VK_NUMLOCK = 0x90
    b = hllDll.GetKeyState(VK_NUMLOCK)

    if b == 65409:
        pave = 1
    else:
        pave = 0
    indic(pave, maj, defil)
    texte(b, "Pavé numérique")


def CAPSLOCK_STATE(maj, pave, defil):       #gère l'état des majuscules et le renvoie
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    a = hllDll.GetKeyState(VK_CAPITAL)

    if a == 65409:
        maj = 1
    else:
        maj = 0
    indic(pave, maj,defil)
    texte(a, "Majuscule")


def SCROLLOCK_STATE(maj,pave,defil):        #gère l'état du défilement et le renvoie
    hllDll = ctypes.WinDLL("User32.dll")
    VK_SCROLL = 0x91
    c = hllDll.GetKeyState(VK_SCROLL)

    if c == 65409:
        defil = 1
    else:
        defil = 0

    indic(pave, maj,defil)
    texte(c, "Défilement")



def affichage(x):           #fais le fade in et le fade out

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



def texte(p, t):            #affichage au user de l'état des touches
    if p == 65409:
        Text.config(background="Black", foreground="Lime", text=t+" activée 😉", font=("Tahoma", 15))
    else:
        Text.config(background="Black", foreground="Red", text=t+" désactivée 😡", font=("Tahoma", 15))

    affichage(1)
    progressbar()


def progressbar():          #timer de l'affichage du root
    global h
    global timer
    try:
        root.after_cancel(timer)
        progressbar()
    except:

        timer = root.after(1500,lambda:affichage(0))



    """global h
    h += 1
    myprogress['value'] = h
    if myprogress['value'] > 100:
        affichage(0)
        h = 0
    else:
        root

    global j
    if h == 0:
        h = 1
        timing = 0
        timing_max = int(time.time())
        while timing < timing_max + 2:
            timing = int(time.time())
            if (j == 0):
                timing = -1
                break
        if timing > 0:
            affichage(0)
            h = 0
            j = 1
        else:
            h = 0
            j = 1
            progressbar()
    else:
        j = 0
        h = 0

    m = myprogress["value"]
    if m < 100:
        myprogress["value"]=m+2
        root.after(25,progressbar)
    else:
        affichage(0)
        myprogress["value"]=0

def timer():
    t = threading.Timer(0.0001, progressbar)
    t.start()
"""
#-----------Coordonnées de aroot et la réutilisation----------------
data ={
    'w':((screen_width * 84) / 85) - (app_width / 2),
    'z':(screen_height * 11) / 12
}

try:
    with open('coord.txt') as coordonnee:
        data = json.load(coordonnee)
except:
    pass


#-----------Configuration de la fenêtre aroot----------------
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


def indic(n, m,s):          #gère l'apparition des lights et leur modification
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


indic(1, 0, 0)



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


#-----------Détecte les touches et les souris à tout moment et les .pack----------------
listener = Listener(on_press=show)
listener.start()
Text.pack()
aroot.bind('<Button-1>', SaveLastClickPos)
aroot.bind('<B1-Motion>', Dragging)
aroot.bind('<ButtonRelease-1>', savecoord)
root.overrideredirect(1)
root.mainloop()
