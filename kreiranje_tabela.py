import sqlite3


conn = sqlite3.connect("obracun_plata.db")


cursor = conn.cursor()

# Kreiranje tabele "Zaposleni"
cursor.execute("""CREATE TABLE Zaposleni (
               IDZaposlenog INTEGER PRIMARY KEY,
               Ime CHAR(15), 
               Prezime CHAR(15), 
               RadnoMjesto CHAR(30), 
               Satnica FLOAT, 
               BrojSati FLOAT)""")

# Kreiranje tabele "Plata"
cursor.execute("""CREATE TABLE Plata (
                ID INTEGER PRIMARY KEY, 
                IDZaposlenog INTEGER, 
                Neto REAL, 
                Bruto REAL, 
                Mjesec TEXT, 
                FOREIGN KEY (IDZaposlenog) REFERENCES Zaposleni(ID))""")

# Kreiranje tabele "Troskovi"
cursor.execute("""CREATE TABLE Troskovi (
                ID INTEGER PRIMARY KEY, 
                IDZaposlenog INTEGER, 
                ZdravstvenoOsiguranje REAL, 
                PenzioniFond REAL, 
                FondSolidarnosti REAL, 
                FOREIGN KEY (IDZaposlenog) REFERENCES Zaposleni(ID))""")

# Kreiranje tabele "Bonus"
cursor.execute("""CREATE TABLE Bonus (
                ID INTEGER PRIMARY KEY, 
                Opis TEXT, 
                Iznos REAL, 
                IDZaposlenog INTEGER, 
                FOREIGN KEY (IDZaposlenog) REFERENCES Zaposleni(ID))""")

# Kreiranje tabele "Izvjestaj"
cursor.execute("""CREATE TABLE Izvjestaj (
                ID INTEGER PRIMARY KEY, 
                Mjesec TEXT, 
                IznosPlate REAL, 
                Bonusi REAL, 
                UkupniTroskovi REAL, 
                IDZaposlenog INTEGER, 
                FOREIGN KEY (IDZaposlenog) REFERENCES Zaposleni(ID))""")


conn.commit()

conn.close()