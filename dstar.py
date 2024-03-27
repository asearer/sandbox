import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math

def draw_wireframe_sphere(radius=1.0, num_segments_per_hemisphere=10):
    """
    Render a wireframe representation of a spherical model.

    Args:
    - radius (float): The radius of the wireframe sphere.
    - num_segments_per_hemisphere (int): The number of segments used per hemisphere to approximate the sphere.

    Note: This function draws a wireframe sphere with the specified radius and number of segments per hemisphere.
    """

    # Set color to white for drawing lines
    glColor3f(1.0, 1.0, 1.0)

    # Calculate the coordinates of the top pole
    top_pole = [0, radius, 0]

    # Calculate the coordinates of the bottom pole
    bottom_pole = [0, -radius, 0]

    # Draw the line passing from pole to pole
    glBegin(GL_LINES)
    glVertex3f(*top_pole)
    glVertex3f(*bottom_pole)
    glEnd()

    # Draw lines from top pole to equator and bottom pole to equator to segment each hemisphere
    for i in range(num_segments_per_hemisphere):
        theta = (2 * math.pi * i) / num_segments_per_hemisphere
        x_top = radius * math.sin(math.pi/4) * math.cos(theta)
        y_top = radius * math.cos(math.pi/4)
        z_top = radius * math.sin(math.pi/4) * math.sin(theta)
        x_bottom = radius * math.sin(-math.pi/4) * math.cos(theta)
        y_bottom = radius * math.cos(-math.pi/4)
        z_bottom = radius * math.sin(-math.pi/4) * math.sin(theta)
        glBegin(GL_LINES)
        glVertex3f(x_top, y_top, z_top)
        glVertex3f(x_bottom, y_bottom, z_bottom)
        glEnd()

    # Draw the equatorial line
    glBegin(GL_LINE_LOOP)
    for i in range(2 * num_segments_per_hemisphere):
        theta = (2 * math.pi * i) / (2 * num_segments_per_hemisphere)
        x = radius * math.cos(theta)
        y = 0
        z = radius * math.sin(theta)
        glVertex3f(x, y, z)
    glEnd()

    # Calculate the coordinates of the point equidistant from the equator and the top pole
    equator_top_midpoint = [0, radius * math.sin(math.pi/4), 0]

    # Calculate the coordinates of the point equidistant from the equator and the bottom pole
    equator_bottom_midpoint = [0, -radius * math.sin(math.pi/4), 0]

    # Draw lines connecting equidistant points to create the additional line
    glBegin(GL_LINES)
    glVertex3f(*equator_top_midpoint)
    glVertex3f(*equator_bottom_midpoint)
    glEnd()

    # Draw lines to approximate the wireframe sphere
    for i in range(2 * num_segments_per_hemisphere):
        theta1 = (2 * math.pi * i) / (2 * num_segments_per_hemisphere)
        theta2 = (2 * math.pi * (i + 1)) / (2 * num_segments_per_hemisphere)

        glBegin(GL_LINES)
        for j in range(num_segments_per_hemisphere):
            phi1 = (math.pi * j) / num_segments_per_hemisphere
            phi2 = (math.pi * (j + 1)) / num_segments_per_hemisphere

            # Calculate vertices for the current segment
            x1 = radius * math.sin(phi1) * math.cos(theta1)
            y1 = radius * math.cos(phi1)
            z1 = radius * math.sin(phi1) * math.sin(theta1)

            x2 = radius * math.sin(phi2) * math.cos(theta1)
            y2 = radius * math.cos(phi2)
            z2 = radius * math.sin(phi2) * math.sin(theta1)

            # Define line segment between vertices
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)

            # Repeat for adjacent longitude
            x1 = radius * math.sin(phi1) * math.cos(theta2)
            y1 = radius * math.cos(phi1)
            z1 = radius * math.sin(phi1) * math.sin(theta2)

            x2 = radius * math.sin(phi2) * math.cos(theta2)
            y2 = radius * math.cos(phi2)
            z2 = radius * math.sin(phi2) * math.sin(theta2)

            # Define line segment between vertices
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
        glEnd()

def main():
    """
    Main function to initialize the OpenGL environment and render the wireframe sphere.
    """

    # Initialize Pygame
    pygame.init()

    # Set up Pygame display with OpenGL support
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Set up perspective projection
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Move the object away from the camera
    glTranslatef(0.0, 0.0, -5)

    # Main loop for rendering
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Exit the program if the window is closed

        # Rotate the object
        glRotatef(1, 3, 1, 1)

        # Clear the color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the wireframe sphere
        draw_wireframe_sphere(radius=1.0, num_segments_per_hemisphere=4)

        # Swap the front and back buffers to display the rendered image
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
