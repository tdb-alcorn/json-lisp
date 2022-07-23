lib = {
    "+": lambda *args: sum(args),
    "#": lambda *args: list(args),
    "if": lambda cnd, thn, els: thn if cnd else els,
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
