import sqlite3


conn = sqlite3.connect("obracun_plata.db")


cursor = conn.cursor()

print(cursor.execute(""" DELETE FROM Izvjestaj WHERE ID>0 and ID<6"""))



conn.commit()

conn.close()