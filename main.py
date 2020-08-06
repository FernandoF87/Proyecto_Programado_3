from tkinter import *
import os
import time
from threading import Thread

on = True
language = True
money = 1000

def load_img(name):
    if isinstance(name, str):
        path = os.path.join("imgs", name)
        img = PhotoImage(file=path)
        return img
    else:
        return "Error"

class Coin():
    def __init__(self, master, x, y, value, change, label, money, machine):
        self.master = master
        self.label = label
        self.machine = machine
        self.money = money
        img = load_img("hundred.png")
        if not change:
            self.button = Button(self.master, image=img, command= self.create_thread, relief=FLAT, width=40, height=70, bg="#6AE1FF")
        else:
            self.button = Button(self.master, image=img, command= self.erase, relief=FLAT, width=40, height=70, bg="#6AE1FF")
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
        if money >= self.value:
            while run:
                if self.y > 270:
                    self.y = self.y - 10
                    self.button.place(x=self.x, y=self.y)
                    time.sleep(0.03)
                elif self.x > 80:
                    self.x = self.x - 10
                    self.button.place(x=self.x, y=self.y)
                    time.sleep(0.03)
                else:
                    run = False
                    self.x = tempx
                    self.y = tempy
                    self.button.place(x=self.x, y=self.y)
            self.machine.add_money(self.value)
            money -= self.value
            self.money.config(text="Dinero disponible: ₡ " + str(money))
        else:
            print("Mirá capo estás limpio")

    def erase(self):
        global money
        money += self.value
        self.money.config(text="Dinero disponible: ₡ " + str(money))
        self.button.destroy()


class Machine():
    def __init__(self, master, cost, label, label_money):
        self.master = master
        self.money = 0
        self.cost = cost
        self.label = label
        self.label_money = label_money

    def add_money(self, value):
        self.money += value
        if self.money >= self.cost:
            if self.money > self.cost:
                self.cambio(self.money-self.cost)
            self.money = 0
            Toplevel(self.master)
        self.label.config(text="₡" + str(self.money))

    def cambio(self, value):
        coin = Coin(self.master, 350, 330, value, True, self.label, self.label_money, self)

def main():
    global money, on
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
    
    label = Label(machine, text="₡ 0", bg="blue", width=18, height=3, font=("Haettenschweiler", 22))
    label.place(x=60, y=89)

    label_money = Label(machine, text="Dinero disponible: ₡ 1000", bg="#6AE1FF", font=("Haettenschweiler", 16))
    label_money.place(x=0, y=0)

    maquina = Machine(root, 200, label, label_money)

    coin = Coin(root, 520, 350, 50, False, label, label_money, maquina)
    coin2 = Coin(root, 570, 350, 150, False, label, label_money, maquina)
    coin3 = Coin(root, 620, 350, 250, False, label, label_money, maquina)

    root.mainloop()

main()
