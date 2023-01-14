from sqlite3 import Error

# Ovdje se nalaze vrijednosti koje u selektovane iz baze
def select_ime_zaposlenog(conn, id_zaposlenog):
    try:
        cur = conn.cursor()
        cur.execute("SELECT Ime FROM Zaposleni WHERE IDZaposlenog=?", (id_zaposlenog,))
        ime = cur.fetchone()[0]
        return ime
    except Error as e:
        print(e)

def select_plata_mjesec(conn, id_zaposlenog):
    try:
        cur = conn.cursor()
        cur.execute("SELECT Mjesec FROM Plata WHERE IDZaposlenog=?", (id_zaposlenog,))
        ans = cur.fetchone()[0]
        return ans
    except Error as e:
        print(e)

def select_iznos_plate(conn, id_zaposlenog):
    try:
        cur = conn.cursor()
        cur.execute("SELECT Neto FROM Plata WHERE IDZaposlenog=?", (id_zaposlenog,))
        ans = cur.fetchone()[0]
        return ans
    except Error as e:
        print(e)

def select_bonus(conn, id_zaposlenog):
    try:
        cur = conn.cursor()
        cur.execute("SELECT Iznos FROM Bonus WHERE IDZaposlenog=?", (id_zaposlenog,))
        ans = cur.fetchone()[0]
        return ans
    except Error as e:
        print(e)

def select_ukupni_troskovi(conn, id_zaposlenog):
    try:
        sql = """ SELECT (ZdravstvenoOsiguranje + PenzioniFond + FondSolidarnosti) AS total 
                                FROM Troskovi WHERE IDZaposlenog = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_zaposlenog,))
        ans = cur.fetchone()[0]
        return ans
    except Error as e:
        print(e)

def select_bruto(conn, id_zaposlenog):
    try:
        cur = conn.cursor()
        cur.execute("SELECT Bruto FROM Plata WHERE IDZaposlenog=?", (id_zaposlenog,))
        ans = cur.fetchone()[0]
        return ans
    except Error as e:
        print(e)

def select_prezime(conn, id_zaposlenog):
    try:
        cur = conn.cursor()
        cur.execute("SELECT Prezime FROM Zaposleni WHERE IDZaposlenog=?", (id_zaposlenog,))
        ans = cur.fetchone()[0]
        return ans
    except Error as e:
        print(e)
