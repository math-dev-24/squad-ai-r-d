import CoolProp.CoolProp as CP
from format import CONVERT_FOR_REF, CONVERT_REF_TO_USER

def ruler(fluid: str, car_need: str, car_1: str, val_1: float, car_2: str, val_2: float, path: str = "") -> int:
    """
    car exemple : P (pressure), T (temperature), H (enthalpy), D (density), V (volume), S (entropy)
    :param fluid: fluid name
    :param car_need: unit of the result
    :param car_1: unit of the first value
    :param val_1: value of the first value
    :param car_2: unit of the second value
    :param val_2: value of the second value
    :param path: path to the REFPROP installation
    :return: result
    """

    if path:
        CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, path)

    val_1: int = CONVERT_FOR_REF[car_1](val_1)
    val_2: int = CONVERT_FOR_REF[car_2](val_2)
    result: float = CP.PropsSI(car_need, car_1, val_1, car_2, val_2, fluid)
    return CONVERT_REF_TO_USER[car_need](result)