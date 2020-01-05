import spruthub
from yeelight import discover_bulbs
from yeelight import Bulb
from time import sleep
import json


def read_config(configFileName):
    with open(configFileName) as json_file:
        config = json.load(json_file)
    interval = config['interval']

    if config['discovery'] == True:
        bulbs = discover_bulbs()
    else:
        bulbs = config['bulbs']
    return bulbs, interval, config


def connect(bulbs, aids):
    if len(bulbs) != len(aids):
        raise ConfigError("List with bulbs hs different shape\nbulbs list:{}\nsh aid list:{}".format(
            bulbs, aids))

    connections = []
    i = 0
    for b, aid in zip(bulbs, aids):
        connections.append([Bulb(ip=b['ip'], port=b['port']),
                            {'currentstatus': None, 'color': None, 'colortemp': None}, aid])
        i+=1
    return connections


def mainLoop(bulbs, interval, config, sh):
    connections = connect(bulbs, config['sh_aid'])
    while True:
        try:
            for b in connections:
                siate_dict = sh.listOfAllCharacteristicsOfOneServiceAndAccessory(
                    b[2], 10)
                if siate_dict[1]['value'] != b[1]['currentstatus']:
                    b[1]['currentstatus'] = siate_dict[1]['value']
                    if b[1]['currentstatus'] == 'true':
                        b[0].turn_on()
                    else:
                        b[0].turn_off()
                h = int(float(siate_dict[2]['value']))
                s = (float(siate_dict[0]['value']) /
                     float(siate_dict[0]['maxValue'])) * 100
                v = int(siate_dict[4]['value'])
                if b[1]['color'] != (h, s, v):
                    b[1]['color'] = (h, s, v)
                    b[0].set_hsv(b[1]['color'][0], b[1]
                                 ['color'][1], b[1]['color'][2])
                if siate_dict[3]['value'] != b[1]['colortemp']:
                    b[1]['colortemp'] = siate_dict[3]['value']
                    b[0].set_color_temp(
                        int((1700 * (500 - int(b[1]['colortemp']))) / 140))
        except Exception as e:
            print(e)
            if e == 'Bulb closed the connection.':
                connections = connect(bulbs, config['sh_aid'])
                continue
            else:
                raise e
            sleep(interval)


if __name__ == '__main__':
    configFileName = 'bulbs_config.json'
    bulbs, interval, config = read_config(configFileName)
    sh = spruthub.api(config['sh_server']['url'])
    sh.auth(config['sh_server']['login'], config['sh_server']['password'])
    mainLoop(bulbs, interval, config, sh)
