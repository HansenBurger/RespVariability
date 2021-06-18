vent_machine_info = {
    "PB840": [1, 50, ["840", "PB840", "xs840", "xsPB 840"]],
    "Maquet": [2, 50, ["Servoi", "Servos", "xsServoi", "xsServos"]],
    "Drager": [3, 62.5, ["V300", "Evita", "Evita4", "xsV300", "xsEvita", "xsEvita4"]],
    "SV300_SV800": [4, 50, ["SV300", "SV800", "xsSV300", "xsSV800"]],
    "V60": [5, 50, ["V60", "xsV60"]],
    "V300": [8, 62.5, ["V300"]],
    "Vela": [11, 50, ["Vela", "xsVela"]],
    "Philips": [135, 128, ["Philips"]],
}


def ReadSamplerate(num_machine_type, str_machine_type=None):

    """
    num_machine_type: the machine ID from wave header
    str_machine_type: default none
    """

    if num_machine_type != None:

        for i in vent_machine_info.values():

            if num_machine_type == i[0]:
                refSampleRate = i[1]
                return refSampleRate

        print("1 - no matching types")

    elif num_machine_type == None and str_machine_type != None:

        try:
            type_name = str_machine_type.split("-")[0]
        except:
            print("Wrong machine name")

        for i in vent_machine_info.values():

            if type_name in i[2]:
                refSampleRate = i[1]
                return refSampleRate

        print("2 - no matching types")

    else:
        print("lack of valid input")

