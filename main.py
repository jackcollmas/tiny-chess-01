import json,os,sys,urllib.error,urllib.request
ENV_URL=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL is not set")
V={"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
P={"p":[0]*8+[78,83,86,73,102,82,85,90,7,29,21,44,40,31,44,7,-17,16,-2,15,14,0,15,-13,-26,3,10,9,6,1,0,-23,-22,9,5,-11,-10,-2,3,-19,-31,8,-7,-37,-36,-14,3,-31,0,0,0,0,0,0,0,0],"n":[-167,-89,-34,-49,61,-97,-15,-107,-73,-41,72,36,23,62,7,-17,-47,60,37,65,84,129,73,44,-9,17,19,53,37,69,18,22,-13,4,16,13,28,19,21,-8,-23,-9,12,10,19,17,25,-16,-29,-53,-12,-3,-1,18,-14,-19,-105,-21,-58,-33,-17,-28,-19,-23],"b":[-29,-51,-23,-15,-22,-18,-50,-64,-40,-27,-42,-18,-27,-39,-46,-35,-39,-35,-50,-37,-61,-43,-52,-28,-23,-9,-23,-5,-9,-16,-5,-17,-14,-18,-7,-1,4,-9,-15,-27,-12,-10,-13,-26,-3,-11,-8,-28,-9,-12,-9,-27,-1,-12,-10,-7,-25,-24,-24,-3,-6,-3,-10,-25],"r":[32,42,32,51,63,9,31,43,27,32,58,62,80,67,26,44,19,35,28,33,45,27,25,15,0,5,16,13,18,-4,-9,17,-26,-12,-1,1,-9,7,-6,-23,-44,-16,-20,-9,-1,11,-6,-71,-19,-13,1,17,16,7,-37,-26,-36,-18,-9,15,6,-7,0,23],"q":[-28,-27,-21,-5,-1,-7,-18,-9,-9,22,22,27,27,19,10,20,-14,20,40,36,24,29,20,24,-2,43,32,60,72,63,43,2,1,36,34,42,59,76,53,30,-18,28,19,47,31,34,39,23,-16,22,1,2,-2,0,-23,-20,-27,-27,-16,-16,-1,17,-2,-27],"k":[-65,23,16,-15,-56,-34,2,13,29,-1,-20,-7,-8,-4,-38,-29,-9,24,2,-16,-20,6,22,-22,19,-3,11,21,23,6,-3,-6,27,12,39,35,29,42,29,25,10,17,23,15,20,45,20,13,-16,20,50,41,47,28,31,-8,-74,-35,-18,-18,-11,15,4,-17]}
D={"n":[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],"b":[(-1,-1),(-1,1),(1,-1),(1,1)],"r":[(-1,0),(1,0),(0,-1),(0,1)],"q":[(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]}
def post(p,b):
 req=urllib.request.Request(ENV_URL+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(req)as res:return json.load(res)
 except urllib.error.HTTPError as e:sys.exit(f"{p}: HTTP {e.code}")
def bd(f):
 b={}
 for i,r in enumerate(f.split()[0].split("/")):
  c=0
  for x in r:
   if x.isdigit():c+=int(x)
   else:b["abcdefgh"[c]+str(8-i)]=x;c+=1
 return b
def atk(b,sq,by_w):
 tr,tc=int(sq[1]),"abcdefgh".index(sq[0]);pr=tr-1 if by_w else tr+1
 for dc in[-1,1]:
  if 0<=tc+dc<8 and (b.get("abcdefgh"[tc+dc]+str(pr),"")==("P" if by_w else "p")):return True
 for dr,dc in D["n"]:
  r,c=tr+dr,tc+dc
  if 1<=r<=8 and 0<=c<8 and (b.get("abcdefgh"[c]+str(r),"")==("N" if by_w else "n")):return True
 for pt in["b","r","q"]:
  for dr,dc in D[pt]:
   r,c=tr+dr,tc+dc
   while 1<=r<=8 and 0<=c<8:
    p=b.get("abcdefgh"[c]+str(r),"")
    if p:
     if (p==pt.upper() if by_w else p==pt) or (pt in["b","r"] and (p=="Q" if by_w else "q")):return True
     break
    r+=dr;c+=dc
 return False
def ev(b,w):
 s=0
 for q,p in b.items():
  r,c=8-int(q[1]),"abcdefgh".index(q[0]);i=r*8+c;v=V[p.lower()];t=P.get(p.lower(),[0]*64)
  if p.isupper():s+=v+t[i]
  else:s-=v+t[63-i]
 return s if w else-s
def mv(b,m,w):
 n=b.copy();p=n.get(m[:2],"")
 if m[2:4]in n:del n[m[2:4]]
 n[m[2:4]]=m[4].upper()if len(m)==5 and w else(m[4].lower()if len(m)==5 else p)
 del n[m[:2]]
 if p.lower()=="p"and m[0]!=m[2]:
  ep=m[2]+m[1]
  if ep in n and n[ep].lower()=="p":del n[ep]
 if p.lower()=="k":
  if m=="e1g1"and"h1"in n:n["f1"]=n.pop("h1")
  elif m=="e1c1"and"a1"in n:n["d1"]=n.pop("a1")
  elif m=="e8g8"and"h8"in n:n["f8"]=n.pop("h8")
  elif m=="e8c8"and"a8"in n:n["d8"]=n.pop("a8")
 return n
def rate(b,w,m):
 n=mv(b,m,w);p=b.get(m[:2],"");pv=V.get(p.lower(),0);dst=m[2:4]
 cap=V.get(b.get(dst,"x").lower(),0);promo=900 if len(m)>4 else 0
 sc=ev(n,w)+cap*10+promo*10
 if atk(n,dst,not w):
  if not atk(n,dst,w):sc-=pv*8
  elif cap<pv:sc-=(pv-cap)*5
 return sc
while True:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  b=bd(g["fen"]);w=g["fen"].split()[1]=="w"
  m=max(g["legal_moves"],key=lambda x:rate(b,w,x))
  g=post("/move",{"game":g["game"],"move":m})
