import socket
import sys  
from PIL import Image
import os
import io
import numpy as np
import cv2

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8081        # The port used by the server

# Create socket
print('Creating socket')
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('Getting remote IP address') 
try:
    remote_ip = socket.gethostbyname(HOST)
except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()


# Predefined variables
im_width = 128
im_height = 96
num_channels = 3
total_length = im_width*im_height*num_channels

# Opens multiple images in the same window
def Receive_image(sock, total_length):
    data = b''
    while len(data) < total_length:
        packet = sock.recv(total_length - len(data))
        # check if the connection is empty 
        if len(packet) == 0:
            break
        data += packet
        
    received_im = Image.frombytes('RGB', (128, 96), data, 'raw')
    # swap BGR to RGB channels:
    new_array = np.asarray(received_im)[:,:,::-1]
    received_im = Image.fromarray(new_array)
    received_im.show()
    received_im.close()
    

try:
    sock.connect((remote_ip, PORT))
    print('Connected to server: ' + HOST + ' (' + remote_ip + ')')
    while True:
        Receive_image(sock, total_length)
except:
    print('Failed to connect to server: ' + HOST + ' (' + remote_ip + ')')  