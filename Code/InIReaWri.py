import configparser

config_path = r"C:\Users\HY_Burger\Desktop\Project\RespVariability\config.ini"


def DecoConf(func):
    def Wrapper(type, name, conf):
        try:
            conf = configparser.ConfigParser()
            conf.read(config_path)
            return func(type, name, conf)
        except:
            print(type + " " + name + " " + "config path error")

    return Wrapper


@DecoConf
def ConfigR(type, name, conf=None):
    return conf[type][name]


@DecoConf
def ConfigW(type, name, info, conf=None):
    if type in conf.sections():
        conf[type][name] = info
    else:
        conf[type] = {}
        conf[type][name] = info
    with open(config_path, "w") as configfile:
        conf.write(configfile)