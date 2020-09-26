SPECTRUM = {
    # ISO 21348. spacewx.com/pdf/SET_21348_2004.pdf
    # tag: (A, B) such that A <= λ < B
    "xray": (0.001, 0.1),
    "XUV": (0.1, 10),

    "ultraviolet": (100, 400),
    "VUV": (10, 200),
    "EUV": (10, 121),
    "H_Lyman_alpha": (121, 122),
    "FUV": (122, 200),
    "UVC": (100, 280),
    "MUV": (200, 300),
    "UVB": (280, 315),
    "NUV": (300, 400),
    "UVA": (315, 400),

    "visible": (380, 760),
    "purple": (360, 450),
    "blue": (450, 500),
    "green": (500, 570),
    "yellow": (570, 591),
    "orange": (591, 610),
    "red": (610, 760),

    "infrared": (760, 1e6),
    "IRA": (760, 1400),
    "IRB": (1400, 3000),
    "IRC": (3000, 1e6),

    "microwave": (1e6, 15e6),
    "W": (3.00e6, 5.35e6),
    "V": (5.35e6, 5.52e6),
    "Q": (6.52e6, 8.33e6),
    "K": (8.33e6, 2.75e7),
    "X": (2.75e7, 5.77e7),
    "C": (4.84e7, 7.69e7),
    "S": (5.77e7, 1.93e8),
    "L": (1.93e8, 7.69e8),
    "P": (7.69e8, 1.33e9),

    "radio": (1e5, 1e11),
    "EHF": (1e6, 1e7),
    "SHF": (1e7, 1e8),
    "UHF": (1e8, 1e9),
    "VHF": (1e9, 1e10),
    "HF": (1e10, 1e11)
}


def spectrum_names(wavelength):
    names = []
    wavelength = float(wavelength) * 1e9
    for name, (a, b) in SPECTRUM.items():
        if a <= wavelength < b:
            names.append((b-a, name))
    return [name for size, name in sorted(names, reverse=True)]
