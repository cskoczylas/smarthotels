import json, socket, struct
from typing import Any, Dict, Union


class TPLinkSmartHomeProtocol:
    """
    Implementation of the TP-Link Smart Home Protocol
    from Gadget Reactor's pyHS100 - Python Library to
    control TP Link Switch
    https://github.com/GadgetReactor/pyHS100

    Encrpytion/Decryption methods

    which are licensed under the Apache License, Version 2.0
    http://www.apache.org/licenses/LICENSE-2.0
    """
    INITIALIZATION_VECTOR = 171
    DEFAULT_PORT = 9999
    DEFAULT_TIMEOUT = 5

    @staticmethod
    def query(host: str,
              request: Union[str, Dict],
              port: int = DEFAULT_PORT) -> Any:
        """
        Request information from a TP-Link SmartHome Device and return the
        response.

        :param str host: host name or ip address of the device
        :param int port: port on the device (default: 9999)
        :param request: command to send to the device (can be either dict or
        json string)
        :return:
        """
        if isinstance(request, dict):
            request = json.dumps(request)

        timeout = TPLinkSmartHomeProtocol.DEFAULT_TIMEOUT
        try:
            sock = socket.create_connection((host, port), timeout)

            sock.send(TPLinkSmartHomeProtocol.encrypt(request))

            buffer = bytes()
            # Some devices send responses with a length header of 0 and
            # terminate with a zero size chunk. Others send the length and
            # will hang if we attempt to read more data.
            length = -1
            while True:
                chunk = sock.recv(4096)
                if length == -1:
                    length = struct.unpack(">I", chunk[0:4])[0]
                buffer += chunk
                if (length > 0 and len(buffer) >= length + 4) or not chunk:
                    break

        finally:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                # OSX raises OSError when shutdown() gets called on a closed
                # socket. We ignore it here as the data has already been read
                # into the buffer at this point.
                pass
            finally:
                sock.close()

        response = TPLinkSmartHomeProtocol.decrypt(buffer[4:])

        return json.loads(response)

    @staticmethod
    def encrypt(request: str) -> bytearray:
        """
        Encrypt a request for a TP-Link Smart Home Device.

        :param request: plaintext request data
        :return: ciphertext request
        """
        key = TPLinkSmartHomeProtocol.INITIALIZATION_VECTOR
        buffer = bytearray(struct.pack(">I", len(request)))

        for char in request:
            cipher = key ^ ord(char)
            key = cipher
            buffer.append(cipher)

        return buffer

    @staticmethod
    def decrypt(ciphertext: bytes) -> str:
        """
        Decrypt a response of a TP-Link Smart Home Device.

        :param ciphertext: encrypted response data
        :return: plaintext response
        """
        key = TPLinkSmartHomeProtocol.INITIALIZATION_VECTOR
        buffer = []

        ciphertext_str = ciphertext.decode('latin-1')

        for char in ciphertext_str:
            plain = key ^ ord(char)
            key = ord(char)
            buffer.append(chr(plain))

        plaintext = ''.join(buffer)

        return plaintext
