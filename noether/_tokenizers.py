from io import BytesIO
from typing import Any, Callable, Generator, Iterable, Iterator, Mapping
from tokenize import tokenize, TokenInfo, NUMBER, NAME, OP, ENCODING


def _t(type: int, string: str):
    return TokenInfo(type, string, (0, 0), (0, 0), '')


TokenStream = Iterator[TokenInfo]

StreamProcessor = Callable[[TokenStream], TokenStream]


def cli_dialect(stream: TokenStream):
    '''
    Process tokens for __main__ dialect, replacing `3u` -> `u(3)` and `in` -> `inch`.
    '''
    num: TokenInfo | None = None
    for token in stream:
        if token.type == NAME and token.string == 'in':
            token = token._replace(string='inch')

        if token.type == NUMBER:
            num = token
        elif num is not None:
            if token.type == NAME:
                yield token
                yield _t(OP, '(')
                yield num
                yield _t(OP, ')')
            else:
                yield num
                yield token
            num = None
        else:
            yield token


def untokenize(stream: TokenStream):
    s = iter(stream)
    assert next(s).type == ENCODING
    return ''.join(token.string for token in s)


def transform(text: str, processor: StreamProcessor):
    return untokenize(processor(tokenize(BytesIO(text.encode()).readline)))


if __name__ == '__main__':
    from sys import argv
    text = ' '.join(argv[1:])
    print(transform(text, cli_dialect))
