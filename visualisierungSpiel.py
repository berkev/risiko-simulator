import pygame

RADIUS = 10
RADIUS_STEP = 5
FPS = 24


def read_game_history(path: str,split: str):
    """Read a specified file.
    path : path to the file to read
    split: String that isolates commands"""
    try:
        with open(path,'rt') as file:
            text = file.read()
        borders = text[text.find("("):text.find("[")-1]
        text = text[text.find('['):]
        return borders.strip(),text.split(split)
    except Exception as err:
        print(err)
        return []

def expand_history(history: list[str]):
    """Expand shortened commands into seperate ones, e. g.
    'v 1 2 3 2 1 2' will be divided into three commands
    'v 1 2', 'v 3 2', 'v 1 2' """
    for s in history:
        s = s.strip()

def animate_bubble_shrink(surf: pygame.Surface, nr: int, sec: float):
    """Animate the shrinking of bubble nr on the surface surf with
    an animation duration of sec s"""
    frames = round(FPS*sec)
    rad = 2


def animate_bubble(surf: pygame.Surface, nr: int, start: int, end: int, col: int):
    """Animate a bubble that"""        

def draw_graph(surf: pygame.Surface, edges: list[tuple],verticeCoords: list[tuple]):
    """draw the underlying graph """

    for edge in edges:
        pygame.draw.line(surf,"White",verticeCoords[edge[0]],verticeCoords[edge[1]])
    
#pygame.init()

if __name__ == "__main__":
    import random
    borders,history = read_game_history("data\\loggame.txt","\n")
    print(borders)
    current = history[0]
    print(current)
    #current = {besatzung: [i,k,j,...], truppen: [3,3,3,...,3]} (i,k,j in {0,1,..,|AnzahlSpieler|})
    H = 720
    W = 1080
    pygame.init()
    screen = pygame.display.set_mode((W,H))
    running = True
    clock = pygame.time.Clock()
    while running:
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.QUIT:
                    running = 0
                case _:
                    pass
        screen.fill("black")
        draw_graph(screen,[(0,1),(1,2),(1,3),(2,3)],[(random.uniform(20,W-20),random.uniform(20,H-20)) for k in range(4)])
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()