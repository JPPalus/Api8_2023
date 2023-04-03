from pyglet import image
from modules.mesh import SolidCubeMesh, WireCubeMesh, TexturedCubeMesh
import modules.glmath as glmath
import numpy as np
import moderngl
import glm


class Texture:
    def __init__(self, context: moderngl.Context, path: str) -> None:
        self._gl_context = context
        self._texture = self.get_texture(path)
        
    def get_texture(self, path: str) -> moderngl.Texture:
        pic = image.load(path)
        raw_pic = pic.get_image_data()
        texture_data = raw_pic.get_data('RGB', raw_pic.width * 3)
        width, height = pic.width, pic.height
        texture = self._gl_context.texture(size = (width, height), 
                                           components = 3, 
                                           data = texture_data)
        return texture
    
    def use(self) -> None:
        self._texture.use()
    
    def destroy(self) -> None:
        self._texture.release()
        
        
class Model:
    def __init__(self, engine, shader_program_path: str = 'shaders/default') -> None:
        self._engine = engine
        self._gl_context = engine.gl_context
        self._shader_program = self.get_shader_program(shader_program_path)
        self._textures: dict[int, Texture] = {}
        self._material = 56.0
        self._vbo: moderngl.Buffer = None
        self._vao: moderngl.VertexArray = None
        self._model_matrix = glmath.identity_matrix()
        
    @property
    def material(self) -> float:
        return self._material
    
    @property
    def model_matrix(self) -> glm.fmat4x4:
        return self._model_matrix
    
    @property
    def shader_program(self) -> moderngl.Program:
        return self._shader_program
    
    def get_texture(self, sampler_id: int) -> Texture:
        return self._textures[sampler_id]
    
    def use_textures(self) -> None:
        for texture_id in self._textures:
            self._textures[texture_id].use()
    
    def set_material(self, material: float) -> None:
        self._material = material
        
    def set_textures(self, textures: dict[int, Texture]) -> None:
        self._textures = textures
        
    def add_texture(self, texture, sampler_id: int) -> None:
        self._textures[sampler_id] = texture
        
    def set_vbo(self, vertex_data: np.ndarray) -> None:
        self._vbo = self._gl_context.buffer(vertex_data)
        
    def set_vao(self, format: str, attributes: list[str]) -> None:
        self._vao = self._gl_context.vertex_array(self._shader_program, 
                                                [(self._vbo, format, *attributes)])
        
    def get_shader_program(self, shader_program_path: str, vertex: bool = True, fragment: bool  = True, 
                                 geometry: bool  = False, tess: bool  = False) -> moderngl.Program:
        if vertex:
            with open(f'{shader_program_path}.vert') as file:
                vertex_shader = file.read()
        else: 
            vertex_shader = None
            
        if fragment:
            with open(f'{shader_program_path}.frag') as file:
                fragment_shader = file.read()
        else:   
            fragment_shader = None  
            
        if geometry:
            with open(f'{shader_program_path}.geom') as file:
                geometry_shader = file.read()
        else:
            geometry_shader = None
            
        if tess:
            with open(f'{shader_program_path}.tesc') as file:
                tessellation_control_shader = file.read()
            with open(f'{shader_program_path}.tese') as file:
                tessellation_evaluation_shader = file.read()
        else:
            tessellation_control_shader = None
            tessellation_evaluation_shader = None  
            
        program = self._gl_context.program(vertex_shader = vertex_shader, 
                                           fragment_shader = fragment_shader,
                                           geometry_shader = geometry_shader, 
                                           tess_control_shader = tessellation_control_shader,
                                           tess_evaluation_shader = tessellation_evaluation_shader)
        return program

            
    def transform(self,  transformations: glm.fmat4x4) -> glm.fmat4x4:
        self._model_matrix *= transformations
    
    def render(self, mode = moderngl.TRIANGLES) -> None:
        self._vao.render(mode)
        
    def destroy(self) -> None:
        self._shader_program.release()
        for texture in self._textures:
            texture.destroy()
        
         
class CompanionCubeModel(Model):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        # shader program
        self._shader_program = self.get_shader_program('shaders/companionCube')
        # cube mesh
        self._mesh = TexturedCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '2f 3f 3f'
        attributes = ['in_texcoord', 'in_normal', 'in_position']
        self.set_vao(format, attributes)
        # texture
        texture = Texture(context = self._gl_context, path = 'textures/companion_cube.png')
        self.add_texture(texture, 0)
        

class ColoredCubeModel(Model):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        # shader program
        self._shader_program = self.get_shader_program('shaders/color_gradiant')
        # cube mesh
        self._mesh = SolidCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '3f 3f'
        attributes = ['in_color', 'in_position']
        self.set_vao(format, attributes)
        

class ColoredCubeModel(Model):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        # shader program
        self._shader_program = self.get_shader_program('shaders/color_gradiant')
        # cube mesh
        self._mesh = SolidCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '3f 3f'
        attributes = ['in_color', 'in_position']
        self.set_vao(format, attributes)
        
        
# must be rendered with LINE STRIP
class WireCubeModel(Model):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        # shader program
        self._shader_program = self.get_shader_program('shaders/outline')
        # cube mesh
        self._mesh = WireCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '3f 3f'
        attributes = ['in_color', 'in_position']
        self.set_vao(format, attributes)
         
        
        
        