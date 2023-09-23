import heapq
import threading
import time
from PIL import Image, ImageDraw

zoom = 32
borders = 6
WIDTH = 20 * zoom
HEIGHT = 20 * zoom
start = 11, 9
end = 1,1
tiles = ['empty', 'block', 'flag2', 'deepempty']
images = []

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 5, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 5, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 3, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 3, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 3, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 3, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
player = Actor("actormichael2", anchor=(0, 0), pos=(start[1] * zoom, start[0] * zoom))

class Node:
    def __init__(Maze, row, col):
        Maze.row = row
        Maze.col = col
        Maze.visited = False
        Maze.parent = None
        Maze.cost = float('inf')

    def set_parent(Maze, parent_node):
        Maze.parent = parent_node

    def __lt__(Maze, other):
        return Maze.cost < other.cost

def build_tree():
    tree = []
    for row in range(len(maze)):
        row_nodes = []
        for col in range(len(maze[row])):
            node = Node(row, col)
            row_nodes.append(node)
        tree.append(row_nodes)
    return tree


# FUNCTION INI UNTUK NGEGAMBAR DIA CARI JALAN PAKE LIBRARY images
def draw_matrix(a, the_path=[]):
    global found
    im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    for i in range(len(a)):
        for j in range(len(a[i])):
            color = (0, 0, 0)
            r = 0
            if a[i][j] == 1: # TEMBOK
                color = (0, 0, 0)
            if a[i][j] > 2: # warnain yang cost gede
                color = (0, 0, 100)
            if i == start[0] and j == start[1]: # POSISI START
                color = (0, 255, 0)
                r = borders
            if i == end[0] and j == end[1]: # POSISI END
                color = (0, 255, 0)
                r = borders
            draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom-r-1, i*zoom+zoom-r-1), fill=color)
            if tree[i][j].visited:
                r = borders  +4
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1), fill=(255,0,0))

    # GAMBAR LINE

    for u in range(len(the_path)-1):
        y = the_path[u][0]*zoom + int(zoom/2)
        x = the_path[u][1]*zoom + int(zoom/2)
        y1 = the_path[u+1][0]*zoom + int(zoom/2)
        x1 = the_path[u+1][1]*zoom + int(zoom/2)
        draw.line((x,y,x1,y1), fill=(255, 0, 0), width=5)

    draw.rectangle((0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0, 0, 255), width=2) # BORDER

    # BUAT GAMBAR BORDER SETIAP WALL
    borderkotak = 0
    if borderkotak == 0:
        for k in range(len(a)):
            for l in range(len(a[k])):
                if a[k][l] == 1:
                    draw.rectangle((l * zoom, k * zoom, zoom * (l+1), zoom * (k+1)), outline=(14, 255, 253), width=2)
            if k == len(a)-1:
                borderkotak = 1

    images.append(im)


def ucs(maze, startNode):
    global hasilAkhir, costAkhir, found

    # Initialize the priority queue with the start node and cost 0
    queue = [(0, startNode)]
    draw_matrix(maze)
    startNode.cost = 0

    # Define directions (right, down, up, left)
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    while not found:
        # POP QUEUE DENGAN COST PALING KECIL
        cost, current_node = heapq.heappop(queue)

        # INI BUAT CEK UDA KETEMU FINISH APA BELUM
        if maze[current_node.row][current_node.col] == maze[end[0]][end[1]]:
            current_node.visited = True
            path = []
            # INI BUAT MASUKIN ROW SAMA COLUMN JALAN MENUJU FINISH KE PATH DARI NODE
            while current_node is not None:
                path.append((current_node.row, current_node.col))
                current_node = current_node.parent

            hasilAkhir = list(reversed(path)) # SIMPAN PATH KE DALAM HASILAKHIR
            costAkhir = cost # SIMPAN COST KE COSTAKHIR
            found = True

            # INI UNTUK KEPERLUAN GAMBAR GIF
            for animate in range(20):
                if animate % 2 == 0:
                    draw_matrix(maze, path)
                else:
                    draw_matrix(maze)

            return

        # TANDAIN KALO POSISI INI UDA PERNAH MAMPIR
        current_node.visited = True

        # INI BUAT CEK SEMUA ARAH
        for dx, dy in directions:
            x, y = current_node.row, current_node.col
            new_x, new_y = x + dx, y + dy

            # Check if the neighbor is within bounds and not a wall
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != 1:
                neighbor_node = tree[new_x][new_y]

                # Calculate the new cost
                new_cost = cost + maze[new_x][new_y]

                # If the neighbor has not been visited or has a lower cost, update it and add it to the queue
                if not neighbor_node.visited or new_cost < neighbor_node.cost:
                    if maze[new_x][new_y] == 2:
                        new_cost = cost
                    neighbor_node.cost = new_cost
                    neighbor_node.set_parent(current_node)
                    heapq.heappush(queue, (new_cost, neighbor_node))

                    draw_matrix(maze)

    return False

# INI UNTUK JALANKAN MICHEAL MENUJU FINISH
def jalan(a):
    row = a[0]
    column = a[1]
    print(a)
    lantai = maze[int(row)][int(column)]
    if lantai != 1:
        player.x = column * zoom
        player.y = row * zoom
    if lantai == 2:
        print("Akhirnya kita menamatkan maze michael")
        # BAGIAN INI TINGGAL TAMBAH BUAT EXIT


def draw():
    screen.clear()
    #membaca tilemap dan memasukkan gambar sesuai angka di tilemap
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            tile = tiles[0]
            x = column * zoom
            y = row * zoom
            if maze[row][column] < 3:
                tile = tiles[maze[row][column]]
            else:
                tile = tiles[3]
            screen.blit(tile, (x, y))

    #masukkan pemain
    player.draw()


tree = build_tree()
found = False  # Define this appropriately
thread_start = False
thread_start1 = False
hasilAkhir = []
costAkhir = 0


# FUNCTION UNTUK JALANKAN MICHEAL
def start_walk():
    global hasilAkhir
    time.sleep(3)
    for i in range(len(hasilAkhir)):
        jalan(hasilAkhir[i])
        time.sleep(0.4)
    exit()


def start_ucs():
    start_node = tree[start[0]][start[1]]
    ucs(maze, start_node)

    print(hasilAkhir)
    print("cost: ", costAkhir)

    images[0].save('mazeUCS.gif', save_all=True, append_images=images[1:], optimize=False, duration=5, loop=0)

def update():
    global thread_start, thread_start1
    if not found and not thread_start:
        thread_start = True
        thread = threading.Thread(target=start_ucs)
        thread.start()

    # JIKA UDAH KETEMU FINISH JALAN INI ARAH KE FUNCTION START_WALK // UNTUK ARAH KE JALANKAN MICHEAL
    if found and not thread_start1:
        thread_start1 = True
        thread = threading.Thread(target=start_walk)
        thread.start()



