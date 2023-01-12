import sqlite3
from sqlite3 import Error

class Zaposleni():
    def __init__(self, idzaposlenog, ime, prezime, radno_mjesto, satnica, broj_sati):
        self.idzaposlenog = idzaposlenog
        self.ime = ime
        self.prezime = prezime
        self.radno_mjesto = radno_mjesto
        self.satnica = satnica
        self.broj_sati = broj_sati

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

#Dodaje novog zaposlenog u tabelu ZAPOSLENI
def create_zaposleni(conn, zaposleni):
    try:
        sql = """INSERT INTO Zaposleni (IDZaposlenog, Ime, Prezime, RadnoMjesto, Satnica, BrojSati) VALUES(?,?,?,?,?,?)"""
        cur = conn.cursor()
        params = (zaposleni.idzaposlenog, zaposleni.ime, zaposleni.prezime, zaposleni.radno_mjesto, zaposleni.satnica, zaposleni.broj_sati)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def update_zaposleni(conn, zaposleni):
    try:
        sql = f"""UPDATE Zaposleni SET Ime = ?, Prezime = ?, RadnoMjesto = ?,
        Satnica = ?, BrojSati = ? WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        params = (zaposleni.ime, zaposleni.prezime, zaposleni.radno_mjesto, zaposleni.satnica, zaposleni.broj_sati, zaposleni.idzaposlenog)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def delete_zaposleni(con, id_zaposlenog):
    try:
        sql = """DELETE FROM Zaposleni WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        conn.commit()
    except Error as e:
        print(e)
def select_all_zaposleni(conn):
        sql = """SELECT * FROM Zaposleni;"""
        cur = conn.cursor()
        cur.execute(sql)
        ans = cur.fetchall()
        return ans
def select_zaposleni(conn, id_zaposlenog):
    try:
        sql = """SELECT * FROM Zaposleni WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        ans = cur.fetchone()
        return ans
    except Error as e:
        print(e)

conn = create_connection("obracun_plata.db")
if conn is not None:
    while True:
        izbor = int(input("Unesite 0 za kraj programa ZAPOSLENI, 1 za unos novog ZAPOSLENOG, 2 za azuriranje ZAPOSLENOG, 3 za brisanje ZAPOSLENOG  :"))

        if izbor == 0:
            break
        #Unosenje novog zaposlenog u tabelu Zaposleni
        elif izbor == 1:
            id_zaposlenog = int(input("Unesite ID zaposlenog:"))
            ime_zaposlenog = input("Unesite ime zaposlenog:")
            prezime_zaposlenog = input("Unesite prezime zaposlenog:")
            radno_mjesto_zaposlenog = input("Unesite radno mjesto zaposlenog:")
            satnica_zaposlenog = input("Unesite satnica zaposlenog:")
            broj_sati_zaposlenog = input("Unesite broj sati zaposlenog:")
            z = Zaposleni(id_zaposlenog, ime_zaposlenog, prezime_zaposlenog,
                          radno_mjesto_zaposlenog, satnica_zaposlenog, broj_sati_zaposlenog)
            create_zaposleni(conn, z)

        #Azuriranje podataka zaposlenog
        elif izbor == 2:
            id_zaposlenog = int(input("Unesite ID zaposlenog kojeg zelite da azurirate: "))

            zaposleni = None
            ans = select_all_zaposleni(conn)
            for a in ans:
                if a[0] == id_zaposlenog:
                    zaposleni = Zaposleni(a[0], a[1], a[2], a[3], a[4], a[5])
                    break

            if zaposleni is not None:

                print("Unesite nove podatke o zaposlenom:")
                ime_zaposlenog = input("Ime (ostavite prazno ako ne želite da mijenjate):")
                prezime_zaposlenog = input("Prezime (ostavite prazno ako ne želite da mijenjate):")
                radno_mjesto_zaposlenog = input("Radno mjesto (ostavite prazno ako ne želite da mijenjate):")
                satnica_zaposlenog = input("Satnica (ostavite prazno ako ne želite da mijenjate):")
                broj_sati_zaposlenog = input("Broj sati (ostavite prazno ako ne želite da mijenjate):")

                if ime_zaposlenog:
                    zaposleni.ime = ime_zaposlenog
                if prezime_zaposlenog:
                    zaposleni.prezime = prezime_zaposlenog
                if radno_mjesto_zaposlenog:
                    zaposleni.radno_mjesto = radno_mjesto_zaposlenog
                if satnica_zaposlenog:
                    zaposleni.satnica = satnica_zaposlenog
                if broj_sati_zaposlenog:
                    zaposleni.broj_sati = broj_sati_zaposlenog

                update_zaposleni(conn, zaposleni)
                print("Podaci o zaposlenom su ažurirani.")
            else:
                print("Zaposleni sa unijeti ID-em ne postoji.")

        # Brisanje zaposlenog iz tabele
        elif izbor == 3:
            id_zaposlenog = int(input("Unesite ID zaposlenog kojeg zelite da obrisete:"))
            zaposleni = select_zaposleni(conn, id_zaposlenog)
            if zaposleni is not None:
                delete_zaposleni(conn, id_zaposlenog)
                print("Zaposleni je obrisan")
            else:
                print("Zaposleni sa tim ID-em ne postoji u bazi")
else:
    print("Error! Cannot create the database connection.")




