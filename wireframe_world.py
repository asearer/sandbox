from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
import sys
import math
import random  # Import the random module for introducing randomness

# Variables for animation
angle = 0
orbit_radius = 3  # Radius of the orbit
rotation_speed = 0.5  # Adjust rotation speed as needed (lower values mean slower rotation)

# List to store the positions of the spheres
sphere_positions = []

def draw_sphere(x, y, z, rotation_angle):
    # Draw a sphere at the specified position and rotate it around its own axis
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, 1, 1, 1)  # Rotate around own axis
    glutWireSphere(0.5, 10, 10)  # Adjust radius as needed
    glPopMatrix()

def check_collision():
    # Check collision between spheres
    for i in range(len(sphere_positions)):
        for j in range(i + 1, len(sphere_positions)):
            # Calculate distance between spheres
            dist = math.sqrt(sum((sphere_positions[i][k] - sphere_positions[j][k]) ** 2 for k in range(3)))
            if dist < 1.0:  # Assuming sphere radius is 0.5
                print("Collision detected!")

def draw():
    global angle
    global sphere_positions
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)
    
    # Clear the sphere_positions list before updating it
    sphere_positions = []
    
    draw_sphere(0, 0, 0, angle)
    
    # Draw spheres in concentric circles around the central sphere
    num_orbits = 4  # Number of orbits
    num_spheres_per_orbit = 8  # Number of spheres per orbit
    
    for i in range(num_orbits):
        orbit_angle = angle + i * 45  # Offset the angle for each orbit
        
        for j in range(num_spheres_per_orbit):
            sphere_angle = j * (360 / num_spheres_per_orbit)  # Angle for placing spheres evenly
                
            x = orbit_radius * math.cos(math.radians(orbit_angle))
            z = orbit_radius * math.sin(math.radians(orbit_angle))
            y = orbit_radius * math.sin(math.radians(sphere_angle)) * math.cos(math.radians(orbit_angle))  # Adjust y position
            
            draw_sphere(x, y, z, angle)
            
            # Append the position of each sphere to the list
            sphere_positions.append((x, y, z))
    
    angle += rotation_speed  # Decreased speed
    
    check_collision()  # Check collision between spheres
    
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
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()

if __name__ == "__main__":
    main()
