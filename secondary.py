import os
import socket
import sys
import time
from func import upload, download, generate_file_md5

root = 'server1/'

BUFSIZE = 4096

list_hash = []
newListHash = []

def list_local(directory):
    temp_list = os.listdir(directory)
    return temp_list

def updateList(a,b):
    return (list(set(b)- set(a)))

def main():
    global newListHash,list_hash
    host = '127.0.0.1'
    port = 8083
    listData = list_local(root)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    for file in listData:
        filename = os.path.join(root,file)
        hashData = generate_file_md5(filename)
        list_hash.append(hashData)

    while True:

        listDataNew = list_local(root)
        
        for file in listDataNew:
            filename = os.path.join(root,file)
            hashData = generate_file_md5(filename)
            newListHash.append(hashData)
            

        change = updateList(list_hash,newListHash)
        list_hash = list_hash + change
        panjang = len(change)
        if (panjang!=0):
            for file in listDataNew:
                for hash_in in change:
                    filename = os.path.join(root,file)
                    hashData = generate_file_md5(filename)
                    if(hash_in==hashData):
                        s.send(('update').encode('unicode_escape'))
                        reply = s.recv(1024).decode('unicode_escape')
                        if('ack' in reply):
                            print('ack_update')
                            upload(s,filename, file, hash_in)
                            print('success')
                        else:
                            pass
        else :
            s.send(('isUpdate').encode('latin-1'))
            reply = ''
            jum = 0
            count = 0
            jum = s.recv(1024).decode('latin-1')
            if('kosong' in jum):
                listDataNew = list_local(root)
                for file in listDataNew:
                    filename = os.path.join(root,file)
                    hashData = generate_file_md5(filename)
                    s.send(('update').encode('unicode_escape'))
                    reply = s.recv(1024).decode('unicode_escape')
                    if('ack' in reply):
                        upload(s,filename, file, hashData)
                        print('success')
                    else:
                        pass

            elif ('noUpdate' in jum) :
                print(jum)
            elif(any(i.isdigit() for i in jum) and len(jum)<5) :
                jum = int(''.join(filter(str.isdigit, jum)))
            else :
                pass

            if(jum!=0):
                while True:
                    reply = ''
                    reply = s.recv(1024).decode('latin-1')
                    if('update' in reply):
                        count +=1
                        if(reply[1] in list_hash):
                            s.sendall(('file exist').encode('utf-8'))
                        else:
                            s.sendall(('ack').encode('utf-8'))
                            download(s, root, list_hash)
                            print('update')
                    elif('noUpdate' in reply):
                        print('ok') 
                    if(count==jum):
                        break
            else :
                pass
        time.sleep(10)

main()