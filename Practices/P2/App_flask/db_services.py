import sqlite3

def create_db(name):
	return sqlite3.connect(name)

def close_db(conexion):
	conexion.close()

def create_tb(conexion):
	cursor_tb = conexion.cursor()
	cursor_tb.execute(
			"""
				create table if not exists usuarios(					
					usr text primary key,
					rou text not null,
					psw text not null
				)
			"""
		)	

def valitate_usr(conexion,usr):
	cursor_tb = conexion.cursor()
	sentencia = "select * from usuarios where usr=?"
	respuesta = cursor_tb.execute(sentencia,(usr,))
	existencia = respuesta.fetchone()
	if existencia!=None:
		existe = 1
		# print("El usuario ya existe")
	else:
		existe = 0
		# print("El usuario NO existe")
	return existe


def insert_data(conexion,list_data):
	cursor_tb = conexion.cursor()
	valida = valitate_usr(conexion,list_data[0])
	if valida == 1:
		print("insert_data no valido")
	else:
		sentencia = "insert into usuarios(usr,rou,psw) values(?,?,?)"
		cursor_tb.execute(sentencia,list_data)
		conexion.commit()
		print("Usuario {} Registrado".format(list_data[0]))

def select_all_data(conexion):
	cursor_tb = conexion.cursor()
	sentencia = "select * from usuarios"
	resultado = cursor_tb.execute(sentencia)
	return resultado

def select_specific(conexion,usr):
	cursor_tb = conexion.cursor()
	valida = valitate_usr(conexion,usr)
	if valida == 0:
		print("Select_specific no valido")
		resultado = None
	else:
		sentencia = "select * from usuarios where usr=?"
		resultado = cursor_tb.execute(sentencia,(usr,))	
	return resultado

def update_data(conexion,list_data):
	cursor_tb = conexion.cursor()
	valida = valitate_usr(conexion,list_data[0])
	if valida == 0:
		print("update_data no valido")		
	else:		
		sentencia = "update usuarios set psw=? , rou=?  where usr=?"		
		lista_data = list(list_data)
		lista_data.reverse()		
		cursor_tb.execute(sentencia,lista_data)
		conexion.commit()
		print("modificando {}".format(list_data[0]))

def delete_data(conexion,usr):
	cursor_tb = conexion.cursor()	
	valida = valitate_usr(conexion,usr)
	if valida == 0:
		print("delete_data no valido")		
	else:		
		sentencia = "delete from usuarios where usr=?"
		cursor_tb.execute(sentencia,(usr,))
		conexion.commit()
		print("eliminando {}".format(usr))	


