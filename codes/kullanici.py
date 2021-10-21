from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
import RPi.GPIO as GPIO
import sqlite3
import MFRC522
import os
import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2,shutil
from tkcalendar import Calendar , DateEntry
con=None
cursor=None
led_durum=0

bit=0
MIFAREReader = MFRC522.MFRC522()
kart_okutun = '''Kartınızı okutunuz'''


num=0
kullaniciadi="Kaan"
sifre="1234"

pencere=Tk()
durum=0
def ekran_degistir(frame):

    frame.tkraise()
    Ekle.gr7.delete(0, END)
    Ekle.gr3.delete(0, END)
    Ekle.gr4.delete(0, END)
    Ekle.gr5.delete(0, END)
    Ekle.gr6.delete(0, END)

class islem():

    global sifre,kullaniciadi
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 20
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # allow the camera to warmup
    time.sleep(0.1)

    def kameraac(self):
        self.zaman = datetime.datetime.now()
        self.i=Ekle.gr3.get()
        self.s=Ekle.gr4.get()
        self.n=Ekle.gr5.get()
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):

            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array

            #pencere.update_idletasks()
            #pencere.update()
            # show the frame
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)
            # if the `q` key was pressed, break from the loop
            if key== ord('s'):
                self.a=self.i+"-"+self.s+"-"+self.n
                cv2.destroyAllWindows()
                try:
                    os.mkdir("//home//pi//python_project//goruntuler//{0}-{1}-{2}".format(str(self.i),str(self.s),str(self.n)))
                    os.mkdir("//home//pi//python_project//goruntuler//{0}-{1}-{2}//Kayit".format(str(self.i),str(self.s),str(self.n)))
                    self.camera.capture('//home//pi//python_project//goruntuler//{0}-{1}-{2}//Kayit//{3}.{4}.{5}-{6}:{7}.jpg'.format(str(self.i),str(self.s),str(self.n),str(self.zaman.day),str(self.zaman.month),str(self.zaman.year),str(self.zaman.hour),str(self.zaman.minute)))
                    break
                except FileExistsError:
                    messagebox.showerror("Hata","Böyle bir kullanıcı var!")
                    self.camera.close()
                    break

            elif key==27:
                cv2.destroyAllWindows()
                self.camera.close()
                break



    def giriskontrol(self):
        self.Ka=Ekle.gr1.get()
        self.Si=Ekle.gr2.get()
        if(self.Ka==kullaniciadi and self.Si==sifre):
            messagebox.showinfo("Bildiri","Giris yapildi!")
            Ekle.gr1.delete(0,END)
            Ekle.gr2.delete(0,END)
            ekran_degistir(f2)
        else:
            messagebox.showerror("Hata", "Sifre yanlis!")

    def kartoku(self):

        Ekle.gr6.delete(0,END)
        self.top = Toplevel()
        self.top.title('Kart bekleniyor')
        Message(self.top, text=kart_okutun, padx=100, pady=100).pack()
        while True:

            #pencere.update_idletasks()
            #pencere.update()

            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            if status == MIFAREReader.MI_OK:
                GPIO.output(11, GPIO.HIGH)
                self.top.destroy()
                (status, uid) = MIFAREReader.MFRC522_Anticoll()
                id_str = "{0} {1} {2} {3}".format(uid[0], uid[1], uid[2], uid[3])
                Ekle.gr6.insert(0, id_str)
                messagebox.showinfo("Bildiri", "Kart okundu")
                GPIO.output(11, GPIO.LOW)
                break

    def kaydet(self):
        global durum

        self.sorgu=messagebox.askquestion("Kaydet", "Kaydedilsin mi?", icon='info')
        if self.sorgu=='yes':
            sure="ÖĞRENCİ"
            con = sqlite3.connect("OgrenciKayitlari.db") # sqllite database oluşturuldu
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Kayitlar (AD TEXT,SOYAD TEXT,NUMARA TEXT,KARTID TEXT,SURE TEXT)")  # database içine tablo oluşturuldu
            con.commit()
            Ad=Ekle.gr3.get()
            Soyad=Ekle.gr4.get()
            Numara=Ekle.gr5.get()
            Kart_ID=Ekle.gr6.get()
            if Ekle.var.get()==2:
                sure=Ekle.cal.get_date()
            if Ad=="" or Soyad=="" or Numara=="" or Kart_ID=="":
                    messagebox.showerror("Hata","Bosluklari doldurun")
            else:
                cursor.execute("SELECT KARTID FROM Kayitlar") # kayitlar içinden kart idleri okundu(sorgulama işlemi basladı)
                data1=cursor.fetchall() # kart id içerisindeki tüm verileri sorgulayıp data1 değişkenine atadı
                cursor.execute("SELECT NUMARA FROM Kayitlar")  # kayitlar içinden kart idleri okundu(sorgulama işlemi basladı)
                data2 = cursor.fetchall()  # kart id içerisindeki tüm verileri sorgulayıp data2 değişkenine atadı
                for veri in data1:
                    atamaveri=veri # tuple olan veri başka değişkene atama yapıldı
                    

                    if strveri==Kart_ID:
                        messagebox.showerror("Hata", "Bu kart daha önceden kayıt edilmiştir")
                        durum=1
                        break

                for veri in data2:
                    atamaveri=veri # tuple olan veri başka değişkene atama yapıldı
                    strveri=''.join(map(str,atamaveri)) # tuple veri string türüne çevirildi

                    if strveri==Numara:
                        messagebox.showerror("Hata", "Bu öğrenci numarası daha önceden kayıt edilmiştir")
                        durum=1
                        break

                if durum==0:
                    cursor.execute("INSERT INTO Kayitlar VALUES (?,?,?,?,?)", (Ad, Soyad, Numara, Kart_ID,sure)) # oluşturulan tabloya veriler eklendi
                    con.commit()
                    con.close()
                    messagebox.showinfo("Başarılı", "Kayıt İşlemi Tamamlandı")
                durum=0
                Ekle.gr3.delete(0, END)
                Ekle.gr4.delete(0, END)
                Ekle.gr5.delete(0, END)
                Ekle.gr6.delete(0, END)
            con.close()

    def kullanicisil(self):
        self.sorgu = messagebox.askquestion("Sil", "Kullanıcı silinsin mi?", icon='warning')
        if self.sorgu == 'yes':
            self.numara=Ekle.gr7.get()
            con = sqlite3.connect("OgrenciKayitlari.db")  # sqllite database oluşturuldu
            cursor = con.cursor()
            delete = con.cursor()
            delete.execute("SELECT AD,SOYAD,NUMARA FROM Kayitlar WHERE NUMARA = ?", (self.numara,))
            ki = delete.fetchall()
            isim = '-'.join(ki[0])
            shutil.rmtree("//home//pi//python_project//goruntuler//" + isim)

            cursor.execute("DELETE FROM Kayitlar WHERE NUMARA = ?",(self.numara,)) # silme işlemi yapıldı   NUMARA=? çalışabilmesi için (self.numara,) dipnot: "virgül" olmazsa hata veriyor.
            con.commit()
            con.close()
            messagebox.showerror("Hata", "Kullanici silindi")
            Ekle.gr7.delete(0,END)
            Ekle.lb1.config(text="")
            Ekle.lb2.config(text="")
            Ekle.lb3.config(text="")

    def kullanicigetir(self):
        self.numara = Ekle.gr7.get()
        con = sqlite3.connect("OgrenciKayitlari.db")  # sqllite database oluşturuldu
        cursor = con.cursor()
        cursor.execute("SELECT AD FROM Kayitlar WHERE NUMARA = ?",(self.numara,))
        data1=cursor.fetchall()
        cursor.execute("SELECT SOYAD FROM Kayitlar WHERE NUMARA = ?",(self.numara,))
        data2 = cursor.fetchall()
        cursor.execute("SELECT KARTID FROM Kayitlar WHERE NUMARA = ?",(self.numara,))
        data3 = cursor.fetchall()
        con.close()

        Ekle.lb1.config(text=data1)
        Ekle.lb2.config(text=data2)
        Ekle.lb3.config(text=data3)
        if len(data1)==0:
            messagebox.showerror('Hata',"Kullanici Kayitli değildir",icon='warning')

    def KaraListeEkle(self):
        self.numara=Ekle.gr7.get()
        con = sqlite3.connect("OgrenciKayitlari.db")  # sqllite database bağlandı
        cursor = con.cursor()
        cursor.execute("SELECT SURE FROM Kayitlar WHERE NUMARA = ?", (self.numara,))
        self.data1 = cursor.fetchall()
        if len(self.data1)!=0:
            self.data1 = (str(self.data1).split("/"))
            if self.data1[0]=="[('K":
                messagebox.showerror('Hata', '{0} numarali kullanici zaten kara listeye eklidir.'.format(self.numara),icon='warning')
                con.close()
            else:
                self.tarih=Ekle.takvim.get_date()
                self.sure="K/{0}".format(self.tarih)
                cursor.execute('''UPDATE Kayitlar SET SURE = ? WHERE NUMARA = ?''', (self.sure, self.numara))
                con.commit()
                messagebox.showinfo('Bildiri','{0} numarali kullanici kara listeye alindi'.format(self.numara),icon='info')
                con.close()
    def KaraListeCikar(self):
        self.numara = Ekle.gr7.get()
        cursor = con.cursor()
        cursor.execute("SELECT SURE FROM Kayitlar WHERE NUMARA = ?", (self.numara,))
        self.data1 = cursor.fetchall()
        self.data1=(str(self.data1).split("/"))
        if self.data1[0]=="[('K":
            cursor.execute('''UPDATE Kayitlar SET SURE = ? WHERE NUMARA = ?''', ("ÖĞRENCİ", self.numara))
            con.commit()
            messagebox.showinfo('Bildiri','{0} numarali kullanici kara listeden kaldirildi'.format(self.numara),icon='info')
        else:
            messagebox.showerror('Hata','{0} numarali kullanici kara listede değildir.'.format(self.numara),icon='warning')
        con.close()

