#import module
import sqlite3
import os.path

if os.path.exists("golibrary.db"):
	os.remove("golibrary.db")

#open Connection
connection = sqlite3.connect('golibrary.db')
cursor=connection.cursor()

#create Table
cursor.execute('''CREATE TABLE antrian (
  ISBN varchar(20) NOT NULL,
  Username varchar(50) NOT NULL,
  Nomor_Antrian int(3) NOT NULL,
  PRIMARY KEY (Nomor_Antrian,Username,ISBN)
);''')

cursor.execute('''CREATE TABLE buku (
  ISBN varchar(20) NOT NULL,
  Judul varchar(50) NOT NULL,
  Pengarang varchar(25) NOT NULL,
  Penerbit varchar(35) NOT NULL,
  Lokasi_Buku varchar(6) NOT NULL,
  Genre varchar(25) NOT NULL,
  Tahun_Terbit year(4) NOT NULL,
  Review varchar(35) NOT NULL,
  Rating int(5) NOT NULL,
  Stok int(5) NOT NULL,
  PRIMARY KEY (ISBN)
);''')

cursor.execute('''INSERT INTO buku VALUES ("112221","The Return of The King","Tolkien","Toko Buku","1","Fantasy","2004","-","-",5)''')
cursor.execute('''INSERT INTO buku VALUES ("331113","The Two Towers","Tolkien","Toko Buku","1","Fantasy","2002","-","-",1)''')
cursor.execute('''INSERT INTO buku VALUES ("223332","The Fellowship of The Ring","Tolkien","Toko Buku","1","Fantasy","2000","-","-",3)''')
connection.commit()

cursor.execute('''CREATE TABLE copy_buku (
  ID_Kopi_Buku varchar(35) NOT NULL,
  ISBN varchar(20) NOT NULL,
  PRIMARY KEY (ID_Kopi_Buku,ISBN)
);''')

cursor.execute('''CREATE TABLE meminjam (
  ISBN varchar(20) NOT NULL,
  Username varchar(35) NOT NULL,
  Tanggal_pengembalian date NOT NULL,
  PRIMARY KEY (ISBN,Username)
);''')

cursor.execute('''CREATE TABLE mengembalikan (
  ISBN varchar(35) NOT NULL,
  Username varchar(35) NOT NULL,
  Tanggal_pengembalian date NOT NULL
);''')

cursor.execute('''CREATE TABLE pustakawan (
  Username varchar(35) NOT NULL,
  Name varchar(50) NOT NULL,
  Pass varchar(35) NOT NULL,
  PRIMARY KEY (Username)
);''')

cursor.execute('''INSERT INTO pustakawan VALUES ("admin","admin","admin")''')
connection.commit()

cursor.execute('''CREATE TABLE user (
  Username varchar(40) NOT NULL,
  Password varchar(30) NOT NULL DEFAULT 'admin1234',
  Universitas varchar(25) NOT NULL,
  Nama varchar(25) NOT NULL,
  TempatTanggalLahir varchar(25) NOT NULL,
  PRIMARY KEY (Username)
);''')

cursor.execute('''INSERT INTO user VALUES ("deryan","deryan","ITB","Deryan","New York, 1 Januari 1998")''')
cursor.execute('''INSERT INTO user VALUES ("athur","athur","ITB","Athur","New York, 2 Januari 1998")''')
cursor.execute('''INSERT INTO user VALUES ("varrel","varrel","ITB","Varrel","New York, 3 Januari 1998")''')
cursor.execute('''INSERT INTO user VALUES ("aisyah","aisyah","ITB","Aisyah","New York, 4 Januari 1998")''')
cursor.execute('''INSERT INTO user VALUES ("ambar","ambar","ITB","Ambar","New York, 5 Januari 1998")''')
cursor.execute('''INSERT INTO user VALUES ("roy","roy","ITB","Roy","New York, 6 Januari 1998")''')

connection.commit()

#commit command
connection.commit()


#close connection
connection.close()
