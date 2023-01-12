import sqlite3
from sqlite3 import Error

from main import create_connection

class Bonus():
    def __init__(self, id_bonusa, opis, iznos, id_zaposlenog):
        self.id_bonusa = id_bonusa
        self.opis = opis
        self.iznos = iznos
        self.id_zaposlenog = id_zaposlenog

def create_bonus(conn, bonus):
    try:
        sql = """INSERT INTO Bonus (ID, Opis, Iznos, IDZaposlenog) VALUES(?,?,?,?)"""
        cur = conn.cursor()
        params = (bonus.id_bonusa, bonus.opis, bonus.iznos, bonus.id_zaposlenog)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def update_bonus(conn, bonus):
    try:
        sql = """UPDATE Bonus SET ID=?, Opis=?, Iznos=? WHERE IDZaposlenog=?"""
        cur = conn.cursor()
        params = (bonus.id_bonusa, bonus.opis, bonus.iznos, bonus.id_zaposlenog)
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

def select_all_bonus(conn):
    sql = """SELECT * FROM Bonus;"""
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    return ans

def select_zaposleni_bonus(conn, id_zaposlenog):
    try:
        sql = """SELECT * FROM Bonus WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        ans = cur.fetchone()
        return ans
    except Error as e:
        print(e)

def delete_zaposleni_bonus(con, id_zaposlenog):
    try:
        sql = """DELETE FROM Bonus WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        conn.commit()
    except Error as e:
        print(e)

conn = create_connection("obracun_plata.db")
if conn is not None:
    while True:
        izbor = int(input("Unesite 0 za kraj programa BONUS, 1 za novi unos BONUSA, 2 za azuriranje BONUSA, 3 za brisanje BONUSA: "))
        if izbor == 0:
            break
        elif izbor == 1:
            id_bonusa = int(input("Unesite ID bonusa:"))
            opis = input("Unesite opis bonusa na platu:")
            iznos = float(input("Unesite iznos bonusa na platu:"))
            id_zaposlenog = int(input("Unesite ID zaposlenog:"))
            b = Bonus(id_bonusa, opis, iznos, id_zaposlenog)
            create_bonus(conn, b)

            ime_zaposlenog = select_ime_zaposlenog(conn, id_zaposlenog)
            print(f"Informacije o bonusu na platu za zaposlenog {ime_zaposlenog} uspjesno sacuvane u bazu")

        elif izbor == 2:
            id_zaposlenog = int(input("Unesite ID zaposlenog kojem zelite promijeniti bonus na platu: "))

            bonus = None
            ans = select_all_bonus(conn)
            for a in ans:
                if a[3] == id_zaposlenog:
                    bonus = Bonus(a[0], a[1], a[2], a[3])
                    break

            if bonus is not None:
                print("Unesite nove podatke o bonusu na platu zaposlenog")
                id_bonus = int(input("ID bonusa:"))
                opis = input("Opis bonusa:")
                iznos = int(input("Iznos bonusa:"))

                if id_bonus:
                    bonus.id_bonus = id_bonus
                if opis:
                    bonus.opis = opis
                if iznos:
                    bonus.iznos = iznos
                if id_zaposlenog:
                    bonus.id_zaposlenog = id_zaposlenog
                update_bonus(conn, bonus)
                print("Uspjesno azurirani podaci")
            else:
                print("Zaposleni sa tim ID-em ne postoji")

        elif izbor == 3:
            id_zaposlenog = int(input("Unesite ID zaposlenog kojem zelite obrisati podatke o BONUSU na platu:"))
            plata = select_zaposleni_bonus(conn, id_zaposlenog)
            if plata is not None:
                delete_zaposleni_bonus(conn, id_zaposlenog)
                print("BONUS zaposlenog je obrisan")
            else:
                print("Zaposleni sa tim ID-em ne postoji u bazi")
else:
    print("Error! Cannot create the database connection.")