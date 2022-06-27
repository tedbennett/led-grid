# This example demonstrates a UART periperhal.

import bluetooth
import random
import struct
import time
from struct import unpack
from ble_advertising import advertising_payload, decode_name, decode_field
from json import loads

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
_COLORS_CHARACTERISTIC = (
    bluetooth.UUID("6e400003-b5a3-f393-e0a9-e50e24dcca9e"),
    _FLAG_WRITE_NO_RESPONSE | _FLAG_NOTIFY,
)
_CONFIG_CHARACTERISTIC = (
    bluetooth.UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e"),
    _FLAG_WRITE_NO_RESPONSE | _FLAG_NOTIFY,
)
_UART_SERVICE = (
    _UART_UUID,
    (_CONFIG_CHARACTERISTIC, _COLORS_CHARACTERISTIC),
)


class LEDGridPeripheral:
    def __init__(self, name, on_colors_change, on_config_change):
        self._ble = bluetooth.BLE()
        self._ble.config(gap_name=name)
        self._ble.active(True)
        self._ble.irq(self._irq)
        (
            (self._handle_colors, self._handle_config),
        ) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._ble.gatts_set_buffer(self._handle_config, 1024)
        self._ble.gatts_set_buffer(self._handle_colors, 1024)
        self._connections = set()
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()
        self.on_colors_change = on_colors_change
        self.on_config_change = on_config_change

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_config:
                print("Received Config")
                self.on_config_change(self._parse_config(value))
            elif value_handle == self._handle_colors:
                print("Received Colors")
                self.on_colors_change(self._parse_colors(value))

    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def _parse_config(self, data):
        config = loads(data.decode())
        return config["delay"]

    def _parse_colors(self, data):
        decoded = data.decode()

        def hex_to_rgb(hex):
            return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))

        colors = [hex_to_rgb(decoded[i : i + 6]) for i in range(0, len(decoded), 6)]
        return colors
