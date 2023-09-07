import base64

class EncodingUtils:

    @staticmethod
    def base64_encode(value_to_encode):
        value_bytes = value_to_encode.encode('utf-8')
        return base64.b64encode(value_bytes).decode('utf-8')