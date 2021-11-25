from grammarconverter import getCNF
from cyk_parser import CYKParser
import sys
import os

keygram = {"if" : "a", "elif" : "b", "else" : "c", "for" : "d", "in" : "e", "while" : "f", "continue" : "g", "pass" : "h", "break" : "i", "class" : "j", "def" : "k", "return" : "l", "as" : "m", "import" : "n", "from" : "o", "raise" : "p", "and" : "q", "or" : "r", "not" : "s", "is" : "t", "True" : "u", "False" : "v", "None" : "w", "with" : "A"}

# PCOLOR
normal = "\033[1;37;40m"
red = "\033[1;37;41m"

def checkFiniteAutomata(inp):
    kataBaru = ""
    res1 = inp.split('\n')
    for res2 in res1:
        res = []
        res2 = res2.translate({ord(":"): " : "})
        res2 = res2.translate({ord("("): " ( "})
        res2 = res2.translate({ord(")"): " ) "})
        res2 = res2.translate({ord("["): " [ "})
        res2 = res2.translate({ord("]"): " ] "})
        res2 = res2.translate({ord('"'): ' """ '})
        res2 = res2.translate({ord('\''): ' """ '})
        res2 = res2.translate({ord(','): ' , '})
        res2 = res2.translate({ord('+'): ' + '})
        res2 = res2.translate({ord('-'): ' - '})
        res2 = res2.translate({ord('/'): ' / '})
        res2 = res2.translate({ord('%'): ' % '})
        res2 = res2.translate({ord('*'): ' * '})
        res2 = res2.translate({ord('^'): ' ^ '})
        res2 = res2.translate({ord('!'): ' ! '})
        res3 = res2.split()
        res = res3
        open1 = True
        open2 = True
        newLine = True
        newLineActive = True
        for i in range(len(res)):
            if(res[i] == "\n"):
                kataBaru += "\n"
                continue
            if(len(res[i]) == 1 and open2):
                j = ord(res[i])
                if(j == 95 or (j > 64 and j < 91) or (j > 96 and j < 123) and open1):
                    kataBaru += "x"
                    newLine = False
                elif(j > 47 and j < 58 and open1):
                    kataBaru += "y"
                    newLine = False
                elif(open1):
                    kataBaru += res[i]
                    newLine = False
            elif(open1):
                if(res[i] in keygram and open2):
                    kataBaru += keygram.get(res[i])
                    newLine = False
                elif(res[i] == "**" or res[i] == "==" and open2):
                    kataBaru += res[i]
                    newLine = False
                elif(res[i] == '"""' or res[i] == '\''):
                    if(open2):
                        open2 = False
                        if(newLine):
                            kataBaru += "x=x"
                            newLine = False
                            newLineActive = False
                        else:
                            kataBaru == "+x"
                    else:
                        open2 = True
                        if(newLineActive):
                            kataBaru += "x"
                        else:
                            kataBaru += "+x"
                elif(open2):
                    benar = True
                    first = True
                    angka = True
                    cekAngka = True
                    for b in res[i]:
                        j = ord(b)
                   
                        if(b == "(" or b == ")" or b == "[" or b == "]"):
                            kataBaru += b
                            newLine = False
                        elif(first and benar):
                            if(j != 95 and (j <= 64 or j >= 91) and (j <= 96 or j >= 123) and (j <= 47 or j >= 58)):
                                benar = False
                                first = False
                                angka = False
                                cekAngka = False
                                kataBaru += "R"
                                newLine = False
                            else:
                                if(j > 47 and j < 58):
                                    first = False
                                    continue
                                else:
                                    first = False
                                    cekAngka = False
                        if(cekAngka):
                            if(j <= 47 or j >= 58):
                                cekAngka = False
                               
                                benar = False
                                angka = False
                        if(benar and not first and not cekAngka):
                            if((j > 47 and j < 58)):
                                continue
                            else: 
                                angka = False
                                if(j != 95 and (j <= 64 or j >= 91) and (j <= 96 or j >= 123)):
                                 
                                    benar = False
                    if(angka or cekAngka):
                        kataBaru += "y"
                        newLine = False
                    elif(benar):
                        kataBaru += "x"
                        newLine = False
                    elif(not benar and not first and not angka):
                        kataBaru += "R"
                        newLine = False
        kataBaru += "\n"
    return (kataBaru)

def readFile(path):
    with open(path, "r") as f:
        content = f.read()
    return content

def header():
    print()
    print("██████╗░██╗░░░██╗████████╗██╗░░██╗░█████╗░███╗░░██╗  ░█████╗░░█████╗░███╗░░░███╗██████╗░██╗██╗░░░░░███████╗██████╗░")
    print("██╔══██╗╚██╗░██╔╝╚══██╔══╝██║░░██║██╔══██╗████╗░██║  ██╔══██╗██╔══██╗████╗░████║██╔══██╗██║██║░░░░░██╔════╝██╔══██╗")
    print("██████╔╝░╚████╔╝░░░░██║░░░███████║██║░░██║██╔██╗██║  ██║░░╚═╝██║░░██║██╔████╔██║██████╔╝██║██║░░░░░█████╗░░██████╔╝")
    print("██╔═══╝░░░╚██╔╝░░░░░██║░░░██╔══██║██║░░██║██║╚████║  ██║░░██╗██║░░██║██║╚██╔╝██║██╔═══╝░██║██║░░░░░██╔══╝░░██╔══██╗")
    print("██║░░░░░░░░██║░░░░░░██║░░░██║░░██║╚█████╔╝██║░╚███║  ╚█████╔╝╚█████╔╝██║░╚═╝░██║██║░░░░░██║███████╗███████╗██║░░██║")
    print("╚═╝░░░░░░░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝  ░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚══════╝╚═╝░░╚═╝")
    print("                                                ʙʏ Mɪᴄʜᴀᴇʟ, Kʀɪsᴛᴏ, ᴀɴᴅ Jᴀsᴏɴ                                      \n")

if __name__ == "__main__":
    header()

    # Get CNF
    CNF = getCNF("grammar.txt")
    namaFile = input("Masukkan nama file: ")

    # Check file exist
    while os.path.isfile(namaFile) == False:
        namaFile = input("File tidak ditemukan! Masukkan ulang nama file yang valid: ")

    # Input
    if (len(sys.argv) < 2):
        path = namaFile
    else:
        path = sys.argv[1]

    try:
        inp = readFile(path)
    except Exception as e:
        print(red + "Error:" + str(e) + normal)
        print("Menggunakan testcase default: 'inputAcc.py'\n")
        try:
            path = "inputAcc.py"
            inp = readFile(path)
        except Exception as e:
            print(red + "Error:" + str(e) + normal)
            print("Menutup program...\n")
            exit(0)

    source = inp

    # Preprocess
    inp = checkFiniteAutomata(inp)
    

    #Waiting message
    print("Compiling " + str(path) + "...\n")
    print("Menunggu hasil compile...\n")

    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%% RESULT %%%%%%%%%%%%%%%%%%%%%%%%%%")
    if (len(inp) == 0):
        print("Accepted. No errors detected.")
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        exit(0)

    # Parse
    CYKParser(inp, CNF, source)
    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")