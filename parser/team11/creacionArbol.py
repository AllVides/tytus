from Ast import Nodo

# Función que crea el Nodo para la producción Alter Table
def getAlterTableNode(t):
    childs = []
    g = '<alter_instr> ::= ALTER TABLE ID '
    if len(t) == 5:
        g += '<list_alter_column>\n'
        childs.append(Nodo('Operacion','ALTER COLUMN',t[4],t.lexer.lineno,0,g))
    elif len(t) == 7:
        g += str(t[4])+' COLUMN <listtablas>\n'
        childs.append(Nodo('Operacion',t[4]+' '+t[5],t[6],t.lexer.lineno,0,g))
    elif len(t) == 9:
        if str(t[4]).upper() == 'RENAME':
            g += '\"RENAME\" COLUMN ID TO ID\n'
            n1 = Nodo('ID',t[6],[],t.lexer.lineno)
            n2 = Nodo('ID',t[8],[],t.lexer.lineno)
            childs.append(Nodo('Operacion',t[4]+' '+t[5],[n1,n2],t.lexer.lineno,0,g))
        else:
            g += '\"ADD\" \"CHECK\" \"PARIZQ\" <condicion> \"PARDER\"\n'  
            childs.append(Nodo('Operacion',t[4]+' '+t[5],[t[7]],t.lexer.lineno,0,g))
    elif len(t) == 11:
        g += '\"ADD\" \"CONSTRAINT\" ID \"UNIQUE\" \"PARIZQ\" ID \"PARDER\"\n'
        n1 = Nodo('ID',t[6],[],t.lexer.lineno)
        n2 = Nodo('ID',t[9],[],t.lexer.lineno)
        childs.append(Nodo('Operacion',t[4]+' '+t[5],[n1,n2],t.lexer.lineno,0,g))
    elif len(t) == 12:
        g += '\"ADD\" \"FOREIGN\" \"KEY\" \"PARIZQ\" ID \"PARDER\" \"REFERENCES\" ID\n'
        n1 = Nodo('Columna',t[8],[],t.lexer.lineno)
        n2 = Nodo('Referencia',t[11],[],t.lexer.lineno)
        childs.append(Nodo('Operacion',t[4]+' '+t[5]+' '+t[6],[n1,n2],t.lexer.lineno,0,g))
    elif len(t) == 10:
        g += '\"ALTER\" \"COLUMN\" ID \"SET\" \"NOT\" \"NULL\"\n'
        n = Nodo('Columna',t[6],[],t.lexer.lineno)
        childs.append(Nodo('Operacion',t[7]+' '+t[8]+' '+t[9],[n],t.lexer.lineno,0,g))
    else:
        childs.append(Nodo('Error','getAlterTable',[],t.lexer.lineno)) 
    return  Nodo('ALTER TABLE',t[3],childs,t.lexer.lineno)

# Función para crear el Nodo del tipo de la Columna
def getColumnTypeNode(t):
    if len(t) == 2:
        return Nodo('Tipo', t[1], [], t.lexer.lineno)
    elif len(t) == 3:
        return Nodo('Tipo', t[1], [t[2]], t.lexer.lineno)
    elif len(t) == 5:
        n = Nodo('Limite',str(t[3]),[],t.lexer.lineno)
        return Nodo('Tipo', t[1], [n], t.lexer.lineno)
    elif len(t) == 6:
        n = Nodo('Limite',str(t[4]),[],t.lexer.lineno)
        return Nodo('Tipo', t[1]+' '+t[2], [n], t.lexer.lineno)
    elif len(t) == 7:
        n1 = Nodo('Digitos',str(t[3]),[],t.lexer.lineno)
        n2 = Nodo('Cifras',str(t[5]),[],t.lexer.lineno)
        return Nodo('Tipo',t[1],[n1,n2],t.lexer.lineno)
    else:
        return Nodo('Error','getColumType',[],t.lexer.lineno)


############################################ Funciones AST Querys ########################################

