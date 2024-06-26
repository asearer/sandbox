#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 16:08:35 2024

@author: asearer
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Define global variables
rotation_x = 0.0
rotation_y = 0.0
mouse_x = 0
mouse_y = 0
is_dragging = False

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
    global rotation_x, rotation_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)

    # Apply rotation
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)

    glPushMatrix()
    glColor3f(1, 1, 1)  # White color for wireframe

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

    # Draw the second joint
    glPushMatrix()
    glTranslatef(0, 0, 2 + -0.25)
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

def special_key_pressed(key, x, y):
    """
    Function to handle special key presses, such as arrow keys for rotation.

    Args:
        key (int): The code of the special key pressed.
        x (int): The x-coordinate of the mouse position when the key was pressed.
        y (int): The y-coordinate of the mouse position when the key was pressed.
    """
    global rotation_x, rotation_y

    # Rotate the view based on the arrow key pressed
    if key == GLUT_KEY_UP:
        rotation_x += 5.0
    elif key == GLUT_KEY_DOWN:
        rotation_x -= 5.0
    elif key == GLUT_KEY_LEFT:
        rotation_y -= 5.0
    elif key == GLUT_KEY_RIGHT:
        rotation_y += 5.0

    glutPostRedisplay()

def mouse(button, state, x, y):
    """
    Function to handle mouse events.

    Args:
        button (int): The button pressed (GLUT_LEFT_BUTTON, GLUT_RIGHT_BUTTON, or GLUT_MIDDLE_BUTTON).
        state (int): The state of the button (GLUT_UP or GLUT_DOWN).
        x (int): The x-coordinate of the mouse position when the button was pressed.
        y (int): The y-coordinate of the mouse position when the button was pressed.
    """
    global is_dragging, mouse_x, mouse_y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            is_dragging = True
            mouse_x = x
            mouse_y = y
        elif state == GLUT_UP:
            is_dragging = False

def mouse_motion(x, y):
    """
    Function to handle mouse motion when a button is pressed.

    Args:
        x (int): The new x-coordinate of the mouse position.
        y (int): The new y-coordinate of the mouse position.
    """
    global mouse_x, mouse_y, rotation_x, rotation_y

    if is_dragging:
        rotation_x += (y - mouse_y) * 0.5
        rotation_y += (x - mouse_x) * 0.5

        mouse_x = x
        mouse_y = y

        glutPostRedisplay()

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
    glutSpecialFunc(special_key_pressed)
    glutMouseFunc(mouse)  # Register mouse callback
    glutMotionFunc(mouse_motion)  # Register mouse motion callback

    glutMainLoop()

if __name__ == "__main__":
    main()
