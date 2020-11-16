import bpy
import random
import math
import mathutils
import time
funcDict ={
    "|test": "blend.Test(%s)",
    "|import": "blend.importer(%s)"

}


class Blender:
    def __init__(self):
        self.fileCurrency = open("CRN.log","r")
        self.log = self.fileCurrency.read()
    def Test(self,lst):
        dict = {
            "sphere": 'bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32,radius=%f, enter_editmode=False, location=(%f, %f, %f))',
            "cylinder": 'bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=%f, depth= %f, enter_editmode=False, location=(%f, %f, %f))',
            "cube": 'bpy.ops.mesh.primitive_cube_add(size=%f, enter_editmode=False, location=(%f, %f, %f))'

            }
        # bpy.context.scene.cycles.device = 'GPU'

        bpy.ops.wm.save_mainfile()
        # bpy.ops.wm.open_mainfile(filepath = "experiment.blend")


        # bpy.ops.object.delete(use_global=False, confirm=False)
        logLst = self.log.split("|")
        print(logLst)
        for logItem in logLst:
            print(logItem)
            if "filepath" in logItem:
                filepath = logItem
        filep = filepath.split("??")
        bpy.ops.wm.open_mainfile(filepath = filep[1])
        bpy.ops.object.select_all(action='DESELECT')
        lst2 = []
        for ob in bpy.data.objects:
            ob.select_set(False)
            if "camera" in ob.name.lower():
                lst2.append(ob)
        print(lst2)

        lst2[0].select_set(True)
        a = float(lst[3])*(2*3.142/360)
        b = float(lst[4])*(2*3.142/360)
        c = float(lst[5])*(2*3.142/360)
        bpy.context.window.scene.transform_orientation_slots[0].type = 'LOCAL'
        # bpy.ops.transform.translate(value=(-float(lst[6])/100, 0, float(lst[7])/100), orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        # bpy.ops.transform.translate(value=(-float(lst[8])/100, float(lst[8])/100, -float(lst[8])/100), orient_type='VIEW', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='VIEW', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        cube = bpy.data.objects["Camera"]
        z =  ((cube.location[2])**2)**0.5
        print(lst)
        vec = mathutils.Vector((-z*float(lst[6])/1500, z*float(lst[7])/1500, -float(lst[8])/40))
        inv = cube.matrix_world.copy()
        inv.invert()
        # vec aligned to local axis in Blender 2.8+
        # https://blender.stackexchange.com/questions/26852/python-move-object-on-local-axis
        vec_rot = vec @ inv
        cube.location = cube.location + vec_rot
        print(inv)
        # cube.rotation = cube.rotation + (inv @ mathutils.vector(a,0,0))
        # bpy.ops.transform.rotate(value=a, orient_axis='Z',orient_type='LOCAL')
        bpy.ops.transform.rotate(value=b, orient_axis='X',orient_type='LOCAL')
        bpy.ops.transform.rotate(value=c, orient_axis='Y',orient_type='LOCAL')


        # bpy.ops.object.light_add(type='AREA', radius=6, location=(-3, 2, 0))
        # bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.0262398, 0.0252707, 0.0207026, 1)



        # for s in lst[:2]:
        #
        #     if s == "cylinder":
        #         exec(dict[s] %(random.random(),random.random(),random.randint(-2,2),random.randint(-2,2),random.randint(-2,2)))
        #     else:
        #         exec(dict[s] % (random.random(),random.randint(-2,2),random.randint(-2,2),random.randint(-2,2)))
        #     if s == "sphere":
        #         bpy.ops.object.shade_smooth()
        bpy.context.scene.render.filepath = "d:\\Uni Material\\Fall 2020\\Intro to CS\\Code\\project\\render"
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, layer='', scene='')
        file2 = open("ob_DATA.data","w")
        for ob in bpy.data.objects:
            file2.write(ob.name+"\n")
        bpy.ops.wm.save_mainfile()
        # file2.close()
        # file1.close()
    def importer(self,lst):
        fileCurrency = open("CRN.log","w")
        bpy.ops.wm.open_mainfile(filepath = lst[0])
        bpy.context.scene.render.filepath = "d:\\Uni Material\\Fall 2020\\Intro to CS\\Code\\project\\render"
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.ops.render.render(animation=False, write_still=True, use_viewport=False, layer='', scene='')
        file2 = open("ob_DATA.data","w")
        for ob in bpy.data.objects:
            file2.write(ob.name+"\n")

        fileCurrency.write("filepath??"+lst[0]+"|")
        fileCurrency.close()
blend = Blender()
file1 = open("something.drm","r")
# fileCurrency.seek(0)

str2 = file1.read()
lst = str2.split("#")

print(lst[1:])
exec(funcDict[lst[0]] % str(lst[1:]))


