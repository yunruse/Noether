from functools import wraps
from collections import deque
from io import BytesIO
from typing import Callable, Iterator
from tokenize import tokenize, TokenInfo, NUMBER, NAME, OP, ENCODING


def _t(type: int, string: str):
    return TokenInfo(type, string, (0, 0), (0, 0), '')


TokenStream = Iterator[TokenInfo]
StreamProcessor = Callable[[TokenStream], TokenStream]


def untokenize(stream: TokenStream):
    s = iter(stream)
    assert next(s).type == ENCODING
    return ''.join(token.string for token in s)


def transformer(
    dialect: Callable[[TokenStream], TokenStream]
):
    @wraps(dialect)
    def my_func(text: str):
        tokens = tokenize(BytesIO(text.encode()).readline)
        return untokenize(dialect(tokens))
    return my_func


@transformer
def units_dialect(stream: TokenStream) -> TokenStream:
    '''
    Process tokens for __main__ dialect, replacing:
    - `in` -> `inch`
    - `-3unit` -> `unit(-3)`
    '''
    queue: deque[TokenInfo] = deque()

    for token in stream:
        if token.type == NAME and token.string == 'in':
            token = token._replace(string='inch')

        queue.append(token)
        if len(queue) == 3:
            tt = [t.type for t in queue]
            if tt[-2:] == [NUMBER, NAME]:
                maybe_minus, number, unit_name = queue
                is_minus = maybe_minus.type == OP and maybe_minus.string == '-'
                if not is_minus:
                    yield maybe_minus
                yield unit_name
                yield _t(OP, '(')
                if is_minus:
                    yield maybe_minus
                yield number
                yield _t(OP, ')')
                queue.clear()
            else:
                yield queue.popleft()


if __name__ == '__main__':
    from sys import argv
    text = ' '.join(argv[1:])
    print(units_dialect(text))
