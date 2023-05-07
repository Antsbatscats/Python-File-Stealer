# Python-Malware-File-Stealer
This is a File Staler written in Python. As of the 07/05/23, this is undetectable in virus total. This is malware designed as powerful file stealer to steal all the files from a victims computer and then forward the files to a discord WebHook.

## Functionality:

This is software designed to steal all of the files from a victims computer. 
It does this by: 
* Blacking out the victims screen. 
* Blocking keyboard inputs into the program so it cant be stopped directly via the commandline when running. 
* All of the open applications are hidden both from view, but also from the taskbar so they cant be re-opened.
* Recursively searching through all of the drives and directories found on a computer
* Finding files which meet the criteria to be sent
* Sending all the files which meet the criteria to a Discord webhook

All you need to do to have this program work is place your discord webhook in the WEBHOOK_URL section:
- `WEBHOOK_URL = "place your discord webhook here"`

## How to install use the porgram:
1. Clone the github repository
2. Unzip the downloded zip file to a location of your choice
3. Go to the place of which you unziped the zip file and open the stealer8.py file in a python IDE of your choice. 
4. Go to the WEBHOOK_URL variable and in the code, and place your discord webhook where it says to - `WEBHOOK_URL = 'place your discord webhook here'`
5. Send this to anyone who has python installed and when they run this, this will immediately start sending files. 

Extra Steps
As this is a python file - this will only run if the victim has python installed, so to get round this, this can be complied into  executable file. 
1. First install pyinstaller in cmd (command prompt) - `pip install pyinstaller`
2. open cmd in the file which you  have the python script and use the command - `pyinstaller --onefile stealer8.py`
3. i would recommend you renaming the executable file after this as 'stealer8.exe' is quite a giveaway. 
4. You can send this file to anyone, and they will be able to run this even if they don't have python installed. 

## Warnings:
As of the 07/05/23 this cannot be detected in virus total when its just as a python script, to look see [here](https://www.virustotal.com/gui/file/718ebf7598cf50b3910119bfce0b51a590eb61530609b55d2baa9d02b922aca2?nocache=1).
However, when this script is compliled into an executable file, six detections are made in virus total (note that I have changed the name of the executable file) to see, look [here](https://www.virustotal.com/gui/file/1c4fde56cc39bbd0d15dec6e91fc973ac686f0e194d7a9de34041d00ff7200e2). 

## If You have been Affected: 

If you have been affected by this software, there should be no worry of infection, this software has no persistence capablities as of now, and can't be used to remotely acess or controll a victim computer in its current form. 

## Notes: 
This program has an in built blacklisting function, if you wish to blacklist more directories, just add them in. If you don't want any blacklisting, just delete the contecnts of the blacklisting variable and replace it with two apostrophes. This program also has a set list of accepted file extensions, so if you want more file types to be sent just add them in as you wish. 

## Find a Bug? 

if you have found a bug in the code, use the issue tab above. If you would like to submit a PR with a fix, reference the issue you are fixing. If you are looking for new features, use the suggestionn function in the issues tab above to do so. 

## LICENCE: 

This project has been Licenced under the GNU Affero General Public License v3.0. It can be found at [LICENCE](https://github.com/Antsbatscats/Python-Malware-File-Stealer/blob/main/LICENSE)

## Legality:

This was a  program designed for education purposes only. I do not accept any responsiblity for the usage of the software for illegal or malicious purposes, nor do I condone it.  
