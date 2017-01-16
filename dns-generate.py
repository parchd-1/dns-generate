#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from os.path import basename, realpath, join

conf_file = "/etc/dns-generate/domains.json"

# defaults
ttl = 300

# Templates
nameserver = ".{domain}::{ns}"
arecord = "={domain}:{ip4}:{ttl}"
mx = "@{domain}:{ip4}:{distance}:{ttl}"
alias = "+{alias}:{ip4}:{ttl}"
spf = "'{domain}:v=spf1 a ~all:{ttl}"
dkim = "'{selector}._domainkey.{domain}:v=DKIM1; k=rsa; p={key}:{ttl}"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():

    with open(conf_file) as fd:
        config = json.load(fd)

    for domain in config:
        dconf = config[domain]
        output = []

        # nameservers
        for ns in dconf['nameservers']:
            output.append(nameserver.format(domain=domain, ns=ns))

        # A record
        output.append(arecord.format(domain=domain, ip4=dconf['ip4'], ttl=ttl))

        # Aliases
        for subd in dconf['aliases']:
            output.append(alias.format(alias=subd, ip4=dconf['ip4'], ttl=ttl))

        # Mail
        prio = 10
        output.append(mx.format(domain=domain, ip4=dconf['ip4'], distance=prio, ttl=ttl))
        output.append(spf.format(domain=domain, ttl=ttl))
        for keyfile in dconf['DKIM']:
            try:
                selector = basename(realpath(keyfile))[:14]
                with open(keyfile) as keyfd:
                    key = "".join([l.strip() for l in keyfd.readlines()[1:-1]])
                output.append(dkim.format(selector=selector, domain=domain, key=key, ttl=ttl))
            except Exception as e:
                eprint(e)

        with open(join(sys.argv[1], "{domain}.txt".format(domain=domain)), "w") as outfile:
            for l in output:
                outfile.write(l+"\n")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print(f"Usage: {argv[0]} output_dir")
