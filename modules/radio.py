import serial, enum
# from .log import *

class radio_types(enum.Enum):
    FLIGHT_TELEM = 0
    FLIGHT_ABORT = 1
    FLIGHT_STAGE = 2
    FLIGHT_LAUNCH = 3

class recipient(enum.Enum):
    LAUNCH = 0
    GROUND = 1
    ROCKET1 = 2
    ROCKET2 = 3
    OTHER = 4

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
    radio_serial.timeout = timeout

def radio_recv():
    return radio_serial.readline()

def radio_send(type_, *args):
    if radio_serial == None:
        logger.error("Tried sending while radio is closed")
        return None
