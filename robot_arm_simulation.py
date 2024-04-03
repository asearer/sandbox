#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 16:08:35 2024

@author: asearer
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_arm_segment(length):
    glutWireCylinder(0.1, length, 20, 20)

def draw_joint():
    glutWireSphere(0.15, 20, 20)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)

    glPushMatrix()
    glColor3f(1, 1, 1)  # White color for wireframe

    # Draw the base segment
    draw_arm_segment(2)

    # Draw the first joint
    glTranslatef(0, 0, 2)
    draw_joint()

    # Draw the second segment
    glRotatef(45, 0, 1, 0)
    glTranslatef(0, 0, 1.5)
    draw_arm_segment(1.5)

    # Draw the second joint
    glTranslatef(0, 0, 1.5)
    draw_joint()

    # Draw the third segment
    glRotatef(45, 0, 1, 0)
    glTranslatef(0, 0, 1)
    draw_arm_segment(1)

    glPopMatrix()

    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400, 400)
    glutCreateWindow(b"Multi-jointed Arm Simulation")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutMainLoop()

if __name__ == "__main__":
    main()
