#!/usr/bin/env python3
import urllib.request
import hashlib
import yaml
import argparse
import sys
import logging

def read_yaml_file(yaml_file_path: str) -> dict:
  with open(yaml_file_path, mode="r", encoding="utf-8") as file:
    return yaml.load(file, yaml.SafeLoader)

def write_yaml_file(yaml_file_path: str, obj):
  with open(yaml_file_path, mode="w", encoding="utf-8") as file:
    yaml.dump(obj, file)

class Pkgbuilder:
    def __init__(self, config: dict):
        self.config = config
        self.output = ""

    def configurate(self):
        for person in self.config["people"]:
            self.print_person(person)
        self.print_header()
        self.print_sources()
        self.print_build()
        self.print_package()
        self.print_options()

    def print_options(self):
        opts = []
        for (k,v) in self.config["options"].items():
            if v:
                opts.append(k)
            else:
                opts.append("!" + k)
        self.output += ("options=(%s)\n" % " ".join(opts))

    def print_person(self, person: dict):
        self.output += ("# %s: %s %s <%s>\n" % (
            person["role"], person["surname"], person["name"], person["email"]
        ))

    def print_header(self):
        self.output += ("pkgname=%s\n" % self.config["pkgname"])
        self.output += ("pkgver=%s\n" % self.config["pkgver"])
        self.output += ("pkgrel=%s\n" % self.config["pkgrel"])
        self.output += ("pkgdesc=\'%s\'\n" % self.config["pkgdesc"])
        self.output += ("license=('%s')\n" % self.config["license"])
        self.output += ("arch=(%s)\n" % " ".join(["'%s'" % arch for arch in self.config["arch"]]))
        self.output += ("depends=(%s)\n" % " ".join(["'%s'" % depends for depends in self.config["depends"]]))
        self.output += ("makedepends=(%s)\n" % " ".join(["'%s'" % makedepends for makedepends in self.config["makedepends"]]))
        self.output += ("url='%s'\n" % self.config["url"])

    def print_sources(self):
        self.output += ("_archive='%s'\n" % self.config["archive"])
        self.output += ("source=(\"$pkgname-$pkgver.tar.gz::$_archive/$pkgver.tar.gz\")\n")
        self.output += ("sha256sums=('%s')\n" % self.compute_hash())

    def compute_hash(self):
        link = "%s/%s.tar.gz" % (self.config["archive"], self.config["pkgver"])
        file = "%s.tar.gz" % self.config["pkgver"]
        logging.debug("Downloading '%s' as '%s'" % (link, file))
        urllib.request.urlretrieve(link, file)
        hash = b""
        with open(file, mode="rb") as _in:
            hash = hashlib.sha256(_in.read()).digest()
        return hash.hex()

    def print_build(self):
        self.output += ("build() {\n")
        self.output += ("  cd %s\n" % "$pkgname-$pkgver")
        for line in self.config["build"]:
            self.output += ("  " + line + "\n")
        self.output += ("}\n")

    def print_package(self):
        self.output += ("package() {\n")
        self.output += ("  cd %s\n" % "$pkgname-$pkgver")
        for line in self.config["package"]:
            self.output += ("  " + line + "\n")
        self.output += ("}\n")

def main_cli():
    cli = argparse.ArgumentParser(description="Declarative PKGBUILD automatic generation")
    cli.add_argument("-V", "--version", type=str, default=None, help="override Version field from CLI")
    cli.add_argument("-v", "--verbose", action='store_true', default=False, help="Enables verbose log")
    cli.add_argument("-o", "--output", default="PKGBUILD", help="Output path")
    will = cli.parse_args(sys.argv[1:])
    if will.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    config = read_yaml_file('pkgbuild.yaml')
    if will.version is not None:
        config['pkgver'] = will.version
    pkgbuild = Pkgbuilder(config)
    pkgbuild.configurate()

    with open(will.output, mode="w", encoding="utf-8") as out:
        out.write(pkgbuild.output)

if __name__ == "__main__":
    main_cli()
