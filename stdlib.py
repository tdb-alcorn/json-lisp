# TODO: implement macro, lambda, apply, quote, and system calls


def reduce(op, default):
    def _inner(*args):
        result = default
        for a in args:
            result = op(result, a)
        return result

    return _inner


product = reduce(lambda x, y: x * y, 1)


def compare(op):
    def _inner(*args):
        result = True
        for i in range(len(args) - 1):
            result = result and op(args[i], args[i + 1])
        return result

    return _inner


class EmptyArgumentsException(Exception):
    pass


def power(*args):
    if len(args) == 0:
        raise EmptyArgumentsException
    result = args[0]
    for a in args[1:]:
        result = result**a
    return result


def remainder(*args):
    if len(args) == 0:
        raise EmptyArgumentsException
    result = args[0]
    for a in args[1:]:
        result = result % a
    return result


def access(obj, *path):
    result = obj
    for p in path:
        result = result[p]
    return result


lib = {
    # boolean logic
    "!": lambda x: not x,
    "and": reduce(lambda x, y: x and y, True),
    "or": reduce(lambda x, y: x or y, False),
    # arithmetic
    "+": lambda *args: sum(args),
    "-": lambda *args: args[0] - sum(args[1:]) if len(args) > 0 else 0,
    "*": product,
    "/": lambda *args: args[0] / product(args[1:]) if len(args) > 0 else 0,
    "^": power,
    "%": remainder,
    # comparators
    ">": compare(lambda x, y: x > y),
    "<": compare(lambda x, y: x < y),
    ">=": compare(lambda x, y: x >= y),
    "<=": compare(lambda x, y: x <= y),
    "=": compare(lambda x, y: x == y),
    # list literal
    "#": lambda *args: list(args),
    # control flow
    "if": lambda cnd, thn, els: thn if cnd else els,
    # objects
    ".": access,
    # OS
    "print": lambda *args: print(*args),
}


def add_stdlib(interpreter):
    add_exec_def(interpreter)
    add_exec_let(interpreter)
    interpreter.lib.update(lib)


def add_exec_def(interpreter):
    lib = interpreter.lib

    def exec_def(fn, argl, impl):
        # def needs to add a new function to lib
        def _inner(*args):
            prev_lib = dict()
            for a, v in zip(argl, args):
                if a in lib:
                    # save value of variable
                    prev_lib[a] = lib[a]
                lib[a] = v
            result = interpreter.exec_json(impl)
            for a in argl:
                del lib[a]
            for a in prev_lib:
                # restore previous value of variable
                lib[a] = prev_lib[a]
            return result

        lib[fn] = _inner
        return _inner

    interpreter.lib["def"] = exec_def


def add_exec_let(interpreter):
    lib = interpreter.lib

    def exec_let(pairs, body):
        prev_lib = dict()
        for k, v in pairs:
            if k in lib:
                prev_lib[k] = lib[k]
            lib[k] = v
        result = interpreter.exec_json(body)
        for k, _ in pairs:
            del lib[k]
        for k in prev_lib:
            lib[k] = prev_lib[k]
        return result

    interpreter.lib["let"] = exec_let
