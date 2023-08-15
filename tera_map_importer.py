import os
import subprocess
import hashlib
import struct
import bpy
import math
from mathutils import Vector
import re, sys

class Printer:
    def __init__(self):
        self.text = ''

    def reprint(self, text):
        empty = ''
        for c in self.text:
            empty += ' '
        print(empty, end='\r')
        print(text, end='\r')
        self.text = text
    
    def print(self, text):
        self.reprint(text + '\n')
printer = Printer()

""" root_dir
    ├── Maps
    └── Packages
-----------------------------
    export_dir
    ├── path/to/gmp
    │   └── tsv files
    └── path/to/gpk
        ├── MaterialInstanceConstant
        ├── StaticMesh3
        └── Texture2D
"""

# --------------------------- options ------------------------------

EXPORT_MESHES = True
EXPORT_LIGHTS = True
SL_ONLY = False

USE_SPECULAR = False

MAP_PATH = 'Maps\\AEN'
START_FROM = ''
INCLUSIONS = ['5064']
EXCLUSIONS = []
# -------------------------- set paths -----------------------------

root_dir = 'D:\\TERA\\Client\\S1Game\\CookedPC\\Art_Data'
maps_dir = os.path.join(root_dir, 'Maps')
packages_dir = os.path.join(root_dir, 'Packages')

export_dir = 'D:\\TERA_Export'
umodel_path = 'D:\\TERA_Export_Tools\\umodel.exe'
terahelpercli_path = 'D:\\TERA_Export_Tools\\TeraHelperCLI.exe'
gpk_history_path = 'D:\\TERA_Export_Tools\\gpk_history.tsv'
gmp_history_path = 'D:\\TERA_Export_Tools\\gmp_history.tsv'

os.chdir(root_dir)

# --------------------- load gpk_history.tsv ------------------------

exported_gpks = []
exported_gmps = []
if os.path.exists(gpk_history_path):
    gpk_history = open(gpk_history_path, 'r')
    for line in gpk_history.readlines():
        t = (line.split('\t')[0], line.split('\t')[1].replace('\n', ''))
        exported_gpks.append(t)
    gpk_history.close()
else:
    gpk_history = open(gpk_history_path, 'w')
    gpk_history.close()

if os.path.exists(gmp_history_path):
    gmp_history = open(gmp_history_path, 'r')
    for line in gmp_history.readlines():
        t = (line.split('\t')[0], line.split('\t')[1].replace('\n', ''))
        exported_gmps.append(t)
    gmp_history.close()
else:
    gmp_history = open(gmp_history_path, 'w')
    gmp_history.close()

# -------------------------------------------------------------------

class StaticMeshComponent:
    def __init__(self, path):
        self.path = path
        self.mesh_path = ""
        self.package = ""
        self.object = ""
        self.mat_path = ""
        self.tex_path = ""
        self.gpk_path = ""
        if os.path.exists(self.path):
            f = open(self.path)
            lines = f.readlines()
            for line in lines:
                if line.startswith('StaticMesh'):
                    smstrarr = line.split('\t')[3].split('.')
                    self.package = smstrarr[0]
                    if len(smstrarr) > 1:
                        self.object = smstrarr[len(smstrarr) - 1].replace('\n', '')
                    self.build_gpk_path()
                    self.build_mesh_path()
                    self.build_mat_path()
                    self.build_tex_path()
            f.close()

    def build_gpk_path(self):
        for root, d, files in os.walk(packages_dir):
            for filename in files:
                if self.package + '.gpk' == filename:
                    self.gpk_path = os.path.join(root, filename)
                    break

    def build_mesh_path(self):
        self.mesh_path = self.gpk_path.replace(packages_dir, export_dir).replace('.gpk', f'\\StaticMesh3\\{self.object}.pskx')

    def build_mat_path(self):
        self.mat_path = self.gpk_path.replace(packages_dir, export_dir).replace('.gpk', '\\MaterialInstanceConstant')

    def build_tex_path(self):
        self.tex_path = self.gpk_path.replace(packages_dir, export_dir).replace('.gpk', '\\Texture2D')

