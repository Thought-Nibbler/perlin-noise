"""OpenGL で三角形描画するスクリプト"""
import ctypes
from pathlib import Path
import sys

import numpy as np

from OpenGL.GL import *
import OpenGL.GL as gl
import glfw


class Shader:
    """_summary_"""

    def __init__(self) -> None:
        self.handle = gl.glCreateProgram()

    def attach_shader(self, shader_file: Path, type: gl.constant.IntConstant) -> bool:
        """
        _summary_

        Parameters
        ----------
        shader_file : Path
            _description_
        type : gl.constant.IntConstant
            _description_

        Returns
        -------
        bool
            _description_
        """
        with shader_file.open() as f:
            content = f.read()

        shader = gl.glCreateShader(type)
        gl.glShaderSource(shader, [content])
        gl.glCompileShader(shader)

        status = ctypes.c_uint(gl.GL_UNSIGNED_INT)
        gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS, status)
        if not status:
            print(gl.glGetShaderInfoLog(shader).decode("utf-8"), file=sys.stderr)
            gl.glDeleteShader(shader)
            return False

        gl.glAttachShader(self.handle, shader)
        gl.glDeleteShader(shader)

        return True

    def link(self) -> bool:
        """
        _summary_

        Returns
        -------
        bool
            _description_
        """
        gl.glLinkProgram(self.handle)
        status = ctypes.c_uint(gl.GL_UNSIGNED_INT)
        gl.glGetProgramiv(self.handle, gl.GL_LINK_STATUS, status)
        if not status:
            print(gl.glGetProgramInfoLog(self.handle).decode("utf-8"), file=sys.stderr)
            return False
        return True

    def use(self) -> None:
        """_summary_"""
        gl.glUseProgram(self.handle)

    def unuse(self) -> None:
        """_summary_"""
        gl.glUseProgram(0)


def main() -> None:
    """
    _summary_

    Raises
    ------
    RuntimeError
        _description_
    RuntimeError
        _description_
    """
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
    program.attach_shader(Path('./src/vertex.glsl'), gl.GL_VERTEX_SHADER)
    program.attach_shader(Path('./src/fragment.glsl'), gl.GL_FRAGMENT_SHADER)
    program.link()

    points = np.array([[0, 1],
                       [1, -1],
                       [-1, -1]])
    colors = np.array([[1, 0, 0],
                       [0, 1, 0],
                       [0, 0, 1]])
    data = np.array([*points[0], *colors[0],
                     *points[1], *colors[1],
                     *points[2], *colors[2]],
                    dtype=gl.GLfloat)

    # GPU上にバッファを生成
    vbo = gl.glGenBuffers(1)  # 頂点バッファオブジェクト（vbo）を 1 つ生成する
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, data.itemsize * data.size, (GLfloat * data.size)(*data), GL_STATIC_DRAW)

    # バッファのデータとシェーダの変数を関連付け
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 5, GLvoidp(0))
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, ctypes.sizeof(GLfloat) * 5, GLvoidp(ctypes.sizeof(GLfloat) * 2))
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
