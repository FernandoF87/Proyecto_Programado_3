from tkinter import *
import os
import time
from threading import Thread

on = True
money = 1000
language = True #Spanish as True, English as False

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
        global money, language
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
            if language:
                self.money.config(text="Dinero disponible: ₡ " + str(money))
            else:
                self.money.config(text="Available money: ₡ " + str(money))
        else:
            print("Mirá capo estás re limpio, andate a la concha de tu vieja bld")
    #Idea para eliminar los botones segun el dinero faltante
    #if self.available < self.valor: kill
    def erase(self):
        global money, language
        money += self.value
        if language:
            self.money.config(text="Dinero disponible: ₡ " + str(money))
        else:
            self.money.config(text="Available money: ₡ " + str(money))
        self.button.destroy()

    def change_lan(self):
        global money, language
        if language:
            self.money.config(text="Dinero disponible: ₡ " + str(money))
        else:
            self.money.config(text="Available money: ₡ " + str(money))

class Machine():
    def __init__(self, master, label, label_money):
        self.init = False

        up = load_img("up.png")
        down = load_img("down.png")
        enter = load_img("enter.png")
        
        self.string = ""
        self.master = master
        self.money = 0
        self.costs = [50,100,200]
        self.calidad = 0
        self.seleccion = ["consejo", "dicho","chiste"]
        
        if language:
            self.calidades = ["NE","Baja","Media", "Alta"]
        else:
            self.calidades = ["NE","Low","Regular", "High"]
            
        self.label = label
        self.label_money = label_money

        self.label_arrow = Label(self.master, text="->", fg="#38C3FF", bg="blue", font=("Fixedsys", 16))
        self.arrow_pos = 1
        self.current_y = 120
        self.label_arrow.place(x=90,y=self.current_y)
        
        self.button_up = Button(self.master, image=up, command= self.up_arrow, relief=FLAT, width=40, height=40, bg="black")
        self.button_down = Button(self.master, image=down, command= self.down_arrow, relief=FLAT, width=40, height=40, bg="black")
        self.button_enter = Button(self.master, image=enter, command= self.purchase, relief=FLAT, width=60, height=30, bg="black")

        self.button_up.image = up
        self.button_down.image = down
        self.button_enter.image = enter

        self.button_up.place(x=430,y=120)
        self.button_down.place(x=430,y=160)
        self.button_enter.place(x=410,y=210)

    def up_arrow(self):
        if self.arrow_pos > 1:
            self.arrow_pos -= 1
            self.current_y -= 25
            self.label_arrow.place(x=90,y=self.current_y)
            
    def down_arrow(self):
        if self.arrow_pos < 3:
            self.arrow_pos += 1
            self.current_y += 25
            self.label_arrow.place(x=90,y=self.current_y)
            
    def purchase(self):
        if self.calidad > 0:
            if self.money > self.costs[self.calidad-1]:
                self.cambio(self.money-self.costs[self.calidad-1])
            self.money = 0
            self.create_thread()
        else:
            print("falta harina pa, va aflojando la mica")
            
    def add_money(self, value):
        global language
        self.init = True
        self.money += value
        self.calidad = 0
        for i in self.costs:
            if self.money >= i:
                self.calidad += 1
            else:
                break
        if language:
            self.string = "Monto actual: "+str(self.money)+"   Calidad: "+self.calidades[self.calidad]
        else:
            self.string = "Current amount: "+str(self.money)+"  Quality: "+self.calidades[self.calidad]
        self.update_text()

    def update_text(self):
        global language
        if language:
            self.label.config(text=self.string+"\n\n1.Consejos"+"\n\n2.Dichos"+"\n\n3.Chistes")
        else:
            self.label.config(text=self.string+"\n\n1.Advice"+"\n\n2.Saying"+"\n\n3.Gag")
        self.label.place(x=80,y=90)

    def reset(self):
        global language
        if language:
            self.label.config(text="Bienvenido, \ninserte una moneda")
        else:
            self.label.config(text="Welcome, \ninsert a coin")
        self.init = False
        self.label.place(x=140, y=90)
        self.arrow_pos = 1
        self.current_y = 120
        self.label_arrow.place(x=90,y=self.current_y)

    def cambio(self, value):
        coin = Coin(self.master, 350, 330, value, True, self.label, self.label_money, self)

    def create_thread(self):
        thread = Thread(target=self.animation)
        thread.daemon = True
        thread.start()

    def animation(self):
        label = Label(self.master, bg="white", width=36, height=1)
        label.place(x=110, y=500)
        temp = 1
        while temp < 10:
            temp += 1
            label.config(height=temp)
            time.sleep(0.04)
        label.destroy()

        message = Message(self.master, self.seleccion[self.arrow_pos - 1], self.calidades[self.calidad])
        self.calidad = 0
        self.reset()

    def change_lan(self):
        global language  
        if language:
            self.calidades = ["NE","Baja","Media", "Alta"]
            self.string = "Monto actual: "+str(self.money)+"   Calidad: "+self.calidades[self.calidad]
        else:
            self.calidades = ["NE","Low","Regular", "High"]
            self.string = "Current amount: "+str(self.money)+"  Quality: "+self.calidades[self.calidad]
            
        if not self.init:
            self.reset()
        else: 
            self.update_text()

class Message():
    def __init__(self, master, type, quality):
        self.master = master
        self.type = type
        self.quality = quality

        self.screen = Toplevel(self.master)
        self.screen.geometry("255x100+300+300")
        self.label_out = Label(self.screen, text=self.type + " " + self.quality, fg="black", bg="white")
        self.label_out.place(x=0, y=0)


def main():
    global money, on, language
    root = Tk()
    root.geometry("700x600+100+100")
    root.title("Main menu")
    root.resizable(False, False)
    bg = load_img("bg.png")
    lan = load_img("lang.png")
    machine = Canvas(root, width=500, height=600, borderwidth=0, highlightthickness=0, bg="black")
    user = Canvas(root, width=200, height=600, borderwidth=0, highlightthickness=0, bg="#6AE1FF")
    machine.create_image(0,0, anchor=NW, image=bg)

    machine.place(x=0,y=0)
    user.place(x=500,y=0)

    #₡
    label = Label(machine, text="Bienvenido, \ninserte una moneda", fg="#38C3FF" ,bg="blue", font=("Fixedsys", 16))

    label_money = Label(machine, text="Dinero disponible: ₡ 1000", bg="#6AE1FF", font=("Haettenschweiler", 16))

    if on:
        label.place(x=140, y=90)
        label_money.place(x=0, y=0)
        maquina = Machine(root, label, label_money)
            
            

    coin = Coin(root, 520, 350, 25, False, label, label_money, maquina)
    coin2 = Coin(root, 570, 350, 50, False, label, label_money, maquina)
    coin3 = Coin(root, 620, 350, 100, False, label, label_money, maquina)

    def change_lan():
        global language
        language = not language
        if not language:
            print("English")
        else:
            print("Spanish")
        if on:
            maquina.change_lan()
            coin.change_lan()
    #self.button_enter.place(x=410,y=210)
    button_lan = Button(root, image=lan, command=change_lan, relief=FLAT, width=60, height=30, bg="black")
    button_lan.image = lan
    button_lan.place(x=410,y=50)
    
    root.mainloop()

main()