# -------------------------------------------------------------------

class StaticMeshActor:
    def __init__(self, path):
        self.path = path
        self.rotation = [0, 0, 0]
        self.location = [0, 0, 0]
        self.scale = [1, 1, 1]
        self.smc_ref = ''
        head, tail = os.path.split(self.path)
        self.index = tail.replace('TheWorld.PersistentLevel.StaticMeshActor', '').replace('.tsv', '').replace('_','')
        if self.index == '':
            self.index = '0'
        f = open(self.path, 'r')
        lines = f.readlines()
        for line in lines:
            if line.startswith('StaticMeshComponent'):
                self.smc_ref = line.split('\t')[3].replace('\n', '')
            elif line.startswith('Location'):
                self.parse_location(line.split('\t')[3].replace('\n', ''))
            elif line.startswith('Rotation'):
                self.parse_rotation(line.split('\t')[3].replace('\n', ''))
            elif line.startswith('DrawScale') and not 'DrawScale3D' in line:
                self.parse_drawscale(line.split('\t')[3].replace('\n', ''))
            elif line.startswith('DrawScale3D'):
                self.parse_drawscale3d(line.split('\t')[3].replace('\n', ''))
        f.close()
        smc_path = os.path.join(os.path.dirname(self.path), self.smc_ref + '.tsv')
        self.smc = StaticMeshComponent(smc_path)

    def extract_gpk(self):
        if not os.path.exists(self.smc.gpk_path):
            # printer.print(f'[StaticMeshActor.extract_gpk] {self.smc.gpk_path} not found')
            return
        gpk_file = open(self.smc.gpk_path, 'rb')
        gpk_bytes = gpk_file.read()
        skip = False
        for tp in exported_gpks:
            if self.smc.gpk_path in tp[0]:
                if hashlib.sha256(gpk_bytes).hexdigest() == tp[1]:
                    skip = True
                else:
                    printer.print(f'[StaticMeshActor.extract_gpk] WARNING: {self.smc.package} changed')
        if not skip:
            printer.print(self.smc.package + ' missing, exporting')
            FNULL = open(os.devnull, 'w')
            subprocess.call([umodel_path, self.smc.gpk_path, '-export', f'-out={self.get_out_path()}'], stdout=FNULL, stderr=subprocess.STDOUT)
            exported_gpks.append((self.smc.gpk_path, hashlib.sha256(gpk_bytes).hexdigest()))
            gpk_history = open(gpk_history_path, 'a')
            gpk_history.write(f'{self.smc.gpk_path}\t{hashlib.sha256(gpk_bytes).hexdigest()}\n')
            gpk_history.close()
        gpk_file.close()

    def get_out_path(self):
        return os.path.dirname(self.smc.gpk_path.replace(packages_dir, export_dir))

    def parse_location(self, raw):
        idx = 0
        for rawcomp in [raw[i:i+8] for i in range(0, len(raw), 8)]:
            self.location[idx] = struct.unpack('<f', bytes.fromhex(rawcomp))[0]
            idx += 1

    def parse_rotation(self, raw):
        idx = 0
        for rawcomp in [raw[i:i+8] for i in range(0, len(raw), 8)]:
            parts = [rawcomp[j:j+4] for j in range(0, len(rawcomp), 4)]
            value = struct.unpack('<H', bytes.fromhex(parts[0]))[0]
            self.rotation[idx] = 360 * (value / 65535)
            #if struct.unpack('<h', bytes.fromhex(parts[1]))[0] != 0:
            self.rotation[idx] += 180
            idx += 1

    def parse_drawscale(self, raw):
        for i in range(0, len(self.scale)):
            self.scale[i] *= float(raw.replace(',', '.'))

    def parse_drawscale3d(self, raw):
        idx = 0
        for rawcomp in [raw[i:i+8] for i in range(0, len(raw), 8)]:
            self.scale[idx] *= struct.unpack('<f', bytes.fromhex(rawcomp))[0]
            idx += 1

