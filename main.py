from modules.core import GLEngine
# from modules.shapes import *
from beta.teapot import Teapot
import modules.scene as scene
import modules.demos as demos



if __name__ == '__main__':
    demo = GLEngine(debug=True)
    demo.set_default_camera()
    
    # scenes = [demos.HelloTriangle(demo)]
    # scenes = [demos.TestCube(demo), demos.SkeletonCube(demo)]
    # scenes = [demos.CompanionCube(demo)]
    # scenes = [Teapot(demo)]
    
    # scenes = [scene.CompanionCube(demo)]
    scenes = [scene.TestCube(demo)]
    demo.set_scenes(scenes)

    demo.run()
