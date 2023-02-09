# import time
# from pyModbusTCP.client import ModbusClient

# # init
# c = ModbusClient(host='192.168.1.58', port=12345, auto_open=True, debug=False)
# bit = True

# # main loop
# while True:
    

#     # read 4 bits in modbus address 0 to 3
#     print('read bits')
#     print('---------\n')
#     bits = c.read_coils(0, 5)
#     if bits:
#         print('coils #0 to 3: %s' % bits)
#     else:
#         print('coils #0 to 3: unable to read')

#     # toggle
#     bit = not bit
#     # sleep 2s before next polling
#     print('')
#     time.sleep(2)
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
import asyncio
import logging
import os

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
# from examples.helper import get_commandline
from pymodbus.client import (
    AsyncModbusSerialClient,
    AsyncModbusTcpClient,
    AsyncModbusTlsClient,
    AsyncModbusUdpClient,
)


_logger = logging.getLogger()


def setup_async_client():
    """Run client setup."""
    
    _logger.info("### Create client object")

    client = AsyncModbusTcpClient(
        '192.168.1.58',
        port=9898,  # on which port
        # Common optional paramers:
        # framer=args.framer,
        #    timeout=10,
        #    retries=3,
        #    retry_on_empty=False,
        #    close_comm_on_error=False,
        #    strict=True,
        # TCP setup parameters
        #    source_address=("localhost", 0),
    )
    
    return client


async def run_async_client(client, modbus_calls=None):
    """Run sync client."""
    _logger.info("### Client starting")
    await client.connect()
    
    assert client.protocol
    
    if modbus_calls:
        await modbus_calls(client)
    await client.close()
    _logger.info("### End of Program")


if __name__ == "__main__":
    # cmd_args = get_commandline(
    #     server=False,
    #     description="Run asynchronous client.",
    # )
    # cmd_args.framer = None
    # cmd_args.comm = 'tcp'
    # cmd_args.host = "192.168.1.58"
    # cmd_args.port = 9898
    testclient = setup_async_client()
    asyncio.run(run_async_client(testclient), debug=True)