# -------------------------------------------------------------------

class LightComponent:
    def __init__(self, path):
        self.path = path
        self.brightness = 1.0
        self.color = 'FFFFFFFF'
        f = open(self.path)
        lines = f.readlines()
        for line in lines:
            if line.startswith('Brightness'):
                self.brightness = float(line.split('\t')[3].replace(',', '.').replace('\n', ''))
            elif line.startswith('LightColor'):
                self.color = line.split('\t')[3].replace('\n', '')

# -------------------------------------------------------------------

class PointLight:
    def __init__(self, path):
        self.path = path
        self.location = [0, 0, 0]
        head, tail = os.path.split(self.path)
        self.index = tail.replace('TheWorld.PersistentLevel.PointLight', '').replace('.tsv', '').replace('_','')
        if self.index == '':
            self.index = '0'
        f = open(self.path, 'r')
        lines = f.readlines()
        for line in lines:
            if line.startswith('LightComponent'):
                self.comp_ref = line.split('\t')[3].replace('\n', '')
            elif line.startswith('Location'):
                self.parse_location(line.split('\t')[3].replace('\n', ''))
        f.close()
        comp_path = os.path.join(os.path.dirname(self.path), self.comp_ref + '.tsv')
        self.light_comp = LightComponent(comp_path)


    def parse_location(self, raw):
        idx = 0
        for rawcomp in [raw[i:i+8] for i in range(0, len(raw), 8)]:
            self.location[idx] = struct.unpack('<f', bytes.fromhex(rawcomp))[0]
            idx += 1

# -------------------------------------------------------------------

class TeraMap:
    def __init__(self, gmp_path):
        self.gmp_path = os.path.abspath(gmp_path)    
        head, tail = os.path.split(self.gmp_path)
        self.name = tail.replace('.gmp', '') 
        self.actors = []
        self.point_lights = []
        self.explode_gmp()

    def explode_gmp(self):
        self.to_tsv()

        found_actors = []
        found_point_lights = []
        for r, d, f in os.walk(self.gmp_path.replace('.gmp', "").replace(maps_dir, export_dir)):
            for file in f:
                if 'StaticMeshActor' in file and not 'Component' in file and EXPORT_MESHES:
                    found_actors.append(os.path.join(r, file))
                elif 'PointLight' in file and not 'Component' in file and EXPORT_LIGHTS:
                    found_point_lights.append(os.path.join(r, file))
        
        count = len(found_actors)
        idx = 0
        for tsv in found_actors:
            sma = StaticMeshActor(path=tsv)
            sma.extract_gpk()
            if SL_ONLY and not '_SL' in sma.smc.mesh_path: continue
            idx += 1
            self.actors.append(sma)
            printer.reprint(f' {idx}/{count} - Found {sma.smc.object}_{sma.index}')
        
        if count > 0: printer.reprint(f'Parsed {count} StaticMeshActors')
        idx = 0
        count = len(found_point_lights)
        for ltsv in found_point_lights:
            pl = PointLight(path=ltsv)
            self.point_lights.append(pl)
            printer.reprint(f' {idx}/{count} - Found PointLight {pl.index}')
        if count > 0: printer.reprint(f'Parsed {count} PointLights')

    def to_tsv(self):
        abs_input = os.path.abspath(self.gmp_path)
        abs_output = os.path.dirname(self.gmp_path.replace(maps_dir, export_dir))
        gmp_file = open(abs_input, 'rb')
        gmp_bytes = gmp_file.read()
        skip = False
        for tp in exported_gmps:
            if abs_input in tp[0]:
                if hashlib.sha256(gmp_bytes).hexdigest() == tp[1]:
                    skip = True
                else:
                    printer.print(f'[StaticMeshActor.to_tsv] WARNING: {abs_input} changed')
        if not skip:
            printer.print(abs_input + ' missing, exporting')
            subprocess.call([terahelpercli_path, '-tsv_export', abs_input, abs_output])
            exported_gmps.append((abs_input, hashlib.sha256(gmp_bytes).hexdigest()))
            gmp_history = open(gmp_history_path, 'a')
            gmp_history.write(f'{abs_input}\t{hashlib.sha256(gmp_bytes).hexdigest()}\n')
            gmp_history.close()
        gmp_file.close()

