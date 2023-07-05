import pygame

class Cell:
    def __init__(self, index, size, resolution):
        self.index = index
        self.size = size
        self.resolution = resolution
        self.x = self.index[0] * self.size
        self.y = self.index[1] * self.size
        self.color = (0, 0, 0)
        self.selected = False
        self.object_indexes = []

        self.neighbor_indexes = self.get_neighbor_indexes()


    def get_neighbor_indexes(self):
        x = self.index[0]
        y = self.index[1]
        all_possible_neighbors = [(x,   y+1),
                                  (x+1, y+1),
                                  (x+1, y  ),
                                  (x+1, y-1),
                                  (x,   y-1),
                                  (x-1, y-1),
                                  (x-1, y  ),
                                  (x-1, y+1)]
        
        neighbor_indexes = []
        for n in all_possible_neighbors:
            if not self.out_of_bounds(n):
                neighbor_indexes.append(n)
            
        return neighbor_indexes
        

    def out_of_bounds(self, idx):
        return (idx[0] < 0 or idx[1] < 0 or idx[0] > self.resolution - 1 or idx[1] > self.resolution - 1)
        

    def draw(self, window):
        rect = (self.x, self.y, self.size, self.size)
        if self.selected:
            pygame.draw.rect(window, self.color, rect)
        else:
            pygame.draw.rect(window, self.color, rect, width=1)


    def contains(self, obj):
            return (obj.x >= self.x
                and obj.x <  self.x + self.size
                and obj.y >= self.y
                and obj.y <  self.y + self.size)
    

    def clear(self):
        self.object_indexes = []

    

    




