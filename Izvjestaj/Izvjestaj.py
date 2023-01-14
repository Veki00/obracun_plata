import sqlite3
from sqlite3 import Error
import random
from selects import *
from PDFcreator import napravi_pdf

class Izvjestaj():
    def __init__(self, ID, mjesec, iznos_plate, bonusi, ukupni_troskovi, id_zaposlenog):
        self.ID = ID
        self.mjesec = mjesec
        self.iznos_plate = iznos_plate
        self.bonusi = bonusi
        self.ukupni_troskovi =ukupni_troskovi
        self.id_zaposlenog = id_zaposlenog

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_izvjestaj(conn, izvjestaj):
    try:
        sql = """INSERT INTO Izvjestaj (ID, Mjesec, IznosPlate, Bonusi, UkupniTroskovi, IDZaposlenog) VALUES(?,?,?,?,?,?)"""
        cur = conn.cursor()
        params = (izvjestaj.ID, izvjestaj.mjesec, izvjestaj.iznos_plate, izvjestaj.bonusi, izvjestaj.ukupni_troskovi, izvjestaj.id_zaposlenog)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def delete_izvjestaj(con, id_zaposlenog):
    try:
        sql = """DELETE FROM Izvjestaj WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        conn.commit()
    except Error as e:
        print(e)


conn = create_connection("../obracun_plata.db")
if conn is not None:
    while True:
        izbor = int(input("Ako zelite da kreirate IZVJESTAJ unesite 1, za brisanje IZVJESTAJA unesite 2, \n"
                          'a za prekidanje programa "kreiranja izvjestaja" i prelazak na kreiranje PDF fajla unesite 0: '))
        if izbor == 0:
            break
        #Kreiranje izvjestaja
        elif izbor == 1:
            id_zaposlenog = int(input("Unesite ID zaposlenog za kojeg zelite kreirati izvjestaj: "))
            ID = random.randint(1,999)
            mjesec = select_plata_mjesec(conn, id_zaposlenog)
            iznos_plate = select_iznos_plate(conn, id_zaposlenog)
            bonusi = select_bonus(conn, id_zaposlenog)
            ukupni_troskovi = select_ukupni_troskovi(conn, id_zaposlenog)
            izvjestaj = Izvjestaj(ID, mjesec, iznos_plate, bonusi, ukupni_troskovi, id_zaposlenog)
            create_izvjestaj(conn, izvjestaj)
            ime_zaposlenog = select_ime_zaposlenog(conn, id_zaposlenog)
            print(f"Izvjestaj za zaposlenog {ime_zaposlenog} je uspjesno kreiran")

        #Brisanje izvjestaja
        elif izbor == 2:
            id_zaposlenog = int(input("Unesite ID zaposlenog kojem zelite izbrisati izvjestaj"))
            delete_izvjestaj(conn, id_zaposlenog)
            ime_zaposlenog = select_ime_zaposlenog(conn, id_zaposlenog)
            print(f"Izvjestaj zaposlenog {ime_zaposlenog} uspjesno izbrisan")

    #Pravljenje PDF fajla
    while True:
        print(f"Da li zelite da napravite PDF izvjestaj?")
        print("(Ako zelite napraviti PDF izvjestaj za odredjenog korisnika unesite Y, za prekid programa unesite N)")
        pdf = input("Y/N: ")

        if pdf == 'Y' or pdf == 'y':
            napravi_pdf()
            print("PDF izvjestaj uspjesno kreiran")
        elif pdf == 'N' or pdf == 'n':
            print("Program uspjesno zavrsen")
            break


else:
    print("Error! Cannot create the database connection.")