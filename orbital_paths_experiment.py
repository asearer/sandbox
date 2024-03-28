#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:04:32 2024

@author: asearer
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Variables for animation
angle = 0
rotation_speed = 0.5

# Orbital parameters for smaller spheres
orbit_radius_x = 2
orbit_radius_y = 1.5

def draw_sphere(x, y, z, rotation_angle, radius):
    """
    Draw a sphere at the specified position and rotate it around its own axis.

    Parameters:
    - x, y, z (float): Position coordinates of the sphere.
    - rotation_angle (float): Angle of rotation for the sphere.
    - radius (float): Radius of the sphere.
    """
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, 1, 1, 1)
    glutWireSphere(radius, 10, 10)  # Use glutWireSphere for wireframe
    glPopMatrix()

def draw():
    """
    Main drawing function.
    """
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    # Draw the central rotating sphere
    draw_sphere(0, 0, 0, angle, 1.0)

    # Draw smaller orbital spheres with elliptical paths
    x1 = orbit_radius_x * math.cos(math.radians(angle))
    y1 = orbit_radius_y * math.sin(math.radians(angle))
    draw_sphere(x1, y1, 0, angle * 2, 0.3)

    x2 = orbit_radius_x * math.cos(math.radians(angle + 180))
    y2 = orbit_radius_y * math.sin(math.radians(angle + 180))
    draw_sphere(x2, y2, 0, angle * 2, 0.3)

    angle += rotation_speed

    glutSwapBuffers()

def main():
    """
    Main function to initialize OpenGL and start the main loop.
    """
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Rotating and Orbiting Spheres")
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()

if __name__ == "__main__":
    main()
