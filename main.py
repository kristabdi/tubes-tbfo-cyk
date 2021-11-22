from rules_lexer import rules
import datetime as time
import lexer

input_file = input("Masukkan nama file yang akan dicek : ")

path = './' + input_file
file = open(path, 'r')
content = file.read()

lx = lexer.Lexer(rules, skip_whitespace=False)
lx.input(content)
output = ''

try:
    for tok in lx.tokens():
        if tok == '' :
            output = output
        else :
            output += tok + ' '
except lexer.LexerError as err:
    print('LexerError at position %s' % err.pos)
    
string_container = output.split('NEWLINE')
    
if_toggle = 0
multiline_toggle = False
start_time = time.datetime.now()
total_string = len(string_container)
total_success = 0
total_error = 0
line_counter = 0
print("Parsing {} line(s) of code...".format(total_string))
for text in string_container :
    line_counter += 1
    if text.find('TRIPLEQUOTE') != -1 and multiline_toggle == False :
        multiline_toggle = True
        total_success += 1
    elif (text.find('TRIPLEQUOTE') != -1) and multiline_toggle == True :
        multiline_toggle = False
        total_success += 1
    else :
        if (text == ' ' or text == ''):
            print("",end='')
            total_success += 1
        elif multiline_toggle == False :
            if text.find(' IF') != -1 :
                if_toggle += 1
                if lexer.process(text) :
                    total_success += 1
                else :
                    print("Error at line {}.".format(line_counter))
                    total_error += 1
            elif text.find('ELIF') != -1 :
                if if_toggle > 0 :
                    text = 'ELIFTOK' + text
                if lexer.process(text) :
                    total_success += 1
                else :
                    print("Error at line {}.".format(line_counter))
                    total_error += 1
            elif text.find('ELSE') != -1 :
                if if_toggle > 0 :
                    text = 'ELIFTOK' + text
                if_toggle -= 1
                if lexer.process(text) :
                    total_success += 1
                else :
                    print("Error at line {}.".format(line_counter))
                    total_error += 1
            else :
                if lexer.process(text) :
                    total_success += 1
                else :
                    print("Error at line {}.".format(line_counter))
                    total_error += 1
    
if (total_error == 0) :
    print("The file is parsed successfully! No errors detected.")
else :
    print("{} Error(s) detected on the file.".format(total_error))
finish_time = time.datetime.now()
elapsed_time = finish_time - start_time
print("Time elapsed : {}.{} seconds".format(elapsed_time.seconds, elapsed_time.microseconds//1000))