from tkinter import *
import os, time, random
from datetime import datetime, date
from threading import Thread

on = True
money = 1000
language = True #Spanish as True, English as False


def popup(message):
    window = Tk()
    window.geometry("200x70+415+350")
    window.title("Popup")

    label = Label(window, text=message, font=("System", 12))
    label.pack()

    if language:
        boton = Button(window, text="Cerrar", command=window.destroy)
    else:
        boton = Button(window, text="Exit", command=window.destroy)
    boton.pack()
    window.mainloop()

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

        if value == 25:
            img = load_img("twenty.png")
        elif value == 50:
            img = load_img("fifty.png")
        elif value == 100:
            img = load_img("hundred.png")
        else:
            img = load_img("change.png")

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
            if language:
                popup("No tiene suficientes fondos")
            else:
                popup("Not enough funds")

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
            self.calidades = ["-","Baja","Media", "Alta"]
        else:
            self.calidades = ["-","Low","Regular", "High"]
            
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
            self.current_y -= 30
            self.label_arrow.place(x=90,y=self.current_y)
            
    def down_arrow(self):
        if self.arrow_pos < 3:
            self.arrow_pos += 1
            self.current_y += 30
            self.label_arrow.place(x=90,y=self.current_y)
            
    def purchase(self):
        if self.calidad > 0:
            if self.money > self.costs[self.calidad-1]:
                self.change = self.money-self.costs[self.calidad-1]
                self.cambio(self.money-self.costs[self.calidad-1])
            else:
                self.change = 0
            self.create_thread()
        else:
            if language:
                popup("Por favor ingresar más dinero")
            else:
                popup("Please insert more money")
            
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
            self.label.config(text=self.string+"\n\n1.Advice"+"\n\n2.Idiom"+"\n\n3.Gag")
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

        message = Message(self.master, self.seleccion[self.arrow_pos - 1], self.calidades[self.calidad], self.money, self.change)
        message.register_receipt()
        self.money = 0
        self.calidad = 0
        self.reset()

    def change_lan(self):
        global language  
        if language:
            self.calidades = ["-","Baja","Media", "Alta"]
            self.string = "Monto actual: "+str(self.money)+"   Calidad: "+self.calidades[self.calidad]
        else:
            self.calidades = ["-","Low","Regular", "High"]
            self.string = "Current amount: "+str(self.money)+"  Quality: "+self.calidades[self.calidad]
            
        if not self.init:
            self.reset()
        else: 
            self.update_text()

class Message():
    def __init__(self, master, type, quality, payment, change):
        global language
        self.master = master
        self.type = type
        self.quality = quality
        self.number = 0
        self.pay = payment
        self.change = change
        if self.quality == "Baja" or self.quality == "Low":
            self.code = random.randint(1,7)
            self.monto = 50
        elif self.quality == "Media" or self.quality == "Regular":
            self.code = random.randint(7,13)
            self.monto = 100
        else:
            self.code = random.randint(13,19)
            self.monto = 200
        #"consejo", "dicho","chiste"
        if self.type == "consejo":
            if language:
                self.title = "Consejo"
            else:
                self.title = "Advice"
            self.color = "blue"
            self.bkgr = load_img("consejo.png")
            self.t = 1
        elif self.type == "dicho":
            if language:
                self.title = "Dicho"
            else:
                self.title = "Idiom"
            self.color = "red"
            self.bkgr = load_img("dicho.png")
            self.t = 2
        else:
            if language:
                self.title = "Chiste"
            else:
                self.title = "Gag"
            self.color = "green"
            self.bkgr = load_img("chiste.png")
            self.t = 3

        self.screen = Toplevel(self.master)
        self.screen.geometry("400x100")
        self.msg = self.parse_message()
        self.bg = Canvas(self.screen, width=400, height=100, borderwidth=0, highlightthickness=0, bg="white")
        self.picture = self.bg.create_image(0,0, anchor=NW, image=self.bkgr)
        self.bg.place(x=0,y=0)
        self.bg.picture = self.bkgr
        self.label_tit = Label(self.screen, text=self.title, fg=self.color, bg="white",  font=("Bodoni MT", 14))
        self.label_tit.place(x=130, y=20)
        self.label_out = Label(self.screen, text=self.msg, fg=self.color, bg="white",  font=("Bodoni MT", 10), justify=CENTER)
        self.label_out.place(x=70, y=45)

    def register_receipt(self):
        global transaccion
        self.date = datetime.now()
        self.day = self.date.strftime("%d/%m/%Y")
        self.time = self.date.strftime("%H:%M")
        self.parse_receipt()

    def parse_receipt(self):
        f = open("facturas.txt", "r")
        words = f.read()
        jump = 0
        str_out = ""
        transaction = -1
        for i in range(len(words)):
            if jump >= 2 and words[i] != "\n":
                str_out += words[i]
            elif words[i] == "\n":
                str_out += words[i]
                jump += 1
                transaction += 1
            else:
                str_out += words[i]

        str_out += str(transaction) + "."+self.day+"."+self.time+"."+self.title+"."+str(self.monto)+"."+str(self.pay)+"."+str(self.change)+"\n"

        writef = open("facturas.txt", "w")
        writef.write(str_out)
        writef.close()


    def parse_message(self):
        global language
        if language:
            f = open("mensajes.txt","r")
        else:
            f = open("messages.txt","r")
        words = f.read()
        jump = 0
        ele = 0
        num_a = ""
        q_found = False
        ph_found = False
        str_out = ""
        phrase = ""
        change = False
        for i in range(len(words)):
            if jump >= 2 and words[i] != "\n":
                if words[i].isnumeric() and ele == 0:
                    if int(words[i]) == self.t:
                        q_found = True
                elif words[i].isnumeric() and ele == 1:
                    num_a += words[i]
                elif words[i] != "." and ele == 2 and ph_found:
                    if words[i] == "/":
                        phrase += "\n"
                    else:
                        phrase += words[i]
                elif words[i].isnumeric() and ele == 4 and ph_found:
                    change = True
                elif words[i] == ".":
                    ele += 1
                    if ele == 2:
                        if int(num_a) == self.code and q_found:
                            ph_found = True
                
                if change:
                    str_out += str(int(words[i])+1)
                else:
                    str_out += words[i]
            elif words[i] == "\n":
                if ph_found:
                    str_out += words[i:]
                    break
                ele = 0
                num_a = ""
                str_out += words[i]
                jump += 1
            else:
                str_out += words[i]
        if language:
            writef = open("mensajes.txt", "w")
        else:
            writef = open("messages.txt", "w")
        writef.write(str_out)
        writef.close()

        return phrase


