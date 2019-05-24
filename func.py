import struct
import os
import hashlib


BLOCKSIZE = 65536

def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb" ) as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update( buf )
    return str(m.hexdigest())

def upload(conn, filename, files, hash_in):
    if os.path.isfile(filename):
        payload = open(filename,'rb').read() 
        size = len(payload)
        message = files + ',' + hash_in
        if filename !='':
            conn.send(message.encode('latin-1'))
        header = struct.pack(">I", size)
        alldata = header + payload
        conn.sendall(alldata)



def download(conn, root, newList_hash):
    message = ''
    hash_in = ''
    message = conn.recv(1024)
    message = message.decode('latin-1').split(',')
    panjangs = len(message)
    if(panjangs>1):
        filename = message[0]
        hash_in = message[1]
    else :
        filename = message[0]
        hash_in = ''
    if(hash_in!=''):
        newList_hash.append(hash_in)
    file_download = root + filename
    header = conn.recv(4)
    size = struct.unpack(">I", header)[0]
    myfile = open(file_download, 'wb')
    data = conn.recv(size)
    myfile.write(data)
    myfile.close()
    print('berhasil membuat file')