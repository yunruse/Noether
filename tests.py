from noether import Unit

tests = (
    (200, 1000, '200 ± 1000'),
    (2e5, 1, '2×10^5 ± 1'),
    (2e6, 1e6, '(2 ± 1)×10^6'),
    (2, 1, '2 ± 1'),
    (2, 800000, '2 ± 8×10^5'),
)

def test():
    Unit.unicodeExponent = False
    success = True
    for num, delta, rep in tests:
        a = Unit(num, _delta=delta)
        result = a._numerical(False)
        if result != rep:
            success = False
            print('{} != {}'.format(
                result, rep))

    if success:
        print('All {} tests passed'.format(len(tests)))
