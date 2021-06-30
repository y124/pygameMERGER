iimport pygame, os, math, random, json
from PIL import Image, ImageDraw
from PIL import ImagePath

os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (50,50)
scaling = 1

def sx(x):
    s = scaling
    m = 800
    v = x - m
    if v >= 0:
        w = v*scaling + m*scaling
    else:
        w = x*scaling
    return int(w)
    
def sy(x):
    s = scaling
    m = 450
    v = x - m
    if v > 0:
        w = v*scaling + m*scaling
    else:
        w = x*scaling
    return int(w)

def s(x, y):
    return (sx(x),sy(y))

def primefactors(n):
       a = []
       while n % 2 == 0:
          a.append(2),
          n = n / 2
       for i in range(3,int(math.sqrt(n))+1,2):  
          while (n % i == 0):
             a.append(i)
             n = n / i
       if n > 2:
          a.append(int(n))
       return a
       
def NPM(n, prime_list):
        if n%100 == 0 or n < 100:
            print(f'[GenShape.py] Function: NPM({n})')
        num = prime_list[-1]
        while len(prime_list) < n:
            for p in prime_list:
                if num % p == 0:
                    break
            else:
                prime_list.append(num)
            num += 2
        return [prime_list[-1], prime_list]

def prime(p, prime_list):
        print(f'[GenShape.py] Function: prime({p})')
        i = len(prime_list)
        while True:
            d = NPM(i, prime_list)
            if p == 2:
                return [3, d[1]]
            if d[0] >= p:
                return [i+2, d[1]]
            i += 1

def shape(side, size):
        print(f'[GenShape.py] Function: shape({side}, {size})')
        global SIZE
        xy = [
            ((math.cos(th) + 1) * size + SIZE-size,
             (math.sin(th) + 1) * size + SIZE-size)
            for th in [i * (2 * math.pi) / side for i in range(side)]
            ]  
          
        image = ImagePath.Path(xy).getbbox()  
          
        img1 = ImageDraw.Draw(img)  
        img1.polygon(xy, fill ="#"+clr+"ff", outline ="#ffffffff") 

prime_list = [2, 3]
def makeShape(shapeArgs):
    global SIZE, prime_list, img, clr
    prime_list = [2, 3]
    SIZE = int(shapeArgs[1])
    try:
        clr = shapeArgs[4]
    except:
        clr = '00ffff'
    img = Image.new("RGBA", (SIZE*2, SIZE*2), "#00000000")
    pfs = sorted(primefactors(int(shapeArgs[2])))
    pfs2 = []
    for pf in pfs:
        pfs2.append(prime(pf, prime_list)[0])
        prime_list = prime(pf, prime_list)[1]
    pfs = pfs2
    help = SIZE/len(pfs)
    x = SIZE
    for i in range(len(pfs)):
        shape(pfs[i], x)
        x -= help
    img.save(shapeArgs[3])

rnd = random.random
folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Assets')
pygame.init()
def getFont(size):
    global folder
    return pygame.font.Font(os.path.join(folder, 'font.ttf'), int(size*scaling))
dis = pygame.display.set_mode((int(1600*scaling), int(900*scaling)))
pygame.display.set_caption('Merge Infinte (OPEN BETA)')
pygame.display.flip()
r = True
hold = [False, None]
images={}
am = False
af = False
scene = 'START'
mode = 'Number'
tablet = False

class mergeable:
    def __init__(self, val, pos):
        self.val = val
        self.pos = pos
        self.shown = True
        self.x = self.pos[0]
        self.y = self.pos[1]
        print('[pygameMERGER.py] Object: mergeable')
        
    def __gt__(self, other):
        return other.val < self.val

digs = '-abcdefghijklmnopqrstuvwxyz'
def i2b(x, base=27):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)

def rgb2hex(r):
    print(f'[pygameMERGER.py] Function: rgb2hex({r})')
    return "{:02x}{:02x}{:02x}".format(r[0],r[1],r[2])

def save(n):
    print('[pygameMERGER.py] Function: save()')
    global mergeables, merges
    q = []
    for m in mergeables:
        q.append([m.val, m.pos])
    q.append(merges)
    with open(os.path.join(folder, f'mydata{n}.json'), 'w') as f:
        json.dump(q, f)
        
def load(n):
    global mergeables, merges
    print('[pygameMERGER.py] Function: load()')
    f = open(os.path.join(folder, f'mydata{n}.json'))
    qs = json.load(f)
    mergeables = []
    merges = qs[-1]
    for q in qs[:-1]:
        mergeables.append(mergeable(q[0], q[1]))
        
