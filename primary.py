import os
import socket
import sys
import threading
import time
from func import upload, download, generate_file_md5

root = 'serverUtama/'

BUFSIZE = 4096

list_hash = []
newList_hash = []
listDataNew = []
lock = threading.Lock()


def list_local(directory):
    temp_list = os.listdir(directory)
    return temp_list


def updateList(a, b):
    return (list(set(b) - set(a)))


def listen_client(clientsocket):
    clientsocket.listen(5)
    while True:
        client_sock_accept, addr = clientsocket.accept()
        print("koneksi dari %s" % str(addr))
        print('berhasil terhubung', addr)
        thread_recieve = threading.Thread(
            target=recieve_from_client, kwargs={"socket": client_sock_accept}
        )
        thread_recieve.start()


def recieve_from_client(socket):
    global list_hash, listDataNew, newList_hash
    while True:
        command = ''
        command = socket.recv(1024).decode('latin-1')

        listDataNew = list_local(root)
        for file in listDataNew:
            filename = os.path.join(root, file)
            hashData = generate_file_md5(filename)
            newList_hash.append(hashData)

        print('REQ diterima '+str(command))

        if ('update' in command):
            socket.send(('ack').encode('latin-1'))
            download(socket, root, newList_hash)
            print('update sucess')
            for file in listDataNew:
                    filename = os.path.join(root, file)
                    hashData = generate_file_md5(filename)
                    if(hashData in newList_hash):
                        pesan = ''
                        pesan = 'update'
                        socket.sendall(pesan.encode())
                        terima = socket.recv(1024).decode('latin-1')
                        if ('ack' in terima):
                            upload(socket, filename, file, hashData)
                            print('success')
                        else:
                            pass
                    else:
                        pass

        elif ('isUpdate' in command):
            listDataNew = list_local(root)
            panjang = len(listDataNew)
            panjang = str(panjang)
            panj = len(panjang)
            if(newList_hash == '' ):
                print('noUpdate')
                socket.send('noUpdate'.encode('utf-8'))
            elif (panjang== '0'):
                print('dir kosong')
                socket.send('kosong'.encode('utf-8'))
            else:
                socket.send(panjang[:5].encode('ascii'))
                for file in listDataNew:
                    filename = os.path.join(root, file)
                    hashData = generate_file_md5(filename)
                    if(hashData in newList_hash):
                        pesan = ''
                        pesan = 'update'
                        socket.sendall(pesan.encode())
                        terima = socket.recv(1024).decode('utf-8')
                        print(terima)
                        if ('ack' in terima):
                            upload(socket, filename, file, hashData)
                            print('success')
                        else:
                            pass
                    else:
                        pass

        else:
            pass


def main():
    host = '127.0.0.1'
    port = 8083
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    print("server ip " + str(host))
    print("bind socket port: %s" % (port))

    listData = list_local(root)

    for file in listData:
        filename = os.path.join(root, file)
        hashData = generate_file_md5(filename)
        list_hash.append(hashData)

    try:
        thread_listen_client = threading.Thread(target=listen_client, kwargs={
                                                "clientsocket": server_socket})
        thread_listen_client.start()
    except:
        print("Error in thread: listen_client")


main()