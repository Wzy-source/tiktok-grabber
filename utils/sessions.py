import requests

requests.packages.urllib3.disable_warnings()


class Sessions(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('verify', False)
        return super(Sessions, self).request(*args, **kwargs)
