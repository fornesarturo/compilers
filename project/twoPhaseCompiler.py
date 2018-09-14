import sys
sys.setrecursionlimit(200)

def parser(tokens, symbol_table):
    new_symbol_table = {}
    current_err = { "level": 0 }
    # Helpers
    def handle_err(message, token, level, can_have_error = False):
        err = {"mensaje": message, "token": token, "level": level}
        if level >= current_err["level"] and not can_have_error:
            current_err.update(err)
        return err
    def check_token(key, expected_value, error_message, level, c, declaration = False, scope = None, can_have_error = False):
        if tokens[c][key] == expected_value:
            if expected_value == "id" and declaration:
                idType = tokens[c - 1]["valor"]
                functionVariable = "función" if tokens[c + 1]["valor"] == "(" else "variable"
                symbol = {
                    'funcion_o_variable': functionVariable,
                    'tipo_de_dato': idType,
                    'tipo': tokens[c]["tipo"],
                    'valor': tokens[c]["valor"],
                    'linea': tokens[c]["linea"],
                    'caracter': tokens[c]["caracter"]
                }
                if new_symbol_table.get(scope):
                    new_symbol_table[scope][tokens[c]["valor"]] = symbol
                else:
                    new_symbol_table[scope] = {}
                    new_symbol_table[scope][tokens[c]["valor"]] = symbol
            return False, c + 1
        else:
            return handle_err(error_message, tokens[c], level, can_have_error), c
    # Producciones:
    # * counter o c, sólo regresará aumentado de ser correcta
    # la derivación.
    # * Las producciones regresarán error, siguiente posición.
    # * Las producciones opcionales ignorarán los errores.
    def inicio(level, counter):
        func_err, c = bloque_de_funciones(level + 1, counter)
        err, c = principal(level + 1, c, "principal")
        if err:
            if func_err and func_err["level"] > err["level"]:
                return func_err, False
            return err, False
        return False, True
    def bloque_de_funciones(level, counter):
        err = False
        c = counter
        while not err:
            err, c = funcion(level + 1, c)
        if c > counter:
            return err, c
        else:
            return err, counter
    def funcion(level, counter):
        err, c = tipo_de_dato(level + 1, counter)
        if err:
            return err, counter
        scope = tokens[c]["valor"]
        err, c = check_token("tipo", "id", "id esperado", level, c, True, scope)
        if err:
            return err, counter
        err, c = check_token("valor", "(", "'(' esperado", level, c)
        if err:
            return err, counter
        err, c = argumentos(level + 1, c, scope)
        err, c = check_token("valor", ")", "')' esperado", level, c)
        if err:
            return err, counter
        
        err, c = check_token("valor", "{", "'{' esperado", level, c)
        if err:
            return err, counter
        err, c = bloque_de_codigo(level + 1, c, scope)
        if err:
            return err, counter
        err, c = check_token("valor", "regresa", "'regresa' esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("tipo", "id", "id esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("valor", ";", "';' esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("valor", "}", "'}' esperado", level, c)
        if err:
            return err, counter
        return False, c
    def tipo_de_dato(level, counter):
        if tokens[counter]["valor"] in ["real", "entero", "logico"]:
            return False, counter + 1
        return handle_err("'tipo de dato' esperado", tokens[counter], level), counter
    def argumentos(level, counter, scope = None):
        err = False
        coma = True
        c = counter
        while not err:
            err, c = argumento(level + 1, c, scope)
            if not err:
                err, c = check_token("valor", ",", "',' esperada", level, c)
                if err:
                    coma = False
                    break
                coma = True
        if c > counter and not coma:
            return False, c
        else:
            return False, counter
    def argumento(level, counter, scope = None):
        err, c = tipo_de_dato(level + 1, counter)
        if err:
            return err, counter
        err, c = check_token("tipo", "id", "id esperado", level, c, True, scope)
        if err:
            return err, counter
        return False, c
    def bloque_de_codigo(level, counter, scope = None):
        err, c = declaraciones(level + 1, counter, scope)
        err, c = sentencias(level + 1, c)
        if err:
            return err, counter
        return False, c
    def declaraciones(level, counter, scope = None):
        err = False
        c = counter
        while not err:
            err, c = declaracion(level + 1, c, scope)
        if c > counter:
            return False, c
        else:
            return False, counter
    def declaracion(level, counter, scope = None):
        err, c = tipo_de_dato(level + 1, counter)
        if err:
            return err, counter
        err, c = check_token("tipo", "id", "id esperado", level, c, True, scope)
        if err:
            return err, counter
        err, c = check_token("tipo", ";", "';' esperado", level, c)
        if err:
            return err, counter
        return False, c
    def sentencias(level, counter):
        err = False
        c = counter
        while not err:
            err, c = sentencia(level + 1, c)
        if c > counter:
            return False, c
        else:
            return False, counter
    def sentencia(level, counter):
        err, c = si(level + 1, counter)
        if not err:
            return False, c
        err, c = mientras(level + 1, counter)
        if not err:
            return False, c
        err, c = asignacion(level + 1, counter)
        if not err:
            return False, c
        return err, counter
    def si(level, counter):
        err, c = check_token("valor", "si", "si esperado", level, counter)
        if err:
            return err, counter
        err, c = check_token("tipo", "(", "'(' esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("tipo", "id", "id esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("tipo", ")", "')' esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("tipo", "{", "'{' esperado", level, c)
        if err:
            return err, counter
        err, c = sentencias(level + 1, c)
        err, c = check_token("tipo", "}", "'}' esperado", level, c)
        if err:
            return err, counter
        return False, c
    def mientras(level, counter):
        err, c = check_token("valor", "mientras", "si esperado", level, counter)
        if err:
            return err, counter
        err, c = check_token("tipo", "(", "'(' esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("tipo", "id", "id esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("tipo", ")", "')' esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("tipo", "{", "'{' esperado", level, c)
        if err:
            return err, counter
        err, c = sentencias(level + 1, c)
        err, c = check_token("tipo", "}", "'}' esperado", level, c)
        if err:
            return err, counter
        return False, c
    def asignacion(level, counter):
        err, c = check_token("tipo", "id", "id esperado", level, counter)
        if err:
            return err, counter
        err, c = check_token("valor", "=", "'=' esperado", level, c)
        if err:
            return err, counter
        err, c = expresion(level + 1, c)
        if err:
            return err, counter
        return False, c
    def expresion(level, counter):
        err, c = aritmetica(level + 1, counter)
        if not err:
            err, c = check_token("valor", ";", "';' esperado", level, c)
            if not err:
                return False, c
        err, c = logica(level + 1, counter)
        if not err:
            err, c = check_token("valor", ";", "';' esperado", level, c)
            if not err:
                return False, c
        err, c = relacional(level + 1, counter)
        if not err:
            err, c = check_token("valor", ";", "';' esperado", level, c)
            if not err:
                return False, c
        err, c = check_token("valor", "!", "'!' esperado", level, counter)
        if err:
            return err, counter
        err, c = check_token("tipo", "id", "id esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("valor", ";", "';' esperado", level, c)
        if err:
            return err, counter
        return False, c
    
    def aritmetica_anidada(level, counter):
        err, c = check_token("valor", "(", "'(' esperado", level, counter)
        if err:
            return err, counter
        err, c = aritmetica(level + 1, c)
        if err:
            return err, counter
        err, c = check_token("valor", ")", "')' esperado", level, c)
        if err:
            return err, counter
        return False, c
    
    def aritmetica(level, counter):
        if tokens[counter]["valor"] == "(":
            err, c = aritmetica_anidada(level + 1, counter)
            if not err:
                err_op, c_op = operador_aritmetico(level, c)
                if not err_op:
                    err, c = aritmetica(level + 1, c_op)
                    if err:
                        return err, c_op
                    return False, c
                else:
                    return False, c
            else:
                return err, counter
        err, c = valor_aritmetico(level + 1, counter)
        if not err:
            err_op, c_op = operador_aritmetico(level, c)
            if not err_op:
                err, c = aritmetica(level + 1, c_op)
                if err:
                    return err, c_op
                return False, c
            else:
                err, c_new = operador_relacional(level, c)
                if not err:
                    return {'level': level, 'mensaje': "Es relacional", 'token': tokens[c]}, counter
                err, c_new = operador_logico(level, c)
                if not err:
                    return {'level': level, 'mensaje': "Es logico", 'token': tokens[c]}, counter 
                return False, c
        return err, counter


    def operador_aritmetico(level, counter):
        if tokens[counter]["valor"] in ["*", "+", "/", "^", "-"]:
            return False, counter + 1
        return handle_err("'operador aritmetico' esperado", tokens[counter], level), counter
    def valor_aritmetico(level, counter):
        err, c = llamada_funcion(level + 1, counter)
        if not err:
            return False, c
        err, c = check_token('tipo', 'id', 'id esperado', level, counter)
        if not err:
            return False, c
        err, c = check_token('tipo', 'real', 'lógico esperado', level, counter)
        if not err:
            return False, c
        err, c = check_token('tipo', 'entero', 'lógico esperado', level, counter)
        if not err:
            return False, c
        return err, counter
    

    def logica_anidada(level, counter):
        err, c = check_token("valor", "(", "'(' esperado", level, counter)
        if err:
            return err, counter
        err, c = logica(level + 1, c)
        if err:
            return err, counter
        err, c = check_token("valor", ")", "')' esperado", level, c)
        if err:
            return err, counter
        return False, c
    
    def logica(level, counter):
        if tokens[counter]["valor"] == "(":
            err, c = logica_anidada(level + 1, counter)
            if not err:
                err_op, c_op = operador_logico(level, c)
                if not err_op:
                    err, c = logica(level + 1, c_op)
                    if err:
                        return err, c_op
                    return False, c
                else:
                    return False, c
            else:
                return err, counter
        err, c = valor_logico(level + 1, counter)
        if not err:
            err_op, c_op = operador_logico(level, c)
            if not err_op:
                err, c = logica(level + 1, c_op)
                if err:
                    return err, c_op
                return False, c
            else:
                err, c_new = operador_relacional(level, c)
                if not err:
                    return {'level': level, 'mensaje': "Es relacional", 'token': tokens[c]}, counter
                err, c_new = operador_aritmetico(level, c)
                if not err:
                    return {'level': level, 'mensaje': "Es aritmetico", 'token': tokens[c]}, counter 
                return False, c
        return err, counter


    def operador_logico(level, counter):
        if tokens[counter]["valor"] in ["&", "|"]:
            return False, counter + 1
        return handle_err("'operador lógico' esperado", tokens[counter], level), counter
    def valor_logico(level, counter):
        err, c = llamada_funcion(level + 1, counter)
        if not err:
            return False, c
        err, c = check_token('tipo', 'id', 'id esperado', level, counter)
        if not err:
            return False, c
        err, c = check_token('valor', 'verdadero', 'lógico esperado', level, counter)
        if not err:
            return False, c
        err, c = check_token('valor', 'falso', 'lógico esperado', level, counter)
        if not err:
            return False, c
        return err, counter
    def llamada_funcion(level, counter):
        err, c = check_token('tipo', 'id', 'id esperado', level, counter)
        if err:
            return err, counter
        err, c = check_token('valor', '(', "'(' esperado", level, c)
        if err:
            return err, counter
        err, c = argumentos_funcion(level + 1, c)
        err, c = check_token('valor', ')', "')' esperado", level, c)
        if err:
            return err, counter
        return False, c
    def argumentos_funcion(level, counter):
        err = False
        coma = True
        c = counter
        while not err:
            err, c = check_token("tipo", "id", "id esperado", level, c)
            if not err:
                err, c = check_token("valor", ",", "',' esperada", level, c)
                if err:
                    coma = False
                    break
                coma = True
        if c > counter and not coma:
            return False, c
        else:
            return False, counter
    def relacional(level, counter):
        err, c = valor_aritmetico(level + 1, counter)
        if err:
            return err, counter
        err, c = operador_relacional(level + 1, c)
        if err:
            return err, counter
        err, c = valor_aritmetico(level + 1, c)
        if err:
            return err, counter
        return False, c
    def operador_relacional(level, counter):
        if tokens[counter]["valor"] in ["<", ">", "=="]:
            return False, counter + 1
        return handle_err("'operador relacional' esperado", tokens[counter], level), counter
    def principal(level, counter, scope):
        err, c = check_token('valor', 'principal', "'principal' esperado", level, counter)
        if err:
            return err, counter
        err, c = check_token("tipo", "(", "'(' esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("tipo", ")", "')' esperado", level, c)
        if err:
            return err, counter
        err, c = check_token("tipo", "{", "'{' esperado", level, c)
        if err:
            return err, counter
        err, c = bloque_de_codigo(level + 1, c, scope)
        if err:
            return err, counter
        err, c = check_token("tipo", "}", "'}' esperado", level, c)
        if err:
            return err, counter
        return False, c
    
    # Producción Inicial
    err, result = inicio(0, 0)
    if err:
        return err, False, None
    return False, True, new_symbol_table

def scanner(filename):
    tokens = []
    errors = []
    symbol_table = {}
    reserved = ['entero', 'real', 'logico', 'regresa', 'si', 'mientras', 'principal', 'verdadero', 'falso']
    unary_tokens = [
        '{', '}', '(', ')', '/', '*', '+', '^', '-', '<', '>', '!', '&', '|', ',', ';'
    ]
    whitespace = [
        '\n', ' ', '\t', '\r'
    ]
    def buffer_match(tipo, valor, linea, caracter):
        if not valor:
            return
        if tipo == 'error':
            errors.append({'tipo': tipo, 'valor': valor, 'linea': linea + 1, 'caracter': caracter + 1})
            return
        if tipo == 'id':
            if valor in reserved:
                tipo = "reservada"
            elif valor not in symbol_table:
                symbol_table[valor] = {'tipo': tipo, 'valor': valor, 'linea': linea + 1, 'caracter': caracter + 1}
        tokens.append({'tipo': tipo, 'valor': valor, 'linea': linea + 1, 'caracter': caracter + 1})
        
    with open(filename, 'r') as f:
        line = f.readline()
        line_no = 0
        c_buffer = ""
        possible_type = ""
        c_no = 0
        c_start = 0
        while line:
            c_no = 0
            line_length = len(line)
            while c_no < line_length:
                c = line[c_no]
                if c in unary_tokens:
                    buffer_match(possible_type, c_buffer, line_no, c_start)
                    buffer_match(c, c, line_no, c_no)
                    possible_type = ""
                    c_no += 1
                    c_buffer = ""
                    continue
                if c in whitespace:
                    buffer_match(possible_type, c_buffer, line_no, c_start)
                    possible_type = ""
                    c_no += 1
                    c_buffer = ""
                    continue
                if possible_type == "" and ord(c) >= ord('a') and ord(c) <= ord('z'):
                    c_start = c_no
                    c_buffer += c
                    c_no += 1
                    possible_type = "id"
                    continue
                if possible_type == "id" and (
                        (ord(c) >= ord('a') and ord(c) <= ord('z')) or
                        (ord(c) >= ord('0') and ord(c) <= ord('9')) or
                        (ord(c) >= ord('A') and ord(c) <= ord('Z'))
                    ):
                    c_buffer += c
                    c_no += 1
                    continue
                if possible_type == "" and ord(c) >= ord('0') and ord(c) <= ord('9'):
                    c_start = c_no
                    c_buffer += c
                    c_no += 1
                    possible_type = "entero"
                    continue
                if (possible_type == "entero" or possible_type == "real") and ord(c) >= ord('0') and ord(c) <= ord('9'):
                    c_buffer += c
                    c_no += 1
                    continue
                if possible_type == "entero" and c == '.':
                    c_buffer += c
                    c_no += 1
                    c = line[c_no]
                    if ord(c) >= ord('0') and ord(c) <= ord('9'):
                        c_buffer += c
                        c_no += 1
                        possible_type = "real"
                        continue
                    else:
                        c_buffer += c
                        c_no += 1
                        possible_type = "error"
                        continue
                if c == "=":
                    buffer_match(possible_type, c_buffer, line_no, c_no)
                    c_buffer = ""
                    possible_type = ""
                    if line[c_no + 1] == '=':
                        buffer_match('==', '==', line_no, c_no)
                        c_no += 2
                        continue
                    else:
                        buffer_match('=', '=', line_no, c_no)
                        c_no += 1
                        continue
                possible_type = "error"
                c_no += 1
                c_buffer += c
            line = f.readline()
            line_no += 1
        buffer_match(possible_type, c_buffer, line_no - 1, c_start)
        return tokens, symbol_table, errors    
    return [], {}, []

if __name__ == '__main__':
    tokens, symbols, errors = scanner("Archivo_Fuente.txt")
    print("\n=====================\nAnálisis Léxico\n=====================")
    print("Tokens\n=====================")
    for token in tokens:
        print(token)
    print("Symbol Table\n=====================")
    for key in symbols:
        print("\"" + key +"\":", symbols[key])
    print("Errors\n=====================")
    for error in errors:
        print(error)

    if len(errors) == 0:
        print("\n=====================\nAnálisis Sintáctico\n=====================")
        err, result, syntax_symbols = parser(tokens, symbols)
        print("Aceptado: ", result)
        if err:
            print("Error: ", err)
        else:
            for scope in syntax_symbols:
                print(scope + ":")
                for symbol in syntax_symbols[scope]:
                    print("  \"" + symbol +"\":", syntax_symbols[scope][symbol])
