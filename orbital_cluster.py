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

# Constants for control panel
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 20
SLIDER_MARGIN = 10
SLIDER_MAX = 100

# Variables for animation
angle = 0
orbit_radius_x = 3  # Semi-major axis
orbit_radius_y = 1.5  # Semi-minor axis
rotation_speed = 0.5

# List to store the positions and velocities of the spheres
sphere_states = []

# List to store collision history
collision_history = []

# Index of the central sphere
central_sphere_index = 0

# Flag to indicate if the user is dragging a sphere
dragging_sphere = False

# Slider values
slider_orbit_radius_x = 0
slider_orbit_radius_y = 0
slider_rotation_speed = 0

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

def draw_control_panel():
    """
    Draw the control panel.
    """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(0.2, 0.2, 0.2)
    glRectf(WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN, SLIDER_MARGIN, WINDOW_WIDTH - SLIDER_MARGIN, SLIDER_MARGIN + SLIDER_HEIGHT)

    # Draw orbit radius X slider
    glColor3f(0.8, 0.2, 0.2)
    glRectf(WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN, SLIDER_MARGIN, WINDOW_WIDTH - SLIDER_MARGIN, SLIDER_MARGIN + SLIDER_HEIGHT)
    glColor3f(0.5, 0.5, 0.5)
    glRectf(WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN + slider_orbit_radius_x, SLIDER_MARGIN, WINDOW_WIDTH - SLIDER_MARGIN + slider_orbit_radius_x, SLIDER_MARGIN + SLIDER_HEIGHT)

    # Draw orbit radius Y slider
    glColor3f(0.2, 0.8, 0.2)
    glRectf(WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN, SLIDER_MARGIN * 3 + SLIDER_HEIGHT, WINDOW_WIDTH - SLIDER_MARGIN, SLIDER_MARGIN * 3 + SLIDER_HEIGHT * 2)
    glColor3f(0.5, 0.5, 0.5)
    glRectf(WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN + slider_orbit_radius_y, SLIDER_MARGIN * 3 + SLIDER_HEIGHT, WINDOW_WIDTH - SLIDER_MARGIN + slider_orbit_radius_y, SLIDER_MARGIN * 3 + SLIDER_HEIGHT * 2)

    # Draw rotation speed slider
    glColor3f(0.2, 0.2, 0.8)
    glRectf(WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN, SLIDER_MARGIN * 5 + SLIDER_HEIGHT * 2, WINDOW_WIDTH - SLIDER_MARGIN, SLIDER_MARGIN * 5 + SLIDER_HEIGHT * 3)
    glColor3f(0.5, 0.5, 0.5)
    glRectf(WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN + slider_rotation_speed, SLIDER_MARGIN * 5 + SLIDER_HEIGHT * 2, WINDOW_WIDTH - SLIDER_MARGIN + slider_rotation_speed, SLIDER_MARGIN * 5 + SLIDER_HEIGHT * 3)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def check_collision():
    """
    Check collisions between spheres and track them within a defined time frame.
    """
    global collision_history
    global angle
    global sphere_states

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

    # Update velocities of the impacted spheres
    for pos1, pos2, vel1, vel2, time in collision_history:
        for i in range(len(sphere_states)):
            if sphere_states[i][0] == pos1:
                # Increase velocity slightly
                sphere_states[i] = (pos1, (vel1[0] * 1.01, vel1[1] * 1.01, vel1[2] * 1.01))
            elif sphere_states[i][0] == pos2:
                # Increase velocity slightly
                sphere_states[i] = (pos2, (vel2[0] * 1.01, vel2[1] * 1.01, vel2[2] * 1.01))

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

    # Draw the control panel
    draw_control_panel()

    glutSwapBuffers()

def mouse(button, state, x, y):
    global dragging_sphere

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            print("Mouse clicked at", x, y)
            # Check if the mouse click is within the vicinity of any sphere except the central one
            viewport = glGetIntegerv(GL_VIEWPORT)
            viewport_x, viewport_y = viewport[2], viewport[3]
            win_x = x
            win_y = viewport_y - y
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            _, _, z_near, _ = gluUnProject(win_x, win_y, 0, modelview, projection, viewport)
            _, _, z_far, _ = gluUnProject(win_x, win_y, 1, modelview, projection, viewport)

            for i, (pos, _) in enumerate(sphere_states):
                depth = pos[2]
                z_min = depth - 0.5
                z_max = depth + 0.5
                if z_min <= z_near <= z_max or z_min <= z_far <= z_max:
                    if i != central_sphere_index:
                        dragging_sphere = i
                        print("Dragging sphere index:", dragging_sphere)
                        break
    elif button == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:
            dragging_sphere = True

def motion(x, y):
    global dragging_sphere

    if dragging_sphere is not False:
        print("Mouse motion while dragging sphere:", x, y)
        viewport = glGetIntegerv(GL_VIEWPORT)
        viewport_x, viewport_y = viewport[2], viewport[3]
        win_x = x
        win_y = viewport_y - y
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        _, _, z_near, _ = gluUnProject(win_x, win_y, 0, modelview, projection, viewport)
        _, _, z_far, _ = gluUnProject(win_x, win_y, 1, modelview, projection, viewport)

        depth = sphere_states[dragging_sphere][0][2]
        z_min = depth - 0.5
        z_max = depth + 0.5
        new_depth = (z_near + z_far) / 2
        if new_depth < z_min:
            new_depth = z_min
        elif new_depth > z_max:
            new_depth = z_max

        x, y, _ = gluUnProject(win_x, win_y, new_depth, modelview, projection, viewport)

        sphere_states[dragging_sphere] = ((x, y, new_depth), sphere_states[dragging_sphere][1])

def handle_control_panel_motion(x, y):
    global slider_orbit_radius_x
    global slider_orbit_radius_y
    global slider_rotation_speed

    if WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN <= x <= WINDOW_WIDTH - SLIDER_MARGIN:
        if SLIDER_MARGIN <= y <= SLIDER_MARGIN + SLIDER_HEIGHT:
            slider_orbit_radius_x = x - (WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN)
        elif SLIDER_MARGIN * 3 + SLIDER_HEIGHT <= y <= SLIDER_MARGIN * 3 + 2 * SLIDER_HEIGHT:
            slider_orbit_radius_y = x - (WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN)
        elif SLIDER_MARGIN * 5 + 2 * SLIDER_HEIGHT <= y <= SLIDER_MARGIN * 5 + 3 * SLIDER_HEIGHT:
            slider_rotation_speed = x - (WINDOW_WIDTH - SLIDER_WIDTH - SLIDER_MARGIN)

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
    gluPerspective(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutPassiveMotionFunc(handle_control_panel_motion)  # Track mouse motion for control panel
    glutMainLoop()

if __name__ == "__main__":
    main()
