
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import asyncio

from std_msgs.msg import String
# from examples.helper import get_commandline
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSparseDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from pymodbus.server import (
    StartAsyncSerialServer,
    StartAsyncTcpServer,
    StartAsyncTlsServer,
    StartAsyncUdpServer,
)
from pymodbus.version import version
import threading
#setup adress 
ADDRESS_WRITE_START = 40001
ADDRESS_READ_START = 40021

class ModbusTCP(Node):
    def __init__(self):
        super().__init__('ModbusTCP')
        print("ok")
        #setup
        self.declare_parameter('host','192.168.1.58')
        self.declare_parameter('port',9898)
        
        self.host = self.get_parameter('host').get_parameter_value().string_value
        self.port = 9898 #self.get_parameter('port').get_parameter_value().string_value
        self.address = (self.host,self.port)
        self.publisher_ = self.create_publisher(String, 'topic', 10)



        datablock = ModbusSequentialDataBlock(ADDRESS_WRITE_START, [0]*100)
        self.store = ModbusSlaveContext(
            di=datablock, co=datablock, hr=datablock, ir=datablock, unit=1
        )
        single = True

        # Build data storage
        self.contexts = ModbusServerContext(slaves=self.store, single=single)

        # ----------------------------------------------------------------------- #
        # initialize the server information
        # ----------------------------------------------------------------------- #
        # If you don't set this or any fields, they are defaulted to empty strings.
        # ----------------------------------------------------------------------- #
        self.ident = ModbusDeviceIdentification(
            info_name={
                "VendorName": "Pymodbus",
                "ProductCode": "PM",
                "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
                "ProductName": "Pymodbus Server",
                "ModelName": "Pymodbus Server",
                "MajorMinorRevision": version.short(),
            }
        )
        
    async def handle_server(self):
        
        try:
            
            task1 = asyncio.create_task(self.run_server())
            task2 = asyncio.create_task(self.get_output())
            await asyncio.gather(task1,task2)
            # self.get_logger().info("runnning server")
            # asyncio.run(self.server)
            
            # while(1):
            #     print("data: ")
            #     self.get_output
        except Exception as ex:
            self.get_logger().info(ex)
    async def get_output(self):
        while(True):
            # print("ok")
            print(self.store.getValues(1,40001,1), self.store.getValues(1,40002,1))
            # value = 
            await asyncio.sleep(0.1)
            

    async def run_server(self):
        server = await StartAsyncTcpServer(
            # host = self.host,
            # port = self.port,
            context=self.contexts,
            identity=self.ident,
            address=self.address,
            # custom_functions= self.handle_request,
            allow_reuse_adress = True,
        )
        await asyncio.sleep(1)
        return server


    # async def updating_task(context):
    #     """Run every so often,

    #     and updates live values of the context. It should be noted
    #     that there is a lrace condition for the update.
    #     """
    #     # _logger.debug("updating the context")
    #     fc_as_hex = 3
    #     slave_id = 0x00
    #     address = 0x10
    #     values = context[slave_id].getValues(fc_as_hex, address, count=5)
    #     values = [v + 1 for v in values]  # increment by 1.
    #     txt = f"new values: {str(values)}"
    #     # _logger.debug(txt)
    #     context[slave_id].setValues(fc_as_hex, address, values)
    #     await asyncio.sleep(1)


    # def setup_updating_server(args):
    #     """Run server setup."""
    #     # The datastores only respond to the addresses that are initialized
    #     # If you initialize a DataBlock to addresses of 0x00 to 0xFF, a request to
    #     # 0x100 will respond with an invalid address exception.
    #     # This is because many devices exhibit this kind of behavior (but not all)

    #     # Continuing, use a sequential block without gaps.
    #     datablock = ModbusSequentialDataBlock(0x00, [17] * 100)
    #     context = ModbusSlaveContext(
    #         di=datablock, co=datablock, hr=datablock, ir=datablock, unit=1
    #     )
    #     args.context = ModbusServerContext(slaves=context, single=True)
    #     return setup_server(args)


    # async def run_updating_server(args):
    #     """Start updater task and async server."""
    #     asyncio.create_task(updating_task(args.context))
    #     await run_async_server(args)


    def start_server(self):
        self.server = self.run_server()
        # asyncio.run(self.handle_server)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.handle_server())
    def stop_server(self):
        self.server.server_close()
        self.server.shutdown()
    def handle_request(self):
        print("ok")
def main(args=None):
    
    rclpy.init(args=args)
    
    ModbusNode = ModbusTCP()
    
    rclpy.spin(ModbusNode)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ModbusNode.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()