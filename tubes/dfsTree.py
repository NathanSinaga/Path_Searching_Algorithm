import threading
import time
from PIL import Image, ImageDraw

zoom = 32
borders = 6
WIDTH = 20 * zoom
HEIGHT = 20 * zoom
start = 9, 9
end = 1,1
tiles = ['empty', 'block', 'flag2']
images = []

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Actor("actormichael2", anchor=(0, 0), pos=(start[1] * zoom, start[0] * zoom))

#struct node
class Node:
    def __init__(Maze, row, col):
        Maze.row = row
        Maze.col = col
        Maze.visited = False

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


def dfs(startNode):
    global path_so_far, hasilAkhir, found

    #JIKA POSISI row DAN col TIDAK DALAM MAP
    if startNode.row < 0 or startNode.col < 0 or startNode.row >= len(maze)-1 or startNode.col >= len(maze[0])-1:
        return

    # JIKA POSISI col DAN row SUDAH PERNAH DIDATANGI ATAU DALAM WALL
    if maze[startNode.row][startNode.col] == 1 or startNode.visited:
        return

    path_so_far.append((startNode.row, startNode.col)) # INI BUAT MASUKIN POSISI KE path_so_far
    startNode.visited = True
    draw_matrix(maze, path_so_far) # INI BUAT NGEGAMBAR JALUR BUAT GIF

    # jika sudah menemukan finish
    if (startNode.row, startNode.col) == (end[0], end[1]):
        hasilAkhir = list(path_so_far) # menyimpan jalan menuju finish di hasil_akhir
        print("Found!", path_so_far)
        found = True

        #INI UNTUK KEPERLUAN GAMBAR GIF
        for animate in range(10):
            if animate % 2 == 0:
                draw_matrix(maze, path_so_far)
            else:
                draw_matrix(maze)
        path_so_far.pop()
        return
    else:
        print("row:", startNode.row)
        print("col:", startNode.col)
        if not found:
            dfs(tree[startNode.row - 1][startNode.col])  # check top
        if not found:
            dfs(tree[startNode.row + 1][startNode.col])  # check bottom
        if not found:
            dfs(tree[startNode.row][startNode.col + 1])  # check right
        if not found:
            dfs(tree[startNode.row][startNode.col- 1])  # check left
    path_so_far.pop()
    draw_matrix(maze, path_so_far)
    return

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
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))

    #masukkan pemain
    player.draw()


tree = build_tree()
found = False
thread_start = False
thread_start1 = False
hasilAkhir = []
path_so_far = []

# FUNCTION UNTUK JALANKAN MICHEAL
def start_walk():
    time.sleep(3)
    for i in range(len(hasilAkhir)):
        jalan(hasilAkhir[i])
        time.sleep(0.4)
    exit()


#FUNCTION BUAT MANGGIL FUNCTION DFS BOSKU
def start_dfs():
    global hasilAkhir
    start_node = tree[start[0]][start[1]]
    dfs(start_node)
    print(hasilAkhir)

    images[0].save('mazeDFS1.gif', save_all=True, append_images=images[1:], optimize=False, duration=50, loop=0)


def update():
    global thread_start, thread_start1
    if not found and not thread_start:
        thread_start = True
        thread = threading.Thread(target=start_dfs)
        thread.start()

    # JIKA UDAH KETEMU FINISH JALAN INI ARAH KE FUNCTION START_WALK // UNTUK ARAH KE JALANKAN MICHEAL
    if found and not thread_start1:
        thread_start1 = True
        thread = threading.Thread(target=start_walk)
        thread.start()
