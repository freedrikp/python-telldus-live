import abc

class BaseMixin(abc.ABC):
    _name_id_map = None
    _mixin = None
    _session = None

    def __init__(self, session):
        self._session = session

    def get_unit_id(self, name):
        if not self._name_id_map:
            self._name_id_map = {}
            units = self._session.communicate('%ss/list' % self._mixin)
            for unit in units[self._mixin]:
                self._name_id_map[unit['name']] = unit['id']

        return self._name_id_map[name]

    def _action(self, action, unit):
        unit_id = unit if unit.isdigit() else self.get_unit_id(unit)
        return self._session.communicate('%s/%s' % (self._mixin, action), params={'id': unit_id})

class DeviceMixin(BaseMixin):
    _mixin = 'device'

    def turn_on_device(self, device):
        return self._action('turnOn', device)

    def turn_off_device(self, device):
        return self._action('turnOff', device)

class SensorMixin(BaseMixin):
    _mixin = 'sensor'

    def sensor_info(self, sensor):
        return self._action('info', sensor)
