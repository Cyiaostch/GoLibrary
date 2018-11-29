from flask import Flask, render_template, redirect, request
import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import sqlite3

app = Flask(__name__)

connection = sqlite3.connect('golibrary.db')

cursor = connection.cursor()

session = dict()
session['user']=str()

#----------------------------------USER---------------------------------

#Login
@app.route('/')
def login():
	return render_template("login.html")

#ausdfiasdf
@app.route('/handleLogin/')
def handleLogin():
	username =  request.args.get('username')
	password = request.args.get('password')
	
	
	cursor.execute("""SELECT * FROM user WHERE Username='{}' AND Password='{}'""".format(username,password))
	result=cursor.fetchall()
	
	if(len(result)==0):
		return render_template("login.html")
	else:
		session['user']=username
		cursor.execute("""SELECT buku.judul, temp.Tanggal_pengembalian  FROM buku INNER JOIN (SELECT * FROM user INNER JOIN meminjam on user.Username=meminjam.Username WHERE user.Username='{}') as temp ON buku.ISBN=temp.ISBN;""".format(session["user"]))
		result=cursor.fetchall()
		result=[[value[0],value[1][:10],"Sedang Meminjam"] for value in result]
		
		cursor.execute("""SELECT buku.judul, temp.Nomor_Antrian FROM Buku INNER JOIN (SELECT * FROM User INNER JOIN Antrian on User.Username=Antrian.Username WHERE User.Username='{}') as temp ON buku.ISBN=temp.ISBN;""".format(session["user"]))
		result_2=cursor.fetchall()
		result_2=[[value[0],"Antrian "+str(value[1]),"Mengantri"] for value in result_2]
				
		return render_template("homepage.html",data=result,data_2=result_2)

#Register
@app.route('/register/')
def register():
	return render_template("register.html")

@app.route('/handleRegister/')
def handleRegister():
	username =  request.args.get('username')
	password = request.args.get('password')
	nama = request.args.get('nama')
	universitas = request.args.get('universitas')
	ttl = request.args.get('ttl')
	
	try:
		cursor.execute('''INSERT INTO user VALUES ("{}","{}","{}","{}","{}")'''.format(username,password,universitas,nama,ttl))
		connection.commit()
	except sqlite3.IntegrityError:
		pass
	
	return render_template("register.html") 

#Homepage
@app.route('/home/')
def homepage():
	cursor.execute("""SELECT buku.judul, temp.Tanggal_pengembalian  FROM buku INNER JOIN (SELECT * FROM user INNER JOIN meminjam on user.Username=meminjam.Username WHERE user.Username='{}') as temp ON buku.ISBN=temp.ISBN;""".format(session["user"]))
	result=cursor.fetchall()
	result=[[value[0],value[1][:10],"Sedang Meminjam"] for value in result]
	
	cursor.execute("""SELECT buku.judul, temp.Nomor_Antrian FROM Buku INNER JOIN (SELECT * FROM User INNER JOIN Antrian on User.Username=Antrian.Username WHERE User.Username='{}') as temp ON buku.ISBN=temp.ISBN;""".format(session["user"]))
	result_2=cursor.fetchall()
	result_2=[[value[0],"Antrian "+ str(value[1]),"Mengantri"] for value in result_2]
				
	
	return render_template("homepage.html",data=result, data_2=result_2)

#Logout
@app.route('/logout/')
def logout():
	return render_template("login.html")
	
#Search
@app.route('/searchResult/')
def searchResult():
	query =  request.args.get('query')
		
	cursor.execute("""SELECT * FROM buku WHERE Judul LIKE '%{}%'""".format(query))
	result=cursor.fetchall()
	
	#isbn, judul, pengarang, penerbit, lokasiBuku, genre, tahunTerbit, review, rating
	return render_template("search_result.html",data=result)

