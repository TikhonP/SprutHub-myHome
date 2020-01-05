import spruthub
from yeelight import discover_bulbs
from yeelight import Bulb
from time import sleep
import json
import logging
from miio import PhilipsBulb


def read_config(configFileName):
    with open(configFileName) as json_file:
        config = json.load(json_file)
    interval = config['interval']

    logging.info('Config ------------\n {} \n------------'.format(interval))
    # yeelight
    if config['yeelight']['discovery'] == True:
        logging.info('Discovery True')
        ybulbs = discover_bulbs()
    else:
        logging.info('Discovery False')
        ybulbs = config['yeelight']['bulbs']
    # philips
    fbulbs = config['philips']['bulbs']
    return ybulbs, fbulbs, interval, config


def connect_yeelight(bulbs, aids):
    if len(bulbs) != len(aids):
        raise ConfigError("List with bulbs hs different shape\nbulbs list:{}\nsh aid list:{}".format(
            bulbs, aids))

    connections = []
    i = 0
    for b, aid in zip(bulbs, aids):
        connections.append([Bulb(ip=b['ip'], port=b['port']),
                            {'currentstatus': None, 'color': None, 'colortemp': None}, aid])
        i += 1
    return connections


def connect_philips(bulbs, aids):
    if len(bulbs) != len(aids):
        raise ConfigError("List with bulbs hs different shape\nbulbs list:{}\nsh aid list:{}".format(
            bulbs, aids))

    connections = []
    i = 0
    for b, aid in zip(bulbs, aids):
        connections.append([PhilipsBulb(str(b['ip']), str(b['token'])),
                            {'currentstatus': None, 'brightness': None, 'colortemp': None}, aid])
        i += 1
    return connections


def mainLoop(ybulbs, fbulbs, interval, config, sh):
    yconnections = connect_yeelight(ybulbs, config['yeelight']['sh_aid'])
    fconnections = connect_philips(fbulbs, config['philips']['sh_aid'])
    print(yconnections)
    print()
    print(fconnections)
    # logging.info('Connections ------------{}------------'.format(connections))

    while True:
        try:
            for b in yconnections:
                siate_dict = sh.listOfAllCharacteristicsOfOneServiceAndAccessory(
                    b[2], 10)
                if siate_dict[1]['value'] != b[1]['currentstatus']:
                    b[1]['currentstatus'] = siate_dict[1]['value']
                    if b[1]['currentstatus'] == 'true':
                        print(b)
                        b[0].turn_on()
                        logging.info('Turn on bulb')
                    else:
                        b[0].turn_off()
                        logging.info('Turn off bulb')
                h = int(float(siate_dict[2]['value']))
                s = (float(siate_dict[0]['value']) /
                     float(siate_dict[0]['maxValue'])) * 100
                v = int(siate_dict[4]['value'])
                if b[1]['color'] != (h, s, v):
                    b[1]['color'] = (h, s, v)
                    b[0].set_hsv(b[1]['color'][0], b[1]
                                 ['color'][1], b[1]['color'][2])
                    logging.info('Set hsv {} {} {}'.format(
                        str(b[1]['color'][0]), str(b[1]['color'][1]), str(b[1]['color'][2])))
                if siate_dict[3]['value'] != b[1]['colortemp']:
                    b[1]['colortemp'] = siate_dict[3]['value']
                    b[0].set_color_temp(
                        int((1700 * (500 - int(b[1]['colortemp']))) / 140))
                    logging.info('Set color temp {}'.format(
                        int((1700 * (500 - int(b[1]['colortemp']))) / 140)))
            for b in fconnections:
                siate_dict = sh.listOfAllCharacteristicsOfOneServiceAndAccessory(
                    b[2], 10)
                if siate_dict[0]['value'] != b[1]['currentstatus']:
                    b[1]['currentstatus'] = siate_dict[1]['value']
                    if b[1]['currentstatus'] == 'true':
                        b[0].on()
                        logging.info('Turn on bulb')
                    else:
                        b[0].off()
                        logging.info('Turn off bulb')
                if b[1]['currentstatus'] == 'false': continue
                if siate_dict[2]['value'] == '0':
                    siate_dict[2]['value'] = '1'
                if b[1]['brightness'] != siate_dict[2]['value']:
                    b[1]['brightness'] = int(siate_dict[2]['value'])
                    b[0].set_brightness(b[1]['brightness'])
                    logging.info('Set brightness {}'.format(
                        b[1]['brightness']))
                if siate_dict[1]['value'] == '0':
                    siate_dict[1]['value'] = '1'
                if siate_dict[1]['value'] != b[1]['colortemp']:
                    b[1]['colortemp'] = siate_dict[1]['value']
                    b[0].set_color_temperature(
                        100 - int((int(siate_dict[1]['value']) * 100) / 500))
                    logging.info('Set color temp {}'.format(
                        100 - int((int(siate_dict[1]['value']) * 100) / 500)))

        except Exception as e:
            logging.error(e)
            if e == 'Bulb closed the connection.':
                yconnections = connect_yeelight(bulbs, config['sh_aid'])
                continue
                logging.warning('Reconnected')
            else:
                raise e
            sleep(interval)
            logging.info('Sleeping {} seconds'.format(interval))


if __name__ == '__main__':
    logging.basicConfig(filename='yeelght_sh.log', filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    logging.info('Starting...')

    configFileName = 'bulbs_config.json'
    logging.info('Filename is "{}"'.format(configFileName))

    ybulbs, fbulbs, interval, config = read_config(configFileName)
    logging.info('bulbs --------\n{}\n--------'.format(ybulbs))

    sh = spruthub.api(config['sh_server']['url'])
    t = sh.auth(config['sh_server']['login'], config['sh_server']['password'])
    logging.info('Token - {}'.format(t))

    mainLoop(ybulbs, fbulbs, interval, config, sh)
