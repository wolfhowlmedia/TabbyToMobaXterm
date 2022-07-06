# TabbyToMobaXterm

## What is it?
It's a crude script that appends your Tabby sessions to your existing MobaXTerm ones

## Requirements
- Python3.7+
- pyyaml

## Usage: 
1) Copy Tabby's config file to the folder containing the script (location found under Settings->Config file->Show config file) and name it tabby.yaml
2) Export all your current sessions from MobaXterm, and save it in the same folder as 'MobaXterm Sessions.mxtsessions'
3) Make a backup of the file
4) Install python's dependancies (either by python -m pip install pyyaml or load it from the requirements.txt file)
5) Run the script
6) Import the newly generated text.mxtsessions file. WARNING! Importing the file will erase your previous section. Make sure you do the step #3 first! (or third)
7) ???
8) Profit!