def main():
    global money, on, language
    root = Tk()
    root.geometry("700x600+100+100")
    root.title("Main menu")
    root.resizable(False, False)
    bg = load_img("bg.png")
    lan = load_img("lang.png")
    admin = load_img("admin.png")
    machine = Canvas(root, width=500, height=600, borderwidth=0, highlightthickness=0, bg="black")
    user = Canvas(root, width=200, height=600, borderwidth=0, highlightthickness=0, bg="#6AE1FF")
    machine.create_image(0,0, anchor=NW, image=bg)

    machine.place(x=0,y=0)
    user.place(x=500,y=0)

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


    def pw_screen():
        admin_s = Toplevel(root)
        admin_s.geometry("500x350+250+200")
        admin_s.resizable(False, False)
        admin_s.title("Admin")
        back_g = Canvas(admin_s, width=500, height=350, borderwidth=0, highlightthickness=0, bg="blue")
        back_g.place(x=0,y=0)

        title = Label(back_g, text="Administrator", fg="white", bg="Blue", font=("Fixedsys", 20))
        title.place(x=150, y=50)
        
        password = StringVar() 
        pw = Entry(back_g, textvariable=password, show='*', width=20, font=("Fixedsys", 12))
        pw.place(x=170, y=100)

        def functions():
            if language:
                end = Button(back_g, command=end_all, relief=FLAT, width=20, height=3, text="Apagar dispensador",bg="red", fg="white", font=("Fixedsys", 8))
                cut = Button(back_g, command=cut_sales, relief=FLAT, width=20, height=3, text="Reiniciar ventas",bg="red", fg="white", font=("Fixedsys", 8))
                report = Button(back_g, command=generate_report, relief=FLAT, width=20, height=3, text="Reporte de ventas",bg="red", fg="white", font=("Fixedsys", 8))
            else:
                end = Button(back_g, command=end_all, relief=FLAT, width=20, height=3, text="Turn off dispenser",bg="red", fg="white", font=("Fixedsys", 8))
                cut = Button(back_g, command=cut_sales, relief=FLAT, width=20, height=3, text="Reset sales",bg="red", fg="white", font=("Fixedsys", 8))
                report = Button(back_g, command=generate_report, relief=FLAT, width=20, height=3, text="Sales report",bg="red", fg="white", font=("Fixedsys", 8))

            end.place(x=170, y=100)
            cut.place(x=170, y=170)
            report.place(x=170, y=240)

        def end_all():
            admin_s.destroy()
            root.destroy()

        def cut_sales():
            f = open("mensajes.txt", "r")
            f2 = open("messages.txt", "r")
            words = f.read()
            jump = 0
            str_out = ""
            str_out_aux = ""
            restarted = False
            for x in range(0,2):
                for i in range(len(words)):
                    if jump >= 2 and words[i] != "\n":
                        if words[i].isnumeric() and ele == 4:
                            if not restarted:
                                str_out += "0"
                                restarted = True
                        elif words[i] == ".":
                            str_out += words[i]
                            ele += 1
                        else:
                            str_out += words[i]
                    elif words[i] == "\n":
                        ele = 0
                        str_out += words[i]
                        jump += 1
                        restarted = False
                    else:
                        str_out += words[i]
                if x == 0:
                    str_out_aux = str_out
                    str_out = ""
                    words = f2.read()

            writef = open("mensajes.txt", "w")
            writef.write(str_out_aux)
            writef.close()

            writef2 = open("messages.txt", "w")
            writef2.write(str_out)
            writef2.close()
            
            f = open("facturas.txt", "r")
            words = f.read()
            jump = 0
            str_out = ""
            for i in range(len(words)):
                if jump < 2:
                    str_out += words[i]
                    if words[i] == "\n":
                        jump += 1
                else:
                    break

            writef = open("facturas.txt", "w")
            writef.write(str_out)
            writef.close()

            if language:
                popup("Ventas reiniciadas")
            else:
                popup("Sales restarted")

        def generate_report():
            f = open("mensajes.txt", "r")
            f2 = open("messages.txt", "r")
            words = f.read()
            jump = 0
            #ele = 0
            str_out = ""
            #reading = False
            #save = False
            params = []
            mat_out = []
            #for i in range(len(words)):
            #    if jump >= 2:
            #        if words[i] != ".":
            #            str_out += words[i]
            #        else:
            #            str_out += " "
            #    elif words[i] == "\n":
            #        jump += 1
            for x in range(2):
                for i in range(len(words)):
                    if jump >= 2 and words[i] != "\n":
                        if words[i] == ".":
                            params += [str_out]
                            #ele += 1
                            str_out = ""
                        elif words[i] != ".":
                            if words[i] != "/":
                                str_out += words[i]
                            else:
                                str_out += " "
                            
                    elif words[i] == "\n":
                        if jump >= 2 and int(str_out) > 0:
                            params += [str_out]
                            mat_out += [params]
                        params = []
                        str_out = ""
                        #ele = 0
                        jump += 1
                        #reading = True
                params = []
                jump = 0
                words = f2.read()

            if language:
                to_write = "Tipo   Codigo\tMensaje\t\t\t\t\t\t\t\t\t\t\tMensajes vendidos   Monto ventas\n"
            else:
                to_write = "Type   Code  \tMessage\t\t\t\t\t\t\t\t\t\t\tMessages sold       Amount in sales\n"
            for i in mat_out:
                for j in range(len(i)):
                    if j != 4:
                        if j == 2:
                            while len(i[j]) < 94:
                                i[j] += " "
                        if j != 3:
                            to_write += i[j] + "\t"
                        else:
                            to_write += i[4] + "\t\t"
                    else:
                        to_write += "₡" + str(int(i[3])*int(i[4]))+"\t"
                to_write += "\n"

            
            report = Toplevel(admin_s)
            report.title("Report")
            bkground = Canvas(report, width=1000, height=1000, borderwidth=0, highlightthickness=0, bg="#001B78")
            bkground.place(x=0, y=0)
            label = Label(report, text=to_write, justify=LEFT, font=("Fixedsys", 8), fg="white", bg="#001B78")
            label.pack()
            report.mainloop()

        def check_pw():
            if password.get() == "acm1pt":
                pw.destroy()
                submit.destroy()
                functions()
            else:
                if language:
                    popup("Clave incorrecta")
                else:
                    popup("Wrong password")
        
        submit = Button(back_g, command=check_pw, relief=FLAT, width=20, height=3, text="Submit",bg="red", fg="white", font=("Fixedsys", 8))
        submit.place(x=165, y=150)

        back = Button(back_g, command=admin_s.destroy, relief=FLAT, width=9, height=3, text="Back",bg="red", fg="white", font=("Fixedsys", 8))
        back.place(x=20, y=280)
        
    #self.button_enter.place(x=410,y=210)
    button_lan = Button(root, image=lan, command=change_lan, relief=FLAT, width=60, height=30, bg="black")
    button_lan.image = lan
    button_lan.place(x=410,y=50)

    button_admin = Button(root, image=admin, command=pw_screen, relief=FLAT, width=60, height=30, bg="black")
    button_admin.image = admin
    button_admin.place(x=410,y=550)
    
    root.mainloop()

main()
