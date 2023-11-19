from socket import *
from multiprocessing import Process

IP = "192.168.72.132"
# 绑定端口
PORT = 1234
ADDR_MAIN = (IP, PORT)
ADDR_EXT = (IP,62501)

def epsv(s_ext,filename):
    s_ext.bind(ADDR_EXT)
    s_ext.listen()
    connect, addr = s.accept()
    connect.send(b'hello')

def center(connect):
    connect.send(b"220 (vsFTPd 3.0.3)\n")
    while True:
        msg = connect.recv(1024)
        print(msg.decode())
        data = ''
        rep = b''
        if 'USER ' == msg.decode()[:5]:
            rep = b'230 Login successful.\n'
        elif 'TYPE I' == msg.decode()[:6]:
            rep = b'200 Switching to Binary mode.\n'
        elif 'TYPE A' == msg.decode()[:6]:
            rep = b'200 Switching to ASCII mode.\n'
        elif 'CWD ' == msg.decode()[:4]:
            data = msg.decode()[4:]
            rep = b'250 Directory successfully changed.\n'
        elif 'EPSV ALL' == msg.decode()[:8]:
            rep = b'200 EPSV ALL ok.\n'
        elif 'EPSV' == msg.decode()[:4]:
            s_ext = s = socket()
            p_ext = Process(target=epsv, args=(s_ext,))
            p_ext.start()
            rep = b'229 Entering Extended Passive Mode (|||62501|)'
        if data != '':
            print(data)
            with open('res.txt','a+') as f:
                f.write(data+'\n')
        if rep == b'':
            print('******  '+msg.decode())
        print('> '+(rep.decode()).replace('\n',''))
        connect.send(rep)

if __name__ == '__main__':
    s = socket()
    s.bind(ADDR_MAIN)
    s.listen()
    while True:
        connect, addr = s.accept()
        p = Process(target=center, args=(connect,))
        p.start()
