from bge import logic
from bge import events
from mathutils import Euler

previousPosition = [-1, -1]

def update():
    global previousPosition
    
    cont = logic.getCurrentController()
    mouseSensor = cont.sensors[0]
    
    if previousPosition == [-1, -1]:
        previousPosition = mouseSensor.position
        return
    
    delta = [mouseSensor.position[0] - previousPosition[0],
             mouseSensor.position[1] - previousPosition[1]]
    previousPosition = mouseSensor.position
    
    if mouseSensor.getButtonStatus(events.LEFTMOUSE) != 0:    
        for scene in logic.getSceneList():
            #scene.active_camera.worldPosition.x += delta[0] / 50.0
            #scene.active_camera.worldPosition.y += delta[1] / 50.0
            scene.objects.get("center").worldOrientation.rotate(Euler((0.0, 0.0, delta[0] / 100.0)))
            scene.objects.get("center").worldOrientation.rotate(Euler((delta[1] / 100.0, 0.0, 0.0)))
                
    elif mouseSensor.getButtonStatus(events.RIGHTMOUSE) != 0:
        for scene in logic.getSceneList():
            scene.active_camera.worldPosition.z += delta[1] / 50.0