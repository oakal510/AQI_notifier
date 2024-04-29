import telnyx


class Notifier:
    def __init__(self, api_key, from_number):
        telnyx.api_key = api_key
        self.from_number = from_number

    def send_sms(self, to, message):
        return telnyx.Message.create(from_=self.from_number, to=to, text=message)
