import pygame
from Grid import Grid
import cProfile

class Main:
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 600
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Verlet physics simulation")
        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()
        self.running = True

        self.grid = Grid(self.width, self.height, 10, 30, 500)   # width, height, circle size, resolution, object count

        
    def run(self):
            while self.running:
                self.handle_events()

                # profiler = cProfile.Profile()
                # profiler.enable()
                self.update()
                # profiler.disable()
                # profiler.print_stats(sort='time')

                self.draw()
                
            pygame.quit()
              
        
    def update(self):
        dt = self.get_delta_time()
        self.grid.update_objects(dt)
                  
    def draw(self):
        self.window.fill((255, 255, 255)) 
        self.draw_fps()
        self.grid.draw(self.window)   
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                self.running = False
                
            # Key down
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass

            # Mouse down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                selected_cell = self.grid.get_cell_from_coordinates(mouseX, mouseY)
                selected_cell.selected = not selected_cell.selected


    def draw_fps(self):
        fps = self.clock.get_fps()
        fps_text = self.font.render("{:.2f}".format(fps), True, (0, 0, 0))
        self.window.blit(fps_text, (20, 20))
        object_count_text = self.font.render(str(len(self.grid.objects)), True, (0, 0, 0))
        self.window.blit(object_count_text, (20, 60))

    def get_delta_time(self):
        # Limiting dt (in seconds) to 1/tickrate
        dt = self.clock.tick(144) / 1000
        return min(dt, 1/144)

           

main = Main()
main.run()
