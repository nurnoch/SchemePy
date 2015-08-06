## A Scheme Interpreter in Python

This is [an implementation of Scheme interpreter][1], but not completed
compared to the Scheme standard.

### Scheme Programming Language
Scheme syntax is different from most other languages you may be familiar
with. Consider:

```Python
# Python Code
if x.val() > 0:
  func(A[i] + 1, ["one", "two"])
```

```Scheme
; Scheme Code
(if (> (val x) 0)
  (func (+ (aref A i) 1)
    (quote (one two)))
```

Scheme syntax is much simpler compared to other programming languages:

- Using a parenthesized-list Polish notation. Everything else is a list.
- Consisting solely of expressions.
- The first element of the list determines what it means. A list may start with a keyword e.g. (if ...) or a non-keyword, e.g. (func ...), is a function call.


### Scheme Interpreter

This interpreter defines a language that is a subset of Scheme using
only six special forms:

1. variable reference. var
2. constant literal. number
3. quotation. (quote exp)
4. conditional. (if test conseq alt)
5. definition. (define var exp)
6. procedure. (proc arg...)

Interpretation process:
program(str) -> **parse** -> abstract syntax tree (list) -> **eval** ->
result (object)

And here is a short example to show what the parse and eval do:
```Scheme
>> program = "(begin (define r 10) (* pi (* r r)))"

>>> parse(program)
['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]

>>> eval(parse(program))
314.1592653589793
```

There is no need to enter "eval(parse(...))" everytime. There is a
`repl` function which allows you to enter an expression, and see it
immediately.

```Scheme
>>> repl()
Scheme> (begin (define r 10) (* pi (* r r)))
314.159265359
Scheme> (if (> (* 10 10) 20) (* 7 6) oops)
42
```
---
###References
1. http://norvig.com/lispy.html
2. http://www.gnu.org/software/mit-scheme/documentation/mit-scheme-ref/Overview.html#Overview
3. http://docs.racket-lang.org/reference/index.html
4. http://deathking.github.io/yast-cn/chapter2.html


  [1]: http://norvig.com/lispy.html
  



 
