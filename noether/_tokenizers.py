from functools import wraps
from collections import deque
from io import BytesIO
from typing import Any, Callable, Generator, Iterable, Iterator, Mapping
from tokenize import tokenize as _tokenize, TokenInfo, NUMBER, NAME, OP, ENCODING


def _t(type: int, string: str):
    return TokenInfo(type, string, (0, 0), (0, 0), '')


TokenStream = Iterator[TokenInfo]
StreamProcessor = Callable[[TokenStream], TokenStream]

def tokenize(text: str):
    return _tokenize(BytesIO(text.encode()).readline)

def untokenize(stream: TokenStream):
    s = iter(stream)
    assert next(s).type == ENCODING
    return ''.join(token.string for token in s)


def transformer(
    dialect: Callable[[TokenStream], TokenStream]
):
    @wraps(dialect)
    def my_func(text: str):
        return untokenize(dialect(tokenize(text)))
    return my_func


@transformer
def noether_dialect(stream: TokenStream) -> TokenStream:
    '''
    Process tokens using a slightly modified dialect
    of Python that is used in the command-line interface
    and the automatic cataloguing (.yaml -> .py) system.

    Replacement rules are:
    - name `x`                -> operator `*`
    - operator `^`            -> operator `**`
    - name `in`               -> name `inch`
    - number-and-name `Xunit` -> `X * unit`

    Take note: currently affine units such as degC or degF
    should be called e.g. `degC(10)` or they will function
    relatively (i.e. `10degC` is equivalent to `10K`)
    '''
    queue: deque[TokenInfo] = deque()

    for token in stream:
        if token.type == OP and token.string == '^':
            token = token._replace(string='**')
        if token.type == NAME and token.string == 'x':
            token = TokenInfo(OP, '*', token.start, token.end, token.line)
        if token.type == NAME and token.string == 'in':
            token = token._replace(string='inch')

        # TODO: can we do a workaround for
        # affine units like degC?
        # would have to capture the minus sign again :<

        queue.append(token)
        if len(queue) == 2:
            tt = [t.type for t in queue]
            if tt[-2:] == [NUMBER, NAME]:
                number, unit_name = queue
                yield number
                yield _t(OP, '*')
                yield unit_name
                queue.clear()
            else:
                yield queue.popleft()

def transform(text: str, processor: StreamProcessor, **args):
    return untokenize(processor(tokenize(text), **args))

if __name__ == '__main__':
    from sys import argv
    text = ' '.join(argv[1:])
    print(noether_dialect(text))
