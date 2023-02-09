#!/usr/bin/env python3
"""Pymodbus Aynchronous Client Example.

An example of a single threaded synchronous client.

usage: client_async.py [-h] [--comm {tcp,udp,serial,tls}]
                       [--framer {ascii,binary,rtu,socket,tls}]
                       [--log {critical,error,warning,info,debug}]
                       [--port PORT]
options:
  -h, --help            show this help message and exit
  --comm {tcp,udp,serial,tls}
                        "serial", "tcp", "udp" or "tls"
  --framer {ascii,binary,rtu,socket,tls}
                        "ascii", "binary", "rtu", "socket" or "tls"
  --log {critical,error,warning,info,debug}
                        "critical", "error", "warning", "info" or "debug"
  --port PORT           the port to use

The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""
import rclpy
from rclpy.node import Node
import asyncio
import logging
import os
import random as rd
# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from pymodbus.client import (
    AsyncModbusSerialClient,
    AsyncModbusTcpClient,
    AsyncModbusTlsClient,
    AsyncModbusUdpClient,
)


_logger = logging.getLogger()

class ModbusClient(Node):
    def __init__(self):
        super().__init__('ModbusClient')
        
        #setup
        self.declare_parameter('host','192.168.1.58')
        self.declare_parameter('port','9898')
        self.host = self.get_parameter('host').get_parameter_value().string_value
        self.port = 9898#self.get_parameter('port').get_parameter_value().string_value
        self.client = self.setup_client()
        
        asyncio.run(self.run_client(),debug=True)
        print("test")
    async def run_client(self):
        # try:
        _logger.info("### Client starting")
        connection = await self.client.connect()
        
        if connection:
            while(True):
                val = rd.randint(0,1)
                result = await self.client.write_coil(40001,val)
                result = await self.client.write_coil(40002,(1-val))
                await asyncio.sleep(0.1)
                # values = []
                # for i in "Hello World":
                #     values.append(ord(i))
                # self.clientwrite_registers(0, values)
        
            
        # except Exception as ex:
        #     print("not connect")
        assert self.client.protocol
        
        await self.client.close()
        
    def setup_client(self):
        client = AsyncModbusTcpClient(
            self.host,
            port=9898,  # on which port
            # Common optional paramers:
            # framer=.framer,
            #    timeout=10,
            #    retries=3,
            #    retry_on_empty=False,
            #    close_comm_on_error=False,
            #    strict=True,
            # TCP setup parameters
            #    source_address=("localhost", 0),
        )
        return client
def main(args=None):
    rclpy.init(args=args)

    ModbusNode = ModbusClient()

    rclpy.spin(ModbusNode)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ModbusNode.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()
