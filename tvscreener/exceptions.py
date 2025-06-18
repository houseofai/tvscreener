class MalformedRequestException(Exception):
    def __init__(self, code, response_msg, url, payload):
        message = f"Error: {code}: {response_msg}\n"
        message += f"Request: {url}\n"
        message += "Payload:\n"
        message += payload
        super().__init__(message)
