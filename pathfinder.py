import pygame, collections, heapq, random
pygame.init()

ROWS = COLS = 15
CELL = 45
W = COLS * CELL
H = ROWS * CELL + 60
DELAY = 40

WIN = pygame.display.set_mode((W, H))
pygame.display.set_caption("AI Pathfinder")
F = pygame.font.SysFont("arial", 13)
FB = pygame.font.SysFont("arial", 13, bold=True)

START, TARGET = (0,0), (ROWS-1, COLS-1)
WALLS = {(2,2),(2,3),(2,4),(5,7),(6,7),(7,7),(4,4),(4,5),
         (8,2),(8,3),(10,9),(10,10),(3,9),(3,10),(12,5),(12,6)}
MOVES = [(-1,0),(0,1),(1,0),(1,1),(0,-1),(-1,-1)]
WEIGHTS = [[random.randint(1,9) for _ in range(COLS)] for _ in range(ROWS)]
ALGOS = ["BFS","DFS","UCS","DLS","IDDFS","BiDir"]

def get_nb(r, c):
    return [(r+dr,c+dc) for dr,dc in MOVES
            if 0<=r+dr<ROWS and 0<=c+dc<COLS and (r+dr,c+dc) not in WALLS]

class App:
    def __init__(self):
        self.sel = 0
        self.vis = {}
        self.costs = {}
        self.path = []
        self.status = "Ready"
        self.stop_flag = False
        self.running = False

    def draw(self):
        WIN.fill((255,255,255))

        for r in range(ROWS):
            for c in range(COLS):
                x, y = c*CELL, r*CELL
                if (r,c) in WALLS:                       col = (0,0,0)
                elif (r,c) == START:                     col = (0,200,0)
                elif (r,c) == TARGET:                    col = (200,0,0)
                elif (r,c) in self.path:                 col = (255,255,0)
                elif self.vis.get((r,c)) == 'frontier':  col = (0,200,220)
                elif self.vis.get((r,c)) == 'explored':  col = (255,165,0)
                else:                                    col = (240,240,240)

                pygame.draw.rect(WIN, col, (x,y,CELL,CELL))
                pygame.draw.rect(WIN, (180,180,180), (x,y,CELL,CELL), 1)

                if self.sel==2 and col==(240,240,240):
                    WIN.blit(F.render(str(WEIGHTS[r][c]),True,(150,150,150)),(x+3,y+3))
                if (r,c) in self.costs:
                    WIN.blit(FB.render(str(self.costs[(r,c)]),True,(0,0,0)),(x+CELL//2-5,y+CELL//2-6))
                if (r,c)==START:  WIN.blit(FB.render("S",True,(0,0,0)),(x+CELL//2-5,y+CELL//2-6))
                if (r,c)==TARGET: WIN.blit(FB.render("T",True,(0,0,0)),(x+CELL//2-5,y+CELL//2-6))

        # bottom bar
        pygame.draw.rect(WIN, (220,220,220), (0, ROWS*CELL, W, 60))
        vc = sum(1 for v in self.vis.values() if v=='explored')
        WIN.blit(FB.render(f"Algo: {ALGOS[self.sel]}  |  {self.status}  |  Explored: {vc}", True, (0,0,0)), (8, ROWS*CELL+8))
        WIN.blit(F.render("1:BFS  2:DFS  3:UCS  4:DLS  5:IDDFS  6:BiDir  |  ENTER=Run  C=Clear  ESC=Stop", True, (80,80,80)), (8, ROWS*CELL+32))

        pygame.display.flip()

    def tick(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.stop_flag = True
        self.draw()
        pygame.time.delay(DELAY)
        return not self.stop_flag

    def bfs(self):
        q = collections.deque([(START,[START])])
        vis = {START}
        while q:
            node,path = q.popleft()
            self.vis[node]='explored'
            if node==TARGET: return path
            for n in get_nb(*node):
                if n not in vis:
                    vis.add(n); self.vis[n]='frontier'; q.append((n,path+[n]))
            if not self.tick(): return None
        return None

    def dfs(self):
        stack = [(START,[START])]
        vis = {START}
        while stack:
            node,path = stack.pop()
            self.vis[node]='explored'
            if node==TARGET: return path
            for n in get_nb(*node):
                if n not in vis:
                    vis.add(n); self.vis[n]='frontier'; stack.append((n,path+[n]))
            if not self.tick(): return None
        return None

    def ucs(self):
        pq = [(0,START,[START])]
        vis = {}
        while pq:
            cost,node,path = heapq.heappop(pq)
            if node in vis and vis[node]<=cost: continue
            vis[node]=cost; self.vis[node]='explored'; self.costs[node]=cost
            if node==TARGET: return path
            for n in get_nb(*node):
                nc = cost+WEIGHTS[n[0]][n[1]]
                self.vis[n]='frontier'; heapq.heappush(pq,(nc,n,path+[n]))
            if not self.tick(): return None
        return None

    def _dls(self, node, goal, limit, path, vis):
        self.vis[node]='explored'
        if not self.tick(): return None, True
        if node==goal: return path, False
        if limit==0: return None, False
        vis.add(node)
        for n in get_nb(*node):
            if n not in vis:
                self.vis[n]='frontier'
                res,stopped = self._dls(n,goal,limit-1,path+[n],vis)
                if stopped: return None,True
                if res: return res,False
        return None, False

    def dls(self):
        res,_ = self._dls(START,TARGET,12,[START],set())
        return res

    def iddfs(self):
        for lim in range(1, ROWS*COLS):
            self.vis.clear()
            res,stopped = self._dls(START,TARGET,lim,[START],set())
            if stopped: return None
            if res: return res
        return None

    def bidir(self):
        qF = collections.deque([(START,[START])])
        qB = collections.deque([(TARGET,[TARGET])])
        vF = {START:[START]}
        vB = {TARGET:[TARGET]}
        while qF and qB:
            fn,fp = qF.popleft(); self.vis[fn]='explored'
            if fn in vB: return fp+vB[fn][::-1][1:]
            for n in get_nb(*fn):
                if n not in vF:
                    vF[n]=fp+[n]; qF.append((n,vF[n])); self.vis[n]='frontier'
            bn,bp = qB.popleft(); self.vis[bn]='explored'
            if bn in vF: return vF[bn]+bp[::-1][1:]
            for n in get_nb(*bn):
                if n not in vB:
                    vB[n]=bp+[n]; qB.append((n,vB[n])); self.vis[n]='frontier'
            if not self.tick(): return None
        return None

    def run_algo(self):
        self.vis.clear(); self.costs.clear(); self.path=[]
        self.stop_flag=False; self.running=True
        self.status=f"Running..."
        fns = [self.bfs,self.dfs,self.ucs,self.dls,self.iddfs,self.bidir]
        result = fns[self.sel]()
        if result:            self.path=result; self.status=f"Done! Steps={len(result)-1}"
        elif not self.stop_flag: self.status="No path found!"
        else:                 self.status="Stopped"
        self.running=False; self.draw()

    def run(self):
        self.draw()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); exit()
                if e.type == pygame.KEYDOWN and not self.running:
                    k = e.key
                    if   k==pygame.K_1: self.sel=0; self.status="Ready"; self.vis.clear(); self.costs.clear(); self.path=[]
                    elif k==pygame.K_2: self.sel=1; self.status="Ready"; self.vis.clear(); self.costs.clear(); self.path=[]
                    elif k==pygame.K_3: self.sel=2; self.status="Ready"; self.vis.clear(); self.costs.clear(); self.path=[]
                    elif k==pygame.K_4: self.sel=3; self.status="Ready"; self.vis.clear(); self.costs.clear(); self.path=[]
                    elif k==pygame.K_5: self.sel=4; self.status="Ready"; self.vis.clear(); self.costs.clear(); self.path=[]
                    elif k==pygame.K_6: self.sel=5; self.status="Ready"; self.vis.clear(); self.costs.clear(); self.path=[]
                    elif k==pygame.K_RETURN: self.run_algo()
                    elif k==pygame.K_c:      self.vis.clear(); self.costs.clear(); self.path=[]; self.status="Ready"
            self.draw()
            pygame.time.delay(16)

App().run()
