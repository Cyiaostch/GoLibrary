from flask import Flask, render_template, redirect, request
import pandas as pd
import numpy as np

app = Flask(__name__)

db = {}
db["pelanggan"]=pd.DataFrame(columns=["username","password","nama","universitas","ttl"])
db["buku"]=pd.DataFrame()
db["pustakawan"]=pd.DataFrame()
db["antrian"]=pd.DataFrame()
db["copy_buku"]=pd.DataFrame()
db["meminjam"]=pd.DataFrame()
db["mengembalikan"]=pd.DataFrame()

logged_in=set()

@app.route('/home/')
def homepage():
	return render_template("homepage.html")

@app.route('/')
def login():
	return render_template("login.html")

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
	index=db["pelanggan"].index.tolist()
	if(len(index)==0):
		db["pelanggan"].set_value(0,"username",username)
		db["pelanggan"].set_value(0,"password",password)
		db["pelanggan"].set_value(0,"nama",nama)
		db["pelanggan"].set_value(0,"universitas",universitas)
		db["pelanggan"].set_value(0,"ttl",ttl)
	else:
		max_index=np.max(index)
		db["pelanggan"].set_value(max_index,"username",username)
		db["pelanggan"].set_value(max_index,"password",password)
		db["pelanggan"].set_value(max_index,"nama",nama)
		db["pelanggan"].set_value(max_index,"universitas",universitas)
		db["pelanggan"].set_value(max_index,"ttl",ttl)
		
	return "{}".format(db["pelanggan"])

@app.route('/handleLogin/')
def handleLogin():
	username =  request.args.get('username')
	password = request.args.get('password')
	index=db["pelanggan"].index[db["pelanggan"]['username']==username].tolist()
	if(len(index)==1):
		index=index[0]
		if(index and (username in list(db["pelanggan"]["username"])) and (db["pelanggan"]["username"][index]==username) and (db["pelanggan"]["password"][index]==password)):
			logged_in.add(username)
	return render_template("homepage.html")

@app.route('/admin/')
def admin_login():
	return render_template("admin_login.html")

@app.route('/admin/home/')
def admin_homepage():
	return render_template("admin_homepage.html")

@app.route('/admin/logout/')
def admin_logout():
	return render_template("admin_login.html")
	
@app.route('/searchResult/')
def searchResult():
	return render_template("search_result.html",data=[["Harry Potter","Fantasy","2010","Luar Negeri","9264756192731","Keren Banget Bukunya","4"],["The Two Tower","Fantasy","2011","Learn Negeri","8256756291652","Bagus Banget Bukunya","4.5"]])

@app.route('/halamanBuku/')
def halamanBuku():
	judul =  request.args.get('judul')
	isbn = request.args.get('isbn')
	genre =  request.args.get('genre')
	tahun = request.args.get('tahun')
	penerbit =  request.args.get('penerbit')
	review =  request.args.get('review')
	rating =  request.args.get('rating')
	return render_template("halaman_buku.html",judul=judul,isbn=isbn,genre=genre,tahun=tahun,penerbit=penerbit,review=review,rating=rating)

@app.route('/admin/inputBookData/')
def inputBookData():
	return render_template("admin_input_book_data.html")

@app.route('/admin/searchResult/')
def admin_searchResult():
	return render_template("admin_search_result.html",data=[["Harry Potter","Fantasy","2010","Luar Negeri","9264756192731","Keren Banget Bukunya","4"],["The Two Tower","Fantasy","2011","Learn Negeri","8256756291652","Bagus Banget Bukunya","4.5"]])

@app.route('/admin/halamanBuku/')
def admin_halamanBuku():
	judul =  request.args.get('judul')
	isbn = request.args.get('isbn')
	genre =  request.args.get('genre')
	tahun = request.args.get('tahun')
	penerbit =  request.args.get('penerbit')
	review =  request.args.get('review')
	rating =  request.args.get('rating')
	return render_template("admin_halaman_buku.html",judul=judul,isbn=isbn,genre=genre,tahun=tahun,penerbit=penerbit,review=review,rating=rating)



if __name__ == "__main__":
    app.run()

