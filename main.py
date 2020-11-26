from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np

# VERTS           COLOR
rect_verts = np.array([0.5, 0.5, 0.5, 1, 0, 0,
                       0.5, -0.5, 0.5, 0, 1, 0,
                       -0.5, -0.5, 0.5, 0, 0, 1,
                       -0.5, 0.5, 0.5, 1, 1, 0,
                       0.5, 0.5, -0.5, 1, 0, 1,
                       0.5, -0.5, -0.5, 0, 1, 1,
                       -0.5, -0.5, -0.5, 1, 1, 1,
                       -0.5, 0.5, -0.5, 0, 0, 0], dtype=np.float32)

rect_indices = np.array([  # front
    0, 1, 3,
    1, 2, 3,
    # left
    4, 5, 0,
    5, 1, 0,
    # back
    7, 6, 4,
    6, 5, 4,
    # right
    3, 2, 7,
    2, 6, 7,
    # top
    1, 5, 2,
    5, 6, 2,
    # bottom
    4, 0, 7,
    0, 3, 7], dtype=np.uint32)

pyramid_verts = np.array([0, 0, 0, 1, 0, 0,
                          0, 0, -1, 1, 0, 0,
                          1, 0, 0, 1, 0, 0,
                          1, 0, -1, 1, 0, 0,
                          0.5, 1, -0.5, 1, 0, 0], dtype=np.float32)

pyramid_indices = np.array([0, 1, 2,
                            1, 2, 3,
                            0, 1, 4,
                            1, 2, 4,
                            2, 3, 4,
                            4, 0, 4], dtype=np.uint32)

octahedron_verts = np.array([0, 1, 0, 1, 0, 0,
                             0, -1, 0, 1, 0, 0,
                             1, 0, 1, 1, 0, 0,
                             -1, 0, 1, 1, 0, 0,
                             1, 0, -1, 1, 0, 0,
                             -1, 0, -1, 1, 0, 0,
                             ], dtype=np.float32)

octahedron_indices = np.array([0, 2, 3,
                               0, 2, 4,
                               0, 3, 5,
                               0, 4, 5,
                               1, 2, 3,
                               1, 2, 4,
                               1, 3, 5,
                               1, 4, 5,
                               ], dtype=np.uint32)

icosahedron_vert = np.array([0, 2, 0, 1, 0, 0,
                             0, 1, -2, 1, 0, 0,
                             2, 1, -1, 1, 0, 0,
                             -2, 1, -1, 1, 0, 0,
                             1, 1, 2, 1, 0, 0,
                             -1, 1, 2, 1, 0, 0,

                             0, -2, 0, 1, 0, 0,
                             0, -1, -2, 1, 0, 0,
                             2, -1, -1, 1, 0, 0,
                             -2, -1, -1, 1, 0, 0,
                             1, -1, 2, 1, 0, 0,
                             -1, -1, 2, 1, 0, 0], dtype=np.float32)

icosahedron_indices = np.array([0, 1, 2,
                                0, 1, 3,
                                0, 2, 4,
                                0, 3, 5,
                                0, 4, 5,
                                6, 7, 8,
                                6, 7, 9,
                                6, 8, 10,
                                6, 9, 11,
                                6, 10, 11,
                                1, 7, 9,
                                1, 3, 9
                                ], dtype=np.uint32)

all_verts = [icosahedron_vert, octahedron_verts, rect_verts, pyramid_verts]

all_indices = [icosahedron_indices, octahedron_indices, rect_indices, pyramid_indices]


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        # Perspective Projection Matrix
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

        self.cube_pos = glm.vec3(0, 0, -3)
        self.camera_pos = glm.vec3(0, 0, 0)
        self.cam_pitch = 0
        self.cam_yaw = 0
        self.cam_roll = 0
        self.current_position = 2

    def wireframe_mode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filled_mode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def get_info(self):
        return [self.cube_pos, self.camera_pos]

    def translate_cube(self, x, y, z):
        self.cube_pos = glm.vec3(x, y, z)

    def translate_camera(self, x, y, z):
        self.camera_pos = glm.vec3(x, y, z)

    def roll_camera(self, x):
        self.cam_roll = x

    def pitch_camera(self, x):
        self.cam_pitch = x

    def yaw_camera(self, x):
        self.cam_yaw = x

    def next_figure(self):
        self.current_position = (self.current_position + 1) % len(all_verts)
        self.create_objects()

    def set_shaders(self, vertex_shader, frag_shader):

        if vertex_shader is not None or frag_shader is not None:
            self.active_shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),
                                                compileShader(frag_shader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

        glUseProgram(self.active_shader)

    def create_objects(self):

        self.VBO = glGenBuffers(1)  # Vertex Buffer Object
        self.EBO = glGenBuffers(1)  # Element Buffer Object
        self.VAO = glGenVertexArrays(1)  # Vertex Array Object

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, all_verts[self.current_position].nbytes, all_verts[self.current_position],
                     GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, all_indices[self.current_position].nbytes,
                     all_indices[self.current_position], GL_STATIC_DRAW)

        # Atributo de posicion de vertices
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Atributo de color de vertices
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)

    def render(self):
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        i = glm.mat4(1)
        # Model/Object matrix: translate * rotate * scale
        translate = glm.translate(i, self.cube_pos)
        pitch = glm.rotate(i, glm.radians(0), glm.vec3(1, 0, 0))
        yaw = glm.rotate(i, glm.radians(0), glm.vec3(0, 1, 0))
        roll = glm.rotate(i, glm.radians(0), glm.vec3(0, 0, 1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, glm.vec3(1, 1, 1))
        model = translate * rotate * scale

        # View Matrix
        # glm.lookAt( eye, center, up)
        cam_translate = glm.translate(i, self.camera_pos)
        cam_pitch = glm.rotate(i, glm.radians(self.cam_pitch), glm.vec3(1, 0, 0))
        cam_yaw = glm.rotate(i, glm.radians(self.cam_yaw), glm.vec3(0, 1, 0))
        cam_roll = glm.rotate(i, glm.radians(self.cam_roll), glm.vec3(0, 0, 1))
        cam_rotate = cam_pitch * cam_yaw * cam_roll
        view = glm.inverse(cam_translate * cam_rotate)

        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"),
                               1, GL_FALSE, glm.value_ptr(model))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"),
                               1, GL_FALSE, glm.value_ptr(view))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projection"),
                               1, GL_FALSE, glm.value_ptr(self.projection))

        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
