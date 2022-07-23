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


def convert_json_lisp_to_json(prog):
    p = split(prog, "[] \n\t")
    for tok in p:
        # leave numbers, booleans (true, false), null alone
        # strings must get escaped "'some_string'"
        # add comma separator to arrays
        # objects should already have comma separators
        pass
