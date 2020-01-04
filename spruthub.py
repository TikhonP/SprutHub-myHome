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
        url = self.url + '/api/server/login/'.format(username)
        data = password
        answer = requests.post(url=url, data=data, headers={
                               'Accept': '*/*', 'Content-Type': '*/*'})
        answer.raise_for_status()

        self.token = answer.headers['Set-Cookie'].split(sep=';')[
            0].split(sep='=')[1]
        self.cookie = {'token': self.token}

        return self.token

    def getAllLinks(self):
        url = self.url + '/api/server/links'
        answer = requests.get(
            url=url, headers={'accept': 'application/json'}, cookies=self.cookie)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def GetServerLogs(self, lastTime, count):
        url = self.url + '/api/server/{}/{}'.format(str(lastTime), str(count))
        answer = requests.get(
            url=url, headers={'accept': 'application/json'}, cookies=self.cookie)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def GetAllServersVariables(self):
        url = self.url + '/api/server/vars'
        answer = requests.get(
            url=url, headers={'accept': 'application/json'}, cookies=self.cookie)
        answer.raise_for_status()
        answer = json.loads(answer.text)

        return answer

    def GetServserVersion(self):
        url = self.url + '/api/server/version'
        answer = requests.get(
            url=url, headers={'accept': 'text/plain'}, cookies=self.cookie)
        answer.raise_for_status()

        return answer

    def GetThreadpoolStats(self, extended, query):
        url = self.url + \
            '/api/server/pools/{}/{}'.format(str(extended), str(query))
        answer = requests.get(
            url=url, headers={'accept': 'text/plain'}, cookies=self.cookie)
        answer.raise_for_status()

        return answer

    def RestartServer(self):
        url = self.url + '/api/server/restart'
        answer = requests.post(
            url=url, headers={'Accept': '*/*'}, cookies=self.cookie)
        answer.raise_for_status()

    def register(self, username, password):
        """Register api

        :param username: string, username or email
        :param password: string, password
        """
        url = self.url + '/api/server/register/'.format(username)
        data = password
        answer = requests.post(url=url, data=data, headers={
                               'Accept': '*/*', 'Content-Type': '*/*'})
        answer.raise_for_status()

    def SetVariable(self, key, value):
        url = self.url + '/api/server/vars/{}/{}'.format(key, value)
        answer = requests.put(
            url=url, headers={'accept': '*/*'}, cookies=self.cookie)
        answer.raise_for_status()

    
