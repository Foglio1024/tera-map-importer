import os
import struct
import bpy
import sys


class static_mesh_actor:
    name = ""
    loc = [0, 0, 0]
    rot = [0, 0, 0]
    scale = [1, 1, 1]
    mesh_name = ""
    actor_area = ""

    def setLoc(self, newloc):
        self.loc = newloc

    def setRot(self, newrot):
        self.rot = newrot

    def setScale(self, newscale):
        self.scale = newscale

    def multScale(self, mult):
        scale[0] *= mult
        scale[1] *= mult
        scale[2] *= mult

    def getMeshPath(self):
        if self.mesh_name == "":
            return ""

        spl = self.mesh_name.split('.')
        if len(spl) < 3:
            return ""
        mname = self.mesh_name.split('.')[2]

        ret = os.path.join(datapath, "StaticMesh3", mname + ".pskx")
        if not os.path.exists(ret):
            ret = os.path.join(datapath, "SkeletalMesh3", mname + ".psk")
        if not os.path.exists(ret):
            return ""

        return ret

    def toString(self):
        ret = self.name
        ret += " -> " + self.mesh_name
        ret += "\nloc: "
        ret += str(self.loc[0]) + " "
        ret += str(self.loc[1]) + " "
        ret += str(self.loc[2]) + " "
        ret += "\nrot: "
        ret += str(self.rot[0]) + " "
        ret += str(self.rot[1]) + " "
        ret += str(self.rot[2]) + " "
        ret += "\nscale: "
        ret += str(self.scale[0]) + " "
        ret += str(self.scale[1]) + " "
        ret += str(self.scale[2]) + " "
        return ret

    def buildName(self):
        # + self.mesh_name.split(".sm.")[1]).replace("_._", "__").replace("__","_")
        return (self.actor_area + "_" + self.name.replace("TheWorld.PersistentLevel.StaticMeshActor", "SMA_").replace("StaticMeshComponent", "_")).replace("__", "_").replace("SMA_.", "SMA_0.").replace("._", "").replace("_SMA_", "_")


for material in bpy.data.materials:
    material.user_clear()
    bpy.data.materials.remove(material)
for img in bpy.data.images:
    img.user_clear()
    bpy.data.images.remove(img)


#areas = ["RNW_A_5654", "RNW_A_5655", "RNW_A_5656", "RNW_B_5754", "RNW_B_5755", "RNW_B_5756", "RNW_B_5854", "RNW_B_5855", "RNW_B_5856", "RNW_B_5955", "RNW_B_5956", "RNW_C_5657", "RNW_C_5757", "RNW_C_5857", "RNW_C_5957" ]
#areas = ["RNW_A_5654_SL", "RNW_A_5655_SL", "RNW_A_5656_SL", "RNW_B_5754_SL", "RNW_B_5755_SL", "RNW_B_5756_SL", "RNW_B_5854_SL", "RNW_B_5855_SL", "RNW_B_5856_SL", "RNW_B_5955_SL", "RNW_B_5956_SL", "RNW_C_5657_SL", "RNW_C_5757_SL", "RNW_C_5857_SL", "RNW_C_5957_SL" ]
#areas = ["RNW_A_5654"]
#areas = ["RNW_A_5654",  "RNW_A_5655", "RNW_A_5656", "RNW_A_5654_SL", "RNW_A_5655_SL", "RNW_A_5656_SL"]
#areas = ["RNW_B_5754", "RNW_B_5755", "RNW_B_5756", "RNW_B_5854", "RNW_B_5855", "RNW_B_5856", "RNW_B_5955", "RNW_B_5956", "RNW_B_5754_SL", "RNW_B_5755_SL", "RNW_B_5756_SL", "RNW_B_5854_SL", "RNW_B_5855_SL", "RNW_B_5856_SL", "RNW_B_5955_SL", "RNW_B_5956_SL"]
#areas = ["RNW_C_5657", "RNW_C_5757", "RNW_C_5857", "RNW_C_5957", "RNW_C_5657_SL", "RNW_C_5757_SL", "RNW_C_5857_SL", "RNW_C_5957_SL"]
#areas = ["RNW_A_SkyCage"]
# areas = [
#  "FDI_20061992_SL",
#  "FDI_20061993_SL",
#  "FDI_20061994_SL",
#  "FDI_20061995_SL",
#  "FDI_20061996_SL",
#  "FDI_20071992_SL",
#  "FDI_20071993_SL",
#  "FDI_20071994_SL",
#  "FDI_20071995_SL",
#  "FDI_20071996_SL",
#  "FDI_20081992_SL",
#  "FDI_20081993_SL",
#  "FDI_20081994_SL",
#  "FDI_20081995_SL",
#  "FDI_20081996_SL",
#  "FDI_20091992_SL",
#  "FDI_20091993_SL",
#  "FDI_20091994_SL",
#  "FDI_20091995_SL",
#  "FDI_20091996_SL"
# ]
areas = [
# "EX_VK_SD1_T42",               
# "EX_VK_SD1_T42_1001996",       
# "EX_VK_SD1_T42_1001997",       
# "EX_VK_SD1_T42_Asset",         
# "EX_VK_SD1_T42_Asset_Basement",
# "EX_VK_SD1_T42_Asset_Outside", 
# "EX_VK_SD1_T42_BB",            
 "EX_VK_SD1_T42_BossRoom",      
# "EX_VK_SD1_T42_CollisionMap",  
# "EX_VK_SD1_T42_P",             
# "EX_VK_SD1_T42_PoisonWater",   
]
region = "StoryDG\\EX_VK"

