names = []

declare_value_type =    { 
                        "int" : "int = 0",
                        "string" : "str = 0", 
                        "char" :  "chr = 0",
                        "boolean" : "bool = False",
                        "double" : "float = 0.0",
                        "array" : "any = []",
                        "matrix" : "any = [[]]"
                        }

def add_variable(variable):
    if(len(names) > 0):
        if variable not in names:
            names.append(variable)
        else:
            raise Exception("(!) Variavel " + str(variable) + " ja existente")
    else:
            names.append(variable)
            
def add_funcao(funcao):
    if(len(names) > 0):
        if funcao not in names:
            names.append(funcao)
        else:
            raise Exception("(!) Variável ou Função " + str(funcao) + " ja existente")
    else:
            names.append(funcao)
            
def existe_funcao(funcao):
    if(len(names) > 0):
        if funcao in names:
            return True;
        else:
            raise Exception("(!) Função " + str(funcao) + " não existente")
    else:
        return False

def verify_for_operation(variable):
    if(len(names) > 0):
        if variable not in names:
            return False
        else:
            return True
    else:
        return False
    
def indent_lines(lines, indent):
    return ' '.join(indent + line for line in lines.splitlines())
    
def format_print(string_l):
    resultado = []
    entre_aspas = False

    for item in string_l:
        if isinstance(item, str) and item.strip().startswith('"') and item.strip().endswith('"'):
            # Se o item é uma string entre aspas, mantenha inalterado
            resultado.append(item)
        elif not entre_aspas and item == '+':
            # Se não estiver entre aspas e for um operador de soma, mantenha inalterado
            resultado.append(item)
        else:
            # Caso contrário, converta para string usando str()
            resultado.append('str('+item+')')

    return " + ".join(resultado)