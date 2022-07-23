def add_stdlib(interpreter):
    add_exec_def(interpreter)
    interpreter.lib["+"] = lambda x, y: x + y
    interpreter.lib["#"] = lambda *args: list(args)


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
