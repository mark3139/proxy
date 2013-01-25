import argparse
import sys

from coreproxy import ProxyCrawl, ProxyValidate


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
                update_progress(i, len(self.proxys))
                if s == 1:
                    self.proxys_en.append((p, t))
            self.write(self.f_proxys_able, self.proxys_en)
        except KeyboardInterrupt:
            self.write(self.f_proxys_able, self.proxys_en)

    def display(self, proxys):
        proxys = sorted(proxys, key=lambda x: int(x[1]))
        print '''\n Proxy(IP:PORT)                         Time\n'''
        for (i, p) in proxys:
            print '{0} \t\t\t {1}ms'.format(i, p)

    def write(self, filename, proxys):
        with open(filename, 'w') as f:
            for p, t in proxys:
                f.write('%s %s\n' % (p, t))


class main():
    @staticmethod
    def set_file_name(args):
        main.proxy = Proxy(args.outfile, args.en_outfile)

    @staticmethod
    def mainproxy():
        main.proxy.crawl()
        print 'Get %s proxys validating...' % len(main.proxy.proxys)
        main.proxy.validate(main.proxy.proxys)
        main.proxy.display(main.proxy.proxys_en)

    @staticmethod
    def display():
        main.proxy.display([line.strip().split() for line in file(main.proxy.f_proxys_able, 'r')])

    @staticmethod
    def validate():
        main.proxy.validate([line.strip().splie() for line in file(main.proxy.f_proxys), 'r'])
        main.proxy.display(main.proxy.proxys_en)


def update_progress(i, total):
    progress = i / float(total)
    sys.stdout.write('\r[{0}] {1}%              validating {2}, total {3}. Press ctrl-c stop validating.'
                     .format('#' * (int(progress * 100) / 10), int(round(progress * 100, 1)), i, total))
    sys.stdout.flush()


def make_parse():
    parser = argparse.ArgumentParser(description='Get enable proxys', prog='Tea Proxy')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-o', '--outfile', default='proxys.txt', metavar='', help='all proxys write to outfile')
    parser.add_argument('-eo', '--en_outfile', default='proxys_able.txt', metavar='', help='en_proxys write to en_outfile')
    group.add_argument('-l', '--list', action='store_const', dest='cmd_handler', const=main.display, help='show proxys')
    group.add_argument('-v', '--validate', action='store_const', dest='cmd_handler', const=main.validate, help='re-validate proxys')
    return parser


if __name__ == '__main__':
    parser = make_parse()
    args = parser.parse_args()
    main.set_file_name(args)
    if args.cmd_handler is None:
        main.mainproxy()
    else:
        args.cmd_handler()
