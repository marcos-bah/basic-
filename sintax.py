from ply import yacc
from declarations import *
from lex import *

# Variáveis auxiliares
ident = '''
    '''

#Análise Sintática

def p_empty(p): 
    '''empty :
    '''
    p[0] = ""

def p_fim_de_instrucao(p): 
    '''end : PONTO_E_VIRGULA
    '''

def p_types(p):
    '''type : TIPO_INT
            | TIPO_DOUBLE
            | TIPO_STRING
            | TIPO_CHAR
            | TIPO_BOOLEAN
    '''
    p[0] = p[1]

def p_valTipo(p): 
    '''valTipo : INT
               | STRING
               | BOOLEAN
               | CHAR
               | DOUBLE
    ''' 
    p[0] = p[1]

def p_main(p): 
    '''main : INICIO COMECO_DELIMITADOR_CHAVES lista_codigo FINAL_DELIMITADOR_CHAVES FIM
    '''
    with open(f"{arquivo}.py", "w") as file0, open(f"./logs/erros_{arquivo}.txt", "w") as file1:
        file0.write(f"{p[3]}")
        #file1.write(f"")
    file0.close()
    file1.close()

def p_codigo(p): 
    '''codigo   : condicional
                | atribuicao end
                | entrada end
                | saida_variavel end
                | saida_string end
                | declaracao end
                | while
                | loop
                | comentario
                | funcao
                | funcao_chamada end
    '''
    p[0] = p[1]

def p_lista_codigo(p): 
    '''lista_codigo : codigo lista_codigo
                    | empty
    '''
    if(len(p) == 2):
        p[0] = f''
    else:
        if p[2] == "":
            p[0] = f'{p[1]}'
        else:
            p[0] = f'{p[1]}'+f'\n'+f'{p[2]}' 

def p_comentario(p):
    '''comentario : COMENTARIO_LINHA
    '''
    aux = p[1].replace("#", '')
    p[0] = f"#{aux}"

def p_declaracao(p): 
    '''declaracao : type VARIAVEL
                  | type VARIAVEL IGUAL expression
                  | type VARIAVEL IGUAL funcao_chamada
                  | type VARIAVEL IGUAL ENTRADA ABRE_PARENTESES STRING FECHA_PARENTESES
                  | type VARIAVEL IGUAL ENTRADA ABRE_PARENTESES expression FECHA_PARENTESES
    '''
    add_variable(p[2])
    if(len(p) > 3):
        if(str(p[4]) == "read"):
            string_f = format_print(p[6].split("+"));
            p[0] = f"{p[2]} = {p[1]}(input({string_f}))"
        else:
            p[0] = f"{p[2]} = {p[4]}"
    else:
        tmp = declare_value_type[p[1]]
        p[0] = f"{p[2]}: {tmp}"
    
def p_funcao(p):
    '''funcao : FUNCAO VARIAVEL ABRE_PARENTESES FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES lista_codigo FINAL_DELIMITADOR_CHAVES
              | FUNCAO VARIAVEL ABRE_PARENTESES FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES lista_codigo RETORNO valTipo end FINAL_DELIMITADOR_CHAVES
              | FUNCAO VARIAVEL ABRE_PARENTESES FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES lista_codigo RETORNO VARIAVEL end FINAL_DELIMITADOR_CHAVES
              | FUNCAO VARIAVEL ABRE_PARENTESES FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES lista_codigo RETORNO expression end FINAL_DELIMITADOR_CHAVES
              | FUNCAO VARIAVEL ABRE_PARENTESES FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES RETORNO valTipo end FINAL_DELIMITADOR_CHAVES
              | FUNCAO VARIAVEL ABRE_PARENTESES FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES RETORNO VARIAVEL end FINAL_DELIMITADOR_CHAVES
              | FUNCAO VARIAVEL ABRE_PARENTESES FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES RETORNO expression end FINAL_DELIMITADOR_CHAVES
    ''' 
    add_funcao(p[2])
    if(str(p[6])==""):
        raise Exception("(!) Função " + str(p[2]) + " não possui corpo")
    
    if(len(p) > 7):
        if (str(p[6]) == "return"):
             p[0] = f"def {p[2]}():"+ident+f"return {p[7]}"
        else:
            p[0] = f"def {p[2]}():{indent_lines(p[6], ident)}"+ident+f"return {p[8]}"
    else:
        p[0] = f"def {p[2]}():{indent_lines(p[6], ident)}"
    
def p_funcao_chamada(p):
    '''funcao_chamada : VARIAVEL ABRE_PARENTESES FECHA_PARENTESES
    ''' 
    existe_funcao(p[1])
    p[0] = f"{p[1]}()"


