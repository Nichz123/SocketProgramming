from socket import *
import sys 
import os
 
#Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM) 

#Prepare the sever socket
#FillInStart
port = 3001
# Get the hostname of the machine
hostname = gethostname()

# Get the IP address of the machine
# Getting IP from host name does not work reliably on linux.
# This works around the issue by connecting to google, then 
# using that connection to determine the actual IP address
with socket(AF_INET, SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    
print(ip_address, port)
serverSocket.bind(('', port))
serverSocket.listen(1)

#FillInEnd 

while True:    
    print('Ready to serve...') 
    #Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    print('Connection from:', addr)

    #If an exception occurs during the execution of try clause
    #the rest of the clause is skipped
    #If the exception type matches the word after except
    #the except clause is executed
    try: 
        #Receive the request message from the client
        #FillInStart
        message = connectionSocket.recv(4096)
        print(message)
        #FillInEnd 
        
        #Extract the path of the requested object from the message
        #The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]
        #Because the extracted path of the HTTP request includes 
        #a character '\', we read the path from the second character 
        f = open(filename[1:])     
        #Store the entire content of the requested file in a buffer
        outputdata = f.read()
        
        #Send the HTTP response header line to the connection socket
        #FillInStart       
        header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n\r\n'
        connectionSocket.send(header.encode())
        #FillInEnd

        #Send the content of the requested file to the client 
        for i in range(0, len(outputdata)): 
            connectionSocket.send(outputdata[i].encode())               
        
        connectionSocket.send("\r\n".encode()) 
        print("Sent, and closing")
        connectionSocket.close() 
    
    except IOError:
        #Send HTTP response message for file not found
        #FillInStart
        print("File not found")
        header = 'HTTP/1.1 404 Not Found\n'
        connectionSocket.send(header.encode())
        #FillInEnd 
        
        #Close client socket 
        connectionSocket.close()

#Terminate the program
serverSocket.close()
sys.exit()
