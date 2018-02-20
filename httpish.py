import socket
import sys

assert sys.version_info >= (2, 5)

ver = sys.version_info[0]

if ver == 2:
    from urllib import urlencode
else:
    from urllib.parse import urlencode


class httpcon:
    def __init__(self, target, host, port=80):
        self.txt = target + " to "+host+":"+str(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s = s
        self.buf = ""
        s.connect((host, port))
        if target[0:1] == "/":
            target = "GET " + target
        self.send(target + " HTTP/1.1\r\n")
        self.send("Host: " + host + "\r\n")  # purposefully ignoring port
        if target[0:5] == "POST ":
            self.send("Content-Type: application/x-www-form-urlencoded\r\n")
            self.send("Transfer-Encoding: chunked\r\n")
        self.send("\r\n")

    def recvline(self):
        return self.recvuntil("\n")

    def recvuntil(self, str):
        while str not in self.buf:
            self.fillBuf()
        end = self.buf.index(str)+len(str)
        ret = self.buf[0:end]
        self.buf = self.buf[end:]
        return ret

    def fillBuf(self):
        self.buf += self.s.recv(1024).decode()

    def send(self, buf):
        return self.s.sendall(buf.encode())

    def sendPostData(self, data):
        send = ""
        if isinstance(data, str):
            send = data
        elif isinstance(data, dict):
            send = urlencode(data)
        else:
            raise ValueError("post data must be dict (or string)")
        self.send(hex(len(send))[2:].upper() + "\r\n" + send + "\r\n")
        self.send("0\r\n\r\n")

    def close(self):
        return self.s.close()

    def getRet(self):
        statusLine = self.recvline().strip()
        self.statusLine = statusLine
        [ver, code] = statusLine.split(" ")[0:2]
        return int(code)

    def expect200(self):
        ret = self.getRet()
        if ret != 200:
            self.close()
            raise HTTPException(
                self.txt + " did not return 200 (returned "+ret+")!")
        return ret


def parseURL(url):
    if url[0:7] == "http://":
        url = url[7:]
    else:
        raise ValueError("HTTP is the only supported protocol")
    host = ""
    port = 80
    if ":" in url:
        idx = url.index(":")
        host = url[0:idx]
        url = url[idx+1:]
        idx = url.index("/")
        port = int(url[0:idx])
        url = url[idx:]
    else:
        idx = url.index("/")
        host = url[0:idx]
        url = url[idx:]
    return [host, port, url]


def verb(url, verb):
    [host, port, path] = parseURL(url)
    return httpcon(verb.upper()+" "+url, host, port)


def GET(url):
    return verb(url, "GET")


def POST(url):
    return verb(url, "POST")


def POSTret(url, dict):
    c = POST(url)
    c.sendPostData(dict)
    ret = c.getRet()
    c.close()
    return ret


def GETret(url):
    c = GET(url)
    ret = c.getRet()
    c.close()
    return ret


def POST200(url, dict):
    ret = POSTret(url, dict)
    if ret != 200:
        raise HTTPException(
            "POST to "+url+" did not return 200 (returned "+ret+")!")
    return ret


def GET200(url):
    ret = GETret(url)
    if ret != 200:
        raise HTTPException(
            "GET to "+url+" did not return 200 (returned "+ret+")!")
    return ret


class HTTPException(Exception):
    pass
