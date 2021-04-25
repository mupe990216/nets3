"""
	Instituto Politecnico Nacional
	Escuela Superior de Computo
	Administracion de servicios en red
	Practica 2 - SSH y Telnet
"""

from flask import Flask, request, render_template
from db_services import *
from conexion_telnet import *
import io
# app = Flask(__name__, template_folder="nombrefolder")
user_admin="admin"
psw_admin="admin01"
app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def inicio():
	return render_template("/index.html")	

@app.route('/alta',methods = ['POST','GET'])
def alta():
	if request.method == 'GET':
		conexion = create_db("P02.db")		
		par1 = request.args.get('usr')
		par2 = request.args.get('rou')
		par3 = request.args.get('psw')
		par4 = request.args.get('registra')
		exist = valitate_usr(conexion,par1)
		insert_data(conexion,(par1,par2,par3))
		host = ""
		if par2 == "R1":
			host = "10.10.0.129"
		elif par2 == "R2":
			host = "10.10.0.130"
		elif par2 == "R3":
			host = "10.10.0.134"
		comandos = ["conf t","username {} privilege 15 password {}".format(par1,par3),"end","exit"]
		conexion_telnet(host,user_admin,psw_admin,comandos)
		return render_template("/alta.html",usr=par1,rou=par2,psw=par3,registra=par4,existe=exist)
	else:
		return render_template("/alta.html",usr=None,rou=None,psw=None,registra=0,existe=None)

@app.route('/consulta',methods = ['POST','GET'])
def consulta():
	if request.method == 'GET':
		conexion = create_db("P02.db")
		par1 = request.args.get('usr')
		par2 = request.args.get('opc')
		if int(par2) == 1:
			atributos = select_specific(conexion,str(par1))
			return render_template("/consulta.html",filas=None,control=1,list_data=atributos)
		elif int(par2) == 3:
			atributos = select_specific(conexion,str(par1))
			return render_template("/consulta.html",filas=None,control=3,list_data=atributos)					
	else:
		conexion = create_db("P02.db")
		resultad = select_all_data(conexion)	
		return render_template("/consulta.html",filas=resultad,control=0)

@app.route('/modifica',methods = ['POST','GET'])
def modifica():
	conexion = create_db("P02.db")
	par1 = request.args.get('usr')
	par2 = request.args.get('rou')
	par3 = request.args.get('psw')
	print("valores: {} {} {}".format(par1,par2,par3))
	update_data(conexion,(str(par1),str(par2),str(par3)))
	atributos = select_specific(conexion,str(par1))
	host = ""
	if par2 == "R1":
		host = "10.10.0.129"
	elif par2 == "R2":
		host = "10.10.0.130"
	elif par2 == "R3":
		host = "10.10.0.134"
	comandos = ["conf t","username {} privilege 15 password {}".format(par1,par3),"end","exit"]
	conexion_telnet(host,user_admin,psw_admin,comandos)
	return render_template("/consulta.html",filas=None,control=2,list_data=atributos)

@app.route('/elimina',methods = ['POST','GET'])
def elimina():
	conexion = create_db("P02.db")
	par1 = request.args.get('usr')
	par2 = request.args.get('rou')
	par3 = request.args.get('psw')
	print("valores: {} {} {}".format(par1,par2,par3))
	delete_data(conexion,str(par1))
	host = ""
	if par2 == "R1":
		host = "10.10.0.129"
	elif par2 == "R2":
		host = "10.10.0.130"
	elif par2 == "R3":
		host = "10.10.0.134"
	comandos = ["conf t","no username {} privilege 15 password {}".format(par1,par3),"end","exit"]
	conexion_telnet(host,user_admin,psw_admin,comandos)
	return render_template("/consulta.html",filas=None,control=4)

@app.route('/SSH',methods = ['POST','GET'])
def SSH():
	if request.method == 'GET':
		return render_template("/SSH.html",control=0)
	else:
		conexion = create_db("P02.db")
		usuario = request.form["usr"]
		contras = request.form["psw"]
		info = select_specific(conexion,usuario)
		return render_template("/SSH.html",control=1,list_data=info)

@app.route('/SSH/CMD',methods = ["POST","GET"])
def CMD():	
	if request.method == "GET":
		par1 = request.args.get("usr")
		par2 = request.args.get("rou")
		par3 = request.args.get("psw")
		par4 = request.args.get("comando")
		host = ""
		if par2 == "R1":
			host = "10.10.0.129"
		elif par2 == "R2":
			host = "10.10.0.130"
		elif par2 == "R3":
			host = "10.10.0.134"

		comandos = []

		# hacemos uso del buffer io, para poder parsear el textarea del CMD.html
		aux_buf = io.StringIO(par4)
		aux_list = aux_buf.readlines()
		print("Comandos sin parsing: {}".format(aux_list))

		for e in aux_list:
			aux_cmd = e[:-2]
			comandos.append(aux_cmd)			

		print(comandos)			
		comandos.append("exit")
		par4 = conexion_telnet(host,par1,par3,comandos,1)
		return render_template("/CMD.html",usr=par1,rou=par2,psw=par3,control=1,cmd=par4)
	else:
		par1 = request.form["usr"]
		par2 = request.form["rou"]
		par3 = request.form["psw"]		
		return render_template("/CMD.html",usr=par1,rou=par2,psw=par3,control=0)

if __name__ == '__main__':	
	conexion = create_db("P02.db")
	create_tb(conexion)
	# close_db(conexion)
	app.run(host='0.0.0.0',debug=True)
	