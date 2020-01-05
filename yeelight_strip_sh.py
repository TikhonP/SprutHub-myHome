import spruthub
from yeelight import discover_bulbs
from yeelight import Bulb
from time import sleep
import json
import logging


def read_config(configFileName):
    with open(configFileName) as json_file:
        config = json.load(json_file)
    interval = config['interval']

    logging.info('Config ------------\n {} \n------------'.format(interval))

    if config['discovery'] == True:
        logging.info('Discovery True')
        bulbs = discover_bulbs()
    else:
        logging.info('Discovery False')
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
        i += 1
    return connections


def mainLoop(bulbs, interval, config, sh):
    connections = connect(bulbs, config['sh_aid'])
    logging.info('Connections ------------{}------------'.format(connections))

    while True:
        try:
            for b in connections:
                siate_dict = sh.listOfAllCharacteristicsOfOneServiceAndAccessory(
                    b[2], 10)
                if siate_dict[1]['value'] != b[1]['currentstatus']:
                    b[1]['currentstatus'] = siate_dict[1]['value']
                    if b[1]['currentstatus'] == 'true':
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

        except Exception as e:
            logging.error(e)
            if e == 'Bulb closed the connection.':
                connections = connect(bulbs, config['sh_aid'])
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

    bulbs, interval, config = read_config(configFileName)
    logging.info('bulbs --------\n{}\n--------'.format(bulbs))

    sh = spruthub.api(config['sh_server']['url'])
    t = sh.auth(config['sh_server']['login'], config['sh_server']['password'])
    logging.info('Token - {}'.format(t))

    mainLoop(bulbs, interval, config, sh)
