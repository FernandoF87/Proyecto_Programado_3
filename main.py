from tkinter import *
import os
import time
from threading import Thread

money = 1000

def load_img(name):
    if isinstance(name, str):
        path = os.path.join("imgs", name)
        img = PhotoImage(file=path)
        return img
    else:
        return "Error"

class Coin():
    def __init__(self, master, x, y, value, change, label):
        self.master = master
        self.label = label
        img = load_img("hundred.png")
        if not change:
            self.button = Button(self.master, image=img, command= self.create_thread, relief=FLAT)
        else:
            self.button = Button(self.master, image=img, command= self.erase, relief=FLAT)
        self.button.image = img
        self.x = x
        self.y = y
        self.value = value
        self.speed = 10
        self.button.place(x=self.x, y=self.y)

    def create_thread(self):
        thread = Thread(target=self.move)
        thread.daemon = True
        thread.start()

    def move(self):
        global money
        tempx = self.x
        tempy = self.y
        run = True
        while run:
            if self.y > 50:
                self.y = self.y - 10
                self.button.place(x=self.x, y=self.y)
                time.sleep(0.03)
            elif self.x > 50:
                self.x = self.x - 10
                self.button.place(x=self.x, y=self.y)
                time.sleep(0.03)
            else:
                run = False
                self.x = tempx
                self.y = tempy
                self.button.place(x=self.x, y=self.y)
        money += self.value
        self.label.config(text=str(money))

    def erase(self):
        self.button.destroy()


def cambio(label):
    global money
    if money > 0:
        money -= 100
    label.config(text=str(money), bg="blue")
    time.sleep(0.1)

def main():
    global money
    root = Tk()
    root.geometry("700x600+100+100")
    root.title("Main menu")
    root.resizable(False, False)
    bg = load_img("bg.png")
    machine = Canvas(root, width=500, height=600, borderwidth=0, highlightthickness=0, bg="black")
    user = Canvas(root, width=200, height=600, borderwidth=0, highlightthickness=0, bg="#6AE1FF")

    machine.create_image(0,0, anchor=NW, image=bg)

    machine.place(x=0,y=0)
    user.place(x=500,y=0)
    
    label = Label(root, text=str(money), bg="red")
    label.place(x=550, y=0)

    coin = Coin(root, 500, 350, 50, False, label)

    root.mainloop()

main()
