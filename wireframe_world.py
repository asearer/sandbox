from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
import sys

# Variables for animation
angle = 0

def draw_cube():
    global angle
    
    glPushMatrix()
    
    # Rotate the cube around the y-axis
    glRotatef(angle, 0, 1, 0)
    
    glBegin(GL_LINES)
    # Front face
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    
    # Back face
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    
    # Connect front and back faces
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glEnd()
    
    glPopMatrix()

def draw():
    global angle
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)  # Eye position, center position, up vector
    
    # Increment rotation angle
    angle += 1
    
    draw_cube()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Wireframe World")
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 50.0)  # Field of view, aspect ratio, near clipping plane, far clipping plane
    glMatrixMode(GL_MODELVIEW)
    glutDisplayFunc(draw)
    glutIdleFunc(draw)  # Register draw function as idle function for continuous animation
    glutMainLoop()

if __name__ == "__main__":
    main()
