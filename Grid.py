from Cell import Cell
from Circle import Circle
import pygame
import random
import math
import itertools

class Grid:
    def __init__(self, width, height, circle_radius, resolution, object_count):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.cell_size = self.width / self.resolution
        self.object_count = object_count
        self.circle_radius = circle_radius

        self.objects = []
        for i in range(self.object_count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.objects.append(Circle(x, y, self.circle_radius))

        self.grid = self.build_grid()
        

    def build_grid(self):
        grid = []
        for i in range(self.resolution):
            grid.append([])
            for j in range(self.resolution):
                grid[i].append(Cell((i, j), self.cell_size, self.resolution))
        
        return grid


    def draw(self, window):
        # for row in self.grid:
        #     for cell in row:
        #         cell.draw(window)

        for obj in self.objects:
            obj.draw(window)


    def handle_collisions(self):
        for x in range(1, self.resolution - 1):
            for y in range(1, self.resolution - 1):
                cell = self.grid[x][y]
                objects_in_range = []

                # For all neighbors, append object indexes to objects in range
                for n in cell.neighbor_indexes:
                    neighbor = self.get_cell_from_index(n)
                    for o in neighbor.object_indexes:
                        objects_in_range.append(o)
                    
                # Check collision between all objects in range
                if(len(objects_in_range) > 0):
                     # Generate all unique pairs efficiently
                     for i, j in itertools.combinations(objects_in_range, 2):
                        self.objects[i].collide_with(self.objects[j])

        # ----- Naive approach (debug) -----
        # for x in range(0, len(self.objects)-1):
        #     for y in range(x + 1, len(self.objects)):
        #         self.objects[y].collide_with(self.objects[x])
               
            
    def clear_cells(self):
        for row in self.grid:
            for cell in row:
                if cell.object_indexes:
                    cell.clear()


    def update_objects(self, dt):
        self.clear_cells()

        gravity = (0, 1000)
        for i in range(len(self.objects)):
            obj = self.objects[i]
            obj.update(dt)
            obj.apply_force(gravity)
            obj.constrain(self.width, self.height)

            cell = self.get_cell_from_coordinates(obj.x, obj.y)
            cell.object_indexes.append(i)
        
        self.handle_collisions()
        self.control()


    def get_cell_from_coordinates(self, x, y):
        # x, y are pixel coordinates (not indexes!!!)
        i = math.floor(x / self.cell_size)
        j = math.floor(y / self.cell_size)
        return self.grid[i][j]


    def get_cell_from_index(self, idx):
        # idx can be out of bounds
        return self.grid[idx[0]][idx[1]]

   
    def control(self):
        UP = (0, -1500)
        DOWN = (0, 500)
        LEFT = (-500, 0)
        RIGHT = (500, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            for circle in self.objects:
                circle.apply_force(UP)
        if keys[pygame.K_s]:
            for circle in self.objects:
                circle.apply_force(DOWN)
        if keys[pygame.K_a]:
            for circle in self.objects:
                circle.apply_force(LEFT)
        if keys[pygame.K_d]:
            for circle in self.objects:
                circle.apply_force(RIGHT)
