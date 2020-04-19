from typing import Callable, List


TYPES = [

    'лог',
    'вещ',
    'цел',

]


class VarSystem:
    #TODO get vars exception
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

    def get_func(self, name: str, res: List[str], is_func=False, args: List[str] = []) -> None:
        self.vars.update({name: FUNCTION(res, is_func=is_func, args=args)})

    def print_var(self) -> List[str]:
        return self.vars.keys()

    def get_var(self, name):
        try:
            return self.vars.get(name)
        except:
            #TODO nofound variable exception
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
    args = {}
    def __init__(self, source: List[str], is_func: bool = False, args: List[str] = False):
        self.source = source
        self.is_func = is_func
        args = ','.join(args)
        for i in TYPES + ['арг', 'рез']:
            try:
                args = args.replace(i, ' ' + i + ' ')
            except: pass
        args = args.replace(',', ' ').split()
        #TODO exception with tipization
        m_type = ''
        m_for_what = 'арг'
        for i in args:
            if i in TYPES:
                m_type = i
                continue
            if i in ['арг', 'рез']:
                m_for_what = i
                continue
            #!
            if m_type != '':
                self.args.update({i: [m_type, m_for_what]})
        print(self.get_args(), 'init')

    def get_args(self):
        return self.args

    def __str__(self):
        return '\n'.join(self.source)