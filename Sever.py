import socket

def CreateSever(host, port): 
	Sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	Sever.bind((host,port))
	Sever.listen(5)
	return Sever

def ReadRequest(Client):
	re = ""
	Client.settimeout(1)
	try:
		re = Client.recv(1024).decode()
		while (re):
			re = re + Client.recv(1024).decode()
	except socket.timeout: # fail after 1 second of no activity
		if not re:
			print("Didn't receive data! [Timeout]")
	finally:
		return re

#2. Client connect Sever + 3. Read HTTP Request
def ReadHTTPRequest(Sever): 
	re = ""
	while (re == ""):
		Client, address = Sever.accept()
		print("Client: ", address," da ket noi toi sever")
		re = ReadRequest(Client)
	return Client, re

def SendFileIndex(Client): 
	f = open ("index.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 200 OK
Content-Length: %d

"""%len(L)
	print("-----------------HTTP respone  Index.html: ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))

def MovePageIndex(Client):
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8081/index.html

"""
	print("---------------HTTP respone move Index.html: ")
	print(header)
	Client.send(bytes(header,'utf-8'))

#4. Send HTTP Response  + 5. Close Sever
def MoveHomePage(Sever, Client, Request):
	if "GET /index.html HTTP/1.1" in Request: 
		SendFileIndex(Client)
		Sever.close()
		return True
	if "GET / HTTP/1.1" in Request:
		#Move Index.html 
		MovePageIndex(Client)
		Sever.close()
		#Tra ve file index.html cho client
		Sever = CreateSever("localhost", 8081)
		Client, Request = ReadHTTPRequest(Sever)
		print("------------------HTTP request: ")
		print(Request)
		MoveHomePage(Sever, Client, Request)
		return True


def CheckPass(Request): 
	if "POST / HTTP/1.1" not in Request:
		return False
	if "Username=admin&Password=admin" in Request: 
		return True
	else: 
		return False


def Move404(Sever, Client): 
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8082/404.html

"""
	print("HTTP respone: ")
	print(header)
	Client.send(bytes(header,"utf-8"))
	Sever.close()

def SendFile404(Client): 
	f = open ("404.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 404 Not Found
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L) 
	print("HTTP respone file 404.html: ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))

def Send404(Sever, Client): 
	Sever = CreateSever("localhost", 8082)
	Client, Request = ReadHTTPRequest(Sever)
	print("HTTP Request: ")
	print(Request)
	if "GET /404.html HTTP/1.1" in Request:
		SendFile404(Client)
	Sever.close()

def MoveInfo(Sever, Client):
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8082/info.html

"""
	print("HTTP respone: ")
	print(header)
	Client.send(bytes(header,"utf-8"))
	Sever.close()

def SendFileInfo(Client): 
	f = open ("info.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
	print("-----------------HTTP respone  Info.html: ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))

def SendInfo(Sever, Client):
	Sever = CreateSever("localhost", 8082)
	Client, Request = ReadHTTPRequest(Sever)
	print("HTTP Request: ")
	print(Request)
	if "GET /info.html HTTP/1.1" in Request:
		SendFileInfo(Client)
	Sever.close()
	#image 1
	#tu viet
	#image 2
	#tu viet 

if __name__ == "__main__":
	print("Phan 1: tra ve trang chu khi truy cap sever")
	#1. Create sever Socket 
	Sever = CreateSever("localhost",8080)
	#2. Client connect Sever + 3. Read HTTP Request
	Client, Request = ReadHTTPRequest(Sever)
	print("----------------HTTP requset: " )
	print(Request)
	#4. Send HTTP Response  + 5. Close Sever
	MoveHomePage(Sever, Client, Request)
	
	#Phan 2 xu ly post user name va pass len sever 
	#1. Create sever Socket 
	Sever = CreateSever("localhost",10000)
	#2. Client connect Sever + 3. Read HTTP Request
	Client, Request = ReadHTTPRequest(Sever)
	print("----------------HTTP requset: " )
	print(Request)
	if CheckPass(Request) == True: 
		MoveInfo(Sever, Client)
		SendInfo(Sever, Client)
	else: 
		Move404(Sever, Client)
		Send404(Sever, Client)
	
	
	
