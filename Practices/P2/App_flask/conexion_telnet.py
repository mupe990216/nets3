import telnetlib

def conexion_telnet(host,usr,psw,cmds,opc=None):
    tn=telnetlib.Telnet(host)
    tn.read_until(b"Username: ")
    tn.write(usr.encode('ascii')+b"\n")
    tn.read_until(b"Password: ")
    tn.write(psw.encode('ascii') + b"\n")
    for i in cmds:
        tn.write(i.encode("ascii")+b"\n")
    if opc==1:
    	result = str(tn.read_all().decode("ascii"))
    	tn.close()
    	return result
    print(tn.read_all().decode("ascii"))
    tn.close()


#lista_comandos = ["conf t","no username holiwis privilege 15 password 1234","end","exit"]
#conexion("192.168.0.1","admin","admin01",lista_comandos)