def PIR(point,rect):
    x1, y1, w, h = rect
    print(f'[pygameMERGER.py] Function: PIR({point},{rect})')
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False

def BRand(M,B):
    a = False
    print(f'[pygameMERGER.py] Function: BRand({M},{B})')
    try:
        for i in range(M):
            if rnd() > 1-(1/(B**(1/(5-int(M**(1/5)))))) and not a:
                a = True
                return i
    except:
        return 0
    return M   

mergeables = []
lmm = 0
mval = 1
merges = 0

def inittext():
    global ftext, ftextRect
    global stext, stextRect
    global aftext, aftextRect
    global amtext, amtextRect
    
    global s1text, s1textRect
    global s2text, s2textRect
    global s3text, s3textRect
    global ntext, ntextRect
    
    global autext, autextRect
    global rtext, rtextRect
    global m2text, m2textRect
    global sttext, sttextRect
    
    global sctext, sctextRect
    global btext, btextRect
    
    ftext = getFont(450).render('+', True, (0,255,127), (50,50,50))
    ftextRect = ftext.get_rect()
    ftextRect.center = s(1150, 250)

    stext = getFont(160).render('sort', True, (0,255,127), (50,50,50))
    stextRect = stext.get_rect()
    stextRect.center = s(1150, 800)
    
    btext = getFont(100).render('bin', True, (255,0,0), (50,50,50))
    btextRect = btext.get_rect()
    btextRect.center = s(1450, 760)

    aftext = getFont(30).render(' Auto Plus Hax ', True, (0,255,127), (50,50,50))
    aftextRect = aftext.get_rect()
    aftextRect.center = s(1500, 300)

    amtext = getFont(30).render(' Auto Merge Hax ', True, (0,255,127), (50,50,50))
    amtextRect = amtext.get_rect()
    amtextRect.center = s(1486, 350)

    s1text = getFont(100).render('Save 1', True, (0,255,255), (50,50,50))
    s1textRect = s1text.get_rect()
    s1textRect.center = s(400, 350)

    s2text = getFont(100).render('Save 2', True, (0,255,255), (50,50,50))
    s2textRect = s2text.get_rect()
    s2textRect.center = s(800, 350)

    s3text = getFont(100).render('Save 3', True, (0,255,255), (50,50,50))
    s3textRect = s3text.get_rect()
    s3textRect.center = s(1200, 350)
    
    sctext = getFont(20).render('press + or - to change scaling', True, (50,50,0))
    sctextRect = sctext.get_rect()
    sctextRect.center = s(800, 450)

    sttext = getFont(200).render('Start', True, (127,0,127))
    sttextRect = sttext.get_rect()
    sttextRect.center = s(800, 150)

    ntext = getFont(100).render('Merge Infinte', True, (0,192,192))
    ntextRect = ntext.get_rect()
    ntextRect.center = s(800, 500)

    autext = getFont(75).render('By y124', True, (0,128,128))
    autextRect = autext.get_rect()
    autextRect.center = s(800, 650)

    rtext = getFont(30).render(' Randomize ', True, (0,255,127), (50,50,50))
    rtextRect = rtext.get_rect()
    rtextRect.center = s(1520, 400)

    m2text = getFont(15).render('Right Click Shape to See in Fullscreen', True, (0,255,255))
    m2textRect = m2text.get_rect()
    m2textRect.center = s(1460, 870)

    dis = pygame.display.set_mode((int(1600*scaling), int(900*scaling)))

inittext()

clock = pygame.time.Clock()

def gsn(num):
    global prime_list
    prime_list = [2, 3]
    num = int(num)
    num += 2
    pfs = sorted(primefactors(int(num)))
    pfs2 = []
    for pf in pfs:
        pfs2.append(prime(pf, prime_list)[0])
        prime_list = prime(pf, prime_list)[1]
    name = ''
    pfs2.reverse()
    for pf in pfs2:
        pfas = str(pf)
        for n in pfas:
            n = int(n)
            name += ['ze','uni','doua','tri','quadra','penta','hexa','septa','octa','nona'][n]
        name += 'gon in\n'
    return name[:-4] + '*'

