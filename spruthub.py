import requests
import json


class api:
    def __init__(self, url):
        """Initial function

        :param url: string, server domen - ip:55555
        """
        self.url = 'http://' + url

    def auth(self, username, password):
        """Authenticate api

        :param username: string, username or email
        :param password: string, password
        """
        url = self.url + '/api/server/login/{}'.format(username)
        data = password
        answer = requests.post(url=url, data=data, headers={
                               'Accept': '*/*', 'Content-Type': '*/*'}, timeout=0.5)
        answer.raise_for_status()

        self.token = answer.headers['Set-Cookie'].split(sep=';')[
            0].split(sep='=')[1]
        self.cookie = {'token': self.token}

        return self.token

    def getAllLinks(self):
        url = self.url + '/api/server/links'
        answer = requests.get(
            url=url, headers={'accept': 'application/json'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def GetServerLogs(self, lastTime, count):
        url = self.url + \
            '/api/server/logs/{}/{}'.format(str(lastTime), str(count))
        answer = requests.get(
            url=url, headers={'accept': 'application/json'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def GetAllServersVariables(self):
        url = self.url + '/api/server/vars'
        answer = requests.get(
            url=url, headers={'accept': 'application/json'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def GetServserVersion(self):
        url = self.url + '/api/server/version'
        answer = requests.get(
            url=url, headers={'accept': 'text/plain'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

        return answer.text

    def GetThreadpoolStats(self, extended, query):
        url = self.url + \
            '/api/server/pools/{}/{}'.format(str(extended), str(query))
        answer = requests.get(
            url=url, headers={'accept': 'text/plain'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

        return answer.text

    def RestartServer(self):
        url = self.url + '/api/server/restart'
        answer = requests.post(
            url=url, headers={'Accept': '*/*'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

    def register(self, username, password):
        """Register api

        :param username: string, username or email
        :param password: string, password
        """
        url = self.url + '/api/server/register/'.format(username)
        data = password
        answer = requests.post(url=url, data=data, headers={
                               'Accept': '*/*', 'Content-Type': '*/*'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

    def SetVariable(self, key, value):
        url = self.url + '/api/server/vars/{}/{}'.format(key, value)
        answer = requests.put(
            url=url, headers={'accept': '*/*'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

# Accessories

    def RemoveAccessory(self, aid):
        url = self.url + '/api/accessories/{}'.format(str(aid))
        answer = requests.delete(url=url, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

    def listOfAllAccessories(self):
        url = self.url + '/api/accessories'
        answer = requests.get(url=url, headers={
                              'Accept': 'application/json'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def InfoAboutAccessory(self, aid):
        url = self.url + '/api/accessories/{}'.format(aid)
        answer = requests.get(url=url, headers={
                              'Accept': 'application/json'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def CreatesNewAccessoryAndService(self, name, serviceType):
        url = self.url + 'api/accessories/{}/{}'.format(name, serviceType)
        answer = requests.post(
            url=url, headers={'accept': '*/*'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

    def HideShowAccessory(self, aid, value):
        url = self.url + '/api/accessories/{}/hidden/{}'.format(aid, value)
        answer = requests.put(url=url, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

    def SetAccessoryName(self, aid, name):
        url = self.url + '/api/accessories/{}/name/{}'.format(aid, name)
        answer = requests.put(url=url, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

    def SetAccessoryRoom(self, aid, rid):
        url = self.url + '/api/accessories/{}/room/{}'.format(aid, rid)
        answer = requests.put(url=url, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

# Characteristics

    def RemoveCharacteristicTrigger(self, in_a_id, in_c_id, in_value, out_a_id, out_c_id):
        url = self.url + '/api/accessories/{}/characteristics/{}/trigger/{}/{}/{}'.format(
            in_a_id, in_c_id, in_value, out_a_id, out_c_id)
        answer = requests.delete(url=url, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

    def InfoAboutOneCharacteristic(self, aid, cid):
        url = self.url + \
            '/api/accessories/{}/characteristics/{}'.format(aid, cid)
        answer = requests.get(url=url, headers={
                              'Accept': 'application/json'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def listOfAllCharacteristicsOfOneServiceAndAccessory(self, aid, sid):
        url = self.url + \
            '/api/accessories/{}/services/{}/characteristics'.format(aid, sid)
        answer = requests.get(url=url, headers={
                              'Accept': 'application/json'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def SetCharacteristicLink(self, aid, cid):
        url = self.url + \
            '/api/accessories/{}/characteristics/{}/link'.format(aid, cid)
        answer = requests.put(
            url=url, headers={'accept': '*/*'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

    def SetCharacteristicTrigger(self, in_a_id, in_c_id):
        url = self.url + \
            'api/accessories/{}/characteristics/{}/triggers'.format(
                in_a_id, in_c_id)
        answer = requests.put(
            url=url, headers={'accept': '*/*'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

    def SetСharacteristicValue(self, aid,  cid):
        url = self.url + \
            '/api/accessories/{}/characteristics/{}/value'.format(aid, cid)
        answer = requests.put(
            url=url, headers={'accept': '*/*'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()

# Services

    def listOfAllServicesOfAccessory(self, aid):
        url = self.url + '/api/accessories/{}/services'.format(aid)
        answer = requests.get(url=url, headers={
                              'Accept': 'application/json'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def listOfServiceLogicTypes(self, aid, sid):
        url = self.url + \
            '/api/accessories/{}/services/{}/logicTypes'.format(aid, sid)
        answer = requests.get(url=url, headers={
                              'Accept': 'application/json'}, cookies=self.cookie, timeout=0.5)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer
