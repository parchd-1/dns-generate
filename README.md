# dns-generate
Generate tinydns configurations from json

## Usage

1. Create /etc/dns-generate/domains.json which contains entries for your domains.
2. Run python dns-generate.py output_directory

See the example configuration provided for what the syntax should look like.

## Currently working

* nameservers
* anames
* mxrecord
* cnames
* spf and dkim

So far only IPv4 has been worked on (although the example file shows what IPv6
support might look like). Anything that also works with IPv6 only does so by
coincidence and as a result of my lack of knowledge and understanding of IP and
DNS.

## Things to note

* If the keyfiles specified for DKIM do not exist, an error message will be
printed by the exit status will indicate success. This is by design, as
a result of how I am using the software.
* My needs are pretty simple, at least
at the moment, and therefore this configurations possible with this software
are also simple, at least at the moment.

## Contributing

Suggestions and contributions welcome
