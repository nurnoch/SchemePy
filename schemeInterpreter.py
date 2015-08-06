### Scheme Interpreter in Python

import math
import operator as op

### Representation of Scheme objects in Python
Symbol = str  # Scheme Symbol is implemented as a Python str
List = list # Scheme List is implemented as a Python list
Number = (int, float) # Scheme Number is implemented as a Python int or float

### Parsing:
# 1. input string is broken up into a sequence of tokens
# 2. tokens are assembled into an abstract syntax tree

# Read a Scheme expression from a string
def parse(program):
    return read_from_tokens(tokenize(program))

# Convert the input string into a list of tokens
def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

# Read an expression from a list of tokens
def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF while reading")
    token = tokens.pop(0) # The first token in the list
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError("Unexpected )")
    else:
        return atom(token)

# Numbers become numbers; every other token is a symbol
def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token) # make it str

### Environments:
# envrionment is a mapping from variable names to their values

# An environment with some Scheme standard procedures
def standard_env():
    env = Env()
    env.update(vars(math)) # pow, sin, cos, exp...
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': apply,
        'begin':lambda *x: x[-1],
        'car': lambda x: x[0], # return the first element
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y, # construct two elements
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': map,
        'max': max, 'min': min,
        'not': op.not_, 'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol': lambda x: instance(x, Symbol),
    })
    return env

# An environment with an outer Env
class Env(dict):
    def __init__(self, params = (), args = (), outer = None):
        self.update(zip(params, args))
        self.outer = outer
    # Find the right environment: the inner or outer
    def find(self, var):
        return self if (var in self) else self.outer.find(var)

global_env = standard_env()


### Eval
# execute the internal representation and carry out the computation

# Evaluate an expression in an environment
def eval(x, env = global_env):
    if isinstance(x, Symbol): # variable reference
        return env.find(x)[x] # return corresponding value
    elif not isinstance(x, List): # constant literal like 'begin'
        return x
    elif x[0] == 'quote': # quote expression
        (_, exp) = x # (quote (+ 1 2))  -> (+ 1 2)
        return exp
    elif x[0] == 'if': # if test conseq alt
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define': # define var exp
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'set!': # set! var exp
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env) # var must be pre-defined
    elif x[0] == 'lambda': # lambda (var...) exp
        (_, var, exp) = x
        return Procedure(var, exp, env) # create a procedure
    else: # + 1 2
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)


### Procedures
# A user-defined Scheme procedure
# params: a list of names; body: a body expression; env: an outer environment
class Procedure(object):
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    def __call__(self, *args):
        return eval(self.body, Env(self.params, args, self.env))

### REPL
# An interactive read-eval-print loop
def repl(prompt = "Scheme> "):
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None:
            print schemeStr(val)

# Convert a Python object to a Scheme-readable string
def schemeStr(exp):
    if isinstance(exp, list):
        return '(' + ''.join(map(schemeStr, exp)) + ')'
    else:
        return str(exp)





