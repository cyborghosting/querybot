from collections import namedtuple


Host = namedtuple("Host", ["hostname", "port"])
Server = namedtuple("Server", ["name", "host"])


def parse_host(host: str) -> Host:
    if ":" in host:
        hostname, port = host.split(":")
        return Host(hostname, int(port))
    return Host(host, 27015)
