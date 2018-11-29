#import module
import sqlite3
import pprint

#open Connection
connection = sqlite3.connect('golibrary.db')
cursor=connection.cursor()

#create Table
cursor.execute("""Select * From User""")
data=cursor.fetchall()
print("Table User")
pprint.pprint(data)
print()

cursor.execute("""Select * From Pustakawan""")
data=cursor.fetchall()
print("Table Pustakawan")
pprint.pprint(data)
print()

cursor.execute("""Select * From Buku""")
data=cursor.fetchall()
print("Table Buku")
pprint.pprint(data)
print()

cursor.execute("""Select * From Meminjam""")
data=cursor.fetchall()
print("Table Meminjam")
pprint.pprint(data)
print()

cursor.execute("""Select * From Mengembalikan""")
data=cursor.fetchall()
print("Table Mengembalikan")
pprint.pprint(data)
print()

cursor.execute("""Select * From Antrian""")
data=cursor.fetchall()
print("Table Antrian")
pprint.pprint(data)
print()

#commit command
connection.commit()


#close connection
connection.close()