islemler=islem()

def configuration():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    GPIO.output(11,GPIO.LOW)



    global pencere
    pencere.title("Kayıt programi")
    pencere.resizable(width=True, height=True)
    pencere.overrideredirect(False)
    #pencere.geometry("1200x1200+400+100")
    pencere.geometry("{0}x{1}+0+0".format(pencere.winfo_screenwidth(),pencere.winfo_screenheight()))
    pencere.focus_set()
    pencere.bind("<Escape>", lambda e: e.widget.quit())

    for frame in (f1, f2, f3,f4,f5):
        #frame.grid(row=0, column=0, sticky='news')
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    Ekle.Admingiris()
    Ekle.Menu()
    Ekle.Kullaniciekle()
    Ekle.Kullanicisil()
    Ekle.Kullanicigoruntule()

    ekran_degistir(f1)


f1=Frame(pencere)
f2=Frame(pencere)
f3=Frame(pencere)
f4=Frame(pencere)
f5=Frame(pencere)

class Eklentiler:
    cal,takvim=None,None

    def Admingiris(self):
        self.foto1 = PhotoImage(file="resim.gif")
        self.foto2 = PhotoImage(file="mekatronik.gif")
        self.foto3 = PhotoImage(file="image3.gif")
        self.gr1 = Entry(f1)
        self.gr2 = Entry(f1, show="*")



        Label(f1, image=self.foto1, height=590, width=590).grid(padx=0, pady=0)
        Label(f1, image=self.foto2, height=590, width=500).place(relx=0.6, rely=0, relheight=0.5, relwidth=0.5)
        Label(f1, image=self.foto3, height=590, width=590).place(relx=0.32, rely=0.48, relheight=0.4, relwidth=0.4)
        Button(f1,text='Giris',bg="green",font=("Comic Sans MS", 18),command=islemler.giriskontrol).place(relx=0.45, rely=0.31, relheight=0.05, relwidth=0.1)
        Label(f1,text="Kullanici Adi", font=("Comic Sans MS", 18), height=100,width=100).place(relx=0.45, rely=0.10, relheight=0.05, relwidth=0.1)
        self.gr1.place(relx=0.45, rely=0.15, relheight=0.05, relwidth=0.1)
        Label(f1,text="Parola", font=("Comic Sans MS", 18)).place(relx=0.45, rely=0.2, relheight=0.05, relwidth=0.1)
        Label(f1, text="KAAN KARADUMAN-OĞUZ AYTEKİN\n tarafından tasarlanmıştır.", font=("Comic Sans MS", 15)).place(relx=0.77, rely=0.88, relheight=0.1, relwidth=0.25)
        self.gr2.place(relx=0.45, rely=0.25, relheight=0.05, relwidth=0.1)

    def Menu(self):

        Button(f2, text='Kullanıcı Ekle', bg="green", font=("Comic Sans MS", 18),command=lambda:ekran_degistir(f3)).place(relx=0.005, rely=0.05, relheight=0.05, relwidth=0.1)
        Button(f2, text='Kullanıcı Sil/Kara Liste Ekle', bg="red", font=("Comic Sans MS", 18),command=lambda:ekran_degistir(f4)).place(relx=0.005, rely=0.12, relheight=0.05, relwidth=0.18)
        Button(f2, text='Kullanıcı Görüntüle', bg="yellow", font=("Comic Sans MS", 18),command=lambda :ekran_degistir(f5)).place(relx=0.005, rely=0.19, relheight=0.05,relwidth=0.13)
        Button(f2, text='Geri', bg="grey", font=("Comic Sans MS", 18), command=lambda: ekran_degistir(f1)).place(relx=0.005, rely=0.01, relheight=0.03, relwidth=0.05)

    def Kullaniciekle(self):

        def secim():
            if self.var.get() == 2:
                self.cal.config(state="normal")

            else:
                self.cal.config(state="disabled")
        self.var =IntVar()
        self.gr3=Entry(f3)
        self.gr4=Entry(f3)
        self.gr5=Entry(f3)
        self.gr6=Entry(f3)
        self.rd1= Radiobutton(f3,font=("Comic Sans MS", 18),text="Öğrenci",value=1,variable=self.var,command=secim)
        self.rd2= Radiobutton(f3,font=("Comic Sans MS", 18),text="Misafir Kullanıcı",value=2,variable=self.var,command=secim)
        self.cal= DateEntry(f3,state = "disabled")

        Label(f3, text="İsim:", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.08, rely=0.10,relheight=0.05,relwidth=0.07)
        Label(f3, text="Soyisim:", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.08, rely=0.17, relheight=0.05, relwidth=0.07)
        Label(f3, text="Numara:", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.08, rely=0.24,relheight=0.05, relwidth=0.07)
        Label(f3, text="Kart ID:", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.08, rely=0.31,relheight=0.05, relwidth=0.07)
        self.gr3.place(relx=0.17, rely=0.10, relheight=0.05, relwidth=0.1)
        self.gr4.place(relx=0.17, rely=0.17, relheight=0.05, relwidth=0.1)
        self.gr5.place(relx=0.17, rely=0.24, relheight=0.05, relwidth=0.1)
        self.gr6.place(relx=0.17, rely=0.31, relheight=0.05, relwidth=0.1)
        self.rd1.place(relx=0.12,rely=0.05)
        self.rd2.place(relx=0.20,rely=0.05)
        self.rd1.select()
        self.cal.place(relx=0.33,rely=0.06)
        Button(f3, text='Kaydet', bg="yellow", font=("Comic Sans MS", 18),command=islemler.kaydet).place(relx=0.08, rely=0.39,relheight=0.05,relwidth=0.1)
        Button(f3, text='Kart Okutunuz', bg="yellow", font=("Comic Sans MS", 18),command=islemler.kartoku).place(relx=0.2, rely=0.39, relheight=0.05,relwidth=0.1)
        Button(f3, text='Geri', bg="grey", font=("Comic Sans MS", 18), command=lambda:ekran_degistir(f2)).place(relx=0.01,rely=0.01, relheight=0.03,relwidth=0.1)
        Button(f3, text='Kamera Aç', bg="yellow", font=("Comic Sans MS", 18), command=islemler.kameraac).place(relx=0.32,rely=0.39,relheight=0.05,relwidth=0.1)
        #Button(f3, text='Resim Çek', bg="yellow", font=("Comic Sans MS", 18), command=islemler.resimcek).place(relx=0.44,rely=0.39,relheight=0.05,relwidth=0.1)

    def Kullanicisil(self):
        self.gr7=Entry(f4)
        Label(f4,text="Numara  :",font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.08, rely=0.10,relheight=0.05,relwidth=0.1)
        Label(f4,text="İsim       :", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.08, rely=0.17, relheight=0.05,relwidth=0.1)
        Label(f4,text="Soyisim  :", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.08, rely=0.24,relheight=0.05, relwidth=0.1)
        Label(f4,text="Kart ID  :", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.08, rely=0.31,relheight=0.05,relwidth=0.1)

        self.lb1=Label(f4, text="", font=("Comic Sans MS", 18))
        self.lb2=Label(f4, text="", font=("Comic Sans MS", 18))
        self.lb3 = Label(f4, text="", font=("Comic Sans MS", 18))

        self.lb1.place(relx=0.20, rely=0.17,relheight=0.05,relwidth=0.15)
        self.lb2.place(relx=0.20, rely=0.24,relheight=0.05,relwidth=0.15)
        self.lb3.place(relx=0.20, rely=0.31, relheight=0.05,relwidth=0.15)

        #Label(f4, text="-", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.17, rely=0.17,relheight=0.05,relwidth=0.1)
        #Label(f4, text="-", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.17, rely=0.24,relheight=0.05,relwidth=0.1)
        #Label(f4, text="-", font=("Comic Sans MS", 18), height=100, width=200).place(relx=0.17, rely=0.31, relheight=0.05,relwidth=0.1)
        self.gr7.place(relx=0.2, rely=0.11, relheight=0.03, relwidth=0.1)
        Button(f4, text='Sil', bg="red", font=("Comic Sans MS", 18), command=islemler.kullanicisil).place(relx=0.08, rely=0.39,relheight=0.05,relwidth=0.1)
        Button(f4, text='Getir', bg="yellow", font=("Comic Sans MS", 18), command=islemler.kullanicigetir).place(relx=0.2, rely=0.39,relheight=0.05,relwidth=0.1)
        Button(f4, text='Kara Listeye Ekle', bg="red", font=("Comic Sans MS", 18), command=islemler.KaraListeEkle).place(relx=0.16, rely=0.48, relheight=0.05, relwidth=0.15)
        Button(f4, text='Kara Listeden Kaldir', bg="green", font=("Comic Sans MS", 18),command=islemler.KaraListeCikar).place(relx=0.16, rely=0.54, relheight=0.05, relwidth=0.15)
        Button(f4, text='Geri', bg="grey", font=("Comic Sans MS", 18), command=lambda: ekran_degistir(f2)).place(relx=0.01, rely=0.01, relheight=0.03, relwidth=0.1)
        self.takvim = DateEntry(f4, state="normal")
        self.takvim.place(relx=0.08, rely=0.49)
    def Kullanicigoruntule(self):

        self.baslik=["AD","SOYAD","NUMARA","KART ID","SURE"]
        tree=ttk.Treeview(f5,column=self.baslik,show="headings")
        vsb = ttk.Scrollbar(f5,orient="vertical", command=tree.yview)
        vsb.place(x=1282, y=0, height=200 + 20)
        tree.configure(yscrollcommand=vsb.set)
        tree.heading('#1',text=self.baslik[0])
        tree.heading('#2', text=self.baslik[1])
        tree.heading('#3', text=self.baslik[2])
        tree.heading('#4', text=self.baslik[3])

        def sortby(tree, col, descending):
            """sort tree contents when a column header is clicked on"""
            # grab values to sort
            data = [(tree.set(child, col), child) \
                    for child in tree.get_children('')]
            # if the data to be sorted is numeric change to float
            # data =  change_numeric(data)
            # now sort the data in place
            data.sort(reverse=descending)
            for ix, item in enumerate(data):
                tree.move(item[1], '', ix)
                # switch the heading so it will sort in the opposite direction
                tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

        lbb=Label(f5, text="-",font=("Comic Sans MS", 18))
        lbb.place(relx=0.2, rely=0.22, relheight=0.03, relwidth=0.3)
        def guncelle():

            con = sqlite3.connect("OgrenciKayitlari.db")
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Kayitlar(AD TEXT,SOYAD TEXT,NUMARA TEXT,KARTID TEXT,SURE TEXT)")
            con.commit()
            cursor.execute("SELECT AD FROM Kayitlar")
            data1 = cursor.fetchall()
            cursor.execute("SELECT SOYAD FROM Kayitlar")
            data2 = cursor.fetchall()
            cursor.execute("SELECT NUMARA FROM Kayitlar")
            data3 = cursor.fetchall()
            cursor.execute("SELECT KARTID FROM Kayitlar")
            data4 = cursor.fetchall()
            cursor.execute("SELECT SURE FROM Kayitlar")
            data5 = cursor.fetchall()
            a = 0

            x = tree.get_children()
            if x !='()':
                for index in x:
                    tree.delete(index)

            for data in data1:
                tree.insert("", tk.END, values=(data, data2[a], data3[a], data4[a],data5[a]))
                a += 1
            lbb.config(text=str(a) + " Öğrenci Kayıtlıdır.")
            con.close()
        tree.place(relx=0.15,rely=0)
        guncelle()
        for col in self.baslik:
            tree.heading(col, text=col.title(), command=lambda c=col: sortby(tree, c, 0))
        Button(f5, text='Geri', bg="grey", font=("Comic Sans MS", 18), command=lambda: ekran_degistir(f2)).place(relx=0.01, rely=0.01, relheight=0.03, relwidth=0.1)
        Button(f5, text='Güncelle', bg="grey", font=("Comic Sans MS", 18), command=guncelle).place(relx=0.7, rely=0.01,relheight=0.03,relwidth=0.1)


Ekle=Eklentiler()
