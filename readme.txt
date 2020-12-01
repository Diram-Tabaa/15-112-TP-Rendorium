Project Name
Rendorium, a 3D rendering and editing program based on Blender

Brief Description
Rendorium alpha is a 3D rendering and editing software that is based on Blender.
Despite being implemented on a pre-existing 3D engine, Rendorium aims to provide its
users with a basic set of implements that can be relevant to people outside the 3D
design circle. Those tools range from an intuitive GUI that can handle 3D navigation of
final-render quality scenes, to a variety of options through which a user can load
templates, modify objects or scenes in such templates or use their own custom templates
in the form of .blend files. The program also serves the users by providing intuitive
export options for still scenes as well as animations. Those export options include but
are not limited to: .png, .jpg, .mkv, .avi, etc. Finally, the user will have the ability to
save the changes he made on his local device, such that when the user launches the
program again and loads his saves, the GUI will be set to the state the user left it when
it was saved. With all such features, users with limited exposure to complex 3D software
packages can gain an insight into the world of 3D design, as well as produce viable
designs themselves.

The program has been tested to work in python 3.7.7; other versions of python have not been tested.

Installation guide
Downloading/Cloning
there are two ways in which you can get the files to be correctly stored on your device

Method 1
download the files from github.com as .zip, then go to blender folder in the reporistory on github.com and download blender.exe separately. Once blender.exe is downloaded. Extract the .zip file downloaded previously, navigate to the blender folder in the extracted directory and replace the blender.exe file in the extract directory (which should be a very small file) with the one downloaded separately (which should be a large file). Do not rename blender or assets folder.

Method 2
if you have access to git bash, type in the following command:

git lfs install (if you dont have git lfs already)
git lfs clone https://github.com/Diram-Tabaa/15-112-TP-Rendorium.git to clone the reporistory
Running the program
first of all, download run the following commands in the shell of your IDE (Pyzo or pyCharm preferred) to download the required libraries

pip install PyQt5

pip install ffmpeg-python

after those libraries are installed, run main.py to start the program.

DO NOT DISPLACE blender FOLDER
