import jinja2
import pdfkit
import random
import sqlite3
from datetime import datetime
from selects import *

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

# Kod u nastavku kreira izvjestaj u PDF formatu na osnovu podataka u bazi
conn = create_connection("../obracun_plata.db")
if conn is not None:
    def napravi_pdf():
        id_zaposlenog = int(input("Unesite ID zaposlenog kojem zelite stampati izvjestaj o plati"))
        ime = select_ime_zaposlenog(conn, id_zaposlenog)
        prezime = select_prezime(conn, id_zaposlenog)
        ID = id_zaposlenog
        IznosPlate = select_iznos_plate(conn, id_zaposlenog)
        Bonusi = select_bonus(conn, id_zaposlenog)
        UkupniTroskovi = select_ukupni_troskovi(conn, id_zaposlenog)
        broj_izvjestaja = random.randint(100000, 1000000)
        mjesec = select_plata_mjesec(conn, id_zaposlenog)
        Bruto = select_bruto(conn, id_zaposlenog)

        today_date = datetime.today().strftime("%d %b, %Y")
        context = {'ime': ime,'prezime': prezime, 'today_date': today_date, 'ID':ID,
                    'broj_izvjestaja': broj_izvjestaja, 'mjesec': mjesec,
                    'Bruto': f'{Bruto:.2f}',
                    'IznosPlate': f'{IznosPlate:.2f}',
                    'Bonusi': f'{Bonusi:.2f}',
                    'UkupniTroskovi': f'{UkupniTroskovi:.2f}'
                   }
        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)
        html_template = 'template.html'
        template = template_env.get_template(html_template)
        output_text = template.render(context)
        config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
        output_pdf = f'Kolekcija_izvjestaja/Izvjestaj -{select_ime_zaposlenog(conn,id_zaposlenog)}_{select_prezime(conn, id_zaposlenog)}.pdf'
        pdfkit.from_string(output_text, output_pdf, configuration=config, css='template.css')

else:
    print("Error! Cannot create the database connection.")