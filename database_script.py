#import module
import sqlite3
import pprint

#open Connection
connection = sqlite3.connect('golibrary.db')
cursor=connection.cursor()

#create Table
cursor.execute("""select * from user""")
data=cursor.fetchall()
pprint.pprint(data)

cursor.execute("""select * from pustakawan""")
data=cursor.fetchall()
pprint.pprint(data)

cursor.execute("""select * from meminjam""")
data=cursor.fetchall()
pprint.pprint(data)

cursor.execute("""select * from mengembalikan""")
data=cursor.fetchall()
pprint.pprint(data)

#commit command
connection.commit()


#close connection
connection.close()
