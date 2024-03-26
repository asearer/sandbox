from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Variables for animation
angle = 0
orbit_radius_x = {
    "Mercury": 0.39,
    "Venus": 0.72,
    "Earth": 1.0,
    "Mars": 1.52,
    "Jupiter": 5.20,
    "Saturn": 9.58,
    "Uranus": 19.20,
    "Neptune": 30.05
}
orbit_radius_y = {
    "Mercury": 0.39 * 0.5,
    "Venus": 0.72 * 0.5,
    "Earth": 1.0 * 0.5,
    "Mars": 1.52 * 0.5,
    "Jupiter": 5.20 * 0.5,
    "Saturn": 9.58 * 0.5,
    "Uranus": 19.20 * 0.5,
    "Neptune": 30.05 * 0.5
}
rotation_speed = {
    "Mercury": 1.0,
    "Venus": 0.7,
    "Earth": 0.5,
    "Mars": 0.4,
    "Jupiter": 0.2,
    "Saturn": 0.15,
    "Uranus": 0.1,
    "Neptune": 0.08
}

# List to store the positions of the spheres
sphere_positions = {}

def draw_sphere(x, y, z, rotation_angle, color, size):
    # Draw a colored sphere at the specified position and rotate it around its own axis
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, 0, 1, 0)  # Rotate around its own axis
    glColor3f(*color)
    glutWireSphere(size, 10, 10)
    glPopMatrix()

def draw():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(10, 10, 10, 0, 0, 0, 0, 1, 0)

    # Draw the Sun
    draw_sphere(0, 0, 0, angle, (1.0, 1.0, 0.0), 0.3)

    # Draw planets in elliptical orbits around the Sun
    for planet, radius_x in orbit_radius_x.items():
        orbit_angle = angle * rotation_speed[planet]
        x = radius_x * math.cos(math.radians(orbit_angle))
        z = orbit_radius_y[planet] * math.sin(math.radians(orbit_angle))
        draw_sphere(x, 0, z, angle, (1.0, 1.0, 1.0), 0.1)
        # Store the position of each planet
        sphere_positions[planet] = (x, 0, z)

    angle += 0.1

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Solar System Model")
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
