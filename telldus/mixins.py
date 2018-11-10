import abc

class BaseMixin(abc.ABC):
    _name_id_map_data = None
    _mixin = None
    _session = None

    def __init__(self, session):
        self._session = session

    @property
    def _name_id_map(self):
        if not self._name_id_map_data:
            self._name_id_map_data = {}
            units = self._session.communicate('%ss/list' % self._mixin)
            for unit in units[self._mixin]:
                self._name_id_map_data[unit['name']] = unit['id']
        return self._name_id_map_data

    @property
    def unit_ids(self):
        for unit_id in self._name_id_map.values():
            yield unit_id

    def get_unit_id(self, name):
        return self._name_id_map[name]

    def _action(self, action, unit, params={}):
        unit_id = unit if unit.isdigit() else self.get_unit_id(unit)
        _params = {'id': unit_id}
        _params.update(params)
        return self._session.communicate('%s/%s' % (self._mixin, action), params=_params)

class DeviceMixin(BaseMixin):
    _mixin = 'device'

    def turn_on_device(self, device):
        return self._action('turnOn', device)

    def turn_off_device(self, device):
        return self._action('turnOff', device)

class SensorMixin(BaseMixin):
    _mixin = 'sensor'

    def sensor_info(self, sensor, include_unit=False):
        params = {}
        if include_unit:
            params = {'includeUnit':'1'}
        return self._action('info', sensor, params)

INSTALLED_MIXINS = {
    'device': DeviceMixin,
    'sensor': SensorMixin
}
