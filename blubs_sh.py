import spruthub
from yeelight import discover_bulbs
from time import sleep
import json
# import logging
from acssesorries import philipsB, yeelightB


def read_config(configFileName):
    with open(configFileName) as json_file:
        config = json.load(json_file)
    interval = config['interval']

    # logging.info('Config ------------\n {} \n------------'.format(interval))
    # yeelight
    if config['yeelight']['discovery'] == True:
        # logging.info('Discovery True')
        ybulbs = discover_bulbs()
    else:
        # logging.info('Discovery False')
        ybulbs = config['yeelight']['bulbs']
    # philips
    fbulbs = config['philips']['bulbs']
    return ybulbs, fbulbs, interval, config


def connect_yeelight(bulbs, aids):
    if len(bulbs) != len(aids):
        raise ConfigError("List with bulbs hs different shape\nbulbs list:{}\nsh aid list:{}".format(
            bulbs, aids))

    connections = []
    for b, aid in zip(bulbs, aids):
        connections.append([yeelightB(ip=b['ip'], port=b['port']), aid])
    return connections


def connect_philips(bulbs, aids):
    if len(bulbs) != len(aids):
        raise ConfigError("List with bulbs hs different shape\nbulbs list:{}\nsh aid list:{}".format(
            bulbs, aids))

    connections = []
    for b, aid in zip(bulbs, aids):
        connections.append([philipsB(str(b['ip']), str(b['token'])), aid])
    return connections


def mainLoop(ybulbs, fbulbs, interval, config, sh):
    yconnections = connect_yeelight(ybulbs, config['yeelight']['sh_aid'])
    fconnections = connect_philips(fbulbs, config['philips']['sh_aid'])
    print(yconnections)
    print()
    print(fconnections)
    print()
    # logging.info('Connections ------------{}------------'.format(connections))

    while True:
        try:
            for b in yconnections:
                state = sh.InfoAboutOneCharacteristic(b[1][0], b[1][1])['value']

                h = int(float(sh.InfoAboutOneCharacteristic(b[1][0], b[1][5])['value']))
                s = (float(sh.InfoAboutOneCharacteristic(b[1][0], b[1][4])['value']) /
                     float(sh.InfoAboutOneCharacteristic(b[1][0], b[1][4])['maxValue'])) * 100
                v = int(sh.InfoAboutOneCharacteristic(b[1][0], b[1][3])['value'])
                hsv = (h, s, v)

                color_temp = int(
                    (1700 * (500 - int(sh.InfoAboutOneCharacteristic(b[1][0], b[1][2])['value']))) / 140)

                # print('Yeelight ', state, ' h ',
                      # h, ' s ', s, ' v ', v, ' color_temp ', color_temp)

                b[0].update(state, hsv, color_temp)
            sleep(interval/2)

            for b in fconnections:
                state = sh.InfoAboutOneCharacteristic(b[1][0], b[1][1])['value']
                brightness = sh.InfoAboutOneCharacteristic(b[1][0], b[1][3])['value']
                color_temp = 100 - int((int(sh.InfoAboutOneCharacteristic(b[1][0], b[1][2])['value']) * 100) / 500)

                # print('Philips ', state, ' brightness ',
                      # brightness, ' color_temp ', color_temp)

                b[0].update(state, brightness, color_temp)
        except Exception as e:
            print(e)
            sleep(20)

        sleep(interval/2)


if __name__ == '__main__':
    # logging.info('Starting...')

    configFileName = 'configs/bulbs_config.json'
    # logging.info('Filename is "{}"'.format(configFileName))

    ybulbs, fbulbs, interval, config = read_config(configFileName)
    # logging.info('bulbs --------\n{}\n--------'.format(ybulbs))

    sh = spruthub.api(config['sh_server']['url'])
    t = sh.auth(config['sh_server']['login'], config['sh_server']['password'])
    # logging.info('Token - {}'.format(t))

    mainLoop(ybulbs, fbulbs, interval, config, sh)