# Función que crea el Nodo para la producción Select
def getSelect(t):
    gramatica = '<select_instr> ::= \"SELECT\" '
    childs = []
    if t[2] != None:
        childs.append(t[2])
        gramatica += '<termdistinct> '
    childs.append(t[3])
    gramatica += '<select_list> '
    if t[4] != None:
        gramatica += '\"FROM\" '
        a = t[4]
        if a[0] != None:
            childs.append(a[0])
            gramatica += '<listatablasselect> '
        if a[1] != None:
            childs.append(a[1])
            gramatica += '<whereselect> '
        if a[2] != None:
            childs.append(a[2])
            gramatica += '<groupby> '
        if a[3] != None:
            childs.append(a[3])
            gramatica += '<orderby> '
    gramatica += '\"PTCOMA\" '
    return Nodo('SELECT', '', childs, t.lexer.lineno, 0, gramatica)

def getSelectSimple(t):
    childs = Nodo('Rows', '', t[2], t.lexer.lineno)     # pendiente 
    return Nodo('SELECT', '', [childs], t.lexer.lineno)

def getDistinct(t) : 
    if t[1] != None:                                    # pendiente
        t[0] = Nodo('DISTINC', '', [], t.lexer.lineno, 0, '<termdistinct> ::= \"DISTINCT\" ')
    return t[0]

def getSelectList(t):
    if t[1] == '*':
        gramatica = '<selectlist> ::= \"ASTERISCO\"'
        return Nodo('ASTERISCO', '*', [], t.lexer.lineno, 0, gramatica)
    else :
        gramatica = '<selectlist> ::= <listaselect> \n'
        gramatica += '<listaselect> ::= <listaselect> \"COMA\" <valselect> \n'
        gramatica += '<listaselect> ::= <valselect>'
        return Nodo('ROWS', '', t[1], t.lexer.lineno, 0, gramatica)

def getValSelect(t, etiqueta) :
    if etiqueta == 'ID':
        if t[2] != None :
            gramatica = '<valselect> ::= \"'+str(t[1])+'\" <alias>'
            return Nodo('ID', t[1], [t[2]], t.lexer.lineno,0, gramatica)
        else :
            gramatica = '<valselect> ::= \"'+str(t[1])+'\" '
            return Nodo('ID', t[1], [], t.lexer.lineno, 0, gramatica)

    elif etiqueta == 'ID.ID':
        childs = []
        gramatica = ''
        if t[4] != None :
            gramatica = '<valselect> ::= \"'+str(t[1])+'\" \"PUNTO\" \"'+str(t[3])+'\" <alias> '
            childs.append(Nodo('ID', t[3], [t[4]], t.lexer.lineno))
        else :
            gramatica = '<valselect> ::= \"'+str(t[1])+'\" \"PUNTO\" \"'+str(t[3])+'\" '
            childs.append(Nodo('ID', t[3], [], t.lexer.lineno))
        return Nodo('AliasTabla', t[1], childs, t.lexer.lineno, 0, gramatica)

    elif etiqueta == 'ID.*':
        childs = Nodo('All', '.*', [], t.lexer.lineno)
        gramatica = '<valselect> ::= \"'+str(t[1])+'\" \"PUNTO\" \"ASTERISCO\"'
        return Nodo('AliasTabla', t[1], [childs], t.lexer.lineno, 0, gramatica)

    elif etiqueta == 'funmat_ws':
        if t[2] != None :
            t[1].hijos.append(t[2])
        t[1].gramatica = '<valselect> ::= <funcion_matematica_ws> <alias>\n' + t[1].gramatica
        return t[1]

    elif etiqueta == 'funmat_s':
        if t[2] != None :
            t[1].hijos.append(t[2])
        t[1].gramatica = '<valselect> ::= <funcion_matematica_s> <alias>\n' + t[1].gramatica
        return t[1]

    elif etiqueta == 'funmat_trig':
        if t[2] != None :
            t[1].hijos.append(t[2])
        t[1].gramatica = '<valselect> ::= <funcion_trigonometrica> <alias>\n' + t[1].gramatica
        return t[1]

    elif etiqueta == 'funcbinstring1':
        if t[2] != None :
            t[1].hijos.append(t[2])
        return t[1]

    elif etiqueta == 'funcbinstring2':
        if t[2] != None :
            t[1].hijos.append(t[2])
        return t[1]

    elif etiqueta == 'funcbinstring4':
        if t[2] != None :
            t[1].hijos.append(t[2])
        return t[1]

    elif etiqueta == 'subquery':
        if t[4] != None :
            gramatica = '<valselect> ::=  \"PARIZQ\" <select_instr1> \"PARDER\" <alias> '
            return Nodo('Subquery', '', [t[2], t[4]], t.lexer.lineno, 0, gramatica)
        else :
            gramatica = '<valselect> ::=  \"PARIZQ\" <select_instr1> \"PARDER\"'
            return Nodo('Subquery', '', [t[2]], t.lexer.lineno, 0, gramatica)  

    elif etiqueta == 'agregacion':
        if t[5] != None :
            gramatica = '<valselect> ::=  <agregacion> \"PARIZQ\" <cualquieridentificador> \"PARDER\" <alia> \n'
            gramatica += '<agregacion> ::= \"' + str(t[1]) + '\" '
            return Nodo('Agregacion', t[1], [t[3], t[5]], t.lexer.lineno, 0, gramatica)
        else :
            gramatica = '<valselect> ::=  <agregacion> \"PARIZQ\" <cualquieridentificador> \"PARDER\" \n'
            gramatica += '<agregacion> ::= \"' + str(t[1]) + '\"'
            return Nodo('Agregacion', t[1], [t[3]], t.lexer.lineno, 0, gramatica)  

    elif etiqueta == 'count_ast':
        childs = Nodo('Asterisco', '*', [], t.lexer.lineno)
        if t[5] != None :
            gramatica = '<valselect> ::=  \"COUNT\" \"PARIZQ\" \"ASTERISCO\" \"PARDER\" <alia>'
            return Nodo('Agregacion', t[1], [childs, t[5]], t.lexer.lineno, 0, gramatica)
        else :
            gramatica = '<valselect> ::=  \"COUNT\" \"PARIZQ\" \"ASTERISCO\" \"PARDER\"'
            return Nodo('Agregacion', t[1], [childs], t.lexer.lineno,0, gramatica)  

    else : #'count_val'
        if t[5] != None :
            gramatica = '<valselect> ::=  \"COUNT\" \"PARIZQ\" <cualquieridentificador> \"PARDER\" <alia>'
            return Nodo('Agregacion', t[1], [t[3], t[5]], t.lexer.lineno, 0, gramatica)
        else :
            gramatica = '<valselect> ::=  \"COUNT\" \"PARIZQ\" <cualquieridentificador> \"PARDER\"'
            return Nodo('Agregacion', t[1], [t[3]], t.lexer.lineno, 0, gramatica) 


