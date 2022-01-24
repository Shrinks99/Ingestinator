import os
import sys
import shutil
import glob
import fnmatch
import subprocess

# User Setings Land

# Nuke EXE location, adds quotes onto the end as a part of the string
nukepath = "C:/Program Files/Nuke13.1v1/Nuke13.1.exe"

# The location your shots will end up in
shotsfolder = r"C:/example/shotsfolder"

#The location of pulled frames sitting in a folder structure
ingestfolder = r"C:/example/ingestfolder"

# Enter the filename for the project Nuke script that will appear in the working directory.  The shot's show code will be prepended to this string
nukefilename = "_INH_cmp_v001.nk"

# Enter the showcode as well as the amount of characters that appear before the show code
showcode = "SHW_###_###_####"
preshowcode = 0

# File type of the frames to ingest
platefiletype = ".exr"

# File type of the CDL to ingest
colorfiletype = ".cdl"

# Frame padding, MUST be hashtags to work in Nuke
padding = "####"

# Number that gets added to the last frame in the sequence.  If your frame sequences start at 1001 this would be 1000
startframe = 1000



# Program Variable Land

shottemplate = sys.path[0] + "/shottemplate"

showcodelength = len(showcode)

filepaddinglength = len(platefiletype) + len(padding)

# All shots to be ingested located in the ingest folder
ingestdirs = [ name for name in os.listdir(ingestfolder) if os.path.isdir(os.path.join(ingestfolder, name)) ]

# All shots that already exist in the project folder
existingshots = [ name for name in os.listdir(shotsfolder) if os.path.isdir(os.path.join(shotsfolder, name)) ]

# List of showcodes to process, trims filename to showcode length
ingestcodes = []
for x in ingestdirs:
    ingestshowcode = x[preshowcode:showcodelength]
    ingestcodes.append(ingestshowcode)

# For each shot, make a new project folder based on the shottemplate folder, rename Nuke project file
for shotcode in ingestcodes:
    if os.path.exists(shotsfolder + "/" + shotcode) == False:
        shutil.copytree(shottemplate, shotsfolder + "/" + shotcode, dirs_exist_ok=True)
        os.rename(shotsfolder + "/" + shotcode + "/" + "comp/template.nk", shotsfolder + "/" + shotcode + "/comp/" + shotcode + nukefilename)
        # Find and copy plates to the project folder
        for file in ingestdirs:
            if fnmatch.fnmatch(file, shotcode + "*") == True:
                # Returns the path of the current shot's plate directory
                currentplatedir = shotsfolder + "/" + shotcode + "/plate"
                shutil.move(ingestfolder + "/" + file, currentplatedir)
            else:
                pass

        # List of all folders moved into the plate's shot directory
        currentplatedirlist = [ name for name in os.listdir(currentplatedir) if os.path.isdir(os.path.join(currentplatedir, name)) ]

        # Returns a list of paths for every frame in the sequence, uses the first entry of the list to create the Nuke read path, runs Nuke
        for sequence in currentplatedirlist:
            # !!! Glob arbitrary path may require changes if you have a different directory structure !!!
            currentsequence = glob.glob(currentplatedir + "/" + sequence + "/**/*" + platefiletype, recursive=True)
            currentcolorfile  = str(glob.glob(currentplatedir + "/" + sequence + "/**/*" + colorfiletype, recursive=True)[0])
            currentcolorfileclean = currentcolorfile.replace("\\", "/")
            lastframe = str(len(currentsequence) + startframe)
            nukeinput = str(currentsequence[0][:-filepaddinglength] + padding + platefiletype)
            nukeinputclean = nukeinput.replace("\\", "/")
            currentcompdir = shotsfolder + "/" + shotcode + "/comp"
            currentcompdirclean = currentcompdir.replace("\\", "/")
            #print("\"" + nukepath + "\"" + " -ti nukestartup.py " + "\"" + nukeinputclean + "\"" + " \"" + lastframe + "\" " + " \"" + currentcolorfileclean + "\" " + "\"" + currentcompdirclean + "/slatemachine.nk" + "\"")
            subprocess.Popen("\"" + nukepath + "\"" + " -ti nukestartup.py " + "\"" + nukeinputclean + "\"" + " \"" + lastframe + "\" " + " \"" + currentcolorfileclean + "\" " + "\"" + currentcompdirclean + "/slatemachine.nk" + "\"", shell=True).wait()
            print("Finished ingest for: " + sequence)
                #print("WARNING: no plates found for " + file)
    # elif os.path.exists(shotsfolder + "/" + shotcode) == True:
    #     print("WARNING: Folder for " + shotcode + " already exists, skipping")
    else:
        pass

print("Ingest finished!")