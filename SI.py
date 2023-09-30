# wykys 2017
# SI convert

PREFIX_DICT = {
    'y': -24,  # yocto
    'z': -21,  # zepto
    'a': -18,  # atto
    'f': -15,  # femto
    'p': -12,  # pico
    'n': -9,   # nano
    'u': -6,   # micro
    'm': -3,   # mili
    'c': -2,   # centi
    'd': -1,   # deci
    'k': 3,    # kilo
    'M': 6,    # mega
    'G': 9,    # giga
    'T': 12,   # tera
    'P': 15,   # peta
    'E': 18,   # exa
    'Z': 21,   # zetta
    'Y': 24,   # yotta
}


def si_to_exp(x: str) -> str:
    """ convert SI prefix to exponencial """
    for prefix, exponent in PREFIX_DICT.items():
        if prefix in x:
            return f'{x.replace(prefix, ".")}e{exponent}'
    return x
