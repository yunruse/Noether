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
def cli_dialect(stream: TokenStream) -> TokenStream:
    '''
    Process tokens for __main__ dialect, used on the
    command-line interface (CLI). Useful for quick
    calculations.
    Replacement rules are:
    - `x` -> `*`
    - `^` -> `**`
    - `in` -> `inch`
    - `Xunit` -> `X * unit` where X is some number eg -3, 4.2
      Using multiply ensures eg `5m^2` is not misinterpreted as `(5m)^2`.
    '''
    queue: deque[TokenInfo] = deque()

    for token in stream:
        if token.type == OP and token.string == '^':
            token = token._replace(string='**')
        if token.type == NAME and token.string == 'x':
            token = TokenInfo(OP, '*', token.start, token.end, token.line)
        if token.type == NAME and token.string == 'in':
            token = token._replace(string='inch')

        # TODO: calling eg `10degC` now gets a wrong result because of *
        # can we fix that?
        # sadly it will have to involve grabbing the minus sign again

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
    print(cli_dialect(text))
