import sqlite3
from sqlite3 import Error


class Troskovi():
    def __init__(self, id_troskovi, id_zaposlenog, zdrav_osiguranje, penzioni_fond, fond_solidarnosti):
        self.id_troskovi = id_troskovi
        self.id_zaposlenog = id_zaposlenog
        self.zdrav_osiguranje = zdrav_osiguranje
        self.penzioni_fond = penzioni_fond
        self.fond_solidarnosti = fond_solidarnosti

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
def create_troskovi(conn, troskovi):
    try:
        sql = """INSERT INTO Troskovi (ID, IDZaposlenog, ZdravstvenoOsiguranje, PenzioniFond, FondSolidarnosti) VALUES(?,?,?,?,?)"""
        cur = conn.cursor()
        params = (troskovi.id_troskovi, troskovi.id_zaposlenog, troskovi.zdrav_osiguranje, troskovi.penzioni_fond, troskovi.fond_solidarnosti)
        cur.execute(sql, params)
        conn.commit()
    except Error as e:
        print(e)

def update_troskovi(conn, troskovi):
    try:
        sql = """UPDATE Troskovi SET ID=?, ZdravstvenoOsiguranje=?, PenzioniFond=?, FondSolidarnosti=? WHERE IDZaposlenog=?"""
        cur = conn.cursor()
        params = (troskovi.id_troskovi, troskovi.zdrav_osiguranje, troskovi.penzioni_fond, troskovi.fond_solidarnosti, troskovi.id_zaposlenog,)
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

def select_all_troskovi(conn):
    sql = """SELECT * FROM Troskovi;"""
    cur = conn.cursor()
    cur.execute(sql)
    ans = cur.fetchall()
    return ans

def select_zaposleni_troskovi(conn, id_zaposlenog):
    try:
        sql = """SELECT * FROM Troskovi WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        ans = cur.fetchone()
        return ans
    except Error as e:
        print(e)

def delete_zaposleni_troskovi(con, id_zaposlenog):
    try:
        sql = """DELETE FROM Troskovi WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        conn.commit()
    except Error as e:
        print(e)

conn = create_connection("obracun_plata.db")
if conn is not None:
    while True:
        izbor = int(input("Unesite 0 za kraj programa TROSKOVI, 1 za novi unos TROSKOVI, 2 za azuriranje TROSKOVI, 3 za brisanje podataka o TROSKOVI: "))
        if izbor == 0:
            break
        elif izbor == 1:
            id_troskovi = int(input("Unesite ID troskova:"))
            id_zaposlenog = int(input("Unesite ID zaposlenog:"))
            zdrav_osiguranje = float(input("Unesite iznos za zdravstveno osiguranje:"))
            penzioni_fond = float(input("Unesite iznos za penzioni fond:"))
            fond_solidarnosti = int(input("Unesite iznos za fond solidarnosti:"))
            t = Troskovi(id_troskovi, id_zaposlenog, zdrav_osiguranje, penzioni_fond, fond_solidarnosti)
            create_troskovi(conn, t)
            ime_zaposlenog = select_ime_zaposlenog(conn, id_zaposlenog)
            print(f"Informacije o troskovima na platu za zaposlenog {ime_zaposlenog} uspjesno sacuvane u bazu")

        elif izbor == 2:
            id_zaposlenog = int(input("Unesite ID zaposlenog kojem zelite promijeniti iznos TROSKOVA na platu: "))

            troskovi = None
            ans = select_all_troskovi(conn)
            for a in ans:
                if a[1] == id_zaposlenog:
                    troskovi = Troskovi(a[0], a[1], a[2], a[3], a[4])
                    break

            if troskovi is not None:
                print("Unesite nove podatke o TROSKOVIMA")
                id_troskovi = int(input("ID troskova:"))
                zdrav_osiguranje = input("Iznos za zdravstveno osiguranje:")
                penzioni_fond = input("Iznos za penzioni fond:")
                fond_solidarnosti = input("Fond solidarnosti:")

                if id_troskovi:
                    troskovi.id_troskovi = id_troskovi
                if zdrav_osiguranje:
                    troskovi.zdrav_osiguranje = zdrav_osiguranje
                if penzioni_fond:
                    troskovi.penzioni_fond = penzioni_fond
                if fond_solidarnosti:
                    troskovi.fond_solidarnosti = fond_solidarnosti
                update_troskovi(conn, troskovi)
                print("Uspjesno azurirani podaci")
            else:
                print("Zaposleni sa tim ID-em ne postoji")

        elif izbor == 3:
            id_zaposlenog = int(input("Unesite ID zaposlenog kojem zelite obrisati podatke o TROSKOVIMA:"))
            plata = select_zaposleni_troskovi(conn, id_zaposlenog)
            if plata is not None:
                delete_zaposleni_troskovi(conn, id_zaposlenog)
                print("TROSKOVI zaposlenog su obrisania")
            else:
                print("Zaposleni sa tim ID-em ne postoji u bazi")
else:
    print("Error! Cannot create the database connection.")