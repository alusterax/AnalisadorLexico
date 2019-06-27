import re
import pandas as pd
import numpy as np
palavrasReservadas = {'AND':'41',
                      'BEGIN':'26',
                      'CALL':'30',
                      'CASE':'45',
                      'CONST':'23',
                      'DO':'35',
                      'ELSE':'33',
                      'END':'27',
                      'FOR':'43',
                      'IF':'31',
                      'INTEGER':'28',
                      'NOT':'42',
                      'OF':'29',
                      'OR':'40',
                      'AND':'41',
                      'PROCEDURE':'25',
                      'PROGRAM':'22',
                      'READLN':'38',
                      'REPEAT':'36',
                      'THEN':'32',
                      'TO':'44',
                      'UNTIL':'37',
                      'VAR':'24',
                      'WHILE':'34',
                      'WRITELN':'39'}

charArray = {'.':['16','PONTO'],';':['14','PONTO E VIRGULA'],',':['15', 'VIRGULA'],':':['13','DOIS PONTOS'],
             '(':['17','ABRE PARENT.'],')':['18','FECHA PARENT.']}
charCombination = {':=':'12','(*':'99','*)':'98'}
operadores = {'<':['9','MENOR'],'>':['7','MAIOR'],'=':['6','IGUAL'],'*':['4','MULTIPLICADOR'],'/':['5','DIVISOR'],
              '+':['2','MAIS'],'-':['3','MENOS']}
operadoresCombinados = {'>=':['8','MAIOR IGUAL'],'<=':['10','MENOR IGUAL']}
rules = ['([0-9]+(.[0-9]+))','DECIMAL']

classificados = []
nextWord = False
comentario = False
isNum = False
isString = False
numeral = ''
fullComment = ''

def readTxt():
    print ('-- Lendo arquivo de texto --\n')
    l,f = [],[]
    g = open('codigoTeste2.txt', 'r')
    g = g.read()
    a = g.replace('\n',' ')
    a = a.replace('.',' . ')
    a = a.replace(';',' ; ')
    a = a.replace(',',' , ')
    a = a.replace('+',' + ')
    a = a.replace('-',' - ')
    a = a.replace('>',' > ')
    a = a.replace('<',' < ')
    a = a.replace(':',' : ')
    a = a.replace('=',' = ')
    a = a.replace('(',' ( ')
    a = a.replace(')',' ) ')
    a = a.replace('*',' * ')
    a = a.replace('"',' " ')
    l = a.split(' ')
    for item in l:
        if (item != ''):
            f.append(item)
    return f

def isPalavraReservada(word):
    return word in palavrasReservadas

def isSpecialChar(word):
    return word in charArray

def isIdentfier(word):
    if re.match('^[0-9]', word) != None: 
        raise ValueError(word + ' Identificadores não podem iniciar com numerais')
    if re.fullmatch('^[a-zA-Z0-9]{1,}$',word) != None:
        if re.fullmatch('^[a-zA-Z0-9]{1,30}$',word) != None:
            return True
        else:
            raise ValueError(word + ' Identificador contém mais de 30 caracteres.')
def isOperador(word):
    return word in operadores
    
def isNumber(word):
    return re.fullmatch('^[0-9]{1,}$',word) != None

def trataInteger(lista, index, char):
    global isNum
    global numeral
    if isNumber(char):
        nextChar = lista[index + 1]
        if nextChar == '.':
            raise ValueError(char + '.' + lista[index + 2] + ' Não é um valor inteiro.')
        elif int(char) > 32767:
            raise ValueError(char + ' Valor ultrapassou o tamanho inteiro máximo permitido de 32767.')
        else:
            classificados.append(('',numeral + char,'INTEIRO'))
            numeral = ''
            
def trataCaracter(lista, index, char):
    global nextWord
    global numeral
    keyChar = charArray[char]
    if keyChar[0] == '13':
        if lista[index + 1].upper() in palavrasReservadas:
            classificados.append((keyChar[0],char,keyChar[1]))
        elif lista[index + 1] == '=':
            c = char + lista[index + 1]
            classificados.append((charCombination[c],c,'ATRIBUIÇÃO'))
            nextWord = True
        else:
            raise ValueError(char + lista[index + 1] + ' Não é reconhecido como comando valido.')
    else:
        classificados.append((keyChar[0],char,keyChar[1]))
        
def trataOperador(lista, index, char):
    global nextWord
    global numeral
    op = operadores[char]
    if char == '-':
        print(char  + ' ' + numeral)
        lastChar = lista[index - 1]
        if len(lista) > index + 1 and not ((isNumber(lastChar) or isIdentfier(lastChar))):
            if numeral != '-': numeral += char
            return
        else:
            classificados.append((op[0],char,op[1]))
            return
    if char in ['<','>']:
        if len(lista) < index + 1 and lista[index + 1] == '=':
            op = operadoresCombinados[char+'=']
            classificados.append((op[0],char+'=',op[1]))
            nextWord = True
        else:
            classificados.append((op[0],char,op[1]))
    else:
        classificados.append((op[0],char,op[1]))
    
def validaExistencia(l, i, word):
    global specialChar
    if isPalavraReservada(word.upper()):
        classificados.append((palavrasReservadas[word.upper()],word,'PALAVRA RESERVADA'))
        return
    if isSpecialChar(word):        
        trataCaracter(l,i,word)
        return
    if isOperador(word):
        trataOperador(l, i, word)
        return
    if isNumber(word):
        trataInteger(l, i, word)
        return
    if isIdentfier(word):
        classificados.append(('102',word,'IDENTIFICADOR'))
        return
    
    raise ValueError(word + ' Não é reconhecido como comando valido.')
        
def validaComentario(lista, index, char):
    global comentario
    global nextWord
    global fullComment
    if lista[index-1]+char == '*)':
        comentario = False
        nextWord = True
        fullComment += char
        classificados.append(('101',fullComment,'COMENTARIO'))
        print(fullComment)
        fullComment = ''
        return True
    elif len(lista) > index + 1 and char+lista[index+1] == '(*':
        comentario = True
        fullComment += char
        return True
    elif comentario:
        fullComment += ' ' + char
        return True
    
def validaString(char):
    global isString
    global nextWord
    global fullComment
    if comentario: return
    if char == '"':
        if isString:
            isString = False
            fullComment += char
            classificados.append(('100',fullComment,'STRING'))
            fullComment = ''
            nextWord = True
        else:
            isString = True
            fullComment += char
            nextWord = True
    elif isString:
        fullComment += ' ' + char
        nextWord = True

def geraHtml():
    global classificados
    pd.set_option('display.max_colwidth', -1)
    classificados = np.array(classificados)
    data = pd.DataFrame({'Código':classificados[:,0],'Token':classificados[:,1],'Descrição':classificados[:,2]})
    data.to_html('Lexico.html', index=False )  

def cursor(l):
    global nextWord
    global comentario
    global fullComment
    global isNum
    global classificados
    global isString
    try:
        for i,p in enumerate(l):
            validaComentario(l, i, p)
            validaString(p)
            if comentario or isString:
                continue
            if nextWord:
                nextWord = False
                continue
            validaExistencia(l, i, p)
        geraHtml()
        print('Finalizada Analise sem Erros.')
    except ValueError as e:
        print('ERRO: ' + str(e)) 
        geraHtml()
        
l = readTxt()
cursor(l)