from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
serverHost = '127.0.0.1'
serverPort = 12000 ###change as needed
try:
    tcpSerSock.bind((serverHost, serverPort))
except:
    print('Binding error')
    sys.exit()

tcpSerSock.listen()
# Fill in end.

received_req = 0
get_traffic = 0
read_cache = 0
cache_traffic_reduce = 0
while 1:
    # Print Statistics
    if received_req != 0:
        cache_traffic_reduce = (read_cache/received_req)*100
    print('\n-----------------------------------------------')
    print('Statistics')
    print('Number of Received Requests:', received_req)
    print('Total size of GET traffic:', get_traffic)
    print('Percentage of traffic reduction with cache', cache_traffic_reduce, '%')
    print('-----------------------------------------------\n')
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    ###issue with message below
    message = tcpCliSock.recv(1024).decode()#tcpCliSock.sendto(('test').encode(), (serverHost, serverPort)) # Fill in start. # Fill in end.
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n", 'utf-8'))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
        #Fill in start.
        page = f.read()
        tcpCliSock.send(bytes(page, 'utf-8'))
        #Fill in end.
        print('\n\n----------Read from cache----------')
        read_cache += 1
        received_req += 1
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM) # Fill in start. # Fill in end.
            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn, 80))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('rw')
                fileobj.write("GET / HTTP/1.0\r\nHost: " + filename + "\r\n\r\n")
                # Read the response into buffer
                # Fill in start.
                fileobj.flush()
                page = fileobj.read()
                get_traffic += len(page)
                page = bytes(page, 'utf-8')
                #get_traffic += len(page)
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the
                # corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                tmpFile.write(page)
                tmpFile.close()
                tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n", 'utf-8'))
                tcpCliSock.send(bytes("Content-Type:text/html\r\n", 'utf-8'))
                tcpCliSock.send(page)
                received_req += 1
                #Fill in start.
                # Fill in end.
            except Exception as e:
                print("Illegal request")
                print(e)
        else:
            # HTTP response message for file not found
            # Fill in start. # Fill in end.
            print('test remove this') ###
    # Close the client and the server sockets
tcpCliSock.close()
# Fill in start.
# # Fill in end.
