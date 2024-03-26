#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 08:15:30 2024

@author: asearer
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
import sys
import math
import random  

# Variables for animation
angle = 0
orbit_radius_x = 3  # Semi-major axis
orbit_radius_y = 1.5  # Semi-minor axis
rotation_speed = 0.5  

# List to store the positions of the spheres
sphere_positions = []

def draw_sphere(x, y, z, rotation_angle):
    # Draw a sphere at the specified position and rotate it around its own axis
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, 1, 1, 1)  
    glutWireSphere(0.5, 10, 10)  
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
    
    # Draw spheres in elliptical orbits around the central sphere
    num_orbits = 4  
    num_spheres_per_orbit = 8  
    
    for i in range(num_orbits):
        orbit_angle = angle + i * 45 
        
        for j in range(num_spheres_per_orbit):
            sphere_angle = j * (360 / num_spheres_per_orbit)  
                
            x = orbit_radius_x * math.cos(math.radians(orbit_angle)) * math.cos(math.radians(sphere_angle))
            y = orbit_radius_y * math.sin(math.radians(orbit_angle)) * math.cos(math.radians(sphere_angle))
            z = orbit_radius_y * math.sin(math.radians(sphere_angle))
            
            draw_sphere(x, y, z, angle)
            
            # Append the position of each sphere to the list
            sphere_positions.append((x, y, z))
    
    angle += rotation_speed  
    
    check_collision()  
    
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
