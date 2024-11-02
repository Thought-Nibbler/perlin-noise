"""OpenGL で三角形描画するスクリプト"""
import ctypes
from pathlib import Path
import sys

import numpy as np

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

    def create_vbo(self, data: np.ndarray) -> np.uintc:
        """
        VBO (Vertex Buffer Object) を生成する。

        参考 : `頂点バッファの基礎 <https://wgld.org/d/webgl/w009.html>`_

        Parameters
        ----------
        data : np.ndarray
            _description_

        Returns
        -------
        np.uintc
            生成した VBO (Vertex Buffer Object) 。
        """
        vbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        size = data.itemsize * data.size
        data_ptr = (gl.GLfloat * data.size)(*data)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, size, data_ptr, gl.GL_STATIC_DRAW)

        return vbo

    def create_vao(self) -> np.uintc:
        """
        VAO (Vertex Array Object) を生成する。

        参考 : `VAO(vertex array object) <https://wgld.org/d/webgl/w073.html>`_

        Returns
        -------
        np.uintc
            生成した VAO (Vertex Array Object) 。
        """
        vao = gl.glGenVertexArrays(1)

        gl.glBindVertexArray(vao)

        # VBO の頂点座標部分の設定
        idx = 0
        size = 2  # 2 次元座標
        data_type = gl.GL_FLOAT
        normalized = gl.GL_FALSE  # 正規化しない
        stride = ctypes.sizeof(gl.GLfloat) * 5  # 1 頂点あたり 5 要素ある
        pointer = gl.GLvoidp(0)  # 頂点座標は VBO の先頭から始まる
        gl.glEnableVertexAttribArray(idx)
        gl.glVertexAttribPointer(idx, size, data_type, normalized, stride, pointer)

        # VBO の色情報部分の設定
        idx = 1
        size = 3  # RGB 値
        data_type = gl.GL_FLOAT
        normalized = gl.GL_FALSE  # 正規化しない
        stride = ctypes.sizeof(gl.GLfloat) * 5  # 1 頂点あたり 5 要素ある
        pointer = gl.GLvoidp(ctypes.sizeof(gl.GLfloat) * 2)  # 色情報は VBO の 3 番目から始まる
        gl.glEnableVertexAttribArray(idx)
        gl.glVertexAttribPointer(idx, size, data_type, normalized, stride, pointer)

        gl.glBindVertexArray(0)  # 一旦 VAO の結合を解除する NOTE: 必要なのか？

        return vao

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

    vbo = program.create_vbo(data)
    vao = program.create_vao()

    gl.glClearColor(0, 0, 0, 1)

    while glfw.window_should_close(window) == glfw.FALSE:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # 描画
        program.use()
        gl.glBindVertexArray(vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        gl.glBindVertexArray(0)
        program.unuse()

        glfw.swap_buffers(window)
        glfw.wait_events()

    gl.glDeleteVertexArrays(1, [vao])
    gl.glDeleteBuffers(1, [vbo])
    gl.glDeleteProgram(program.handle)

    glfw.terminate()


if __name__ == "__main__":
    main()