maps_root = "D:\\Program Files (x86)\\TERA\\Client\\S1Game\\CookedPC\\Art_Data\\Maps\\"
for area in areas:
    loaded_actors = []
    print("Importing area " + area)
    coll = None
    for c in bpy.data.collections:
        if c.name == area:
            coll = c
    if coll == None:
        coll = bpy.data.collections.new(area)
    csvpath = maps_root + region + "\\csv\\" + area + "\\"
    datapath = maps_root + region + "\\data\\" + area + "\\"
    sma_paths = []
    smc_paths = []

    for r, d, f in os.walk(csvpath):
        for file in f:
            if "StaticMeshActor" in file and not "StaticMeshComponent" in file:
                sma_paths.append(os.path.join(r, file))
            elif "StaticMeshComponent.csv" in file:
                smc_paths.append(os.path.join(r, file))

    actors = []

    for path in sma_paths:
        f = open(path, "r")
        lines = f.readlines()
        a = static_mesh_actor()
        a.actor_area = area
        for l in lines:
            split = l.replace("\n", "").split(";")
            if l.startswith("StaticMeshComponent"):
                a.name = split[5]
            elif l.startswith("Location"):
                idxl = 0
                locstr = split[5].replace("\n", "")
                loc = [0, 0, 0]
                for lcomp in [locstr[i:i+8] for i in range(0, len(locstr), 8)]:
                    lc = struct.unpack('<f', bytes.fromhex(lcomp))[0]
                    loc[idxl] = lc
                    idxl += 1
                a.setLoc(loc)
            elif l.startswith("Rotation"):
                idxr = 0
                rotstr = split[5].replace("\n", "")
                rot = [0, 0, 0]
                for rcomp in [rotstr[i:i+8] for i in range(0, len(rotstr), 8)]:
                    # 1234 value int16 (little endian)
                    # 5678 sign int16 0x0000 = 0, 0xFFFF = -1

                    parts = [rcomp[j:j+4] for j in range(0, len(rcomp), 4)]

                    value = struct.unpack('<H', bytes.fromhex(parts[0]))[0]
                    if struct.unpack('<h', bytes.fromhex(parts[1]))[0] != 0:
                        value = value * -1

                    if parts[1] == 'FFFF':
                        value *= (-1)

                    rot[idxr] = (value/65535)*360
                    idxr += 1
                a.setRot(rot)
            elif l.startswith("DrawScale3D"):
                idxs = 0
                scstr = split[5].replace("\n", "")
                scale = [0, 0, 0]
                for scomp in [scstr[i:i+8] for i in range(0, len(scstr), 8)]:
                    scc = struct.unpack('<f', bytes.fromhex(scomp))[0]
                    scale[idxs] = scc
                    idxs += 1
                a.setScale(scale)
            elif l.startswith("DrawScale") and not "DrawScale3D" in l:
                mult = split[5].replace("\n", "")
        if a.name != "":
            actors.append(a)

    count = 0
    total = len(actors)
    for actor in actors:
        count += 1
        f = open(os.path.join(csvpath, actor.name + ".csv"), "r")
        lines = f.readlines()
        for l in lines:
            split = l.replace("\n", "").split(";")
            if l.startswith("StaticMesh"):
                actor.mesh_name = split[5]

        if actor.getMeshPath() != "" and ".sm." in actor.mesh_name:
            try:
                o = None
                for loaded in loaded_actors:
                    if loaded.getMeshPath() == actor.getMeshPath():
                        src = bpy.data.objects[loaded.buildName()]
                        cp = src.copy()
                        cp.data = src.data.copy()
                        o = cp
                        print(" ["+area+"] "+str(count)+"/" + str(total) +
                              " [C] " + actor.buildName() + " <- " + loaded.buildName())
                        break
                if o is None:
                    print(" ["+area+"] "+str(count)+"/" +
                          str(total) + " [L] " + actor.buildName())
                    bpy.ops.import_scene.psk(filepath=actor.getMeshPath())
                    o = bpy.context.selected_objects[0]

                o.scale.x = actor.scale[0]
                o.scale.y = -actor.scale[2]
                o.scale.z = actor.scale[1]

                o.rotation_euler.x = actor.rot[0]*3.14/180
                o.rotation_euler.y = -actor.rot[2]*3.14/180
                o.rotation_euler.z = actor.rot[1]*3.14/180

                o.location.x = actor.loc[0]
                o.location.y = actor.loc[1]
                o.location.z = actor.loc[2]

                # todo: mirror across X axis
                 # create empty in origin
                 # parent everything to it
                 # scale by -1 on X
                 # unparent
                 # remove empty

                if "SL" in actor.mesh_name:
                    bpy.ops.object.shade_smooth()

                o.name = actor.buildName()
                coll.objects.link(o)
                if o.name in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.unlink(o)

                mat_dir = os.path.join(datapath, "MaterialInstanceConstant")
                for mat_slot in o.material_slots:
                    mat = mat_slot.material
                    mat.use_nodes = True
                    #mat.blend_method = "BLEND"
                    mat_path = os.path.join(mat_dir, mat.name + ".mat")
                    princ = mat.node_tree.nodes["Principled BSDF"]
                    princ.inputs[7].default_value = 0.6

                    if os.path.exists(mat_path):
                        mf = open(os.path.join(mat_path), "r")
                        diff_path = ""
                        nrm_path = ""
                        spec_path = ""
                        for ml in mf.readlines():
                            # Diffuse
                            if ml.startswith("Diffuse=") or ml.startswith("Emissive="):
                                tex_name = ml.replace("Diffuse=", "").replace(
                                    "Emissive=", "").replace("\n", "")
                                skip = False
                                for node in mat.node_tree.nodes:
                                    if node.name == tex_name:
                                        skip = True
                                        break
                                if "Default" in tex_name or "Test" in tex_name:
                                    skip = True
                                if not skip:
                                    diff_path = os.path.join(
                                        datapath, "Texture2D", tex_name + ".tga")
                                    if os.path.exists(diff_path):
                                        tex = mat.node_tree.nodes.new(
                                            type="ShaderNodeTexImage")
                                        tex.name = tex_name
                                        tex.image = bpy.data.images.load(
                                            filepath=diff_path)
                                        mat.node_tree.links.new(
                                            princ.inputs["Base Color"], tex.outputs["Color"])

                                        mat.node_tree.links.new(
                                            princ.inputs["Alpha"], tex.outputs["Alpha"])

                            # Normal
                            elif ml.startswith("Normal="):
                                tex_name = ml.replace(
                                    "Normal=", "").replace("\n", "")
                                skip = False
                                for node in mat.node_tree.nodes:
                                    if node.name == tex_name:
                                        skip = True
                                        break
                                if "Default" in tex_name or "Test" in tex_name:
                                    skip = True
                                if not skip:
                                    nrm_path = os.path.join(
                                        datapath, "Texture2D", tex_name + ".tga")
                                    if os.path.exists(nrm_path):
                                        tex = mat.node_tree.nodes.new(
                                            type="ShaderNodeTexImage")
                                        tex.name = tex_name
                                        bump = mat.node_tree.nodes.new(
                                            "ShaderNodeNormalMap")
                                        tex.image = bpy.data.images.load(
                                            filepath=nrm_path)
                                        tex.image.colorspace_settings.name = "Non-Color"
                                        mat.node_tree.links.new(
                                            princ.inputs["Normal"], bump.outputs["Normal"])
                                        mat.node_tree.links.new(
                                            bump.inputs["Color"], tex.outputs["Color"])
                            # Specular
                            elif ml.startswith("Specular="):
                                tex_name = ml.replace("Specular=", "").replace("\n", "")
                                skip = False
                                for node in mat.node_tree.nodes:
                                    if node.name == tex_name:
                                        skip = True
                                        break
                                if "Default" in tex_name or "Test" in tex_name:
                                    skip = True
                                if not skip:
                                    spec_path = os.path.join(datapath, "Texture2D", tex_name + ".tga")
                                    if os.path.exists(spec_path):
                                        tex = mat.node_tree.nodes.new(type="ShaderNodeTexImage")
                                        tex.name = tex_name
                                        tex.image = bpy.data.images.load(filepath=spec_path)
                                        mat.node_tree.links.new(princ.inputs["Specular"], tex.outputs["Color"])
            except AttributeError as err:
                print(err)
            loaded_actors.append(actor)
    if coll.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(coll)