while r:
    clock.tick(60)
    dis.fill((0,0,0))
    if len(mergeables) >= lmm:
        GridSize = int(math.sqrt(mval+1)) + 1
        lmm = len(mergeables)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                if scaling > 0.2:
                    scaling -= 0.1
                inittext()
            if event.key == pygame.K_EQUALS:
                scaling += 0.1
                inittext()
        
        if event.type == pygame.MOUSEBUTTONUP:
        
            if scene == 'BIG SHAPE' and event.button == 1:
                scene = 'MAIN'
        
            if scene == 'START':
                if PIR (pygame.mouse.get_pos(), tuple(s2textRect)):
                    try:
                        load(2)
                    except FileNotFoundError:
                        save(2)
                    scene = 'MAIN'
                    sav = 2
                if PIR (pygame.mouse.get_pos(), tuple(s1textRect)):
                    try:
                        load(1)
                    except FileNotFoundError:
                        save(1)
                    scene = 'MAIN'
                    sav = 1
                if PIR (pygame.mouse.get_pos(), tuple(s3textRect)):
                    try:
                        load(3)
                    except FileNotFoundError:
                        save(3)
                    scene = 'MAIN'
                    sav = 3
            
            if scene == 'MAIN' and tablet:
                if PIR (pygame.mouse.get_pos(), tuple(btextRect)):
                    for m in mergeables:
                        if m.shown == False:
                            mergeables.remove(m)
                            hold = [False]
                            
                if pygame.mouse.get_pos()[0] < int(900*scaling):
                    print('[pygameMERGER.py] Click: Board')
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        x, y = int(x*(GridSize/int(900*scaling))), int(y*(GridSize/int(900*scaling)))
                        end = False
                        
                        for i in range(len(mergeables)):
                            try:
                                m = mergeables[i]
                            except:
                                m = mergeable(-1, (-1, -1))
                            if not end:
                                if m.shown == False and tablet:
                                    check = [False]
                                    for m2 in mergeables:
                                        if (m2.x, m2.y) == (x, y) and m2.shown == True:
                                            check = [True, m2]
                                    if not check[0]:
                                        print('[pygameMERGER.py] Click: Move')
                                        mergeables[i].shown = True
                                        mergeables[i].pos = (x, y)
                                        mergeables[i].x = x
                                        mergeables[i].y = y
                                        hold = [False]
                                    elif check[1].val == m.val and check[1].pos != m.pos:
                                        print('[pygameMERGER.py] Click: Merge')
                                        hold = [False]
                                        mergeables.append(mergeable(check[1].val + 1, check[1].pos))
                                        mergeables.remove(m)
                                        mergeables.remove(check[1])
                                        merges += 1
                                    else:
                                        print('[pygameMERGER.py] Click: Fail')
                                    end = True
                            
        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                save(sav)
            except:
                None == None
            if event.button == 3 and scene == 'MAIN' and pygame.mouse.get_pos()[0] < int(900*scaling):
                try:
                    save(sav)
                except:
                    None == None
                x, y = pygame.mouse.get_pos()
                x, y = int(x*(GridSize/int(900*scaling))), int(y*(GridSize/int(900*scaling)))
                for m in mergeables:
                    if (m.x, m.y) == (x, y):
                        path = f'{folder}/{int(900*scaling)}_{m.val}.png'
                        try:
                            img = images[path]
                        except:
                            try:
                                images[path] = pygame.image.load(path)
                                img = images[path]
                            except:
                                command = f'--- {int(900*scaling/2)} {m.val+2} {folder}/{int(900*scaling)}_{m.val}.png {rgb2hex((25*(m.val%10+1),(25*(int(m.val/10)%10+1)),(25*(int(m.val/100)%10+1))))}'
                                args = command.split(' ')[:3]
                                args.append(' '.join(command.split(' ')[3:-1]))
                                args.append(command.split(' ')[-1])
                                makeShape(args)
                                print('[pygameMERGER.py] Command: '+command)
                                images[path] = pygame.image.load(path)
                                img = images[path]
                        imgRect = img.get_rect()
                        imgRect.center = s(800, 450)
                        dis.blit(img, imgRect)
                        scene = 'BIG SHAPE'
                        bsv = m.val
                        
            if event.button == 1:
            
                if PIR (pygame.mouse.get_pos(), tuple(btextRect)):
                    for m in mergeables:
                        if m.shown == False:
                            mergeables.remove(m)
                            hold = [False]
                
                print('[pygameMERGER.py] Event: Left Click')
                
                if scene == 'MAIN':
                    if PIR (pygame.mouse.get_pos(), tuple(ftextRect)) and (((int(math.sqrt(mval+1)) + 1)**2) - 1) >= len(mergeables):
                        print('[pygameMERGER.py] Click: Plus')
                        going = True
                        for y in range(GridSize):
                            for x in range(GridSize):
                                mf = False
                                for m in mergeables:
                                    if (m.x, m.y) == (x, y):
                                        mf = True
                                if not mf and going:
                                    going = False
                                    mergeables.append(mergeable(BRand(mval, merges), (x, y)))
                    
                    if PIR (pygame.mouse.get_pos(), tuple(stextRect)) or PIR (pygame.mouse.get_pos(), tuple(rtextRect)):
                        print('[pygameMERGER.py] Click: Sort')
                        if PIR (pygame.mouse.get_pos(), tuple(stextRect)):
                            mergeables = sorted(mergeables)
                            mergeables.reverse()
                        else:
                            random.shuffle(mergeables)
                        gss = []
                        for i in range(GridSize):
                            for ii in range(GridSize):
                                gss.append((ii, i))
                        for i in range(len(mergeables)):
                            x, y = gss[i][0], gss[i][1]
                            mergeables[i].pos = (x,y)
                            mergeables[i].x = x
                            mergeables[i].y = y
                    
                    if PIR (pygame.mouse.get_pos(), tuple(amtextRect)):
                        print('Auto Merge: ', ['On', 'Off'][am])
                        am = not am
                        
                    if PIR (pygame.mouse.get_pos(), tuple(aftextRect)):
                        print('Auto Plus: ', ['On', 'Off'][af])
                        af = not af
                        
                    if PIR (pygame.mouse.get_pos(), tuple(ttextRect)):
                        print('Tablet Mode: ', ['On', 'Off'][af])
                        tablet = not tablet
                        
                    if PIR (pygame.mouse.get_pos(), tuple(mtextRect)):
                        mode1 = {0: 'Number', 1: 'None    ', 2: 'Letter'}
                        mode2 = {'Number': 0, 'None    ': 1, 'Letter': 2}
                        try:
                            mode = mode1[mode2[mode]+1]
                        except:
                            mode = 'Number'
                        print('Mode:  ' + mode)
                                    
                    if pygame.mouse.get_pos()[0] < int(900*scaling):
                        print('[pygameMERGER.py] Click: Board')
                        x, y = pygame.mouse.get_pos()
                        x, y = int(x*(GridSize/int(900*scaling))), int(y*(GridSize/int(900*scaling)))
                        end = False
                        
                        for i in range(len(mergeables)):
                            try:
                                m = mergeables[i]
                            except:
                                m = mergeable(-1, (-1, -1))
                            if not end:
                                if (m.x, m.y) == (x, y) and hold[0] == False and m.shown == True:
                                    print('[pygameMERGER.py] Click: Shape')
                                    m.shown = False
                                    qq = int(int(900*scaling)/GridSize*0.9)
                                    path = f'{folder}/{qq}_{m.val}.png'
                                    try:
                                        img = images[path]
                                    except:
                                        command = f'--- {int(qq/2)} {m.val+2} {folder}/{qq}_{m.val}.png {rgb2hex((25*(m.val%10+1),(25*(int(m.val/10)%10+1)),(25*(int(m.val/100)%10+1))))}'
                                        args = command.split(' ')[:3]
                                        args.append(' '.join(command.split(' ')[3:-1]))
                                        args.append(command.split(' ')[-1])
                                        makeShape(args)
                                        print(command)
                                        images[path] = pygame.image.load(path)
                                        img = images[path]
                                    textRect = img.get_rect()
                                    textRect.center = (x, y)
                                    dis.blit(img, textRect)
                                    hold = [True, m]
                                    end = True
                                    
                                elif m.shown == False and not tablet:
                                    check = [False]
                                    for m2 in mergeables:
                                        if (m2.x, m2.y) == (x, y) and m2.shown == True:
                                            check = [True, m2]
                                    if not check[0]:
                                        print('[pygameMERGER.py] Click: Move')
                                        mergeables[i].shown = True
                                        mergeables[i].pos = (x, y)
                                        mergeables[i].x = x
                                        mergeables[i].y = y
                                        hold = [False]
                                    elif check[1].val == m.val and check[1].pos != m.pos:
                                        print('[pygameMERGER.py] Click: Merge')
                                        hold = [False]
                                        mergeables.append(mergeable(check[1].val + 1, check[1].pos))
                                        mergeables.remove(m)
                                        mergeables.remove(check[1])
                                        merges += 1
                                    else:
                                        print('[pygameMERGER.py] Click: Fail')
                                    end = True
    if scene == 'MAIN':             
        for m in mergeables:
            if m.val > mval:
                mval = m.val
        
            if m.shown:
                qq = int(int(900*scaling)/GridSize*0.9)
                path = f'{folder}/{qq}_{m.val}.png'
                try:
                    img = images[path]
                except:
                    try:
                        images[path] = pygame.image.load(path)
                        img = images[path]
                    except:
                        command = f'--- {int(qq/2)} {m.val+2} {folder}/{qq}_{m.val}.png {rgb2hex((25*(m.val%10+1),(25*(int(m.val/10)%10+1)),(25*(int(m.val/100)%10+1))))}'
                        args = command.split(' ')[:3]
                        args.append(' '.join(command.split(' ')[3:-1]))
                        args.append(command.split(' ')[-1])
                        makeShape(args)
                        print('[pygameMERGER.py] Command: '+command)
                        images[path] = pygame.image.load(path)
                        img = images[path]
                textRect = img.get_rect()
                textRect.center = ((int(900*scaling) // GridSize)*(m.x+0.5), (int(900*scaling) // GridSize)*(m.y+0.5))
                dis.blit(img, textRect)
                
                if mode == 'Number':
                    text = getFont(int((qq/scaling)*0.35)).render(f'{str(m.val)}', True, (0,0,0))
                    textRect = text.get_rect()
                    textRect.center = ((int(900*scaling) // GridSize)*(m.x+0.5), (int(900*scaling) // GridSize)*(m.y+0.5))
                    dis.blit(text, textRect)
                    
                    text = getFont(int((qq/scaling)*0.3)).render(f'{str(m.val)}', True, (255, 255, 255))
                    textRect = text.get_rect()
                    textRect.center = ((int(900*scaling) // GridSize)*(m.x+0.5), (int(900*scaling) // GridSize)*(m.y+0.5))
                    dis.blit(text, textRect)
                    
                elif mode == 'Letter':
                    text = getFont(int((qq/scaling)*0.35)).render(f'{i2b(m.val)}', True, (0,0,0))
                    textRect = text.get_rect()
                    textRect.center = ((int(900*scaling) // GridSize)*(m.x+0.5), (int(900*scaling) // GridSize)*(m.y+0.5))
                    dis.blit(text, textRect)
                    
                    text = getFont(int((qq/scaling)*0.3)).render(f'{i2b(m.val)}', True, (255, 255, 255))
                    textRect = text.get_rect()
                    textRect.center = ((int(900*scaling) // GridSize)*(m.x+0.5), (int(900*scaling) // GridSize)*(m.y+0.5))
                    dis.blit(text, textRect)
    
    if scene == 'START':  
        dis.blit(ntext, ntextRect)
        dis.blit(s1text, s1textRect)
        dis.blit(s2text, s2textRect)
        dis.blit(s3text, s3textRect)
        dis.blit(sctext, sctextRect)
        dis.blit(sttext, sttextRect)
        dis.blit(autext, autextRect)
    
    if scene == 'BIG SHAPE':
        dis.blit(img, imgRect)
        
        mtext = getFont(100).render(f'{str(bsv)}', True, (0,255,255))
        mtextRect = mtext.get_rect()
        mtextRect.center = s(150, 100)
        dis.blit(mtext, mtextRect) 
        
        mtext = getFont(100).render(f'{i2b(bsv)}', True, (0,255,255))
        mtextRect = mtext.get_rect()
        mtextRect.center = s(150, 200)
        dis.blit(mtext, mtextRect) 
        
        fs = 1500/len(gsn(bsv))
        v2 = 0
        for v in gsn(bsv).split('\n'):
            mtext = getFont(fs).render(f'{v}', True, (255,0,255), (50,50,50))
            mtextRect = mtext.get_rect()
            mtextRect.center = s(800, (1000/len(gsn(bsv)))+(v2*fs))
            dis.blit(mtext, mtextRect) 
            v2+=1
        
        mtext = getFont(50).render(f'Left Click to Exit', True, (0,64,64))
        mtextRect = mtext.get_rect()
        mtextRect.center = s(1350, 850)
        dis.blit(mtext, mtextRect) 
        
        mtext = getFont(20).render(f'*Shape name may not represent real shape name', True, (64,0,64))
        mtextRect = mtext.get_rect()
        mtextRect.center = s(1350, 800)
        dis.blit(mtext, mtextRect) 
              
    if scene == 'MAIN':            
        dis.blit(ftext, ftextRect)
        dis.blit(stext, stextRect)
        dis.blit(rtext, rtextRect)
        dis.blit(aftext, aftextRect)      
        dis.blit(amtext, amtextRect)      
        dis.blit(m2text, m2textRect)   
        dis.blit(btext, btextRect)  
        
        mtext = getFont(25).render(f' Overlay Mode: {mode} ', True, (0,255,127), (50,50,50))
        mtextRect = mtext.get_rect()
        mtextRect.center = s(1465, 450)
        dis.blit(mtext, mtextRect) 
        
        ttext = getFont(25).render(f" Tablet Mode: {['off', 'on '][tablet]} ", True, (0,255,127), (50,50,50))
        ttextRect = ttext.get_rect()
        ttextRect.center = s(1495, 250)
        dis.blit(ttext, ttextRect) 
        
        if (((int(math.sqrt(mval+1)) + 1)**2) - 1) >= len(mergeables) and int(pygame.time.get_ticks()/100)%2 == 1 and af:
            print('[pygameMERGER.py] Click: Plus')
            going = True
            for y in range(GridSize):
                for x in range(GridSize):
                    mf = False
                    for m in mergeables:
                        if (m.x, m.y) == (x, y):
                            mf = True
                        if not mf and going:
                            going = False
                            mergeables.append(mergeable(BRand(mval, merges), (x, y)))
            print('[pygameMERGER.py] Click: Sort')
            mergeables = sorted(mergeables)
            mergeables.reverse()
            gss = []
            for i in range(GridSize):
                for ii in range(GridSize):
                    gss.append((ii, i))
            for i in range(len(mergeables)):
                x, y = gss[i][0], gss[i][1]
                mergeables[i].pos = (x,y)
                mergeables[i].x = x
                mergeables[i].y = y
            
        if int(pygame.time.get_ticks()/100)%2 == 0 and am:
            for m in mergeables:
                for m2 in mergeables:
                    if m.val == m2.val and m.pos != m2.pos:
                        hold = [False]
                        mergeables.append(mergeable(m.val + 1, m.pos))
                        mergeables.remove(m2)
                        try:
                            mergeables.remove(m)
                        except:
                            print()
                        merges += 1
                    
                    
        if hold[0] == True:
            m = hold[1]
            qq = int(int(900*scaling)/GridSize*0.9)
            path = f'{folder}/{qq}_{m.val}.png'
            try:
                img = images[path]
            except:
                try:
                    images[path] = pygame.image.load(path)
                    img = images[path]
                except:
                    command = f'--- {int(qq/2)} {m.val+2} {folder}/{qq}_{m.val}.png {rgb2hex((25*(m.val%10+1),(25*(int(m.val/10)%10+1)),(25*(int(m.val/100)%10+1))))} '
                    args = command.split(' ')[:3]
                    args.append(' '.join(command.split(' ')[3:-1]))
                    args.append(command.split(' ')[-1])
                    makeShape(args)
                    print('[pygameMERGER.py] Command: '+command)
                    images[path] = pygame.image.load(path)
                    img = images[path]
            textRect = img.get_rect()
            textRect.center = pygame.mouse.get_pos()
            dis.blit(img, textRect)
            
            if mode == 'Number':
                text = getFont(int((qq/scaling)*0.35)).render(f'{str(m.val)}', True, (0,0,0))
                textRect = text.get_rect()
                textRect.center = pygame.mouse.get_pos()
                dis.blit(text, textRect)
                    
                text = getFont(int((qq/scaling)*0.3)).render(f'{str(m.val)}', True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = pygame.mouse.get_pos()
                dis.blit(text, textRect)
                
            elif mode == 'Letter':
                text = getFont(int((qq/scaling)*0.35)).render(f'{i2b(m.val)}', True, (0,0,0))
                textRect = text.get_rect()
                textRect.center = pygame.mouse.get_pos()
                dis.blit(text, textRect)
                    
                text = getFont(int((qq/scaling)*0.3)).render(f'{i2b(m.val)}', True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = pygame.mouse.get_pos()
                dis.blit(text, textRect)
            
        try:
            text = getFont(15).render(f'({str(1-(1/(merges**(1/(5-int(mval**(1/5)))))))[:8]} chance of higher block)', True, (0, 127, 127), (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = s(1450, 80)
            dis.blit(text, textRect)
            text = getFont(40).render(f'merges: {merges}', True, (0, 255, 255), (0,0,0))
            textRect = text.get_rect()
            textRect.center = s(1450, 35)
            dis.blit(text, textRect)
        except ZeroDivisionError:
            None == None
    
    pygame.display.update()
