# README #

### What is this repository for? ###

* A binder is a program that merges two binaries together. It's a way to "infect" binaries, as one can hide a malicious executable inside a "legit" one (overly used in the wild, so this is educational purpose only. Obviously.)
* Can also be used as a way to keep a "foothold" on a system after a successfull hack
* This repository contains the actual code of the binder, but also a user-friendly wrapper around the binder, so one can binds two binaries without the previous required steps. Which were :
 Rename target binary to "target.txt"
 Rename payload binary to "payload.txt"
 Rename icon to "target_icon.ico"
 Compile binder.c
 Remove temp files

* A significative + side of using this wrapper : cross-compilation from a Linux system (ArchLinux)

###Important###
* The script bind.py was made with cross-compilation from Archlinux to Windows in mind. May need some minor tweaking for other systems (I am not sorry)

### Dependencies ###
* mingw-w64-gcc (Archlinux)
* required includes to compile binder.c are in src/includes (you can trust theses headers, I am a nice guy, as well as the guys that made these headers available to me (probably) (Qt))

###Goals###

* Inconspicuous (complete clean up once the execution has completed)
* AV Evasion
* Easily configurable
* Clean code (remember, we are doing art)


### How do I get set up? ###

* sudo pacman -S mingw-w64-gcc
* Download bind.py and src folder
* Positive thinking

### Contribution guidelines ###

* Code review
* Harsch critics (Ask yourself : what insults would Linus Torvalds yell to the guy who made this "utter crap" (me))
