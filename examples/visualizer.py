import pygame


class AnalysisTool:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Curling Trainer')
        self.screen = pygame.display.set_mode((500, 500))

    def draw_point(self, point):
        pygame.draw.circle(self.screen, (255, 0, 0), (round(point.x), round(point.y)), 4)

    def update_display(self, tracking_area, nodes):
        self.screen.fill((255, 255, 255))

        t_x1, t_y1, t_x2, t_y2 = tracking_area
        width = t_x2 - t_x1
        height = t_y2 - t_y1
        pygame.draw.rect(self.screen, (0, 0, 0), (t_x1, t_y1, width, height), 1)

        for node in nodes:
            x, y = node.position
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 5)
            if node.distance >= 1:
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), round(node.distance), 1)

    def update(self):
        pygame.display.flip()
