from .radio import Recipient, RadioTypes
import time
from loguru import logger

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

""" # for reference
def radio_send_packet(type_, *args, broadcast = False, recipient = None):
    # 37 is % in ascii
    if not broadcast:
        packet = bytearray((37, 37, 37, Recipient.GROUND.value, ord(":"), recipient.value, ord(";")))
    else:
        packet = bytearray((37, 37, 37, Recipient.GROUND.value, ord(":"), Recipient.BROADCAST.value, ord(";")))

    # combine args
    data = b""
    for i in args:
        if isinstance(i, str):
            data += bytes(i, "UTF-8")
        elif isinstance(i, int):
            data += i.to_bytes(2, "little")
        elif isinstance(i, float): # hopefully never use this
            data += struct.pack("f", i)
        else:
            data += i

    packet.append(type_.value)
    packet.append(ord(";"))
    packet += len(data).to_bytes(2, "little")
    packet.append(ord(";"))
    packet += data
    packet.append(ord(";"))

    packet += checksum(data).to_bytes(2, "little") + b"%%%"

    return bytes(packet)
    # radio_send_raw(packet)
    # return True

def radio_recv_packet():
    packet = radio_recv_raw()

    if not (packet.startswith(b"%%%") and packet.endswith(b"%%%")):
        logger.warning("Recieved potental false-rx")
        with open("false-rx.log", "ab") as f:
            f.write(packet + b"\n")

    # parse args

"""

class Packet():
    def __init__(self, sender, recipient, type_, data, checksum = b"", time_ = 0):
        self.sender = sender
        self.recipient = recipient
        self.type = type_
        self.data = data
        self.checksum = checksum
        self.time = time_
        self.broadcast = True if self.recipient == Recipient.GROUND else False

    def encode(self):
        # 37 is % in ascii
        if not self.broadcast:
            packet = bytearray((37, 37, 37, Recipient.GROUND.value, ord(":"), self.recipient.value, ord(";")))
        else:
            packet = bytearray((37, 37, 37, Recipient.GROUND.value, ord(":"), Recipient.BROADCAST.value, ord(";")))
        
        packet.append(self.type.value)
        packet.append(ord(";"))
        packet += len(self.data).to_bytes(2, "little")
        packet.append(ord(";"))
        packet += self.data
        packet.append(ord(";"))

        packet += checksum(self.data).to_bytes(2, "little") + b"%%%"

        self.time = int(time.time())

        return bytes(packet)

    def decode(self, string, log_false_rx = True):
        if isinstance(string, str):
            string = string.encode()

        if not (string.startswith(b"%%%") and string.endswith(b"%%%")):
            logger.warning("Recieved potential false-rx")
            if log_errors:
                with open("errors.log", "ab") as f:
                    f.write(str(datetime.fromtimestamp(int(time.time()))).encode() + b": " + string + b"\n")
            return

        if not self.check_format(string):
            logger.warning("Recieved bad format packet")
            if log_errors:
                with open("errors.log", "ab") as f:
                    f.write(str(datetime.fromtimestamp(int(time.time()))).encode() + b": " + string + b"\n")
            return

        if not self.check_checksum(string):
            logger.warning("Recieved bad checksum in packet")
            if log_errors:
                with open("errors.log", "ab") as f:
                    f.write(str(datetime.fromtimestamp(int(time.time()))).encode() + b": " + string + b"\n")
            return

        # all checks done

        self.sender = Recipient(string[3])
        self.recipient = Recipient(string[5])
        self.type = RadioTypes(string[7])
        datalength = int.from_bytes(string[9:11], "little")
        self.data = string[12:datalength + 12]
        self.checksum = checksum(data)
        self.time = int(time.time())

    def check_format(self, string):
        if isinstance(string, str):
            string = string.encode()

        if string[4] != ord(":"):
            return False
        if string[6] != ord(";") or string[8] != ord(";") or string[11] != ord(";"):
            return False
        
        return True

    def check_checksum(self, string):
        if isinstance(string, str):
            string = string.encode()

        datalength = int.from_bytes(string[9:11], "little")
        if datalength > 1024:
            return False

        data = string[12:datalength + 12]
        old_checksum = int.from_bytes(string[datalength + 13:datalength + 15], "little")
        
        return checksum(data) == old_checksum