def getTablaSelect(t) :
    if len(t) == 3:
        if t[2] != None:
            return Nodo('Tabla', t[1], [t[2]], t.lexer.lineno, 0, '<tablaselect> ::= \"'+str(t[1])+'\" <alias>')
        else :
            return Nodo('Tabla', t[1], [], t.lexer.lineno, 0, '<tablaselect> ::= \"'+str(t[1])+'\"')
    else:
        if t[4] != None :
            gramatica = '<tablaselect> ::= \"PARIZQ\" <select_instr1> \"PARDER\" <alias>'
            return Nodo('Subquery', '', [t[2], t[4]], t.lexer.lineno, 0, gramatica)
        else :
            gramatica = '<tablaselect> ::= \"PARIZQ\" <select_instr1> \"PARDER\"'
            return Nodo('Subquery', '', [t[2]], t.lexer.lineno, 0, gramatica)  

def getAlias(t):
    if t[1] == None:
        return t[1]
    elif t[1].lower() == 'as':
        gramatica = '<alias> ::= \"AS\" \"' + str(t[2]) + '\"'
        return Nodo('Alias', t[2], [], t.lexer.lineno, 0, gramatica)
    else :
        gramatica = '<alias> ::= \"'+ str(t[1]) + '\"'
        return Nodo('Alias', t[1], [], t.lexer.lineno, 0, gramatica)

def getSubstring(t):
    childs = [t[3]]
    gramatica = '<condicionwhere> ::= <wheresubstring>\n'
    gramatica += '<wheresubstring> ::= \"SUBSTRING\" \"PARIZQ\" <cadenastodas> \"COMA\" \"ENTERO\" \"COMA\" \"ENTERO\" \"PARDER\" \"IGUAL\" \"CADENASIMPLE\"'
    childs.append(Nodo('DE', str(t[5]), [], t.lexer.lineno))
    childs.append(Nodo('HASTA', str(t[7]), [], t.lexer.lineno))
    childs.append(Nodo('IGUAL', t[9], [], t.lexer.lineno))
    childs.append(Nodo('CADENA', t[10], [], t.lexer.lineno))
    return Nodo("SUBSTRING", '', childs, t.lexer.lineno, 0, gramatica)

