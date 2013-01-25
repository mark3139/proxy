import argparse
import sys


from coreproxy import ProxyCrawl, ProxyValidate


def update_progress(progress):
    sys.stdout.write('\r[{0}] {1}%'.format('#' * (int(progress * 100) / 10), int(round(progress * 100, 1))))
    sys.stdout.flush()


class Proxy():
    def __init__(self, f, f_en):
        self.proxys = None
        self.proxys_en = []
        self.f_proxys = f
        self.f_proxys_able = f_en

    def crawl(self):
        crawl = ProxyCrawl()
        self.proxys = crawl.get_proxy()
        self.write(self.f_proxys, [(p, 0) for p in self.proxys])

    def validate(self, proxys):
        v = ProxyValidate()
        try:
            for (i, (p, s, t)) in enumerate(v.validates(self.proxys)):
                update_progress(i / float(len(self.proxys)))
                if s == 1:
                    self.proxys_en.append((p, t))
            self.write(self.f_proxys_able, self.proxys_en)
        except KeyboardInterrupt:
            self.write(self.f_proxys_able, self.proxys_en)

    def display(self, proxys):
        proxys = sorted(proxys, key=lambda x: int(x[1]))
        print '''Proxy(IP:PORT)                      Time'''
        for (i, p) in proxys:
            print i, '\t\t\t', p, 'ms'

    def write(self, filename, proxys):
        with open(filename, 'w') as f:
            for p, t in proxys:
                f.write('%s %s\n' % (p, t))


def main(args):
    proxy = Proxy(args.outfile, args.en_outfile)

    def main_proxy():
        proxy.crawl()
        proxy.validate(proxy.proxys)
        proxy.display(proxy.proxys_en)

    def display():
        proxy.display([line.strip().split() for line in file(proxy.f_proxys_able, 'r')])

    def validate():
        proxy.validate([line.strip().splie() for line in file(proxy.f_proxys), 'r'])
        proxy.display(proxy.proxys_en)

    if args.list:
        display()
    elif args.validate:
        validate()
    else:
        main_proxy()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get enable proxys', prog='Tea Proxy')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-o', '--outfile', default='proxys.txt', metavar='', help='all proxys write to outfile')
    parser.add_argument('-eo', '--en_outfile', default='proxys_able.txt', metavar='', help='en_proxys write to en_outfile')
    group.add_argument('-l', '--list', action='store_true', help='show proxys')
    group.add_argument('-v', '--validate', action='store_true', help='re-validate proxys')
    args = parser.parse_args()
    main(args)
