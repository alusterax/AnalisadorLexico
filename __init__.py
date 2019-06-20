def readTxt():
    print ('-- Lendo arquivo de texto --\n')
    l,f = [],[]
    g = open('codigoTeste.txt', 'r')
    g = g.read()
    print (f'{g} \n')
    a = g.replace('\n',' ')
    l = a.split(' ')
    for item in l:
        if (item != ''):
            f.append(item)
    return f

def validaExistencia(wordFull):
    print('\n')

def cursor(l):
    for p in l:
        wordFull = ''
        for idx,letra in enumerate(p):
            if (idx == 0):
                wordFull = letra
            else:
                wordFull = f'{wordFull}{letra}'
            validaExistencia(wordFull)
            print(wordFull)

l = readTxt()
print (f'Keys: \n\n{l}\n')
cursor(l)
