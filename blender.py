#Diram Tabaa
#Andrew ID: dtabaa
#TP3 Date: 12/1/2020
#blender.py

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
    "|Save": "blend.fileSaver(%s)",
    "|Anim": "blend.renderAnimation(%s)",
    "|UpdMat": "blend.materialUpdater(%s)",
    "|addObj": "blend.addObj(%s)",
    "|delObj": "blend.objDelete(%s)",
    "|rigidBake":"blend.rigidBake(%s)",
    "|rendSettings":"blend.rendSettings(%s)",
    "|RigidData": "blend.rigidData(%s)"

}


class Blender:
    def __init__(self):
        self.fileCurrency = open("FILE_BLEND.data","r")
        self.log = self.fileCurrency.read()
        self.imgPath = open("IMG_PATH.data","r").read()
        self.displayPath = ""
        self.materialDict = {
            "diffuse": {"subsurface": 0,
                        "transmission": 0,
                        "metallic": 0,
                        "emission": 0
            },
            "metallic": {"subsurface": 0,
                        "transmission": 0,
                        "metallic": 1,
                        "emission": 0
            },
            "subsurface":{"subsurface": 1,
                        "transmission": 0,
                        "metallic": 0,
                        "emission": 0
            },
            "glossy":{ "subsurface": 0,
                        "transmission": 0,
                        "metallic": 0,
                        "emission": 0
            },
            "glass":{"subsurface": 0,
                        "transmission": 1,
                        "metallic": 0,
                        "emission": 0
            },
            "emission":{"subsurface": 0,
                        "transmission": 0,
                        "metallic": 0,
                        "emission": 1
            }
        }
    def dataOut(self):
        file2 = open("ob_DATA.data","w")
        for ob in bpy.data.objects:
            file2.write(ob.name+"\n")

    def rendSettings(self,lst):
        self.fileOpener()
        if lst[0] == "Eevee":
            engine = "BLENDER_EEVEE"
            bpy.context.scene.render.engine = engine
            bpy.context.scene.eevee.taa_render_samples = int(lst[2])
        else:
            engine = "CYCLES"
            bpy.context.scene.render.engine = engine
            bpy.context.scene.cycles.device = lst[1]
            bpy.context.scene.cycles.samples = int(lst[2])
        self.fileStatus(2)
        self.renderer()
        bpy.ops.wm.save_mainfile()

    def rigidData(self,lst):
        self.fileOpener()

        bpy.ops.object.select_all(action='DESELECT')
        r1 = bpy.data.objects[lst[0]].rigid_body

        if r1 != None:
            r1 = bpy.data.objects[lst[0]].rigid_body.enabled
            r2 = bpy.data.objects[lst[0]].rigid_body.type
            r3 = bpy.data.objects[lst[0]].rigid_body.mass
        else:
            r2 = None
            r3 = None
        lst2 = [r1,r2,r3]
        lst2 = list(map(lambda x: str(x),lst2))
        fileRigid = open("rigid_DATA.data","w")
        fileRigid.write("#".join(lst2))
        fileRigid.close()
        self.fileStatus(2)







    def objDelete(self,lst):
        self.fileOpener()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[lst[0]].select_set(True)
        bpy.ops.object.delete(use_global=False, confirm=False)
        self.dataOut()
        self.fileStatus(2)
        self.renderer()
        bpy.ops.wm.save_mainfile()

    def rigidBake(self,lst):
        self.fileOpener()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[lst[0]].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[lst[0]]
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.type = lst[2].upper()
        bpy.context.object.rigid_body.collision_shape = 'MESH'
        bpy.context.object.rigid_body.mass = float(lst[1])
        bpy.ops.ptcache.free_bake_all()
        bpy.ops.ptcache.bake_all(bake=True)
        self.fileStatus(2)
        self.renderer()
        bpy.ops.wm.save_mainfile()




    def addObj(self,lst):
        self.fileOpener()
        objList = [["cube","monkey"],["cone","cylinder"],["uv_sphere"],["torus"]]
        bpy.ops.object.select_all(action='DESELECT')
        lst2 = []
        for ob in bpy.data.objects:
            ob.select_set(False)
            if "camera" in ob.name.lower():
                lst2.append(ob)
        lst2[0].select_set(True)
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                area.spaces.active.region_3d.view_perspective = 'CAMERA'
        z =  ((lst2[0].location[2])**2)**0.5
        vec = mathutils.Vector((0,0,-0.7*z))
        inv = lst2[0].matrix_world.copy()
        vec_rot = inv @ vec
        loco = "location=vec_rot"
        adder = "bpy.ops.mesh.primitive"
        for list in objList:
            if lst[0] in list:
                if objList[0] == list:
                    exec(adder+"_"+lst[0]+"_add(size= 0.5,"+loco+")")
                elif objList[1] == list:
                    exec(adder+"_"+lst[0]+"_add(vertices = 64,"+loco+",scale=(0.5, 0.5, 0.5))")
                elif objList[2] == list:
                    exec(adder+"_"+lst[0]+"_add(radius = 0.5,segments =64,ring_count = 32,"+loco+")")
                    bpy.ops.object.shade_smooth()

                else:
                    exec(adder+"_"+lst[0]+"_add(major_segments=64, minor_segments=24,"+loco+")")
                    bpy.ops.object.shade_smooth()


        file2 = open("ob_DATA.data","w")
        for ob in bpy.data.objects:
            file2.write(ob.name+"\n")

        self.fileStatus(2)
        self.renderer()
        bpy.ops.wm.save_mainfile()



    def materialUpdater(self,lst):
        self.fileOpener()
        bpy.ops.object.select_all(action='DESELECT')
        ob = bpy.data.objects[lst[0]]
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
        #https://blender.stackexchange.com/a/23434
        mat = bpy.data.materials.get("RendoriumMaterial"+lst[0])
        if mat == None:
            mat = bpy.data.materials.new(name="RendoriumMaterial"+lst[0])

        if ob.data.materials:

            ob.data.materials[0] = mat
        else:
            ob.data.materials.append(mat)
        materials = ob.material_slots.keys()
        index = len(materials)-1

        bpy.context.object.active_material_index = index
        col = lst[4].strip("()").split(",")
        col = tuple(list(map(lambda x: float(x)/255,col)))


        valuesDict = self.materialDict[lst[1]]
        bpy.data.materials["RendoriumMaterial"+lst[0]].use_nodes = True
        bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[1].default_value = valuesDict["subsurface"]
        bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[4].default_value = valuesDict["metallic"]
        bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[15].default_value = valuesDict["transmission"]
        bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[0].default_value = col
        if valuesDict["subsurface"]:
            bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[3].default_value = col
        else:
            bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[3].default_value = (0,0,0,0)
        if valuesDict["emission"]:
            bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[17].default_value = col
        else:
            bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0,0,0,0)
        bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[14].default_value = float(lst[3])
        bpy.data.materials["RendoriumMaterial"+lst[0]].node_tree.nodes["Principled BSDF"].inputs[7].default_value = float(lst[2])/1000







        self.fileStatus(2)
        bpy.ops.wm.save_mainfile()
        self.renderer()
    def fileOpener(self):
        bpy.ops.wm.save_mainfile()
        logLst = self.log.split("|")
        for logItem in logLst:
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

    def renderAnimation(self,lst):
        self.fileOpener()
        bpy.context.scene.render.filepath = self.imgPath + "\\anim.mkv"
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        lst = list(map(lambda x : int(x), lst))
        bpy.context.scene.frame_start = lst[0]
        bpy.context.scene.frame_step = lst[2]
        bpy.context.scene.frame_end = lst[1]
        bpy.ops.render.render(animation=True, use_viewport=False, layer='', scene='')
        er = open("signalANIMR","w")
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
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                area.spaces.active.region_3d.view_perspective = 'CAMERA'

       # ^^ https://blender.stackexchange.com/q/15008
        camera = bpy.data.objects[lst2[0].name]
        z =  ((camera.location[2])**2)**0.5
        vec = mathutils.Vector((-z*float(lst[0])/1500, z*float(lst[1])/1500, -float(lst[2])/40))
        inv = camera.matrix_world.copy()
        inv.invert()
        # vec aligned to local axis in Blender 2.8+
        # https://blender.stackexchange.com/questions/26852/python-move-object-on-local-axis
        vec_rot = vec @ inv
        camera.location = camera.location + vec_rot
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


        file3 = open("rend_DATA.data","w")
        rendEng = bpy.context.scene.render.engine
        if rendEng =="CYCLES":
            rendDev = bpy.context.scene.cycles.device
            rendSamp = bpy.context.scene.cycles.samples
        else:
            rendDev = False
            rendSamp = bpy.context.scene.eevee.taa_render_samples
        rendLst = [rendEng,rendDev,rendSamp]
        rendLst = list(map(lambda x: str(x),rendLst))
        file3.write("#".join(rendLst))


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
        dataFile.close()
        self.fileStatus(2)
    def objTransform(self,lst):
        self.fileOpener()
        ObjCor = ["xT","yT","zT","xR","yR","zR","xS","yS","zS"]
        obj = bpy.data.objects[lst[0]]
        ind = ObjCor.index(lst[1])
        if ind//3 == 0:
            obj.location[ind%3] = float(lst[2])
        elif ind//3 == 1:
            obj.rotation_euler[ind%3] = math.radians(float(lst[2]))
        else:
            if lst[3] == "False":
                obj.scale[ind%3] = float(lst[2])
            else:
                s1 = obj.scale[0]
                s2 = obj.scale[1]
                s3 = obj.scale[2]
                sAnon = obj.scale[ind%3]
                scaleLst = [s1,s2,s3]
                for s in range(len(scaleLst)):
                    if s == ind%3:
                        obj.scale[s] = float(lst[2])
                    else:
                        obj.scale[s] = scaleLst[s]*(float(lst[2])/sAnon)


        self.renderer()
        self.fileStatus(2)
        bpy.ops.wm.save_mainfile()



blend = Blender()
file1 = open("DT_PIPIN.data","r")


str2 = file1.read()
lstComm = str2.split("|")
lstComm = lstComm[1:]


for command in lstComm:
    command = "|"+command
    lst = command.split("#")
    exec(funcDict[lst[0]] % str(lst[1:]))


