from typing import Callable, List


class VarSystem:
    def __init__(self):
        self.vars = {}

    def set_var(func: Callable) -> Callable:
        def wrapper(self, name: str, res):
            name = name.replace(' ', '')
            res = res.replace(' ', '')
            func(self, name, res)

        return wrapper

    @set_var
    def get_int_var(self, name: str, res: int) -> None:
        self.vars.update({name: INTEGER(res)})

    @set_var
    def get_bool_var(self, name: str, res: bool) -> None:
        self.vars.update({name: BOOLEAN(res)})

    def get_func(self, name: str, res: List[str]) -> None:
        self.vars.update({name: FUNCTION(res)})

    def print_var(self) -> List[str]:
        return self.vars.keys()

    def get_var(self, name):
        try:
            return self.vars.get(name)
        except:
            pass


class INTEGER:
    def __init__(self, val: int):
        self.val = val

    def __str__(self):
        return str(self.val)


class BOOLEAN:
    def __init__(self, val: bool):
        self.val = val

    def __str__(self):
        return str(self.val)


class STRING:
    def __init__(self, val: str):
        self.val = val

    def __str__(self):
        return str(self.val)


class CHAR:
    def __init__(self, val: str):
        if len(val) == 1:
            self.val = val

    def str(self):
        return str(self.val)

class FLOAT:
    def __init__(self, val: int):
        self.val = val
    def __str__(self):
        return str(self.val)

class FUNCTION:
    def __init__(self, source: List[str]):
        self.source = source
    def __str__(self):
        return '\n'.join(self.source)