import spruthub
import json
from time import sleep


def read_config(sfilename, serfilename):
    with open(sfilename) as json_file:
        config = json.load(json_file)

    seqd = config['alarm_dev']
    devs = config['devs']
    interval = config['interval']

    with open(serfilename) as json_file:
        config = json.load(json_file)

    sh_server = config['sh_server']

    return seqd, devs, sh_server, interval


def convertValue(value):
    if value == 'true':
        return True
    elif value == 'false':
        return False
    elif value == '1':
        return True
    elif value == '0':
        return False
    else:
        raise Exception('InvalidValue')


def is_alarm(devs, sh):
    dev_satate = []
    for dev in devs:
        state = sh.InfoAboutOneCharacteristic(dev[0], dev[1])['value']
        state = convertValue(state)
        dev_satate.append(state)
    # print(dev_satate)
    return True in dev_satate


def mainLoop(seqd, devs, sh, interval):
    while True:
        try:
            if sh.InfoAboutOneCharacteristic(seqd[0], seqd[1])['value'] == '1':
                if is_alarm(devs, sh):
                    sh.SetСharacteristicValue(seqd[0], seqd[2], '4')
            sleep(interval)
        except Exception as e:
            print(e)
            print('\n Sleeeeeeeeeeping')
            sleep(15)


if __name__ == "__main__":
    configFileName = 'configs/config_security.json'
    file = 'configs/bulbs_config.json'
    seqd, devs, sh_server, interval = read_config(configFileName, file)
    sh = spruthub.api(sh_server['url'])
    t = sh.auth(sh_server['login'], sh_server['password'])
    mainLoop(seqd, devs, sh, interval)
