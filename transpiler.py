def split(s, chars):
    result = list()
    tok = ""
    for c in s:
        if c in chars:
            result.append(tok)
            result.append(c)
            tok = ""
        else:
            tok += c
    return result


digits = "0123456789"
letters_lower = "abcdefghijklmnopqrstuvwxyz"
letters_upper = letters_lower.upper()
variable_chars = set(letters_lower + letters_upper + "_")


def convert_json_lisp_to_json(prog):
    p = split(prog, ",[]\{\} \n\t")
    result = list()
    for tok in p:
        result.append(convert_token)


symbols = set(",:#[]\{\}")
whitespace = set(" \n\t")


def tokenize(prog):
    result = list()
    escape = False
    in_string = False
    current_token = ""
    list_literal = False
    for char in prog:
        # print(char, result)
        if char == '"':
            current_token += char
            if in_string:
                if not escape:
                    result.append(current_token)
                    current_token = ""
                    in_string = False
            else:
                in_string = True
        elif in_string:
            current_token += char
            if char == "\\":
                escape = True
            else:
                escape = False
        elif char in whitespace:
            if len(current_token) > 0:
                result.append(current_token)
                current_token = ""
        elif char == "#":
            current_token += char
            list_literal = True
        elif char == "[":
            if list_literal == True:
                current_token += char
                result.append(current_token)
                current_token = ""
                list_literal = False
            else:
                result.append(char)
        elif char in symbols:
            if len(current_token) > 0:
                result.append(current_token)
                current_token = ""
            result.append(char)
        else:
            current_token += char
    if len(current_token) > 0:
        result.append(current_token)
    return result


def convert_token(tok):
    # leave numbers, booleans (true, false), null alone
    # strings must get escaped "'some_string'"
    # add comma separator to arrays
    # objects should already have comma separators
    # variables and object keys become strings
    # list literals go from #[...] to ["#", ...]
    # x.y.z becomes [".", "x", "y", "z"]
    start_char = tok[0]
    if len(tok) == 0:
        raise Exception("got empty token")
    if start_char == '"':  # handle string
        return "\"'" + tok[1:-1] + "'\""
    elif start_char in variable_start_chars:  # handle variables
        if ":" in tok:
            k, v = tok.split(":")
            result.append('"' + k + '":')
        else:
            result.append('"' + tok + '"')
