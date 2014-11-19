import bge
import struct, time
from math import floor
from pyshmdata import Writer

class Anamorphose(bge.types.KX_GameObject):
    def __init__(self, old_owner):
        self.writer = Writer(path="/tmp/anamorphose", datatype="application/x-polymesh")
        self.start_time = time.clock_gettime(time.CLOCK_REALTIME)
        
        scene = bge.logic.getCurrentScene()
        callback = lambda: self.update()
        scene.pre_draw.append(callback)
    
    def update(self):
        scene = bge.logic.getCurrentScene()
        camera = scene.active_camera
        
        worldM = self.worldTransform
        cameraM = camera.modelview_matrix
        projM = camera.projection_matrix
        transM = projM * cameraM * worldM
        
        buffer = bytearray()
        mesh = self.meshes[0]
        vertNbr = mesh.getVertexArrayLength(0)
        polyNbr = mesh.numPolygons
        buffer += struct.pack("ii", vertNbr, polyNbr)
        
        for index in range(vertNbr):
            vert = mesh.getVertex(0, index)
            p = worldM * vert.XYZ
            uv = camera.getScreenPosition(worldM * vert.XYZ)
            buffer += struct.pack("ffffffff", p[0], p[1], p[2], uv[0], uv[1], 0, 0, 0)
            
        for index in range(polyNbr):
            p = mesh.getPolygon(index)
            if p.getNumVertex() == 3:
                buffer += struct.pack("iiii", 3, p.v1, p.v2, p.v3)
            elif p.getNumVertex() == 4:
                buffer += struct.pack("iiiii", 4, p.v1, p.v2, p.v3, p.v4)
                
        currentTime = time.clock_gettime(time.CLOCK_REALTIME) - self.start_time
        self.writer.push(buffer, floor(currentTime * 1e9))

def init():
    cont = bge.logic.getCurrentController()
    this = cont.owner
    
    if type(this) is not Anamorphose:
        anamorphose = Anamorphose(this)