def p_atribuicao(p): 
    '''atribuicao : VARIAVEL IGUAL expression
                  | VARIAVEL IGUAL funcao_chamada
                  | VARIAVEL IGUAL valTipo
                  | VARIAVEL IGUAL ENTRADA ABRE_PARENTESES STRING FECHA_PARENTESES
                  | VARIAVEL IGUAL ENTRADA ABRE_PARENTESES expression FECHA_PARENTESES
    '''

    if(verify_for_operation(p[1])):
        if(str(p[3]) == "read"):
            string_f = format_print(p[5].split("+"));
            p[0] = f"{p[1]} {p[2]} type({p[1]}) (input({string_f}))"
        else:
            p[0] = f"{p[1]} {p[2]} {p[3]}"
    else:
        with open(f"erros_{arquivo}.txt", "w") as file1:
            file1.write(f"(!) Variavel {p[1]} nao existe\n")
        raise Exception("(!) Variavel " + str(p[1]) + " nao existe")

def p_entrada(p): 
    '''entrada  : VARIAVEL IGUAL ENTRADA ABRE_PARENTESES STRING FECHA_PARENTESES
                | VARIAVEL IGUAL ENTRADA ABRE_PARENTESES expression FECHA_PARENTESES
    '''
    p[0] = f"{p[3]} = type({p[3]}) (input())"

def p_saida_string(p): 
    '''saida_string : SAIDA ABRE_PARENTESES STRING FECHA_PARENTESES
                    | SAIDA ABRE_PARENTESES QUEBRA_LINHA FECHA_PARENTESES
                    | SAIDA ABRE_PARENTESES CHAR FECHA_PARENTESES
    '''
    p[0] = f'print({p[3]}, end="")'

def p_saida(p): 
    '''saida_variavel : SAIDA ABRE_PARENTESES VARIAVEL FECHA_PARENTESES    
                      | SAIDA ABRE_PARENTESES comparacao FECHA_PARENTESES 
                      | SAIDA ABRE_PARENTESES expression FECHA_PARENTESES 
    '''
    p[0] = f'print({format_print(p[3].split("+"))}, end="")'

def p_opRel(p):
    '''opRel : IGUAL_IGUAL 
             | MAIOR_OU_IGUAL
             | MENOR_OU_IGUAL
             | MAIOR
             | MENOR
             | DIFERENTE
    '''      
    p[0] = p[1]

def p_opArit(p):
    '''opArit : SOMA 
              | SUBTRACAO
              | MULTIPLICACAO
              | DIVISAO
              | MODULO
    '''
    p[0] = p[1]

def p_opUna(p):
    '''opUna : TILNOT_BITWISE 
             | NOT
    '''
    p[0] = p[1]

def p_comparacao_parenteses(p): 
    '''comparacao : ABRE_PARENTESES comparacao FECHA_PARENTESES
    '''
    p[0] = f"({p[2]})"

def p_comparacao_solo(t):
    '''comparacao : relacional
                  | unario
    '''
    t[0] = t[1]

def p_logico(p): 
    '''comparacao : comparacao AND comparacao
                  | comparacao OR comparacao
    '''
    if(p[2] == "&&"):
        p[0] = f"{p[1]} and {p[3]}"
    elif(p[2] == "||"):
        p[0] = f"{p[1]} or {p[2]}"
    else:
        with open(f"erros_{arquivo}.txt", "w") as file1:
            file1.write(f"(!) Operacao invalida\n")
        raise Exception("(!) Operacao invalida")

def p_unario(p):
    '''unario : opUna VARIAVEL
              | opUna INT
              | opUna BOOLEAN
    '''
    if(p[1] == '!'):
        p[0] = f"not {p[2]}"
    elif(p[1] == '~'):
        p[0] = f"~ {p[2]}"

def p_relacional_options(p): 
    '''relacional : VARIAVEL
                  | valTipo
    '''
    p[0] = f"{p[1]}"

