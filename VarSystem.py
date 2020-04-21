from typing import Callable, List


TYPES = [

    'лог',
    'вещ',
    'цел'

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

    def get_func(self, name: str, res: List[str], is_func=False, args: List[str] = [], type: str = None) -> None:
        self.vars.update({name: FUNCTION(res, is_func=is_func, args=args, type=type)})

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
    def __init__(self, source: List[str], is_func: bool = False, args: List[str] = [], type: str = None):
        self.args = {}
        print(args, 'args in parent')
        self.source = source
        self.is_func = is_func
        args = ','.join(args)
        for i in TYPES + ['арг', 'рез']:
            try:
                args = args.replace(i, ' ' + i + ' ')
            except: pass
        args = args.replace(',', ' ').split()
        if not is_func:
            try:
                for i in range(len(args)):
                    if args[i] == 'знач':
                        del args[i]
            except: pass
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
        self.namespace = VarSystem()
        #TODO get types of vars
        for i in self.args.keys():
            if self.args[i][0] == 'цел':
                self.namespace.get_int_var(i, '-9999')
            elif self.args[i][0] == 'лог':
                self.namespace.get_bool_var(i, 'False')
        if is_func:
            if 'цел' in type:
                self.namespace.get_int_var('знач', '-9999')
                self.args.update({'знач': ['цел', 'рез']})
            elif 'лог' in type:
                self.namespace.get_bool_var('знач', 'False')
                self.args.update({'знач': ['лог', 'рез']})
        print(self.namespace.vars)


    def reinit(self):
        for i in self.args.keys():
            if self.args[i][0] == 'цел':
                self.namespace.get_int_var(i, self.args[i][-1])
            elif self.args[i][0] == 'лог':
                self.namespace.get_bool_var(i, self.args[i][-1])
    def get_args(self):
        return self.args

    def __str__(self):
        return '\n'.join(self.source)