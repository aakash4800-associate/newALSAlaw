import sys
from PIL import Image
src, out_a, out_v = sys.argv[1:4]
im = Image.open(src).convert("RGBA"); W,H = im.size; px = im.load()
AL = lambda x,y: px[x,y][3]
def runs_all(y):
    r=[];s=None
    for x in range(W):
        if AL(x,y)>8:
            if s is None: s=x
        elif s is not None: r.append((s,x-1)); s=None
    if s is not None: r.append((s,W-1))
    return r
LAYER={"A_L":"A","A_R":"A","V_L":"V","V_R":"V"}
fL=lambda y,s: s+(1-AL(s,y)/255)-0.5
fR=lambda y,e: e-(1-AL(e,y)/255)+0.5
# 1) unambiguous samples: rows where all four strokes are separate
iso={k:{"L":[],"R":[]} for k in LAYER}
for y in list(range(85,176))+list(range(330,413)):
    r=[q for q in runs_all(y) if q[1]-q[0]>=3]
    if len(r)!=4: continue
    order = ["V_L","A_L","A_R","V_R"] if y<250 else ["A_L","V_L","V_R","A_R"]
    for k,(s,e) in zip(order,r):
        iso[k]["L"].append((y,fL(y,s))); iso[k]["R"].append((y,fR(y,e)))
# 1b) reject rows that don't agree with a coarse straight-line fit of each stroke
def _lin(pts):
    n=len(pts); sy=sum(p[0] for p in pts); sv=sum(p[1] for p in pts)
    syy=sum(p[0]**2 for p in pts); syv=sum(p[0]*p[1] for p in pts)
    b=(n*syv-sy*sv)/(n*syy-sy*sy); return (sv-b*sy)/n, b
for _ in range(3):
    for k in LAYER:
        for E in ("L","R"):
            a,b=_lin(iso[k][E]); res=[abs(v-(a+b*y)) for y,v in iso[k][E]]
            cut=max(3.0, sorted(res)[int(len(res)*0.8)]*1.5)
            iso[k][E]=[p for p,r in zip(iso[k][E],res) if r<=cut]
for k in LAYER: print(k,"clean samples L/R:",len(iso[k]["L"]),len(iso[k]["R"]))

# 2) straight line per stroke edge (fit on clean, unambiguous rows)
def lin(pts):
    n=len(pts); sy=sum(p[0] for p in pts); sv=sum(p[1] for p in pts)
    syy=sum(p[0]**2 for p in pts); syv=sum(p[0]*p[1] for p in pts)
    b=(n*syv-sy*sv)/(n*syy-sy*sy); return (sv-b*sy)/n,b
EL={k:lin(iso[k]["L"]) for k in LAYER}; ER={k:lin(iso[k]["R"]) for k in LAYER}
INSET=2.0
Lx=lambda k,y: EL[k][0]+EL[k][1]*y+INSET; Rx=lambda k,y: ER[k][0]+ER[k][1]*y-INSET
ctr=lambda k,y:(Lx(k,y)+Rx(k,y))/2
# gold colour of the mark
cols=[px[x,y][:3] for y in range(0,H,3) for x in range(0,W,3) if px[x,y][3]==255 or px[x,y][3]>=250]
cols.sort(key=lambda c:sum(c)); GOLD=cols[len(cols)//2]
YS0,YS1,B=140,380,14       # synthetic body rows, blend length into the real serifs
def wsyn(y):
    if y<YS0 or y>YS1: return 0.0
    if y<YS0+B: return (y-YS0)/B
    if y>YS1-B: return (YS1-y)/B
    return 1.0
# 3) real pixels split by run (valid everywhere outside the crossings)
realA=Image.new("RGBA",(W,H),(0,0,0,0)); realV=Image.new("RGBA",(W,H),(0,0,0,0)); ra,rv=realA.load(),realV.load()
for y in range(H):
    for (s0,e0) in runs_all(y):
        ks=[k for k in LAYER if s0-2<=ctr(k,y)<=e0+2] or [min(LAYER,key=lambda k: abs(ctr(k,y)-(s0+e0)/2))]
        if len({LAYER[k] for k in ks})==1:
            tgt=ra if LAYER[ks[0]]=="A" else rv
            for x in range(s0,e0+1): tgt[x,y]=px[x,y]
# 4) compose: real near the serifs, clean straight band through the body (feathered)
A=Image.new("RGBA",(W,H),(0,0,0,0)); V=Image.new("RGBA",(W,H),(0,0,0,0)); pa,pv=A.load(),V.load()
for y in range(H):
    w=wsyn(y)
    for x in range(W):
        for lay,real,tgt in (("A",ra,pa),("V",rv,pv)):
            rp=real[x,y]
            if w==0.0:
                if rp[3]: tgt[x,y]=rp
                continue
            cov=max(max(0.0,min(1.0,min(x+0.5,Rx(k,y))-max(x-0.5,Lx(k,y)))) for k in LAYER if LAYER[k]==lay)
            a=w*255*cov+(1-w)*rp[3]
            if a>=1:
                c=GOLD if rp[3]==0 else tuple(round(w*g+(1-w)*r) for g,r in zip(GOLD,rp[:3]))
                tgt[x,y]=(c[0],c[1],c[2],round(a))
A.save(out_a); V.save(out_v)
qa,qv=A.load(),V.load()
holes=sum(1 for y in range(H) for x in range(W) if px[x,y][3]>=200 and max(qa[x,y][3],qv[x,y][3])<128)
extra=sum(1 for y in range(H) for x in range(W) if px[x,y][3]<=40 and max(qa[x,y][3],qv[x,y][3])>128)
print("vs original -> holes:",holes," extra:",extra, " gold:",GOLD)
