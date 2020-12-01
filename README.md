# 15-112-TP-Rendorium

 This project has been developed as a Term project for one of my courses at CMU (15-112). Rendorium is a 3D rendering and editing program based on Blender.
 
 The program has been tested to work in python 3.7.7; other versions of python have not been tested.
 
 
## Installation guide
### Downloading/Cloning
there are two ways in which you can get the files to be correctly stored on your device 
#### Method 1
download the files from github.com as .zip, then go to blender folder in the reporistory on github.com and download blender.exe separately. Once blender.exe is downloaded. Extract the .zip file downloaded previously, navigate to the blender folder in the extracted directory and replace the blender.exe file in the extract directory (which should be a very small file) with the one downloaded separately (which should be a large file). Do not rename blender or assets folder.

#### Method 2
if you have access to git bash, type in the following command:
`git lfs install` if you dont have git lfs already
`git lfs clone https://github.com/Diram-Tabaa/15-112-TP-Rendorium.git` to clone the reporistory

### Running the program
first of all, download run the following commands in the shell of your IDE (Pyzo or pyCharm preferred) to download the required libraries

`pip install PyQt5` \n
`pip install ffmpeg-python`


after those libraries are installed, run `main.py` to start the program.

**DO NOT DISPLACE `blender` FOLDER**

