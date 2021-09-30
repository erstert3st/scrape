import requests
from bs4 import BeautifulSoup
import string
import os
from signal import signal, SIGINT #async
import sys
import argparse
from colorama import init
from string import ascii_lowercase
from itertools import product
init()

#ToDo, DB handler for codes,  DockerImage, Volume, Image Compare Tool, VPN  

def handler(signal_received, frame):
    print("hi")
    sys.exit(0)


headers = {
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
}


code_chars_123 = list(string.ascii_lowercase) + ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
code_chars_abc = list(string.ascii_lowercase) + ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]


base_123 = len(code_chars_123)
#add db


def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number, base):
    if number < 0:
        return '-' + str_base(-number, base)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)

def next_code_123(curr_code):
    curr_code_num = int(curr_code, base_123)
    return str_base(curr_code_num + 1, base_123)

def next_code_abc(curr_code):
 #   print("-----")
  #  print(curr_code)
    curr_code_Var = curr_code[-1]
  #  print(curr_code_Var)

    if curr_code_Var == 'z':
        curr_code_Var = "aa"
   #     print("nextRound-----")
    else:
        curr_code_Var = chr(ord(curr_code_Var) + 1)
   # print(curr_code_Var)
    #print(curr_code)

    curr_code = curr_code[:-1] + curr_code_Var
    #print(curr_code)
    #print("----------")

    return curr_code


def generateNextAll(code):
    codeTemp = code
    print(codeTemp)    
    codeList = []
    abcList = [''.join(i) for r in range(1,4) for i in product(ascii_lowercase, repeat=r)]    
    for abcVal in abcList:
        codeList.append(codeTemp + abcVal)
    #print(codeList)
    return codeList

def generateNext26(code, codeList, counterAbc, counterMultiplier):
   # print("---------")
    codeTemp = ""
    if(counterAbc == 0):
        codeTemp = code[:-1]
        codeList.clear()
    elif(counterAbc >= 1 and  counterAbc <= 52):
        codeTemp = code[:-1]
        codeTemp += code_chars_abc[counterAbc -1]
        codeList.clear()
    elif(counterAbc >= 53 ):
        exit(0)
    else:
        print("lol2")

        exit(0)    

    for currentNumber in range(0, 26):
           # print(currentNumber)
            codeList.append(codeTemp + code_chars_abc[currentNumber])
           # print(codeList[currentNumber])
           # print(counterAbc)
    return codeList,counterMultiplier

def get_img_url(code):
    html = requests.get(f"https://prnt.sc/{code}", headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    img_url = soup.find_all('img', {'class': 'no-click screenshot-image'})
    return img_url[0]['src']

def get_img(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{path}.png", 'wb') as f:
            f.write(response.content)


def action(code,imagedir,no_entropy,no_cc,no_keyword):
    print(code)
    codeTemp = code
    zaeler = ['1']
    for val in zaeler:
        codeTemp = codeTemp[:-1]
        print(codeTemp)
        codeListDone = generateNextAll(codeTemp)
       
        for currentCode in codeListDone:
            try:
                print(os.getcwd()+"/output/"+currentCode)
                img_path = os.getcwd()+"/output/"+currentCode
                url = get_img_url(currentCode)
                get_img(url, img_path) 
                            
            except Exception as e:
                print(e)


signal(SIGINT, handler)

parser = argparse.ArgumentParser()
parser.add_argument('--code', action='store', dest='code', help='Start code for prnt.sc', required=True)
parser.add_argument('--imagedir', action='store', dest='imagedir', help='Image directory for logo search', default=None)
parser.add_argument('--no-entropy', action='store_true', dest='no_entropy', help="Don't search for high entropy", default=None)
parser.add_argument('--no-cc', action='store_true', dest='no_cc', help="Don't search for credit card", default=None)
parser.add_argument('--no-keyword', action='store_true', dest='no_keyword', help="Don't search for keywords", default=None)
argv = parser.parse_args()

if argv.no_entropy:
    argv.no_entropy = True
if argv.no_cc:
    argv.no_cc = True
if argv.no_keyword:
    argv.no_keyword = True

action(argv.code,argv.imagedir,argv.no_entropy,argv.no_cc,argv.no_keyword)