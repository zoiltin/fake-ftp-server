from socket import *
from multiprocessing import Process

IP = "192.168.72.132"
PORT = 1234
ADDR_MAIN = (IP, PORT)
ADDR_EXT = (IP,62501)

def epsv(s_ext):
    s_ext.bind(ADDR_EXT)
    s_ext.listen()
    connect, addr = s.accept()
    connect.send(b'hello')

def center(connect):
    res = []
    connect.send(b"220 (vsFTPd 3.0.3)\n")
    while True:
        msg = connect.recv(1024)
        print(msg.decode())
        data = ''
        rep = b'\n'
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
            s_ext = socket()
            p_ext = Process(target=epsv, args=(s_ext,))
            p_ext.start()
            rep = b'229 Entering Extended Passive Mode (|||62501|)\n'
            # connect.send(rep)
            # data = connect.recv(1024).decode()
            # p_ext.close()
            # print(data)
            # return 0
        elif 'RETR ' == msg.decode()[:5]:
            data = msg.decode()[5:]
        res.append(data)
        # if rep == b'':
        #     print('******  '+msg.decode())
        # print('> '+(rep.decode()).replace('\n',''))
        connect.send(rep)
        if 'RETR ' == msg.decode()[:5]:
            # s.close()
            print('asdadsasdadsasdasdasd')
            s_ext.close()
            p_ext.join()
            return '.'.join(res)

if __name__ == '__main__':
    s = socket()
    s.bind(ADDR_MAIN)
    s.listen()
    connect, addr = s.accept()
    data = center(connect)
    with open('res.txt','w+') as f:
        f.write(data)
    
