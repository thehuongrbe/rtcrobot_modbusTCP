import time
from pyModbusTCP.client import ModbusClient
import random
# init
c = ModbusClient(host='192.168.1.58', port=12345, auto_open=True, debug=False)


# main loop
while True:
    # write 4 bits in modbus address 0 to 3

    print('write bits')
    print('----------\n')
    for ad in range(5):
        bit = random.randint(0, 1)
        is_ok = c.write_single_coil(ad, bit)
        if is_ok:
            print('coil #%s: write to %s' % (ad, bit))
        else:
            print('coil #%s: unable to write %s' % (ad, bit))
        time.sleep(0.5)

    print('')
    time.sleep(1)

  