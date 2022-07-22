import json

prog = '''
[def main [argc argv] [+ 1 1]]
'''
# json_prog = '''
# {"main": ["def", "main", ["argc", "argv"], ["+", 1, 1]]}
# '''
# json_prog = '''
# ["+", 1, 1]
# '''

# json_prog = '''
# {
#     "main": ["def", "main", [], ["foo", 1, 1]],
#     "foo": ["def", "foo", ["a", "b"], ["+", "a", "b"]],
#     "x": ["foo", 1, 1],
#     "y": true,
#     "z": "'foo'",
#     "zz": null
# }
# '''

json_prog = '''
["#", ["+", 1, 1]]
'''

def split(s, chars):
    result = list()
    tok = ''
    for c in s:
        if c in chars:
            result.append(tok)
            result.append(c)
            tok = ''
        else:
            tok += c
    return result

def convert_json_lisp_to_json(prog):
    p = split(prog, '[] \n\t')
    for tok in p:
        # leave numbers, booleans (true, false), null alone
        # strings must get escaped "'some_string'"
        # add comma separator to arrays
        # objects should already have comma separators
        pass

def exec_json(lib, j):
    # conventions
    # {"main: ["def", "main", ["argc", "argv"], ["+", 1, 1]]}
    # main is a function under main
    # other functions are just looked up in the namespace
    # there is a standard library of stuff already in the namespace
    if type(j) is list:
        return exec_list(lib, j)
    elif type(j) is dict:
        return exec_dict(lib, j)
    elif type(j) is str:
        # unescape the inner ''
        if j[0] == "'" and j[-1] == "'":
            return j[1:-1]
        else: # or else look up the name of the var
            return lib[j]
    else: # int, float, bool, None
        return j
        
def exec_list(lib, l):
    fn = l[0]
    f = lib[fn]
    if fn == "def":
        args = l[1:]
    else:
        args = [exec_json(lib, a) for a in l[1:]]
    return f(*args)

def exec_dict(lib, d):
    result = dict()
    for k in d:
        result[k] = exec_json(lib, d[k])
    return result

lib = dict()

def exec_def(fn, argl, impl):
    # def needs to add a new function to lib
    def _inner(*args):
        prev_lib = dict()
        for a, v in zip(argl, args):
            if a in lib:
                # save value of variable
                prev_lib[a] = lib[a]
            lib[a] = v
        result = exec_json(lib, impl)
        for a in argl:
            del lib[a]
        for a in prev_lib:
            # restore previous value of variable
            lib[a] = prev_lib[a]
        return result
    lib[fn] = _inner
    return _inner

lib["+"] = lambda x, y: x + y
lib["def"] = exec_def
lib["#"] = lambda *args: list(args)


# result = split(prog, '[] \n\t')
# print(result)

j = json.loads(json_prog)
print(j)
result = exec_json(lib, j)
print(result)
