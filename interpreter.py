import json
from stdlib import add_stdlib


class Interpreter:
    def __init__(self):
        self.lib = dict()
        add_stdlib(self)

    def exec_json(self, j):
        if type(j) is list:
            return self.exec_list(j)
        elif type(j) is dict:
            return self.exec_dict(j)
        elif type(j) is str:
            if j[0] == "'" and j[-1] == "'":  # unescape the inner ''
                return j[1:-1]
            else:  # or else look up the name of the var
                return self.lib[j]
        else:  # int, float, bool, None
            return j

    def exec_list(self, l):
        fn = l[0]
        f = self.lib[fn]
        # handle special forms
        if fn == "def":
            args = l[1:]
        elif fn == "if":
            cnd = self.exec_json(l[1])
            if cnd:
                args = [cnd, self.exec_json(l[2]), l[3]]
            else:
                args = [cnd, l[2], self.exec_json(l[3])]
        elif fn == "let":
            args = l[1:]
        else:
            args = [self.exec_json(a) for a in l[1:]]
        return f(*args)

    def exec_dict(self, d):
        result = dict()
        for k in d:
            result[k] = self.exec_json(d[k])
        return result

    def exec(self, prog):
        j = json.loads(prog)
        return self.exec_json(j)
