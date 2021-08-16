TITLE
KPA101 Python Data Logger

DESCRIPTION
provided by pythonnet library, using a .NET interface layer to communicate with the KPA101, 
the python file will extract the signal and PSD location data from the KPA101 and write it out to a csv file

REQUIRED
- KPA101, PDP90A PSD or other PSD, kpadatalogger.py file
- csv, datetime, pythonnet, schedule, time, sys, pathlib libraries
- source files, in the kpadatalogger.py file, there is a reference to a directory where these folders are also located, 
so ensure the sources folder has the same files as this path. They are from the 64bit kinesis app, they are important dll files. 
My path is "C:\Program Files\Thorlabs\Kinesis_2" that is where I have the required files, I also have them in the ./sources folder.

HOW TO USE
1. plug PSD into KPA101, power KPA101 on, and plug into your PC
2. in kpadatalogger.py file, ensure sys.path.append(r"C:\Program Files\Thorlabs\Kinesis_2") has the source files from the sources folder
3. also in the file, have the KPA101 serial number filled out at serial=str(<kap101 serial number>)
4. choose your desired polling interval and sampling interval
	4a. polling interval is how often the KPA101 is polled and sampling interval is how often the mose recent poll is sampled
	4b. max poll and sample rates are unknown, 1kHz poll and sample rate is the max that has been tested
5. with everything connected, run kpadatalogger.py in the terminal
6. press ctrl+c in terminal to stop, the output data csv will be in the output folder


NOTES
- having the correct sources files with the dlls is very important, thorlabs has the different Kinesis app versions which all have the 
source files in C:\Program Files (x86)\Thorlabs\Kinesis or C:\Program Files\Thorlabs\Kinesis. 
copy all the files in this folder to the sources folder to have on hand. 
and have the sys.path.append("") point to C:\Program Files (x86)\Thorlabs\Kinesis or C:\Program Files\Thorlabs\Kinesis
- the kpadatalogger.py is commented to describe the code

CREDITS
all credit for this goes to ppakotze-sarao on github, I originally used his repository and file "Thorlabs kpa101 with pdp90a logger.ipynb"
and changed it for my use case. 
