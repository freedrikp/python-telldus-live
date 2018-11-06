import argparse

from configuration import JSONTelldusConfiguraton
from session import TelldusSession

def parse_args():
    parser = argparse.ArgumentParser("Telldus REST API CLI")
    parser.add_argument('-f', '--file', type=str, default="telldus.json", help="Configuration file.")
    subparsers = parser.add_subparsers()
    add_device_args(subparsers)
    add_sensor_args(subparsers)
    return parser.parse_args()

def add_device_args(subparsers):
    parser = subparsers.add_parser('device')
    parser.add_argument('--on', type=str, nargs='+', help="Devices to turn on.")
    parser.add_argument('--off', type=str, nargs='+', help="Devices to turn off.")
    parser.set_defaults(func=run_device_cli)

def run_device_cli(session, args):
    if args.on:
        for device in args.on:
            print(session.device.turn_on_device(device))

    if args.off:
        for device in args.off:
            print(session.device.turn_off_device(device))

def add_sensor_args(subparsers):
    parser = subparsers.add_parser('sensor')
    parser.add_argument('--info', type=str, nargs='+', help="Sensor to collect info from.")
    parser.set_defaults(func=run_sensor_cli)

def run_sensor_cli(session, args):
    if args.info:
        for sensor in args.info:
            print(session.sensor.sensor_info(sensor))

def run_cli():
    args = parse_args()
    session = TelldusSession(JSONTelldusConfiguraton(args.file))
    args.func(session, args)