def getOpRelacional(t):
    if t[2] == '<>':
        gramatica = '<condicion> ::= <expresion> \"DIFERENTE\" <expresion>'
        return Nodo('OPREL', '\\<\\>', [t[1], t[3]], t.lexer.lineno, 0, gramatica)
    gramatica = '<condicion> ::= <expresion> \"' +t[2]+'\" <expresion>'
    return Nodo('OPREL', '\\'+str(t[2]), [t[1], t[3]], t.lexer.lineno, 0, gramatica)

ef getGroupby(t):
    if len(t) == 4:
        gramatica = '<groupby> ::= \"GROUP\" \"BY\" <listagroupby>' 
        childs = Nodo('LISTA', '', t[3], t.lexer.lineno)
        return Nodo('GROUPBY', '', [childs], t.lexer.lineno, 0, gramatica) 
    else:
        gramatica = '<groupby> ::= \"GROUP\" \"BY\" <listagroupby> \"HAVING\" <condicioneshaving>'
        childs = [Nodo('LISTA', '', t[3], t.lexer.lineno)]
        childs.append(Nodo('HAVING', '', [t[5]], t.lexer.lineno))
        return Nodo('GROUPBY', '', childs, t.lexer.lineno, 0, gramatica) 

def getOrderBy(t) :
    if len(t) == 4:
        gramatica = '<orderby> ::= \"ORDER\" \"BY\" <listaorderby>'
        childs = Nodo('LISTA', '', t[3], t.lexer.lineno)
        return Nodo('ORDERBY', '', [childs], t.lexer.lineno, 0, gramatica)
    else:
        gramatica = '<orderby> ::= \"ORDER\" \"BY\" <listaorderby> <instrlimit>'
        childs = [Nodo('LISTA', '', t[3], t.lexer.lineno)]
        childs.append(t[4])
        return Nodo('ORDERBY', '', childs, t.lexer.lineno, 0, gramatica)

def getValOrder(t):
    if t[3] != None:
        gramatica = '<valororderby> ::= <cualquieridentificador> <ascdesc> <anular>'
        return Nodo('COLUMN', '', [t[1], t[2], t[3]], t.lexer.lineno, 0, gramatica)
    else : 
        gramatica = '<valororderby> ::= <cualquieridentificador> <ascdesc>'
        return Nodo('COLUMN', '', [t[1], t[2]], t.lexer.lineno, 0, gramatica)

def getAscDesc(t) :
    if t[1] != None:
        gramatica = '<ascdesc> ::= \"' + t[1] +'\"'
        return Nodo(t[1], '', [], t.lexer.lineno, 0, gramatica)
    else:
        return Nodo('ASC', '', [], t.lexer.lineno)

def getLimit(t):
    if t[3] != None:
        gramatica = '<instrlimit> ::= \"LIMIT\" \"'+str(t[2])+'\" <instroffset>'
        return Nodo(t[1], str(t[2]), [t[3]], t.lexer.lineno, 0, gramatica)
    else:
        gramatica = '<instrlimit> ::= \"LIMIT\" \"'+t[2]+'\"'
        return Nodo(t[1], str(t[2]), [], t.lexer.lineno, 0, gramatica)

def getIdentificador(t):
    if len(t) == 2:
        gramatica = '<cualquieridentificador> ::= \"'+str(t[1])+'\"'
        return Nodo('ID', t[1], [], t.lexer.lineno,0, gramatica)
    else :
        gramatica = '<cualquieridentificador> ::= \"'+str(t[1])+'\" \"PUNTO\" \"'+str(t[3])+'\"'
        childs = [Nodo('ID', t[3], [], t.lexer.lineno)]
        return Nodo('AliasTabla', t[1], childs, t.lexer.lineno, 0, gramatica)

def getValorNumerico(t):
    if isinstance(t[1], float):
        gramatica = '<cualquiernumero> ::= \"'+str(t[1])+'\"'
        return Nodo('DECIMAL', str(t[1]), [], t.lexer.lineno, 0, gramatica)     
    else:
        gramatica = '<cualquiernumero> ::= \"'+str(t[1])+'\"'
        return Nodo('ENTERO', str(t[1]), [], t.lexer.lineno, 0, gramatica)