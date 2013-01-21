from coreproxy import ProxyCrawl, Proxy


class HttpProxy(Proxy):
    p = ProxyCrawl()

    def __init__(self):
        self.proxys = self.p.get_proxy()

    def validates(self, proxys):
        http_proxys = {}
        for p in proxys:
            status, time = self.validate(p)
            if status == 1:
                http_proxys[p] = time





