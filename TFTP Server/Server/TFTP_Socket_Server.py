#!/usr/bin/env python
# coding: utf-8

# ### TFTP_Socket_Server_Angel ###

# In[1]:


import struct
import socket
from threading import Thread


# In[2]:


# Client download thread
def download_thread(fileName, clientInfo):
    print("Responsible for processing client download files")
    
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    fileNum = 0     # Serial number of the received file
    
    try:
        f = open(fileName,'rb')
    except:
        # Packing
        errorData = struct.pack('!HHHb', 5, 5, 5, fileNum) 
        # Send an error message when the file does not exist
        s.sendto(errorData, clientInfo) 
        # Exit the download thread
        exit() 
        
    while True:
        # Read file contents 512 bytes from local server
        readFileData = f.read(512)
        
        # The block number range is [0, 65535]. Increments by one each time.
        if fileNum < 65535:
            fileNum += 1
        else:
            fileNum = 0
 
        # Packing (network character order, data, block number)
        sendData = struct.pack('!HH', 3, fileNum) + readFileData 
        
        # Send file data to the client
        s.sendto(sendData, clientInfo)  # Data sent for the first time
        
        # When the data received by the client is less than 516 bytes, it means that the transmission is completed!
        if len(sendData) < 516:
            print("User"+str(clientInfo), end='')
            print('：Download '+fileName+' completed！')
            print("File size: " + str(f.tell()) + " bytes")
            print("Last block number: " + str(fileNum))
            break
            
        # Receiving data for the second time
        recvData, clientInfo = s.recvfrom(1024)
#         print(recvData, clientInfo)

        # Unpacking
        packetOpt = struct.unpack("!H", recvData[:2])  #Opcode
        packetNum = struct.unpack("!H", recvData[2:4]) #Block number        
#         print(packetOpt, packetNum)
        
        if packetOpt[0] != 4 or packetNum[0] != fileNum:
            print("File transfer error！")
            break
                   
    # Close file
    f.close()
    
    # Close UDP port
    s.close()

    # Exit the download thread
    exit()


# In[3]:


# Client uploading thread
def upload_thread(fileName, clientInfo):
    print("Responsible for processing client upload files")
    
    fileNum = 0  # Serial number of the received file
    
    # Open the file in binary mode
    f = open(fileName, 'wb')
    
    # Create a UDP port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Packing (network character order, id of an unsigned short(16bits))
    sendDataFirst = struct.pack("!HH", 4, fileNum) 

    # Reply to the client upload request
    s.sendto(sendDataFirst, clientInfo)  # Sent with a random port at first time

    while True:
        # Receive data sent by the client
        recvData, clientInfo = s.recvfrom(1024) # Client connects to my random port at second time       
#         print(recvData, clientInfo)
        
        # Unpacking
        packetOpt = struct.unpack("!H", recvData[:2])  # Identify opcode
        packetNum = struct.unpack("!H", recvData[2:4]) # Block number
#         print(packetOpt, packetNum)
        
        # Client upload data
        # opcode == 3 means Data
        if packetOpt[0] == 3 and packetNum[0] == fileNum:
            #　Save data to file
            f.write(recvData[4:])
            
            # Packing
            sendData = struct.pack("!HH", 4, fileNum)
            
            # Reply client's ACK signal
            s.sendto(sendData, clientInfo) # The second time using a random port to sent

            # The block number range is [0, 65535]. Increments by one each time.
            if fileNum < 65535:
                fileNum += 1
            else:
                fileNum = 0
            
            #If len(recvData) < 516 means the file goes to the end
            if len(recvData) < 516:
                print("User"+str(clientInfo), end='')
                print('：Upload '+fileName+' complete!')
                print("File size: " + str(f.tell()) + " bytes")
                print("Last block number: " + str(fileNum))
                break
                
    # Close the file
    f.close()
    
    # Close UDP Port
    s.close()
    
    # Exit upload thread
    exit()


# In[4]:


# Main function
def main():
    # Create a UDP port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Resolve duplicate binding ports
    # setsockopt(level,optname,value)
    # Level: defines which option will be used. Usually use "SOL_SOCKET", it means the socket option being used.
    # optname: Provide special options for use. Ex: SO_BINDTODEVICE, SO_BROADCAST, SO_DONTROUTE, SO_REUSEADDR, etc.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind local host and port number 69
    s.bind(('127.0.0.1', 69))
    
    print("TFTP Server start successfully!")
    print("Server is running...")
    
    while True:
        
        # Receive messages sent by the client
        recvData, clientInfo = s.recvfrom(1024)  #　Client connects to port 6969 at the first time
        print(clientInfo) 
        
        # Unpacking
        # !: Indicates that we want to use network character order parsing because our data is received from the network. 
        #    When transmitting on the network, it is the network character order. 
        # b: signed char
        # There can be one number before each format, indicating the number
        # s: char[]
        if struct.unpack('!b5sb', recvData[-7:]) == (0, b'octet', 0):
            opcode = struct.unpack('!H',recvData[:2])  #　Opcode
            fileName = recvData[2:-7].decode('ascii') #　Filename
            
            # Request download
            # opcode == 1 means download
            if opcode[0] == 1:
                t = Thread(target=download_thread, args=(fileName, clientInfo))
                t.start() # Start the download thread
                
            # Request uploading
            # opcode == 2 means uploading
            elif opcode[0] == 2:
                t = Thread(target=upload_thread, args=(fileName, clientInfo))
                t.start() # Start uploading thread
                
    # Close UDP port
    s.close()


# In[ ]:


# Call the main function
if __name__ == '__main__':
    main()


# ### Comments ###
# Create bigfile.txt in terminal:<br/>
# mkfile -n 64m bigfile.txt<br/>
# <br/>
# Testing Result: <br/>
# TFTP Server start successfully!<br/>
# Server is running...<br/>
# ('127.0.0.1', 57541)<br/>
# Responsible for processing client download files<br/>
# User('127.0.0.1', 57541)：Download bigfile.txt completed！<br/>
# File size: 67108864 bytes<br/>
# Last block number: 1<br/>
