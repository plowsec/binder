#!/usr/bin/python
import argparse,sys

class Main:

    def __init__(self, quiet = False):

        self.quiet = quiet

    def execute(self):
        """Here, we parse the commandline options and react according to them"""

        parser = argparse.ArgumentParser(description="A simple binder, which will merge two Windows binaries together")

        parser.add_argument("binary1", help="path to binary1")
        parser.add_argument("binary2", help="path to binary2")

        parser.add_argument("-o", "--output", metavar="OUTPOUT FILENAME", default="output.exe", help="name of output binary", dest="output")
        parser.add_argument("-i", "--icon", metavar="ICON", help="path to desired icon to output binary", dest="icon", default="")

        options = parser.parse_args()
        print (options.binary1)
        print (options.binary2)
        print(options.output)
        print(options.icon)


if __name__ == "__main__":
    main = Main()
    main.execute()
