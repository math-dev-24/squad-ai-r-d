CONVERT_FOR_REF: dict = {
    "P": lambda x: x * 101325,
    "H": lambda x: x * 1000,
    "T": lambda x: x + 273.15,
    "Q": lambda x: x / 100,
    "D": lambda x: x,
    "V": lambda x: x,
    "S": lambda x: x,
}

CONVERT_REF_TO_USER: dict = {
    "P": lambda x: round((x / 10**5), 2),
    "T": lambda x: round((x - 273.15), 2),
    "H": lambda x: round((x / 1000), 2),
    "Q": lambda x: round(x * 100, 2),
    "D": lambda x: round(x, 2),
    "V": lambda x: x,
    "S": lambda x: round(x / 1000, 3)
}
