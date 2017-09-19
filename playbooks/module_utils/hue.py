import os
from ansible.module_utils.urls import open_url


class HueLight(object):
    def __init__(self, module_):
        self.module_ = module_

        self.ip = module_.params.get('ip')
        self.user = module_.params.get('user')
        self.light_id = module_.params.get('light')

        if not self.ip:
            if os.environ.get('HUE_IP'):
                self.ip = os.environ['HUE_IP']
        if not self.user:
            if os.environ.get('HUE_USER'):
                self.user = os.environ['HUE_USER']

        self.base_url = 'http://{ip}/api/{user}/lights'.format(
            ip=self.ip,
            user=self.user,
        )

    @staticmethod
    def argument_spec():
        return dict(
            ip=dict(
                type='str',
                required=False,
            ),
            user=dict(
                type='str',
                required=False,
            ),
            light=dict(
                type='str',
                required=True,
            ),
        )

    @staticmethod
    def rgb_to_xy(red, green, blue):
        a = red * 0.664511 + green * 0.154324 + blue * 0.162028
        b = red * 0.283881 + green * 0.668433 + blue * 0.047685
        c = red * 0.000088 + green * 0.072310 + blue * 0.986039

        x = a / (a + b + c)
        y = b / (a + b + c)

        return [round(x, 4), round(y, 4)]

    def _change_light_state(self, data):
        url = '{base_url}/{light}/state'.format(
            base_url=self.base_url,
            light=self.light_id,
        )
        return open_url(url, method='PUT', data=self.module_.jsonify(data))

    def _get_light(self):
        url = '{base_url}/{light}'.format(
            base_url=self.base_url,
            light=self.light_id,
        )
        return open_url(url, method='GET')

    def on(self, bri=None, sat=None, transitiontime=None):
        data = dict(on=True,)
        if bri:
            data['bri'] = bri
        if sat:
            data['sat'] = sat
        if transitiontime:
            data['transitiontime'] = transitiontime

        return self._change_light_state(data)

    def off(self, transitiontime=None):
        data = dict(on=False,)
        if transitiontime:
            data['transitiontime'] = transitiontime

        return self._change_light_state(data)

    def light(self):
        return self._get_light()

    def effect_none(self, bri=None, sat=None, transitiontime=None):
        data = dict(effect='none')
        if bri:
            data['bri'] = bri
        if sat:
            data['sat'] = sat
        if transitiontime:
            data['transitiontime'] = transitiontime

        return self._change_light_state(data)

    def color_xy(self, x, y, bri=None, sat=None, transitiontime=None):
        data = dict(xy=[x, y])
        if bri:
            data['bri'] = bri
        if sat:
            data['sat'] = sat
        if transitiontime:
            data['transitiontime'] = transitiontime

        self.effect_none(bri=bri, sat=sat, transitiontime=0)

        return self._change_light_state(data)

    def color_rgb(self, r, g, b, bri=None, sat=None, transitiontime=None):
        x, y = HueLight.rgb_to_xy(r, g, b)
        return self.color_xy(x, y, bri, sat, transitiontime)

    def colorloop(self, bri=None, sat=None, transitiontime=None):
        data = dict(effect='colorloop')
        if bri:
            data['bri'] = bri
        if sat:
            data['sat'] = sat
        if transitiontime:
            data['transitiontime'] = transitiontime

        return self._change_light_state(data)
