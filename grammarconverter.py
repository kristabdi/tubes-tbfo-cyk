from copy import deepcopy
import string

def isNonTerminal(elem):
    # Fungsi untuk mengecek elem dan mengembalikan true jika elem adalah non terminal atau variabel
    if len(elem) == 1:
        return False
    for char in elem:
        # Grammar dibuat dengan memisahkan dengaj _ jika terdiri seperti IF_CONTENT, ITERATE_CONTENT, FLOW_CONTENT ataupun satu kata seperti START, CONTENT
        if char not in (string.ascii_uppercase + '_' + string.digits):
            return False
    return True

def removeUnit(CFG):
    for var in CFG:
        # Mengambil satu line Produksi dari CFG
        productions = CFG[var]
        boolean = True
        while boolean:
            boolean = False
            # Iterasi untuk setiap unit produksi yang ada di setiap line productions
            for tempProduction in productions:
                if len(tempProduction) == 1 and isNonTerminal(tempProduction[0]):
                    # Jika production adalah suatu unit produksi dan memiliki panjang 1 maka dihapuskan
                    productions.remove(tempProduction)
                    #  Mengganti non terminal menjadi produksi
                    newProduction = deepcopy([tempProduction for tempProduction in CFG[tempProduction[0]] if tempProduction not in productions])
                    productions.extend(newProduction)
                    boolean = True
                    break
    return CFG
'''
Example
S->0A|1B|C
A->0S|00
B->1|A
C->01

Explanation
Remove S -> C, B -> A karena non terminal -> non terminal
S->0A|1B|01
A->0S|00
B->1|0S|00
C->01
'''

def getCFGFile(filename):
    RULE_DICT = {}
    with open(filename, 'r') as f:
        # Lines adalah list berisi string yang dipisah setiap -> dan \n
        lines = [line.split('->')
                    for line in f.read().split('\n')
                    if len(line.split('->')) == 2]
        for line in lines:
            #  Menghilangan whitespaces
            var = line[0].replace(" ", "")
            rawprod = [rawprodline.split() for rawprodline in line[1].split('|')]
            production = []
            for rawprodline in rawprod:
                production.append([ " " if elem == "__space__" else
                                    "|" if elem == "__or_sym__" else
                                    "\n" if elem == "__new_line__" else
                                    elem for elem in rawprodline])
            RULE_DICT.update({var: production})
    return RULE_DICT

def convertToCNF(CFG):
    newRule = {}
    for var in CFG:
        terminals = []
        productions = CFG[var]
        # Mengumpulkan semua terminal yang ada di produksi
        processProduction = [production for production in productions if len(production) > 1]
        for production in processProduction:
            for elem in production:
                if not(isNonTerminal(elem)) and elem not in terminals:
                    terminals.append(elem)
        # Mmebuat rule baru dan mengupdate produksi
        for i, terminal in enumerate(terminals):
            newRule.update({f"{var}_TERM_{i + 1}": [[terminal]]})
            for idx, j in enumerate(productions):
                if len(j) > 1:
                    for k in range(len(j)):
                        if len(productions[idx][k]) == len(terminal):
                            productions[idx][k] = productions[idx][k].replace(terminal, f"{var}_TERM_{i + 1}")
        # Mengupdate produksi sehingga sesuai dengan A -> BC atau A -> terminal
        idx = 1
        for i in range(len(productions)):
            while len(productions[i]) > 2:
                newRule.update({f"{var}_EXT_{idx}": [[productions[i][0], productions[i][1]]]})
                productions[i] = productions[i][1:]
                productions[i][0] = f"{var}_EXT_{idx}"
                idx += 1
    CFG.update(newRule)
    return CFG

def display(GRAMMAR_DICT):
    for var in GRAMMAR_DICT:
        print(var,"-> ",end="")
        for i in range(len(GRAMMAR_DICT[var])):
            if i == len(GRAMMAR_DICT[var]) - 1:
                print(GRAMMAR_DICT[var][i])
            else:
                print(GRAMMAR_DICT[var][i],"| ",end="")

# FUNGSI UTAMA MENERIMA PATH GRAMMAR DAN MENGEMBALIKAN CNF HASIL KONVERSI
def getCNF(filename) :
    CFG = getCFGFile(filename)
    removedUnitCFG = removeUnit(CFG)
    CNF = convertToCNF(removedUnitCFG)
    return CNF


def CNFtoFile(CNF) :
    cnftofile = "\n".join([str(elem) for elem in CNF])
    open('cnf.txt', 'w').write(cnftofile)

# Driver
CNF = getCNF("grammar.txt")
# display(CNF)
CNFtoFile(CNF)