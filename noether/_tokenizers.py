from collections import deque
from io import BytesIO
from itertools import chain
from typing import Any, Callable, Generator, Iterable, Iterator, Mapping
from tokenize import (
    tokenize as _tokenize, TokenInfo,
    NUMBER, NAME, OP, ENCODING, ENDMARKER
)


def _t(type: int, string: str):
    return TokenInfo(type, string, (0, 0), (0, 0), '')


TokenStream = Iterator[TokenInfo]

StreamProcessor = Callable[[TokenStream], TokenStream]


def cli_dialect(stream: TokenStream, pythonesque=False):
    '''
    Process tokens for __main__ dialect, used on the
    command-line interface (CLI). Useful for quick
    calculations.
    Replacement rules are:
    - `Xunit` -> `X * unit` where X is some number eg -3, 4.2

    Additional rules if PYTHONESQUE is false:
    - `in` -> `inch`
    - `x` -> `*`
    - `^` -> `**`
    '''
    queue: deque[TokenInfo] = deque()

    # Because the queue may optionally process 3 extra tokens:
    dummy_stream = [_t(ENDMARKER, '')] * 3
    for token in chain(stream, dummy_stream):
        if not pythonesque:
            if token.type == OP and token.string == '^':
                token = token._replace(string='**')
            if token.type == NAME and token.string == 'x':
                token = TokenInfo(OP, '*', token.start, token.end, token.line)
            if token.type == NAME and token.string == 'in':
                token = token._replace(string='inch')

        # in the following queue, we might match `-5m**-2`:
        #  OP       -
        #  NUMBER
        #  NAME
        #  OP       **
        #  OP       -
        #  NUMBER
        #  we want to transform that to (m**-2)(-5)

        def is_op(op: TokenInfo, string: str):
            return op.type == OP and op.string == string

        queue.append(token)
        if len(queue) == 6:
            tt = [t.type for t in queue]
            if tt[1:3] == [NUMBER, NAME]:
                # here '_' indicates 'maybe'
                _m1, num, unit_name, _exp, _e1, _e2 = queue

                if is_op(_m1, '-'):
                    number = [_m1, num]
                else:
                    number = [num]
                    yield _m1

                unit = [unit_name]
                excess = [_exp, _e1, _e2]

                # handle `** (-)NUM`
                if is_op(_exp, '**'):
                    if is_op(_e1, '-') and _e2.type == NUMBER:
                        # unit ** -x
                        unit = [unit_name, _exp, _e1, _e2]
                        excess = []
                    elif _e1.type == NUMBER:
                        # unit ** x
                        unit = [unit_name, _exp, _e1]
                        excess = [_e2]

                yield _t(OP, '(')
                yield from unit
                yield _t(OP, ')')
                yield _t(OP, '(')
                yield from number
                yield _t(OP, ')')

                queue.clear()
                queue.extend(excess)
            else:
                yield queue.popleft()
    yield from queue

def tokenize(text: str):
    return _tokenize(BytesIO(text.encode()).readline)

def untokenize(stream: TokenStream):
    s = iter(stream)
    assert next(s).type == ENCODING
    return ''.join(token.string for token in s)


def transform(text: str, processor: StreamProcessor, **args):
    return untokenize(processor(tokenize(text), **args))


if __name__ == '__main__':
    from sys import argv
    text = ' '.join(argv[1:])
    print(transform(text, cli_dialect))