@app.route('/halamanBuku/')
def halamanBuku():
	isbn =  request.args.get('isbn')
	cursor.execute("""SELECT * FROM buku WHERE ISBN LIKE '%{}%'""".format(isbn))
	data=cursor.fetchall()[0]
	isbn =  data[0]
	judul = data[1]
	pengarang = data[2]
	genre =  data[5]
	tahun = data[6]
	penerbit =  data[3]
	review =  data[7]
	rating =  data[8]
	stok = data[9]

	if(stok==0):
		return render_template("halaman_buku_kosong.html",judul=judul,isbn=isbn,genre=genre,pengarang=pengarang,tahun=tahun,penerbit=penerbit,review=review,rating=rating,isbn_parameter=isbn,stok=stok)
	else:
		return render_template("halaman_buku.html",judul=judul,isbn=isbn,genre=genre,pengarang=pengarang,tahun=tahun,penerbit=penerbit,review=review,rating=rating,isbn_parameter=isbn,stok=stok)
#Peminjaman
@app.route('/handlePeminjaman/')
def handlePeminjaman():
	isbn =  request.args.get('isbn')
	cursor.execute("""SELECT * FROM buku WHERE ISBN LIKE '%{}%'""".format(isbn))
	data=cursor.fetchall()[0]
	
	try:
		cursor.execute('''INSERT INTO meminjam VALUES ("{}","{}","{}")'''.format(isbn,session['user'],datetime.datetime.now()+timedelta(days=7)))
		connection.commit()
		
		cursor.execute("""	UPDATE Buku SET Stok = Stok-1 WHERE ISBN = '{}';""".format(isbn))
		connection.commit()
	except sqlite3.IntegrityError:
		pass
	
	judul =  data[1]
	isbn = data[0]
	genre =  data[5]
	tahun = data[6]
	penerbit =  data[3]
	pengarang = data[2]
	review =  data[7]
	rating =  data[8]
	stok = data[9]
	
	if(stok==0):
		return render_template("halaman_buku_kosong.html",judul=judul,isbn=isbn,genre=genre,pengarang=pengarang,tahun=tahun,penerbit=penerbit,review=review,rating=rating,isbn_parameter=isbn,stok=stok)
	else:
		return render_template("halaman_buku.html",judul=judul,isbn=isbn,genre=genre,pengarang=pengarang,tahun=tahun,penerbit=penerbit,review=review,rating=rating,isbn_parameter=isbn,stok=stok)
#Antrian
@app.route('/handleAntrian/')
def handleAntrian():
	isbn =  request.args.get('isbn')
	cursor.execute("""SELECT * FROM Antrian WHERE ISBN LIKE '%{}%'""".format(isbn))
	data=cursor.fetchall()
	antrian_max=len(data)
	
	cursor.execute('''INSERT INTO Antrian VALUES ("{}","{}","{}")'''.format(isbn,session['user'],antrian_max+1))
	connection.commit()
	
	cursor.execute("""SELECT * FROM buku WHERE ISBN LIKE '%{}%'""".format(isbn))
	data=cursor.fetchall()[0]
	isbn =  data[0]
	judul = data[1]
	pengarang = data[2]
	genre =  data[5]
	tahun = data[6]
	penerbit =  data[3]
	review =  data[7]
	rating =  data[8]
	stok = data[9]

	if(stok==0):
		return render_template("halaman_buku_kosong.html",judul=judul,isbn=isbn,genre=genre,pengarang=pengarang,tahun=tahun,penerbit=penerbit,review=review,rating=rating,isbn_parameter=isbn,stok=stok)
	else:
		return render_template("halaman_buku.html",judul=judul,isbn=isbn,genre=genre,pengarang=pengarang,tahun=tahun,penerbit=penerbit,review=review,rating=rating,isbn_parameter=isbn,stok=stok)

#-------------------------------ADMIN-----------------------------------
#Login
@app.route('/admin/')
def admin_login():
	return render_template("admin_login.html")

@app.route('/admin/handleLogin/')
def admin_handleLogin():
	username =  request.args.get('username')
	password = request.args.get('password')
	
	cursor.execute("""SELECT * FROM pustakawan WHERE Username='{}' AND Pass='{}'""".format(username,password))
	result=cursor.fetchall()
	
	if(len(result)==0):
		return render_template("admin_login.html")
	else:
		return render_template("admin_homepage.html")