# -------------------------------------------------------------------

def HexToColor(hexcol):
    hexcol = hexcol.strip()
    r, g, b, a = hexcol[:2], hexcol[2:4], hexcol[4:6], hexcol[6:]
    r, g, b, a = [int(n, 16) / 255.0 for n in (r, g, b, a)]
    return (b, g, r)

def SkipMap(map_name):
    if len(INCLUSIONS) > 0:
        for inclusion in INCLUSIONS:
            if inclusion not in file: 
                return True
    if len(EXCLUSIONS) > 0:
        for exclusion in EXCLUSIONS:
            if exclusion in file:
                return True
    return False

def BuildTextureNode(mat, tex_name):
    skip = False
    # if "Default" in tex_name or "Test" in tex_name:
    if "Test" in tex_name:
        skip = True
    if not skip:
        if tex_name in mat.node_tree.nodes: return mat.node_tree.nodes[tex_name]
        img = None
        if f'{tex_name}.tga' in bpy.data.images:
            img = bpy.data.images[f'{tex_name}.tga']
        else:
            tex_path = os.path.join(mat_path.replace('MaterialInstanceConstant', 'Texture2D').replace(f'{mat.name}.mat', ''), tex_name + ".tga")
            if not os.path.exists(tex_path):
                for r, d, f in os.walk(export_dir):
                    for file in f:
                        if tex_name + '.tga' in file:
                            tex_path = os.path.join(r, file)
            img = bpy.data.images.load(filepath=tex_path)

        tex = mat.node_tree.nodes.new(type="ShaderNodeTexImage")
        tex.name = tex_name
        tex.image = img
        return tex
    return None

def SetTransform(staticMeshActor, obj):
    obj.scale.x = staticMeshActor.scale[0]
    obj.scale.y = staticMeshActor.scale[1] * (-1)
    obj.scale.z = staticMeshActor.scale[2]

    obj.rotation_euler.x = math.radians(staticMeshActor.rotation[2] * (-1) )
    obj.rotation_euler.y = math.radians(staticMeshActor.rotation[0]        )
    obj.rotation_euler.z = math.radians(staticMeshActor.rotation[1]        )

    obj.location.x = staticMeshActor.location[0]
    obj.location.y = staticMeshActor.location[1]
    obj.location.z = staticMeshActor.location[2]

def ParsePointLights(tera_map, coll, pivot):
    for pl in tera_map.point_lights:
        printer.reprint(f' Creating light {pl.index}')
        l_data = bpy.data.lights.new(name=f'L_{tera_map.name}_{pl.index}', type='POINT')
        l_data.energy = pl.light_comp.brightness * 100000
        l_data.color = HexToColor(pl.light_comp.color)
        l_obj = bpy.data.objects.new(name=f'L_{tera_map.name}_{pl.index}', object_data=l_data)
        coll.objects.link(l_obj)
        if l_obj.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(l_obj)
        l_obj.location = (pl.location[0], pl.location[1], pl.location[2])
        l_obj.parent = pivot

# -------------------------------------------------------------------

loaded_maps = []
loaded_meshes = []
maps_to_load = []


printer.print(f'--- START ---')

start = START_FROM == ''

