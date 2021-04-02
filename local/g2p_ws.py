#!/usr/bin/env python3

import clam.common.client
import clam.common.data
import clam.common.status
import random
import sys
import os
import time


if (len(sys.argv)<5):
    print("You should add four arguments: username and password for the G2P webservice, a folder path for auxiliary files and a folder for storing server data")
    sys.exit(-1)


#create client, connect to server.
#the latter two arguments are required for authenticated webservices, they can be omitted otherwise
#if you use SSL (https) and SSL verification fails, you can pass a verify= parameter with the path to your certificate of certificate authority bundle
#if the server only accepts HTTP Basic Authentication, add a basicauth=True parameter
clamclient = clam.common.client.CLAMClient(
    "https://webservices.cls.ru.nl/g2pservice", sys.argv[1], sys.argv[2], basicauth=True)


#The following applies to older CLAM clients only (< v3)! If your webservice uses custom formats, and you use an older client, you need to import or redefine them here (each format is a Python class), and register them with the client:
#class SomeCustomFormat(clam.common.data.CLAMMetaData):
#    mimetype = 'text/plain'
#clamclient.register_custom_formats([ SomeCustomFormat ])



#Set a project name (it is recommended to include a sufficiently random naming component here, to allow for concurrent uses of the same client)
project = "homed" + str(random.getrandbits(64))

#Now we call the webservice and create the project (in this and subsequent methods of clamclient, exceptions will be raised on errors).

clamclient.create(project)

#Get project status and specification

data = clamclient.get(project)


#Add one or more input files according to a specific input template. 
# The following input templates are defined,
#each may allow for extra parameters to be specified, this is done in the form of Python
#  keyword arguments to the addinputfile() method, (parameterid=value)
#inputtemplate="wordlist" #Word List (PlainTextFormat)
#	The following parameters may be specified for this input template:
#		encoding=...  #(StaticParameter) -   Encoding -  The character encoding of the file
directory = sys.argv[3]
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        clamclient.addinputfile(project, data.inputtemplate(
            "wordlist"), directory+filename)


#Start project execution with custom parameters. Parameters are specified as Python keyword arguments to the start() method (parameterid=value)
#language=...  #(ChoiceParameter) -   Language -  Language of the G2P
#	valid choices for this parameter: 
#	nld - dutch
#	eng - english
#n=...  #(IntegerParameter) -   n -  nbest

data = clamclient.start(project)


#Always check for parameter errors! Don't just assume everything went well! Use startsafe() instead of start
#to simply raise exceptions on parameter errors.
if data.errors:
    print("An error occured: " + data.errormsg, file=sys.stderr)
    for parametergroup, paramlist in data.parameters:
        for parameter in paramlist:
            if parameter.error:
                print("Error in parameter " + parameter.id + ": " + parameter.error, file=sys.stderr)
    clamclient.delete(project) #delete our project (remember, it was temporary, otherwise clients would leave a mess)
    sys.exit(1)

#If everything went well, the system is now running, we simply wait until it is done and retrieve the status in the meantime
while data.status != clam.common.status.DONE:
    time.sleep(5) #wait 5 seconds before polling status
    data = clamclient.get(project) #get status again
    print("\tRunning: " + str(data.completion) + '% -- ' + data.statusmessage, file=sys.stderr)

#Iterate over output files
for outputfile in data.output:
    try:
        outputfile.loadmetadata() #metadata contains information on output template
    except:
        continue

    outputtemplate = outputfile.metadata.provenance.outputtemplate_id
    
	#You can check this value against the following predefined output templates, and determine desired behaviour based on the output template:
	#if outputtemplate == "dict": #Dictionary (PlainTextFormat)
	#if outputtemplate == "errorlog": #Log file with (standard) error output (PlainTextFormat)
	#Download the remote file

    localfilename = os.path.basename(str(outputfile))
    outputfile.copy(localfilename)
    os.rename(localfilename, str(sys.argv[4])+localfilename)

    
	#..or iterate over its (textual) contents one line at a time:
    #for line in outputfile.readlines():
    #    print(line)

#delete the project (otherwise it would remain on server and clients would leave a mess)

clamclient.delete(project)
