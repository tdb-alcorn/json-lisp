from enum import Enum


digits = set("0123456789")
letters_lower = "abcdefghijklmnopqrstuvwxyz"
letters_upper = letters_lower.upper()
identifier_start_chars = set(letters_lower + letters_upper + "_")
identifier_chars = set(list(identifier_start_chars) + list(digits) + ["."])


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


class Token(Enum):
    INVALID = 0
    BRACKET = 1
    BRACE = 2
    COMMA = 3
    COLON = 4
    BOOLEAN = 5
    NULL = 6
    NUMBER = 7
    STRING = 8
    IDENTIFIER = 9


def classify_token(tok):
    if tok == "[" or tok == "]":
        return Token.BRACKET
    elif tok == "{" or tok == "}":
        return Token.BRACE
    elif tok == ",":
        return Token.COMMA
    elif tok == ":":
        return Token.COLON
    elif tok == "null":
        return Token.NULL
    elif tok == "false" or tok == "true":
        return Token.BOOLEAN
    elif tok[0] == '"' and tok[-1] == '"':
        return Token.STRING
    elif tok[0] in digits:
        # TODO regex for number
        return Token.NUMBER
    elif tok[0] in identifier_start_chars:
        is_valid = all([char in identifier_chars for char in tok[1:-1]])
        if is_valid:
            return Token.IDENTIFIER
        else:
            return Token.INVALID
    else:
        return Token.INVALID


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


def convert_json_lisp_to_json(prog):
    p = split(prog, ",[]\{\} \n\t")
    result = list()
    for tok in p:
        result.append(convert_token)