for r,d,f in os.walk(MAP_PATH):
    for file in f:
        if START_FROM in file: start = True
        if not start: continue
        if SkipMap(file): continue
        maps_to_load.append(os.path.join(r, file))

maps_count = len(maps_to_load)
map_idx = 0

for gmp in maps_to_load:
    map_idx += 1
    # parse and explode the map
    msg = f'- Loading {gmp} ({map_idx}/{maps_count}) -'
    sep = ''
    for c in msg:
        sep += '-'
    printer.print(f'{sep}\n{msg}\n{sep}')
    tera_map = TeraMap(gmp)

    # iterate StaticMeshActors and import pskx
    count = len(tera_map.actors)

    # find or create collection for map
    coll = None
    for c in bpy.data.collections:
        if c.name == tera_map.name:
            coll = c
    if coll == None:
        coll = bpy.data.collections.new(tera_map.name)
    # add the collection to the scene
    if coll.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(coll)

    pivot = bpy.data.objects.new('Pivot', None)
    coll.objects.link(pivot)

    idx = 0

    for sma in tera_map.actors:
        idx += 1
        copied = False
        if not os.path.exists(sma.smc.mesh_path):
            printer.print(f' {idx}/{count} - Cannot find mesh file for actor {sma.index}')
            printer.print(f'                 data path: {sma.smc.package}.{sma.smc.object}')
            printer.print(f'                 mesh path: {sma.smc.mesh_path}')
            printer.print(f'                 gpk  path: {sma.smc.gpk_path}')
        else:
            imported = None
            for loaded_name, loaded_path in loaded_meshes:
                if loaded_path == sma.smc.mesh_path:
                    printer.reprint(f' {idx}/{count} - Copying {sma.smc.object} <- {loaded_name}')
                    src = bpy.data.objects[loaded_name]
                    cp = src.copy()
                    cp.data = src.data
                    imported = cp
                    copied = True
                    break

            if imported == None:
                printer.reprint(f' {idx}/{count} - Importing {sma.smc.object}.pskx')
                bpy.ops.import_scene.psk(filepath=sma.smc.mesh_path)
                imported = bpy.context.selected_objects[0]
                loaded_meshes.append((f'{tera_map.name}_{sma.index}', sma.smc.mesh_path))

            mesh_name = imported.data.name
            imported.name = f'{tera_map.name}_{sma.index}'
            imported.data.name = mesh_name
            SetTransform(sma, imported)

            imported.parent = pivot

            coll.objects.link(imported)
            # unlink object from main collection
            if imported.name in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.unlink(imported)

            if not copied:
                for slot in imported.material_slots:
                    mat = slot.material
                    mat.use_nodes = True
                    mat.blend_method = "HASHED"
                    if len(mat.node_tree.nodes) > 2: continue
                    princ = mat.node_tree.nodes['Principled BSDF']
                    princ.inputs['Specular'].default_value = 0.05
                    princ.inputs['Base Color'].default_value = (0,0,0,0)
                    

                    mat_path = os.path.join(sma.smc.mat_path, f'{mat.name}.mat')
                    if not os.path.exists(mat_path):
                        for r, d, f in os.walk(export_dir):
                            for file in f:
                                if f'{mat.name}.mat' in file:
                                    mat_path = os.path.join(r, file)

                    if os.path.exists(mat_path):
                        matfile = open(os.path.join(mat_path), 'r')
                        for ml in matfile.readlines():
                            # Diffuse
                            if ml.startswith('Diffuse='):
                                tex_name = ml.replace("Diffuse=", "").replace("\n", "")
                                tex = BuildTextureNode(mat, tex_name)
                                if tex is not None:
                                    tex.location.x = -600
                                    tex.location.y = princ.location.y + princ.height/2 - tex.height/2
                                    mat.node_tree.links.new(princ.inputs["Base Color"], tex.outputs["Color"])
                                    mat.node_tree.links.new(princ.inputs["Alpha"], tex.outputs["Alpha"])
                            # Emission
                            elif ml.startswith('Emissive='):
                                tex_name = ml.replace("Emissive=", "").replace("\n", "")
                                tex = BuildTextureNode(mat, tex_name)
                                if tex is not None:
                                    tex.location.x = -600
                                    tex.location.y = -150
                                    emis_shader = mat.node_tree.nodes.new(type="ShaderNodeEmission")
                                    add_shader = mat.node_tree.nodes.new(type="ShaderNodeAddShader")
                                    emis_shader.inputs["Strength"].default_value = 10
                                    mat.node_tree.links.new(princ.outputs["BSDF"], add_shader.inputs[1])
                                    mat.node_tree.links.new(emis_shader.outputs["Emission"], add_shader.inputs[0])
                                    mat.node_tree.links.new(add_shader.outputs[0], mat.node_tree.nodes['Material Output'].inputs['Surface'])
                                    mat.node_tree.links.new(emis_shader.inputs["Color"], tex.outputs["Color"])
                                    add_shader.location.x = princ.location.x + 300
                                    add_shader.location.y = princ.location.y + princ.height/2 - add_shader.height/2
                                    emis_shader.location.x = princ.location.x + princ.width/2 - emis_shader.width/2
                                    emis_shader.location.y = princ.location.y + 100 + princ.height/2 
                                    mat.node_tree.nodes['Material Output'].location.x = add_shader.location.x + 200
                            # Specular
                            elif ml.startswith('Specular=') and USE_SPECULAR:
                                tex_name = ml.replace('Specular=', '').replace('\n', '')
                                tex = BuildTextureNode(mat, tex_name)                               
                                if tex is not None:
                                    tex.location.x = -600
                                    tex.location.y = -450
                                    mat.node_tree.links.new(princ.inputs['Specular'], tex.outputs['Color'])
                            # Opacity
                            elif ml.startswith('Opacity='):
                                tex_name = ml.replace('Opacity=', '').replace('\n', '')
                                tex = BuildTextureNode(mat, tex_name)      
                                if tex is not None:
                                    tex.location.x = -600
                                    tex.location.y = -300
                                    mat.node_tree.links.new(princ.inputs['Alpha'], tex.outputs['Color'])             
                            # Normal
                            elif ml.startswith('Normal='):
                                tex_name = ml.replace("Normal=", "").replace("\n", "")
                                tex = BuildTextureNode(mat, tex_name)                               
                                if tex is not None:
                                    tex.location.x = -600
                                    tex.location.y = -600
                                    bump = mat.node_tree.nodes.new("ShaderNodeNormalMap")
                                    tex.image.colorspace_settings.name = "Non-Color"
                                    mat.node_tree.links.new(princ.inputs["Normal"], bump.outputs["Normal"])
                                    mat.node_tree.links.new(bump.inputs["Color"], tex.outputs["Color"])
                                    bump.location.x = princ.location.x - 300
                                    bump.location.y = tex.location.y



    printer.print('Adding lights')
    ParsePointLights(tera_map, coll, pivot)
    
    pivot.scale.x *= 0.08 * (-1)
    pivot.scale.y *= 0.08
    pivot.scale.z *= 0.08
    bpy.context.evaluated_depsgraph_get().update() 
    for child in pivot.children:
        pwm = child.matrix_world.copy()
        child.parent = None
        child.matrix_world = pwm

    # hide non-SL collections before scripts ends to avoid lag
    bpy.context.window.view_layer.layer_collection.children[coll.name].exclude = 'SL' not in coll.name

    bpy.data.objects.remove(bpy.data.objects[pivot.name])

    loaded_maps.append(tera_map)

# ---------------------- update gpk_history -------------------------
gpk_history.close()
gmp_history.close()
printer.print('--- FINISHED ---')
