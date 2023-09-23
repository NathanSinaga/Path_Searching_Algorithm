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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
player = Actor("actormichael2", anchor=(0, 0), pos=(start[1] * zoom, start[0] * zoom))

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
# FUNCTION UNTUK GAMBAR JADI GIF
def draw_matrix(a,m, the_path = []):
    #dasar putih / jalan yang dapat dilalui
    im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(len(a)):
        for j in range(len(a[i])):
            color = (255, 255, 255)
            r = 0
            #color beton/wall
            if a[i][j] == 1:
                color = (0, 0, 0)
            #color start kotak
            if i == start[0] and j == start[1]:
                color = (0, 255, 0)
                r = borders
            #color finish kotak
            if i == end[0] and j == end[1]:
                color = (0, 255, 0)
                r = borders
            draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom-r-3, i*zoom+zoom-r-3), fill=color, outline=(151,255,244), width=1)

            if m[i][j] > 0:
                r = borders  +4
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                               fill=(255,0,0))

    #buat garis dari finish ke start
    for u in range(len(the_path)-1):
        y = the_path[u][0]*zoom + int(zoom/2)
        x = the_path[u][1]*zoom + int(zoom/2)
        y1 = the_path[u+1][0]*zoom + int(zoom/2)
        x1 = the_path[u+1][1]*zoom + int(zoom/2)
        draw.line((x,y,x1,y1), fill=(255, 0,0), width=5)

    #border ijo paling luar pemanis doang
    #draw.rectangle((0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0,255,0), width=2)
    images.append(im)


# INI FUNCTION UNTUK CARI JALAN TERUS SETIAP JALAN ITU DICATAT DENGAN VALUE K YANG TERUS +1 DARI VALUE SEBELUMNYA
def cekTetangga(k):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == k:
                if i>0 and maze[i-1][j] != 1 and not tree[i-1][j].visited:
                    #kiri
                    m[i-1][j] = k + 1
                    tree[i-1][j].visited = True
                if j>0 and maze[i][j-1] != 1 and not tree[i][j-1].visited:
                    #atas
                    m[i][j-1] = k + 1
                    tree[i][j-1].visited = True
                if i<len(m)-1 and maze[i+1][j] != 1 and not tree[i+1][j].visited:
                    #kanan
                    m[i+1][j] = k + 1
                    tree[i+1][j].visited = True
                if j<len(m[i])-1 and maze[i][j+1] != 1 and not tree[i][j+1].visited:
                    #bawah
                    m[i][j+1] = k + 1
                    tree[i][j+1].visited = True

# INI FUNCTION BUAT JALAN SAMPE KETEMU FINISH
def bfs(startNode):
    global m, hasilAkhir, found

    m[startNode.row][startNode.col] = 1 # UBAH VALUE M DI POSISI START MENJADI 1
    tree[startNode.row][startNode.col].visited = True

    #kalau belum sampe finish/goal // INI LOOPING SAMPAI KETEMU FINISH BARU BERHENTI
    k = 0
    while m[end[0]][end[1]] == 0:
        k += 1
        cekTetangga(k)
        draw_matrix(maze, m)

    endNode = tree[end[0]][end[1]]
    k = m[endNode.row][endNode.col]
    the_path = [(endNode.row,endNode.col)]


    # INI BUAT MENYIMPAN JALAN YANG SESUAI DENGAN YANG UDAH DICARI
    while k > 1:
      if endNode.row > 0 and m[endNode.row - 1][endNode.col] == k-1: # KIRI
        endNode = tree[endNode.row - 1][endNode.col]
        the_path.append((endNode.row, endNode.col))
        k-=1
        print("hehe "+str(k) + ", ", endNode.row, endNode.col)
      elif endNode.col > 0 and m[endNode.row][endNode.col - 1] == k-1: # ATAS
        endNode = tree[endNode.row][endNode.col - 1]
        the_path.append((endNode.row, endNode.col))
        k-=1
        print("hihi "+str(k) + ", ", endNode.row, endNode.col)
      elif endNode.row < len(m) - 1 and m[endNode.row + 1][endNode.col] == k-1: # KANAN
        endNode = tree[endNode.row + 1][endNode.col]
        the_path.append((endNode.row, endNode.col))
        k-=1
        print("hoho "+str(k) + ", ", endNode.row, j)
      elif endNode.col < len(m[endNode.row]) - 1 and m[endNode.row][endNode.col + 1] == k-1: # BAWAH
        endNode = tree[endNode.row][endNode.col + 1]
        the_path.append((endNode.row, endNode.col))
        k -= 1
        print("huhu "+str(k) + ", ", endNode.row, endNode.col)
      draw_matrix(maze, m, the_path)
      print()

    #ini untuk ngeblink pas akhir doang
    for i in range(10):
        if i % 2 == 0:
            draw_matrix(maze, m, the_path)
        else:
            draw_matrix(maze, m)

    hasilAkhir = the_path
    found = True

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
m = []
# INI BUAT MEMBUAT SEMUA VALUE M MENJADI 0
for i in range(len(maze)):
    m.append([])
    for j in range(len(maze[i])):
        m[-1].append(0)
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


def start_bfs():
    global hasilAkhir
    start_node = tree[start[0]][start[1]]
    bfs(start_node)
    hasilAkhir = list(reversed(hasilAkhir))
    print(hasilAkhir)

    images[0].save('mazeBFS1.gif', save_all=True, append_images=images[1:], optimize=False, duration=5, loop=0)

def update():
    global thread_start, thread_start1
    if not found and not thread_start:
        thread_start = True
        thread = threading.Thread(target=start_bfs)
        thread.start()

    # JIKA UDAH KETEMU FINISH JALAN INI ARAH KE FUNCTION START_WALK // UNTUK ARAH KE JALANKAN MICHEAL
    if found and not thread_start1:
        thread_start1 = True
        thread = threading.Thread(target=start_walk)
        thread.start()
