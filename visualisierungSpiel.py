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
    

def draw_vertices(surf: pygame.Surface, rects: list[pygame.Rect], colors: list[pygame.Color|tuple]):
    """Draw the bubbles centered on the given rects"""
    for k in range(len(rects)):
        pygame.draw.circle(surf,colors[k],rects[k].center,float(rects[k].w)/2)
def random_color():
    """generate a random tripple representing a color"""
    r,g,b = random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)
    return (r,g,b)
def check_collision(pos: tuple[float], rects: list[pygame.Rect]):
    """check the list of rects for collision. Return the index of the colliding rect
    Returns -1 if no collision is detected"""
    for k in range(len(rects)):
        if rects[k].collidepoint(pos):
            return k
    return -1
def move_vertice(ind: int, rects: list[pygame.Rect], coords: list[tuple], delta: tuple):
    """Move the ind. rect in rects by delta. The new center will be written to coords[ind] 
    """
    try:
        rects[ind].move_ip(*delta)
        coords[ind] = rects[ind].center
    except IndexError:
        print(f"No vertice at index {ind}")
    except Exception as err:
        print(err)
#pygame.init()

if __name__ == "__main__":
    import random
    # borders,history = read_game_history("data\\loggame.txt","\n")
    # print(borders)
    # current = history[0]
    # print(current)
    #current = {besatzung: [i,k,j,...], truppen: [3,3,3,...,3]} (i,k,j in {0,1,..,|AnzahlSpieler|})

    #Code for the graph visualisation


    H = 720
    W = 1080
    pygame.init()
    screen = pygame.display.set_mode((W,H))
    running = True
    clock = pygame.time.Clock()

    #data
    graph, coords = [(0,1),(1,2),(1,3),(2,3)],[(random.uniform(20,W-20),random.uniform(20,H-20)) for k in range(4)]
    bubbles = [pygame.Rect(coord[0]-RADIUS,coord[1]-RADIUS,2*RADIUS,2*RADIUS) for coord in coords]
    bubblesColor = [random_color() for bub in bubbles]
    mousePos = (0,0)
    focusBubble = -1
    #mainloop
    while running:


        #eventhandling
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.QUIT:
                    running = 0
                case pygame.MOUSEMOTION:
                    mousePos = pygame.mouse.get_pos()
                    delta = pygame.mouse.get_rel()
                    if focusBubble+1:
                        move_vertice(focusBubble,bubbles,coords,delta)
                case pygame.MOUSEBUTTONDOWN:
                    focusBubble = check_collision(mousePos,bubbles)
                case pygame.MOUSEBUTTONUP:
                    focusBubble = -1
                case _:
                    pass
        
        
        
        #draw stuff
        screen.fill("black")
        draw_graph(screen,graph,coords)
        draw_vertices(screen,bubbles,bubblesColor)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()