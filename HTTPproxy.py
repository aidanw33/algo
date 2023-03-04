# Place your imports here
import signal
import sys
import re
import socket
import threading
from urllib.parse import urlsplit
from optparse import OptionParser

# Signal handler for pressing ctrl-c
def ctrl_c_pressed(signal, frame):
	sys.exit(0)

# TODO: Put function definitions here
def parse(clientRequest) :
    clientRequest = clientRequest.decode()

    port = 80
    #bool to check for 501 error
    fiveOOne = False
    fourHundred = False

    #check first line for proper GET and HTTP/1.0
    splitByLine = clientRequest.split("\r\n")

    firstLine = splitByLine[0]

    firstLine = firstLine.split(" ")
    #check for proper GET
    if not (firstLine[0] == "GET") :
        fiveOOne = True

    #check for proper HTTP/1.0
    if(len(firstLine) < 3 or firstLine[2] != "HTTP/1.0") :
        fourHundred = True
    
    #--------------------------------------
    #Check for a proper URL
    url = firstLine[1]
    parsedURL = urlsplit(url)

    #check for protocol
    if(parsedURL.scheme == "") :
        fourHundred = True

    #check for hostname
    if(parsedURL.netloc == "") :
        fourHundred = True

    #check for protocol
    if(parsedURL.path == "") :
        fourHundred = True

    hostName = parsedURL.netloc
    #check for a new port number, if so get a new netloc
    if ":" in parsedURL.netloc :
        increment = parsedURL.netloc.index(":")
        port = int(parsedURL.netloc[increment + 1:])
        hostName = parsedURL.netloc[:increment]
    
    #first line should be good enough right now, I now need to check for correcet header formats

    i = 1
    headers = ""
    while(i < len(splitByLine) ) : 
        currentLine = splitByLine[i]
        p = re.compile("^[^\s:]+: .*$")
        connection = re.compile("Connection")
        if not (currentLine == "") :
            if(p.match(currentLine)) :
                if not (connection.match(currentLine)) :
                    headers += currentLine + "\r\n"
            else :
                fourHundred = True
        i += 1
    
    #Handle all of the bad inputs
    if(fourHundred) :
        errorCode = "HTTP/1.0 400 Bad Request\r\n\r\n" 
        return errorCode.encode(), hostName, -1

    if(fiveOOne) :
        errorCode = "HTTP/1.0 501 Not Implemented\r\n\r\n"
        return errorCode.encode(), hostName, -1
    
    

    #make the first line of the Get request
    returnFirstLine = firstLine[0] + " " + parsedURL.path + " " + firstLine[2] + "\r\n"

    #make second line
    returnSecondLine = "Host: " + str(hostName) + "\r\n"

    #make connection line
    returnThirdLine = "Connection: close\r\n"

    #make header line
    returnFourthLine = headers + "\r\n"

    returnLine = returnFirstLine + returnSecondLine + returnThirdLine + returnFourthLine

    return returnLine.encode(), str(hostName), int(port)
    

def handleClient(clientSocket) :
  
    #set to none
    remoteSocket = None

    while True:

        #Receive all the data from client and forward it to remote server
        fromClient = b''
        while True :
            temp = clientSocket.recv(4096)
            fromClient += temp
            if(fromClient.endswith(b'\r\n\r\n')) :
                break
        
        fromClientParsed = parse(fromClient)
        
        if(fromClientParsed is None) :
            break
        
        toSendToRemote, host, port = parse(fromClient)
        if(port == -1) :
            clientSocket.sendall(toSendToRemote)
            clientSocket.close()
            break

        #Send the data to the remote server
        remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remoteSocket.connect((host, port))
        remoteSocket.sendall(toSendToRemote)


        #Recieve data back from the remote server
        remote_Response = b''
        while True :
            temp = remoteSocket.recv(4096)
            remote_Response += temp
            if(len(temp) < 1) :
                break
            
        #Send back to client
        clientSocket.sendall(remote_Response)
        break

    clientSocket.close()
    if remoteSocket is not None :
        remoteSocket.close()


# Start of program execution
# Parse out the command line server address and port number to listen to
parser = OptionParser()
parser.add_option('-p', type='int', dest='serverPort')
parser.add_option('-a', type='string', dest='serverAddress')
(options, args) = parser.parse_args()

port = options.serverPort
address = options.serverAddress
if address is None:
    address = 'localhost'
if port is None:
    port = 2100

# Set up signal handling (ctrl-c)
signal.signal(signal.SIGINT, ctrl_c_pressed)

#Create our proxys socket
pSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Connect to incoming traffic
pSocket.bind((address, port))

pSocket.listen()

while True : 

    #We connect to a socket
    clientSocket, clientAddr = pSocket.accept()
    thread = threading.Thread(target=handleClient, args=(clientSocket,))
    thread.start()



