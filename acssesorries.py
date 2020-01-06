from yeelight import Bulb
from miio import PhilipsBulb


class philipsB:
    def __init__(self, ip, token):
        self.ip = str(ip)
        self.token = str(token)

        self.bulb = PhilipsBulb(self.ip, self.token)

        self.cur_state = None
        self.cur_brightness = None
        self.cur_color_temp = None

    def update(self, state, brightness, color_temp):
        state = str(state)
        brightness = int(brightness)
        color_temp = int(color_temp)
        if brightness == 0:
            brightness = 1
            print('brightness set ', brightness)
        if brightness == 100:
            brightness = 99
            print('brightness set ', brightness)
        if color_temp == 0:
            color_temp = 1
            print('color_temp set ', color_temp)
        if color_temp == 100:
            color_temp = 99
            print('color_temp set ', color_temp)

        if state != self.cur_state:
            self.cur_state = state
            if self.cur_state == 'true':
                try:
                    self.bulb.on()
                except Exception as e:
                    self.bulb = PhilipsBulb(self.ip, self.token)
                    self.bulb.on()
                    print(e)
            else:
                try:
                    self.bulb.off()
                except Exception as e:
                    self.bulb = PhilipsBulb(self.ip, self.token)
                    self.bulb.off()
                    print(e)
        elif self.cur_state == 'true':
            if brightness != self.cur_brightness:
                self.cur_brightness = brightness
                try:
                    self.bulb.set_brightness(self.cur_brightness)
                except Exception as e:
                    self.bulb = PhilipsBulb(self.ip, self.token)
                    self.bulb.set_brightness(self.cur_brightness)
                    print(e)
            if color_temp != self.cur_color_temp:
                self.cur_color_temp = color_temp
                try:
                    self.bulb.set_color_temperature(self.cur_color_temp)
                except Exception as e:
                    self.bulb = PhilipsBulb(self.ip, self.token)
                    self.bulb.set_color_temperature(self.cur_color_temp)
                    print(e)


class yeelightB:
    def __init__(self, ip, port):
        self.ip = str(ip)
        self.port = int(port)

        self.bulb = Bulb(self.ip, self.port)

        self.cur_state = None
        self.cur_hsv = None
        self.cur_color_temp = None

    def update(self, state, hsv, color_temp):
        state = str(state)
        hsv = tuple(hsv)
        color_temp = int(color_temp)

        if state != self.cur_state:
            self.cur_state = state
            if self.cur_state == 'true':
                try:
                    self.bulb.turn_on()
                except Exception as e:
                    if e == 'Bulb closed the connection.':
                        self.bulb = Bulb(self.ip, self.port)
                        self.bulb.turn_on()
                    else:
                        print(e)
            else:
                try:
                    self.bulb.turn_off()
                except Exception as e:
                    if e == 'Bulb closed the connection.':
                        self.bulb = Bulb(self.ip, self.port)
                        self.bulb.turn_off()
                    else:
                        print(e)
        elif self.cur_state == 'true':
            if hsv != self.cur_hsv:
                self.cur_hsv = hsv
                try:
                    self.bulb.set_hsv(hsv[0], hsv[1], hsv[2])
                except Exception as e:
                    if e == 'Bulb closed the connection.':
                        self.bulb = Bulb(self.ip, self.port)
                        self.bulb.set_hsv(hsv[0], hsv[1], hsv[2])
                    else:
                        print(e)
            if color_temp != self.cur_color_temp:
                self.cur_color_temp = color_temp
                try:
                    self.bulb.set_color_temp(self.cur_color_temp)
                except Exception as e:
                    if e == 'Bulb closed the connection.':
                        self.bulb = Bulb(self.ip, self.port)
                        self.bulb.set_color_temp(self.cur_color_temp)
                    else:
                        print(e)
