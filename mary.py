from httpish import GET200, POST200, GET
import re

BASE = "http://pegasus.noise"

def mute():
    return GET200(BASE+"/mute/")


def unmute():
    return GET200(BASE+"/unmute/")


def say(text):
    return POST200(BASE+"/say/", {'txt': text})


def setLanguage(code):
    return POST200(BASE+"/lang/", {'lang': code})


def getLanguage():
    c = GET(BASE+"/lang/")
    c.expect200()
    c.recvuntil("selected>")
    lang = c.recvuntil("<")[0:-1].strip()
    c.recvuntil("</html>")
    c.close()
    return lang


def getLanguages():
    c = GET(BASE+"/lang/")
    c.expect200()
    c.recvuntil('<select name="lang">')
    options = c.recvuntil("</select>").strip()
    c.recvuntil("</html>")
    c.close()
    return re.split(r"\s+", re.sub(r'<[^>]+>', " ", options))[1:-1]
