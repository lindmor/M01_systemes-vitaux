import smbus
from  helpers import *

bus = smbus.SMBus(1)

BOXES = 0x38
CABLES = 0x3F

bus.write_byte(BOXES, 0x00)
bus.write_byte(CABLES, 0x00)

boxes_status = bus.read_byte_data(BOXES, 0xFF)
print(str(bin(boxes_status)))
