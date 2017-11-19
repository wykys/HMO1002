# wykys 2017
# SI convert

def si_to_exp(x):
    """ convert SI prefix to exponencial """
    if type(x) is str:
        prefix = {
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

        for i in prefix:
            if i in x:
                return x.replace(i, '.') + 'e{}'.format(prefix[i])
    return x
