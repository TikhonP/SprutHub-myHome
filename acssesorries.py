from yeelight import discover_bulbs
from yeelight import Bulb
from miio import PhilipsBulb


class philipsB:
    def __init__(self, ip, token):
        self.ip = str(ip)
        self.token = str(token)

        self.cur_state = None
        self.cur_brightness = None
        self.cur_color_temp = None

    def update(self, state, brightness, color_temp):
        state = str(state)
        brightness = int(brightness)
        color_temp = int(color_temp)

        if state != self.cur_state:
            self.cur_state = state
            if self.cur_state == 'true':
                try:
                    self.bulb.turn_on()
                except Exception:
                    self.bulb = PhilipsBulb(self.ip, self.token)
            else:
                try:
                    self.bulb.turn_off()
                except Exception:
                    self.bulb = PhilipsBulb(self.ip, self.token)
                continue
        elif self.cur_state == 'true':
            if brightness != self.cur_brightness:
                self.cur_brightness = brightness
                try:
                    self.bulb.set_brightness(self.cur_brightness)
                except Exception:
                    self.bulb = PhilipsBulb(self.ip, self.token)
            if color_temp != self.cur_color_temp:
                self.cur_color_temp = color_temp
                try:
                    self.bulb.set_color_temperature(self.cur_color_temp)
                except Exception:
                    self.bulb = PhilipsBulb(self.ip, self.token)
