dict_invert = lambda d: dict(map(reversed, list(d.items()) ))

SUPERSCRIPT = str.maketrans(
    "-0123456789",
    "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"
)

NONBREAKING = {
    0x20: 0xA0,    # SPACE
    0x2009: 0x202F # THIN SPACE
}

def translate_by_if(obj, mapping: dict, condition: bool):
    return str(obj).translate(mapping) if condition else str(obj)
