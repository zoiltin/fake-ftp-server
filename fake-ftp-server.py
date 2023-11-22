from socket import *
from multiprocessing import Process
import time
import sys

def get_host_ip():
    try:
        s = socket(AF_INET,SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def epsv(s_ext):
    s_ext.bind(ADDR_EXT)
    s_ext.listen()
    time.sleep(0.5)   # wait for 2th channel
    s_ext.close()
    return 0

def clear_null(res):
    new = []
    for i in res:
        if i != '':
            new.append(i)
    return new

def center(connect):
    res = []
    connect.send(b"220 (vsFTPd 3.0.3)\n")
    print('[*]Waiting for data...')
    while True:
        msg = connect.recv(1024)
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
            rep = b'229 Entering Extended Passive Mode (|||63568|)\n'
            time.sleep(0.5)  # wait for 2th channel
        elif 'RETR ' == msg.decode()[:5]:
            data = msg.decode()[5:]
        res.append(data[:-2])
        connect.send(rep)
        if 'RETR ' == msg.decode()[:5]:
            time.sleep(1)  # wait for 2th channel
            p_ext.close()
            return '/'.join(clear_null(res))

if __name__ == '__main__':
    IP = get_host_ip()
    PORT = int(sys.argv[1])
    ADDR_MAIN = (IP, PORT)
    ADDR_EXT = (IP,63568)
    print(f'[*]Listening {IP} on {PORT} and 63568 ...')
    output = sys.argv[2]
    s = socket()
    s.bind(ADDR_MAIN)
    s.listen()
    connect, addr = s.accept()
    print(f'[*]Get connection from {addr}.')
    try:
        data = center(connect)
    except:
        print('[-]Failed to get data.')
    finally:
        s.close()
        print('asdasdads')
    with open(output,'w+') as f:
        f.write(data)
    print(f'[*]Data has been written into {output}.')