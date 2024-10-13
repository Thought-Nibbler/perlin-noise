from ctypes import sizeof
import sys

import numpy as np

from OpenGL.GL import *
import glfw

class Shader:
    def __init__(self):
        self.handle = glCreateProgram()

    def attach_shader(self, content, type):
        shader = glCreateShader(type)
        glShaderSource(shader, [content])
        glCompileShader(shader)

        status = ctypes.c_uint(GL_UNSIGNED_INT)
        glGetShaderiv(shader, GL_COMPILE_STATUS, status)
        if not status:
            print(glGetShaderInfoLog(shader).decode("utf-8"), file=sys.stderr)
            glDeleteShader(shader)
            return False

        glAttachShader(self.handle, shader)
        glDeleteShader(shader)
        return True

    def link(self):
        glLinkProgram(self.handle)
        status = ctypes.c_uint(GL_UNSIGNED_INT)
        glGetProgramiv(self.handle, GL_LINK_STATUS, status)
        if not status:
            print(glGetProgramInfoLog(self.handle).decode("utf-8"), file=sys.stderr)
            return False
        return True

    def use(self):
        glUseProgram(self.handle)

    def unuse(self):
        glUseProgram(0)

vert = """
#version 450

layout (location = 0) in vec2 vertex;
layout (location = 1) in vec3 color;

layout (location = 0) out vec3 outColor;

void main() {
    gl_Position = vec4(vertex, 0, 1);
    outColor = color;
}
"""

frag = """
#version 450

layout (location = 0) in vec3 color;

layout (location = 0) out vec4 outColor;

void main() {
    outColor = vec4(color, 1);
}
"""

def main():
    if not glfw.init():
        raise RuntimeError("failed to initialize GLFW")

    window = glfw.create_window(700, 700, "triangle", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("failed to create GLFWwindow")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)
    glfw.make_context_current(window)

    # シェーダの生成
    program = Shader()
    program.attach_shader(vert, GL_VERTEX_SHADER)
    program.attach_shader(frag, GL_FRAGMENT_SHADER)
    program.link()

    data = np.array([
        0, 1,  1, 0, 0, # 頂点(0, 1)，  色(1, 0, 0)
        1, -1,  0, 1, 0,# 頂点(1, -1)， 色(0, 1, 0)
        -1, -1, 0, 0, 1 # 頂点(-1, -1)，色(0, 0, 1)
    ], dtype=GLfloat)

    # GPU上にバッファを生成
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.itemsize * data.size, (GLfloat * data.size)(*data), GL_STATIC_DRAW)

    # バッファのデータとシェーダの変数を関連付け
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(GLfloat) * 5, GLvoidp(0))
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(GLfloat) * 5, GLvoidp(sizeof(GLfloat) * 2))
    glBindVertexArray(0)

    glClearColor(0, 0, 0, 1)
    while glfw.window_should_close(window) == glfw.FALSE:
        glClear(GL_COLOR_BUFFER_BIT)

        # 描画
        program.use()
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)
        program.unuse()

        glfw.swap_buffers(window)
        glfw.wait_events()
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteProgram(program.handle)

    glfw.terminate()

if __name__ == "__main__":
    main()
