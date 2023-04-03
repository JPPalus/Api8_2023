from modules.core import GLEngine
# from modules.shapes import *
from beta.teapot import Teapot
import modules.scene as scene
import modules.shapes as shapes



if __name__ == '__main__':
    demo = GLEngine(debug=True)
    demo.set_default_camera()
    
    # scenes = [shapes.HelloTriangle(demo)]
    # scenes = [shapes.TestCube(demo), shapes.SkeletonCube(demo)]
    # scenes = [shapes.CompanionCube(demo)]
    # scenes = [Teapot(demo)]
    
    # scenes = [scene.CompanionCube(demo)]
    scenes = [scene.TestCube(demo)]
    demo.set_scenes(scenes)

    demo.run()
