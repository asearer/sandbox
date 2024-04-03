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
    """
    Draw an arm segment as a cylinder.

    Args:
        length (float): The length of the arm segment.
    """
    glutWireCylinder(0.1, length, 20, 20)

def draw_joint():
    """
    Draw a joint as a sphere.
    """
    glutWireSphere(0.15, 20, 20)

def display():
    """
    Display function called by OpenGL to render the scene.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)

    glPushMatrix()
    glColor3f(1, 1, 1)  # White color for wireframe

    # Calculate total arm length
    total_arm_length = 2 + 0.15 + 1.5  # Base segment + joint + second segment

    # Calculate the amount to translate to center the arm simulation
    center_translation = total_arm_length / 2

    # Translate the entire arm to the center and then move it to the right
    glTranslatef(-center_translation + 1.5, 0, 0)

    # Draw the base segment
    draw_arm_segment(2)

    # Draw the first joint at the pole
    glPushMatrix()
    glTranslatef(0, 0, 2)
    draw_joint()
    glPopMatrix()

    # Draw the second segment
    glTranslatef(0, 0, 2)
    draw_arm_segment(0.15)

    # Draw the second joint at the pole
    glPushMatrix()
    glTranslatef(0, 0, 0.15)
    draw_joint()
    glPopMatrix()

    # Draw the third segment
    glTranslatef(0, 0, 0.15)
    draw_arm_segment(1.5)

    glPopMatrix()

    glutSwapBuffers()

def reshape(width, height):
    """
    Reshape function to handle window resizing.

    Args:
        width (int): The new width of the window.
        height (int): The new height of the window.
    """
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    """
    Main function to initialize OpenGL and start the main loop.
    """
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400, 400)
    glutCreateWindow(b"Single-jointed Arm Simulation")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutMainLoop()

if __name__ == "__main__":
    main()
