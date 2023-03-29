import moderngl
from pyglet import image

class Texture:
    def __init__(self, context) -> None:
        self._gl_context = context
        self._texture = None
        
    def get_texture(self, path) -> moderngl.Texture:
        pic = image.load(path)
        raw_pic = pic.get_image_data()
        texture_data = raw_pic.get_data('RGB', raw_pic.width * 3)
        width, height = pic.width, pic.height
        texture = self._gl_context.texture(size = (width, height), 
                                           components = 3, 
                                           data = texture_data)
        return texture
    
    def destroy(self) -> None:
        self._texture.release()