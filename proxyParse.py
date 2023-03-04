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

def main():
    stringToParse = "GET http://someexamplehost/proxy/cache/enable HTTP/1.0"
    parse(stringToParse)