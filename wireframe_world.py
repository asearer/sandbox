from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
import sys
import math

# Variables for animation
angle = 0
orbit_radius = 3  # Radius of the orbit

def draw_sphere(x, y, z, rotation_angle):
    # Draw a sphere at the specified position and rotate it around its own axis
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, 1, 1, 1)  # Rotate around own axis
    glutWireSphere(0.5, 10, 10)  # Adjust radius as needed
    glPopMatrix()

def draw():
    global angle
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)  # Eye position, center position, up vector
    
    # Draw the central sphere and rotate it
    draw_sphere(0, 0, 0, angle)
    
    # Calculate positions and rotation angles of orbiting spheres
    x1 = orbit_radius * math.cos(math.radians(angle))
    z1 = orbit_radius * math.sin(math.radians(angle))
    x2 = orbit_radius * math.cos(math.radians(angle + 120))  # Offset the angle for the second orbiting sphere
    z2 = orbit_radius * math.sin(math.radians(angle + 120))
    
    # Draw the orbiting spheres and rotate them
    draw_sphere(x1, 0, z1, angle)
    draw_sphere(x2, 0, z2, angle)
    draw_sphere(-x1, 0, -z1, angle)
    
    # Increment rotation angle
    angle += 1
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Rotating and Orbiting Spheres")
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
