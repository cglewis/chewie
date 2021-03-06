import struct


def hwaddr_to_string(hwaddr):
    return ":".join(["%02x" % x for x in hwaddr])


AUTH_8021X_HEADER_LENGTH = 1 + 1 + 2


class Auth8021x:
    """basically a EAPOL packet"""
    def __init__(self, version, packet_type, data):
        self.version = version
        self.packet_type = packet_type
        self.data = data

    @classmethod
    def parse(cls, packed_message):
        """construct an Auth8021x from a packed_message
        Args:
            packed_message (bytes):
        Returns:
            Auth8021x
        """
        version, packet_type, length = struct.unpack("!BBH",
                                                     packed_message[:AUTH_8021X_HEADER_LENGTH])
        data = packed_message[AUTH_8021X_HEADER_LENGTH:AUTH_8021X_HEADER_LENGTH+length]
        return cls(version, packet_type, data)

    def pack(self):
        """Pack up the EAPOL packet to bytes.
        Returns:
            bytes
        """
        header = struct.pack("!BBH", self.version, self.packet_type, len(self.data))
        return header + self.data

    def __repr__(self):
        return "%s(version=%s, packet_type=%s, data=%s)" % \
            (self.__class__.__name__, self.version, self.packet_type, self.data)

    def __str__(self):
        return "%s<packet_type=%d, data=%s>" % \
            (self.__class__.__name__, self.packet_type, self.data)