#Homepage
@app.route('/admin/home/')
def admin_homepage():
	return render_template("admin_homepage.html")

#Logout
@app.route('/admin/logout/')
def admin_logout():
	return render_template("admin_login.html")
	
#Input Book
@app.route('/admin/inputBookData/')
def inputBookData():
	return render_template("admin_input_book_data.html")

@app.route('/admin/handleInputBookData/')
def handleinputBookData():
	isbn =  request.args.get('isbn')
	judul = request.args.get('judul')
	pengarang = request.args.get('pengarang')
	penerbit = request.args.get('penerbit')
	lokasiBuku = request.args.get('lokasiBuku')
	genre = request.args.get('genre')
	tahunTerbit = request.args.get('tahunTerbit')
	review = request.args.get('review')
	rating = request.args.get('rating')
	stok = request.args.get('stocks')
	print(genre)
	
	try:
		cursor.execute('''INSERT INTO buku VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(isbn,judul,pengarang,penerbit,lokasiBuku,genre,tahunTerbit,review,rating,stok))
		connection.commit()
	except sqlite3.IntegrityError:
		pass
		
	return render_template("admin_input_book_data.html")


#Search
@app.route('/admin/searchResult/')
def admin_searchResult():
	query =  request.args.get('query')
		
	cursor.execute("""SELECT * FROM buku WHERE Judul LIKE '%{}%'""".format(query))
	result=cursor.fetchall()
	
	#isbn, judul, pengarang, penerbit, lokasiBuku, genre, tahunTerbit, review, rating
	return render_template("admin_search_result.html",data=result)

	
@app.route('/admin/halamanBuku/')
def admin_halamanBuku():
	isbn =  request.args.get('isbn')
	cursor.execute("""SELECT * FROM buku WHERE ISBN LIKE '%{}%'""".format(isbn))
	data=cursor.fetchall()[0]
	isbn =  data[0]
	judul = data[1]
	pengarang = data[2]
	genre =  data[5]
	tahun = data[6]
	penerbit =  data[3]
	review =  data[7]
	rating =  data[8]
	stok = data[9]

	return render_template("admin_halaman_buku.html",judul=judul,isbn=isbn,genre=genre,pengarang=pengarang,tahun=tahun,penerbit=penerbit,review=review,rating=rating,isbn_parameter=isbn,stok=stok)

#Pengembalian
@app.route('/adminPengembalian/')
def pengembalian():
	return render_template("admin_pengembalian.html")

@app.route('/handlePengembalian/')
def handlePengembalian():
	isbn =  request.args.get('isbn')
	username =  request.args.get('username')
	
	cursor.execute("""SELECT * FROM Meminjam WHERE ISBN='{}' AND Username='{}';""".format(isbn,username))
	temp=cursor.fetchall()
	if(len(temp)!=0):
	
		cursor.execute('''INSERT INTO mengembalikan VALUES ("{}","{}","{}")'''.format(isbn,username,datetime.datetime.now()))
		connection.commit()
	
		cursor.execute('''DELETE FROM meminjam WHERE ISBN = '{}' AND Username = '{}';'''.format(isbn,username))
		connection.commit()
	
		cursor.execute("""	UPDATE Buku SET Stok = Stok+1 WHERE ISBN = '{}';""".format(isbn))
		connection.commit()
	
		cursor.execute("""	UPDATE Antrian SET Nomor_Antrian = Nomor_Antrian-1 WHERE ISBN = '{}';""".format(isbn))
		connection.commit()
	
		cursor.execute("""SELECT * FROM Antrian WHERE Nomor_Antrian=0;""")
		result=cursor.fetchall()
	
		cursor.execute('''DELETE FROM Antrian WHERE Nomor_Antrian=0;''')
		connection.commit()
	
		cursor.execute('''INSERT INTO meminjam VALUES ("{}","{}","{}")'''.format(isbn,result[0][1],datetime.datetime.now()+timedelta(days=7)))
		connection.commit()
	
	
	
	return render_template("admin_pengembalian.html")
#-----------------------------------------------------------------------

if __name__ == "__main__":
    app.run()

