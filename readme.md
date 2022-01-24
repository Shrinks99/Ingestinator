# Ingestinator

Ingestinator is my personal VFX pipeline tool for ingesting folders containing frame sequences that have been pulled and downloaded to a local folder.  It creates a shot folder based on a template, moves the folders containing frames into the `/plate` directory (which along with `/comp` needs to exist in the template), and renders a reference MOV based on a template Nuke script titled "slatemachine" which is also included in this repo.  Ingestinator expects plates to exist as a single sequence per folder in the specified ingest directory, other than that it's decently customizable and _reasonably_ robust.  It may not work for you without some modification to suit your show or local environment.

### Dependencies
Ingestinator requires the following software:

- Python 3.10
- Nuke

### Setup

The beginning of the script is tagged as "User Settings Land", these are the things you're expected to change to suit your project / environment!

```python

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

```

Be sure to set up slatemachine.nk with your slating script of choice, note that the Nuke script runs `nukestartup.py` and certain values in there may have to be changed based on what you want to pass along to your slating script.

You may have to change the directory structure that glob looks at to generate the `currentsequence` variable to suit your dailies vendor's plate pull directory structure in `ingest.py`.

### Running the tool

CD to the program's directory on your drive (path will likely be different for you):

```bash
cd /path/to/ingestinator
```

Run the tool!

```bash
python ingest.py
```