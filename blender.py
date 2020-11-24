import bpy
import random
import math
import mathutils
import time
import os
funcDict ={
    "|cameraPan": "blend.cameraPan(%s)",
    "|import": "blend.importer(%s)",
    "|ObjData": "blend.dataRetrieve(%s)",
    "|ObjTrans": "blend.objTransform(%s)",
    "|SaveAs": "blend.fileSaverAs(%s)",
    "|Save": "blend.fileSaver(%s)"

}


class Blender:
    def __init__(self):
        self.fileCurrency = open("FILE_BLEND.data","r")
        self.log = self.fileCurrency.read()
        self.imgPath = open("IMG_PATH.data","r").read()
        self.displayPath = ""
    def fileOpener(self):
        bpy.ops.wm.save_mainfile()
        logLst = self.log.split("|")
        print(logLst)
        for logItem in logLst:
            print(logItem)
            if "filepath" in logItem:
                filepath = logItem
        filep = filepath.split("??")
        bpy.ops.wm.open_mainfile(filepath = filep[1])

    def fileStatus(self,i,name = "temp.blend"):
        if i == 1:
            fileStat = open("BLEND_SAVE.data","w")
            fileStat.write("(%s)"%name)
        elif i == 2:
            fileStat = open("BLEND_SAVE.data","a")
            fileStat2 = open("BLEND_SAVE.data","r")
            data = fileStat2.read()
            if data[len(data)-1] != "*":

                fileStat.write("*")

    def fileSaverAs(self,lst):
        self.fileOpener()
        bpy.ops.wm.save_as_mainfile(filepath = lst[0])
        self.displayPath = lst[0]
        self.fileStatus(1,lst[0])

    def fileSaver(self,lst):
        self.fileOpener()
        fileStat2 = open("BLEND_SAVE.data","r")
        filePath = fileStat2.read().strip("()*")
        bpy.ops.wm.save_as_mainfile(filepath = filePath)
        self.fileStatus(1,filePath)

    def renderer(self):
        bpy.context.scene.render.filepath = self.imgPath + "\\render"
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, layer='', scene='')


    def cameraPan(self,lst):
        self.fileOpener()
        bpy.ops.object.select_all(action='DESELECT')
        lst2 = []
        for ob in bpy.data.objects:
            ob.select_set(False)
            if "camera" in ob.name.lower():
                lst2.append(ob)
        lst2[0].select_set(True)
        bpy.context.window.scene.transform_orientation_slots[0].type = 'LOCAL'
        cube = bpy.data.objects["Camera"]
        z =  ((cube.location[2])**2)**0.5
        print(lst)
        vec = mathutils.Vector((-z*float(lst[0])/1500, z*float(lst[1])/1500, -float(lst[2])/40))
        inv = cube.matrix_world.copy()
        inv.invert()
        # vec aligned to local axis in Blender 2.8+
        # https://blender.stackexchange.com/questions/26852/python-move-object-on-local-axis
        vec_rot = vec @ inv
        cube.location = cube.location + vec_rot
        print(inv)
        self.renderer()
        file2 = open("ob_DATA.data","w")
        for ob in bpy.data.objects:
            file2.write(ob.name+"\n")
        self.fileStatus(2)
        bpy.ops.wm.save_mainfile()


    def importer(self,lst):
        fileCurrency = open("FILE_BLEND.data","w")
        bpy.ops.wm.open_mainfile(filepath = lst[0])
        os.chdir(self.imgPath)
        os.system("del temp.blend")
        bpy.ops.wm.save_as_mainfile(filepath = self.imgPath+"\\temp.blend")
        bpy.context.scene.render.filepath = self.imgPath + "\\render"
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, layer='', scene='')
        file2 = open("ob_DATA.data","w")
        for ob in bpy.data.objects:
            file2.write(ob.name+"\n")

        fileCurrency.write("filepath??"+self.imgPath+"\\temp.blend"+"|")
        fileCurrency.write(lst[0])
        fileCurrency.close()
        self.fileStatus(1,lst[0])

    def dataRetrieve(self,lst):
        self.fileOpener()
        bpy.ops.object.select_all(action='DESELECT')
        RL = bpy.data.objects[lst[0]].rotation_euler[0:4]
        RL = list(RL)
        for r in range(len(RL)):
            RL[r] = str(round(math.degrees(RL[r]),3))
        TL = bpy.data.objects[lst[0]].location[0:4]
        SL = bpy.data.objects[lst[0]].scale[0:4]
        TL = list(map(lambda x: str(round(x,3)),TL))
        SL = list(map(lambda x: str(round(x,3)),SL))
        bpy.data.objects[lst[0]].show_bounds = True
        dataFile = open("ob_TRANS.data","w")
        dataFile.write("#".join(TL+RL+SL))
        self.fileStatus(2)
    def objTransform(self,lst):
        self.fileOpener()
        print(lst)
        ObjCor = ["xT","yT","zT","xR","yR","zR","xS","yS","zS"]
        obj = bpy.data.objects[lst[0]]
        ind = ObjCor.index(lst[1])
        print(ind)
        if ind//3 == 0:
            obj.location[ind%3] = float(lst[2])
        elif ind//3 == 1:
            obj.rotation_euler[ind%3] = float(lst[2])
        else:
            obj.scale[ind%3] = float(lst[2])
        self.renderer()
        self.fileStatus(2)
        bpy.ops.wm.save_mainfile()



blend = Blender()
file1 = open("DT_PIPIN.data","r")
# fileCurrency.seek(0)

str2 = file1.read()
lst = str2.split("#")

print(lst[1:])
exec(funcDict[lst[0]] % str(lst[1:]))


