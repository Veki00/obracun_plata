import sqlite3
from sqlite3 import Error

from main import create_connection

class Plata():
    def __init__(self, id_plata, id_zaposlenog, neto_plata, bruto_plata, mjesec):
        self.id_plata = id_plata
        self.id_zaposlenog = id_zaposlenog
        self.neto_plata = neto_plata
        self.bruto_plata = bruto_plata
        self.mjesec = mjesec

def create_plata(conn, plata):
    try:
        sql = """INSERT INTO Plata (ID, IDZaposlenog, Neto, Bruto, Mjesec) VALUES(?,?,?,?,?)"""
        cur = conn.cursor()
        params = (plata.id_plata, plata.id_zaposlenog, plata.neto_plata, plata.bruto_plata, plata.mjesec)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def update_plata(conn, plata):
    try:
        sql = """UPDATE Plata SET Neto=?, Bruto=?, Mjesec=? WHERE IDZaposlenog=?"""
        cur = conn.cursor()
        params = (plata.neto_plata, plata.bruto_plata, plata.mjesec, plata.id_zaposlenog)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def select_ime_zaposlenog(conn, IDzaposlenog):
    try:
        cur = conn.cursor()
        cur.execute("SELECT Ime FROM Zaposleni WHERE IDZaposlenog=?", (id_zaposlenog,))
        ime = cur.fetchone()[0]
        return ime
    except Error as e:
        print(e)

def select_all_plata(conn):
    sql = """SELECT * FROM Plata;"""
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    return ans
def select_zaposleni_plata(conn, id_zaposlenog):
    try:
        sql = """SELECT * FROM Plata WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        ans = cur.fetchone()
        return ans
    except Error as e:
        print(e)

def delete_zaposleni_plata(con, id_zaposlenog):
    try:
        sql = """DELETE FROM Plata WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        conn.commit()
    except Error as e:
        print(e)

conn = create_connection("obracun_plata.db")
if conn is not None:
    while True:
        izbor = int(input("Unesite 0 za kraj programa PLATA, 1 za novi unos PLATE, 2 za azuriranje PLATE: "))
        if izbor == 0:
            break
        elif izbor == 1:
            id_plata = int(input("Unesite ID plate:"))
            id_zaposlenog = int(input("Unesite ID zaposlenog:"))
            neto_plata = float(input("Unesite neto platu:"))
            bruto_plata = float(input("Unesite bruto platu:"))
            mjesec = input("Unesite mjesec:")
            p = Plata(id_plata, id_zaposlenog, neto_plata, bruto_plata, mjesec)
            create_plata(conn, p)
            ime_zaposlenog = select_ime_zaposlenog(conn, id_zaposlenog)
            print(f"Informacije o plati za zaposlenog {ime_zaposlenog} uspjesno sacuvane u bazu")

        elif izbor == 2:
            id_zaposlenog = int(input("Unesite ID zaposlenog kojem zelite promijeniti platu: "))

            plata = None
            ans = select_all_plata(conn)
            for a in ans:
                if a[1] == id_zaposlenog:
                    plata = Plata(a[0], a[1], a[2], a[3], a[4])
                    break

            if plata is not None:
                print("Unesite nove podatke o plati")
                id_plata = int(input("ID plate:"))
                neto_plata = int(input("Neto plata:"))
                bruto_plata = int(input("Bruto plata:"))
                mjesec = input("Mjesec:")

                if id_plata:
                    plata.id_plata = id_plata
                if neto_plata:
                    plata.neto_plata = neto_plata
                if bruto_plata:
                    plata.bruto_plata = bruto_plata
                if mjesec:
                    plata.mjesec = mjesec
                update_plata(conn, plata)
                print("Uspjesno azurirani podaci")
            else:
                print("Zaposleni sa tim ID-em ne postoji")

        elif izbor == 3:
            id_zaposlenog = int(input("Unesite ID zaposlenog kojem zelite obrisati podatke o PLATI:"))
            plata = select_zaposleni_plata(conn, id_zaposlenog)
            if plata is not None:
                delete_zaposleni_plata(conn, id_zaposlenog)
                print("PLATA zaposlenog je obrisana")
            else:
                print("Zaposleni sa tim ID-em ne postoji u bazi")
else:
    print("Error! Cannot create the database connection.")


