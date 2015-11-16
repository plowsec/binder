# README #

### What is this repository for? ###

* A dropper is a program (malware component) that has been designed to "install" some sort of malware (virus, backdoor, etc.) to a target system. The malware code can be contained within the dropper (single-stage) in such a way as to avoid detection by virus scanners or the dropper may download the malware to the target machine once activated (two stage).
* This project is a possible implementation in artistic C++ of a two-staged dropper

###Goals###

* As fast as possible
* As light as possible (final build should be packed)
* Inconspicuous (complete clean up once the execution has completed)
* AV Evasion
* Easily configurable
* Clean code (remember, we are doing art)


### How do I get set up? ###

* Set your Command and Control config in Constants.h


### Contribution guidelines ###

* Code review
* Other guidelines