def p_relacional(p): 
    '''relacional : relacional opRel relacional
    '''
    try: 
        try:
            tmp1 = verify_for_operation(p[1])
            vl1 = names[p[1]][1]
        except:
            tmp1 = type(p[1])
            vl1 = p[1]
        try:
            tmp2 = verify_for_operation(p[3])
            vl2 = names[p[3]][1]
        except:
            tmp2 = type(p[3])
            vl2 = p[3]
        if(tmp1 != tmp2):
            with open(f"erros_{arquivo}.txt", "w") as file1:
                file1.write(f"(!) Operacao com tipos distintos\n")
            raise Exception ("(!) Operacao com tipos distintos")
        else:
            if(type(p[1]) == str and type(p[3]) == str):
                if(p[2] == '=='):
                    p[0] = f"{p[1]} == {p[3]}"
                elif(p[2] == '>='):
                    p[0] = f"{p[1]} >= {p[3]}"
                elif(p[2] == '<='):
                    p[0] = f"{p[1]} <= {p[3]}"
                elif(p[2] == '>'):
                    p[0] = f"{p[1]} > {p[3]}"
                elif(p[2] == '<'):
                    p[0] = f"{p[1]} < {p[3]}"
                elif(p[2] == '!='):
                    p[0] = f"{p[1]} != {p[3]}"
                else:
                    with open(f"erros_{arquivo}.txt", "w") as file1:
                        file1.write(f"(!) Operador invalido\n")
                    raise Exception("(!) Operador invalido")
            else:
                if(p[2] == '=='):
                    p[0] = f"{vl1} == {vl2}"
                elif(p[2] == '>='):
                    p[0] = f"{vl1} >= {vl2}"
                elif(p[2] == '<='):
                    p[0] = f"{vl1} <= {vl2}"
                elif(p[2] == '>'):
                    p[0] = f"{vl1} > {vl2}"
                elif(p[2] == '<'):
                    p[0] = f"{vl1} < {vl2}"
                elif(p[2] == '!='):
                    p[0] = f"{vl1} != {vl2}"
                else:
                    with open(f"erros_{arquivo}.txt", "w") as file1:
                        file1.write(f"(!) Operador invalido\n")
                    raise Exception("(!) Operador invalido")
    except:
        if(type(p[1]) != type(p[3])):
            with open(f"erros_{arquivo}.txt", "w") as file1:
                file1.write(f"(!) Operacao com tipos distintos\n")
            raise Exception ("(!) Operacao com tipos distintos")
        else:
            if(p[2] == '=='):
                p[0] = f"{p[1]} == {p[3]}"
            elif(p[2] == '>='):
                p[0] = f"{p[1]} >= {p[3]}"
            elif(p[2] == '<='):
                p[0] = f"{p[1]} <= {p[3]}"
            elif(p[2] == '>'):
                p[0] = f"{p[1]} > {p[3]}"
            elif(p[2] == '<'):
                p[0] = f"{p[1]} < {p[3]}"
            elif(p[2] == '!='):
                p[0] = f"{p[1]} != {p[3]}"
            else:
                with open(f"erros_{arquivo}.txt", "w") as file1:
                    file1.write(f"(!) Operador invalido\n")
                raise Exception("(!) Operador invalido")

def p_expression_parenthesis(p):
    '''expression : ABRE_PARENTESES expression FECHA_PARENTESES
    '''
    p[0] = f"({p[2]})"

def p_expression_uminus(p):
    '''expression : SUBTRACAO expression %prec UMINUS
    '''
    p[0] = -p[2]
    
def p_expressao_valor(p):
    '''expression : valTipo
                  | VARIAVEL
    '''
    p[0] = f"{p[1]}"

def p_binary_operators(p):
    '''expression : expression opArit expression %prec SOMA
    '''
    if p[2] == '+':
        p[0] = f"{p[1]} + {p[3]}"
    elif p[2] == '-':
        p[0] = f"{p[1]} - {p[3]}"
    elif p[2] == '*':
        p[0] = f"{p[1]} * {p[3]}"
    elif p[2] == '/':
        p[0] = f"{p[1]} / {p[3]}"
    elif p[2] == '%':
        p[0] = f"{p[1]} % {p[3]}"
    else:
        with open(f"erros_{arquivo}.txt", "w") as file1:
            file1.write(f"(!) Sinal invalido\n")
        raise Exception("(!) Sinal invalido")

def p_condicional(p): 
    '''condicional : IF ABRE_PARENTESES comparacao FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES lista_codigo FINAL_DELIMITADOR_CHAVES
                   | IF ABRE_PARENTESES comparacao FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES lista_codigo FINAL_DELIMITADOR_CHAVES ELSE COMECO_DELIMITADOR_CHAVES lista_codigo FINAL_DELIMITADOR_CHAVES
    '''

    tmp1 = p[6].replace("\n", ident)
    tmp2 = p[10].replace("\n", ident)

    if(len(p) == 8):
        p[0] = f'''if {p[3]}:{ident}{tmp1}'''
    else:
        p[0] = f'''if {p[3]}:{ident}{tmp1}\nelse:{ident}{tmp2}''' 

def p_while(p): 
    '''while : WHILE ABRE_PARENTESES comparacao FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES lista_codigo FINAL_DELIMITADOR_CHAVES
    '''
    
    tmp = p[6].replace("\n", ident)

    p[0] = f'''while {p[3]}:{ident}{tmp}'''
    
def p_loop(p): 
    '''loop : LOOP ABRE_PARENTESES comparacao FECHA_PARENTESES COMECO_DELIMITADOR_CHAVES lista_codigo FINAL_DELIMITADOR_CHAVES
    '''
    
    tmp = p[6].replace("\n", ident)

    p[0] = f'''while {p[3]}:{ident}{tmp}'''

errossintaticos = []
def p_error(p):
    if(p):
        errossintaticos.append(p)
        print("ERRO: ",p)

parser = yacc.yacc(start = 'main') #errorlog=lex.NullLogger(),
result = parser.parse(text)