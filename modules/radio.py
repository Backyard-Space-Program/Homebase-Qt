import serial, enum, struct
# from .log import *
from .packet import *

def checksum(string): # taken from https://en.wikipedia.org/wiki/NMEA_0183
    """
    c = 0
    for i in string:
        if isinstance(i, str):
            c ^= ord(i)
        else:
            c ^= i
    return c
    """
    crc = 0xffff
    for i in range(len(string)):
        if isinstance(string, str):
            crc ^= ord(string[i]) << 8
        else:
            crc ^= string[i] << 8
        for ii in range(0, 8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xffff

class RadioTypes(enum.Enum):
    FLIGHT_TELEM = 0
    FLIGHT_ABORT = 1
    FLIGHT_STAGE = 2
    FLIGHT_LAUNCH = 3

class Recipient(enum.Enum):
    BROADCAST = 0
    PAD1 = 1
    GROUND = 2
    ROCKET1 = 3
    ROCKET2 = 4
    OTHER = 5

radio_enabled = False
radio_serial = None

def radio_is_closed():
    return radio_serial == None

def radio_is_open():
    return radio_serial != None

def radio_open_serial(port):
    logger.info("Opening radio port " + port)
    if radio_serial == None:
        radio_serial = serial.Serial(port=port, baudrate=9600)
    else:
        logger.error("Tried opening serial while radio is already open")
        return None

def radio_close_serial():
    if radio_serial == None:
        logger.error("Tried closing serial while radio is closed")
        return None
    logger.info("Closing radio serial")
    radio_serial.close()
    radio_serial = None

def radio_change_port(port):
    if radio_serial == None:
        logger.error("Tried changing port while radio is closed")
        return None
    logger.info("Changing radio port from " + radio_serial.port + " to " + port)
    radio_serial.port = port

def radio_change_baud(baud):
    if radio_serial == None:
        logger.error("Tried changing baud rate while radio is closed")
        return None
    logger.info("Changing radio baud from " + str(radio_serial.baudrate) + " to " + str(baud))
    radio_serial.baudrate = baud

def radio_timeout(timeout):
    if radio_serial == None:
        logger.error("Tried changing timeout while radio is closed")
        return None
    logger.info(f"Changing radio timeout to {timeout} s")
    radio_serial.timeout = timeout

def radio_recv_raw():
    if radio_serial == None:
        logger.error("Tried reading from radio while radio is closed")
        return None
    return radio_serial.readline()

def radio_send_raw(*args):
    if radio_serial == None:
        logger.error("Tried sending to radio while radio is closed")
        return None
    for i in args:
        radio_serial.write(bytes(i, "UTF-8"))
    radio_serial.flush() # :flushed:
    
def radio_send_packet(type_, *args, broadcast = False, recipient = None, spacer = b""):
    to_send = b""
    for i in args:
        if isinstance(i, str):
            to_send += i.encode() + spacer
        else:
            to_send += i + spacer

    if not broadcast and not recipient:
        return False

    packet = Packet(Recipient.GROUND, recipient, type_, to_send)
    radio_send_raw(packet.encode())
    return True

def radio_recv_packet():
    return Packet().decode(radio_recv_raw())
