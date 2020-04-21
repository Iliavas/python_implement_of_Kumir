import math
import re
from utils import split_string, get_quoters_under_func
from math import *
from tkinter import END
from time import sleep

from typing import Callable, List, Dict

from VarSystem import FUNCTION

CHARCH = [
    '+',
    '-',
    '*',
    '/',
]

to_replace = {

    'не' : 'not',
    'и' : 'and',
    'или' : 'or'

}

class Parser:
    def __init__(self, hero, namespace):
        self.namespace = namespace
        for i in dir(math):
            CHARCH.append(i)
        self.hero = hero

    def parse(self, string : str, namespace, is_function: bool = False, args: Dict = {}):
        self.namespace = namespace
        counter = 0
        is_if = False
        text = string.split('\n')
        for i in text:
            i = self.insert_nl(i)
            for j in i.split():
                if j == 'алг':
                    text[counter:] = self.parsing_algoritms(i, text[counter:])
            counter += 1
        word_counter = 0
        counter = 0
        for i in text:
            i = self.insert_nl(i)
            for j in i.split():
                if j == 'если':
                    self.if_parse(i, string.split('\n')[counter+1:], self.get_spaces(i))
                    is_if = True
                elif j == 'пока':
                    text = self.while_parse(string.split('\n')[counter+1:], i, self.get_spaces(i), text, counter)
                elif j == ':=':
                    self.parse_equal(i)
                    is_if = True
                    break
                elif j == 'вывод':
                    self.printing(i)
                    break
                elif j == 'цел':
                    self.get_int_var(i.replace('цел', ''))
                    break
                elif j == 'лог':
                    self.get_bool_var(i.replace('лог', ''))
                    break
                elif j == 'ввод':
                    self.parsing_input(i.split('ввод')[-1])
                    break
                elif re.sub('\(.*\)', '', j) in list(namespace.vars.keys()):
                    self.solving(' '.join(i.split()[word_counter:]))
                else:
                    self.parsing_comands(i)
                word_counter += 1
            counter += 1
            word_counter = 0
            if is_if: break
        if is_function:
            to_ret = {}
            for i in args.keys():
                if args[i][1] == 'рез':
                    if i != 'знач':
                        to_ret.update({args[i][2]: self.namespace.vars[i]})
                    else:
                        print('self.namespace', self.namespace.vars, self.namespace.vars['знач'])
                        return self.namespace.vars['знач']
            return to_ret

    def solving(self, string):
        loc_s = list(string)
        for i in enumerate(loc_s):
            loc_s[i[0]] = i[1].replace(' ', '')
        if '\n' in loc_s:
            return '\n'
        from MapScene import walls
        for i in enumerate(list(self.namespace.vars.keys())):
            try:
                it = re.finditer('[^A-z](' + i[1] + ')[^A-z]|^'+i[1]+'|$'+i[1], string)
            except: continue
            for j in it:
                print(i[1])
                if not isinstance(self.namespace.vars[i[1]], FUNCTION):
                    string = split_string(string, j.start() + 1, str(self.namespace.vars[j.group().replace(' ', '').replace('(', '').replace(')', '')]), j.end() - 1)
                else:
                    example = self.namespace.vars[j.group().replace(' ', '')]
                    try:
                        args = re.findall(r'\(.+\)', string)[0].replace(' ', '').replace('(', '').replace(')', '').replace(',', ' ').split()
                    except:
                        #TODO exception call function without ()
                        args = []
                    for i in enumerate(example.args.keys()):
                        try:
                            example.args[i[1]].append(args[i[0]])
                        except: pass
                        #TODO exception low amount of arg's
                    example.reinit()
                    ret = self.parse(str(example), example.namespace, is_function=True, args=example.args)
                    if not example.is_func:
                        for k in ret.keys():
                            self.namespace.vars[k] = ret[k]
                        return 0
                    try:
                        end = re.search(r'\)', string).end()
                        string = split_string(string, j.start(), ret, end)
                    except: print(string)
        for i in enumerate(list(CHARCH)):
            try:
                it = re.finditer('[^A-z](' + i[1] + ')[^A-z]', string)
                for j in it:
                    string = split_string(string, j.start(), j.group(), j.end())
            except: pass
        s = string.split()
        f = False
        Hor_dir = False
        for i in enumerate(s):
            if i[1] == 'сверху':
                f = True
                Hor_dir = True
                s[i[0]] = str([self.hero.pos[0], self.hero.pos[1]])
            elif i[1] == 'справа':
                f = True
                s[i[0]] = str([self.hero.pos[0] + 30, self.hero.pos[1]])
            elif i[1] == 'слева':
                f = True
                s[i[0]] = str([self.hero.pos[0], self.hero.pos[1]])
            elif i[1] == 'снизу':
                f = True
                Hor_dir = True
                s[i[0]] = str([self.hero.pos[0], self.hero.pos[1] + 30])
            elif f == True:
                f = False
                if i[1] == 'не':
                    s[i[0]] = str(' not in ')
                else:
                    s.insert(i[0], ' in ')
        for i in enumerate(s):
            if i[1] == 'стена':
                if Hor_dir:
                    s[i[0]] = str(walls['horizontal'])
                else:
                    s[i[0]] = str(walls['vertical'])
        string = ' '.join(s)
        st = ''
        try:
            if string[0] == ' ':
                st += ' '
        except: pass
        for i in string.split():
            if i in list(self.namespace.vars.keys()):
                st += str(self.namespace.vars[i])
            elif i in list(to_replace.keys()):
                st += to_replace.get(i)
            else:
                st += i
            st += ' '
        try:
            return str(eval(st))
        except:
            #TODO exception unrecognised expression
            pass

    def parse_equal(self, i):
        res = i.split(':=')[1]
        for j in i.split(':=')[1].split(' '):
            if j in CHARCH or j in list(self.namespace.vars.keys()):
                res = self.solving(i.split(':=')[1])
                break
        #try:
        self.namespace.vars[i.split(':=')[0].replace(' ', '')] = res
        #except: print('sosat')

    def printing(self, string):
        res = ''
        q = []
        c = 0
        for i in string + ' ':
            if i == '"':
                q.append(c)
                if len(q) == 2:
                    self.hero.console.write(string[q[0]+1:q[1]])
            if len(q) >= 2:
                q = []
            c += 1
        string = re.sub(r'".*"', '', string)
        a = string.split('вывод')[-1]
        a = get_quoters_under_func(a)

        for j in range(len(a)):
            res += self.solving(a[j])
        self.hero.console.write(res)

    def parsing_comands(self, string):
        for j in string.split(' '):
            if j == 'вправо':
                self.hero.pos = self.hero.controller.move_one_forward(self.hero.pos)
            elif j == 'вниз':
                self.hero.pos = self.hero.controller.move_one_down(self.hero.pos)
            elif j == 'влево':
                self.hero.pos = self.hero.controller.move_one_backward(self.hero.pos)
            elif j == 'вверх':
                self.hero.pos = self.hero.controller.move_one_up(self.hero.pos)
            elif j == 'закрасить':
                self.hero.controller.fill()
            #sleep(0.5)

    def parsing_input(self, string):
        f = False
        string = re.sub(' ', '', string)
        string = string.split(',')
        if string[0][0] == '"':
            a = string[0]
            del string[0]
            self.printing(a)
        buffer = string[0]
        for i in string[1:]:
            if i == 'нс':
                self.printing('\n')
                self.parsing_input(buffer)
                f = True
            buffer = i
        if f: return 0
        self.hero.console.curr_val = string
        self.hero.console.pre_string = self.hero.console.get_string()
        self.namespace.get_int_var(string[-1], -9999)
        while self.namespace.get_var(string[-1]) == -9999:
            sleep(1)

    def insert_nl(self, string: str):
        nl = re.sub('нс', '\n', string)
        return nl

    def get_var(func: Callable) -> Callable:
        def wrapper(self, string: str, l: List[str] = []):
            a = re.sub(' ', '', string)
            a = get_quoters_under_func(a)
            func(self, string, l=a)
        return wrapper

    @get_var
    def get_int_var(self, string: str, l: List[str] = []):
        for i in l:
            try:
                name, res = i.split(':=')
                res = self.solving(res)
            except:
                name, res, = i, ''
            self.namespace.get_int_var(name, res)
    @get_var
    def get_bool_var(self, string: str, l: List[str] = []):
        for i in l:
            try:
                name, res = i.split(':=')
            except:
                name, res = i, ''
            self.namespace.get_bool_var(name, res)

    def get_spaces(self, string: str):
        return len(re.split('\S', string)[0])

    def if_parse(self, string, program, spaces=2):
        string = string.split()
        del string[0], string[-1]
        boolean = self.solving(' '.join(string))
        if boolean == 'False':
            for i in range(len(program)):
                try:
                    del program[0]
                    if ('все' in program[0] or 'иначе' in program[0]) and self.get_spaces(program[0]) == spaces:
                        break
                except: pass
        if boolean == 'True':
            min_, max_ = 0, 0
            for i in range(len(program)):
                if 'иначе' in program[i] and spaces == self.get_spaces(program[i]):
                    min_ = i
                elif 'все' in program[i] and spaces == self.get_spaces(program[i]) and min_:
                    max_ = i
            program[min_: max_] = ''
        self.parse('\n'.join(program))

    def while_parse(self, program, s, spaces, text, counter):
        end = 0
        for i in enumerate(program):
            if 'кц' in i[1] and self.get_spaces(i[1]) == spaces:
                program = program[:i[0]]
                break
            end += 1
        while True:
            self.parse('\n'.join(program))
            if self.solving(' '.join(s.split()[2:-1])) == 'False': break
        for i in range(counter, counter+end):
            del text[i]
        return text

    def parsing_algoritms(self, string: str, program: List[str]) -> List[str]:
        if not len(re.findall(r'\w', string.replace('алг', ''))): return program
        is_function = False
        s = re.sub(r'\(.+\)', '', string)
        name = s.replace('алг', '', 1)
        t = None
        if len(name.split()) > 1:
            #TODO fix tipization
            t = name.split()[0]
            name = name.split()[-1]

            is_function = True
        try:
            args = re.findall('\(.*\)', string)[0].replace(' ', '').replace('(', '').replace(')', '').split(',')
        except: args = []
        end = 0
        for i in enumerate(program):
            if 'кон' in i[1] and self.get_spaces(i[1]) == 0:
                end = i[0]
                break
        self.namespace.get_func(name.replace(' ', ''), program[2:end], is_func=is_function, args=args, type=t)
        del program[:end]
        return program