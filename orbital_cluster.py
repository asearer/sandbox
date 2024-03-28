#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 08:15:30 2024

@author: asearer
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Variables for animation
angle = 0
orbit_radius_x = 3  # Semi-major axis
orbit_radius_y = 1.5  # Semi-minor axis
rotation_speed = 0.5

# List to store the positions and velocities of the spheres
sphere_states = []

# List to store collision history
collision_history = []

def draw_sphere(x, y, z, rotation_angle):
    """
    Draw a sphere at the specified position and rotate it around its own axis.

    Parameters:
    - x, y, z (float): Position coordinates of the sphere.
    - rotation_angle (float): Angle of rotation for the sphere.
    """
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, 1, 1, 1)
    glutWireSphere(0.5, 10, 10)  # Use glutWireSphere for wireframe
    glPopMatrix()

def check_collision():
    """
    Check collisions between spheres and track them within a defined time frame.
    """
    global collision_history
    collision_time_frame = 10  # Time frame to track collisions in seconds

    # Check collision between spheres
    for i in range(len(sphere_states)):
        for j in range(i + 1, len(sphere_states)):
            pos1, vel1 = sphere_states[i]
            pos2, vel2 = sphere_states[j]
            # Calculate distance between spheres
            dist = math.sqrt(sum((pos1[k] - pos2[k]) ** 2 for k in range(3)))
            if dist < 1.0:  # Assuming sphere radius is 0.5
                collision_history.append((pos1, pos2, vel1, vel2, angle))

    # Remove collisions that are older than the time frame
    collision_history = [(pos1, pos2, vel1, vel2, time) for pos1, pos2, vel1, vel2, time in collision_history if angle - time <= collision_time_frame]

    # Print colliding pairs
    if collision_history:
        print("Collisions within the last", collision_time_frame, "seconds:")
        for pos1, pos2, vel1, vel2, time in collision_history:
            print("Collision between spheres at positions", pos1, "and", pos2, "at angle", time, "with velocities", vel1, "and", vel2)

def draw():
    """
    Main drawing function.
    """
    global angle
    global sphere_states

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)

    # Clear the sphere_states list before updating it
    sphere_states = []

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

            # Append the position and velocity of each sphere to the list
            sphere_states.append(((x, y, z), (0, 0, 0)))  # Velocity initialized as zero

    # Update velocities (positions from previous frame are stored)
    for i in range(len(sphere_states)):
        pos, _ = sphere_states[i]
        sphere_states[i] = (pos, (pos[0] - sphere_states[i][0][0], pos[1] - sphere_states[i][0][1], pos[2] - sphere_states[i][0][2]))

    angle += rotation_speed

    check_collision()

    glutSwapBuffers()

def main():
    """
    Main function to initialize OpenGL and start the main loop.
    """
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

