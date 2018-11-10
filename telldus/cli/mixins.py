import abc
from datetime import datetime

class BaseCliMixin(abc.ABC):
    _command = None

    def __init__(self, subparsers):
        parser = subparsers.add_parser(self._command)
        self._add_arguments(parser)
        parser.set_defaults(func=self.run)

    @abc.abstractmethod
    def _add_arguments(self, subparsers):
        pass

class DeviceCliMixin(BaseCliMixin):
    _command = 'device'

    def _add_arguments(self, parser):
        parser.add_argument('--on', type=str, nargs='+', help="Devices to turn on.")
        parser.add_argument('--off', type=str, nargs='+', help="Devices to turn off.")

    def run(self, session, args):
        if args.on:
            for device in args.on:
                session.pprint(session.device.turn_on_device(device))

        if args.off:
            for device in args.off:
                session.pprint(session.device.turn_off_device(device))

class SensorCliMixin(BaseCliMixin):
    _command = 'sensor'
    __battery_indicator = {
        253: "OK",
        254: "Unknown",
        255: "Low"
    }

    def _add_arguments(self, parser):
        parser.add_argument('--info', type=str, nargs='+', help="Sensor to collect info from.")

    def __print_battery_status(self, battery):
        print("Battery: %s" % self.__battery_indicator.get(battery, "%s%%" % battery))

    def __print_data_entry(self, entry):
        print("Name: %s" % entry["name"])
        print("Last updated: %s" % datetime.fromtimestamp(entry["lastUpdated"]))
        print("Value: %s%s" % (entry["value"], entry.get("unit", "")))
        if "max" in entry and "min" in entry:
            print("Max: %s%s at %s" % (entry["max"], entry.get("unit", ""), datetime.fromtimestamp(entry["maxTime"])))
            print("Min: %s%s at %s" % (entry["min"], entry.get("unit", ""), datetime.fromtimestamp(entry["minTime"])))

    def __print_sensor_info(self, info):
        print("-"*50)
        print("Client: %s" % info["clientName"])
        self.__print_battery_status(int(info["battery"]))
        for entry in info["data"]:
            self.__print_data_entry(entry)
        print("-"*50)

    def run(self, session, args):
        if args.info:
            for sensor in args.info:
                self.__print_sensor_info(session.sensor.sensor_info(sensor, include_unit=True))


INSTALLED_MIXINS = [
    DeviceCliMixin,
    SensorCliMixin
]
