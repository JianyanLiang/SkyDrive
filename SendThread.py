# -*- coding:utf-8 -*-
import socket
import time
import json
from resource import source_rc
from hashlib import md5
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal

class SendThread(QObject):

    new_msg_signal = pyqtSignal(str)

    def __init__(self, queue):
        super(SendThread, self).__init__()
        self.queue = queue

    def login(self, ip_address, port, username, password):
        self.ip_address = ip_address
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print('正在与', self.ip_address, ':', self.port, '建立连接...')
            self.sock.connect((self.ip_address, self.port))
            password =md5(password.encode()).hexdigest()
            thread = Thread(target=self.send_message, args=('LOGIN',username,password))
            thread.start()
        except socket.error:
            return False

    def send_message(self, cmd='LOGIN', username='admin', \
                    password=md5('123456'.encode()).hexdigest(), source='', target=''):
        send_data = {'CMD': cmd, 
                    'USERNAME': username,
                    'PASSWORD': password,
                    'SOURCE':source,
                    'TARGET':target}
        for key in list(send_data.keys()):
            if send_data[key] == '':
                del send_data[key]
        self.sock.send(bytes(json.dumps(send_data), encoding='utf-8'))
        recv_data = self.sock.recv(1024).decode()
        self.queue.put(json.loads(recv_data))

    # def register(self, username, password, question, answer, activeCode):
    #     senddata = {'type': 1, 'userName': username,
    #                 'passWord': md5(password.encode()).hexdigest(), 'question': question,
    #                 'answer': answer, 'activeCode': activeCode}
    #     return self.sendMessage(senddata)

    # def findquestion(self, username):
    #     senddata = {'type': 2, 'userName': username}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     data = self.sock.recv(1024).decode()
    #     data = json.loads(data)
    #     return data

    # def findpass(self, username, answer, newPassword):
    #     senddata = {'type': 3, 'userName': username, 'answer': answer, 'newPassword': md5(newPassword.encode()).hexdigest()}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     recvdata = self.sock.recv(1024).decode()
    #     data = json.loads(recvdata)
    #     return data

    # def back(self):
    #     senddata = {'CMD': 'BACK'}
    #     return self.sendMessage(senddata)

    # def put(self, filelist, sizes):
    #     senddata = {'CMD': 'PUT', 'files': filelist, 'sizes': sizes}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     data = self.sock.recv(1024).decode()
    #     data = json.loads(data)
    #     return data['port']

    # def get(self, filelist, isshare=0):
    #     if isshare == 0:
    #         cmd = 'GET'
    #     else:
    #         cmd = 'SHAREGET'
    #     senddata = {'CMD': cmd,
    #                 'files': filelist}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     data = self.sock.recv(1024).decode()
    #     data = json.loads(data)
    #     return data['port']

    # def delete(self, filename, filetype):
    #     senddata = {'CMD': 'DELETE', 'fileName':filename,
    #                 'fileType': filetype}
    #     return self.sendMessage(senddata)

    # def rename(self, sourcename, destname):
    #     senddata = {'CMD': 'RENAME', 'sourceName': sourcename, 'destName': destname}
    #     return self.sendMessage(senddata)

    # def makedir(self, dirname):
    #     senddata = {'CMD': 'MAKEDIR', 'dirName': dirname}
    #     return self.sendMessage(senddata)

    # def listinfo(self, dirname=''):
    #     senddata = {'CMD': 'LIST', 'dirName': dirname}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     recvdata = self.sock.recv(1024*100).decode()
    #     data = json.loads(recvdata)
    #     return data

    # def looksharefile(self, sharecode):
    #     senddata = {'CMD': 'SHARELIST', 'SHARECODE': sharecode}
    #     self.sock.send(bytes(json.dumps(senddata), encoding='utf-8'))
    #     recvdata = self.sock.recv(1024*100).decode()
    #     data = json.loads(recvdata)
    #     return data

    # def move(self, filepath, filetype, destpath='share'):
    #     senddata = {'CMD': 'MOVE', 'filePath': filepath, 'destPath': destpath, 'fileType': filetype}
    #     return self.sendMessage(senddata)

    # def bye(self):
    #     self.sock.close()

