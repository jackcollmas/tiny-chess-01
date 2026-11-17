import json,os,sys,urllib.error,urllib.request
ENV_URL=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL is not set")
V={"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
PST={"p":[0]*16+[50,50,60,60,60,60,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5]+[0]*24,"n":[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,5,5,0,-20,-40,-30,5,10,15,15,10,5,-30,-30,0,15,20,20,15,0,-30,-30,5,15,20,20,15,5,-30,-30,0,10,15,15,10,0,-30,-40,-20,0,0,0,0,-20,-40,-50,-40,-20,-20,-20,-20,-40,-50],"b":[-20,-10,-10,-10,-10,-10,-10,-20,-10,5,0,0,0,0,5,-10,-10,10,10,10,10,10,10,-10,-10,0,10,10,10,10,0,-10,-10,5,5,10,10,5,5,-10,-10,0,5,10,10,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-10,-10,-10,-10,-20],"r":[0,0,5,10,10,5,0,0,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,5,10,10,10,10,10,10,5,0,0,0,0,0,0,0,0],"q":[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,5,5,5,5,5,0,-10,0,0,5,5,5,5,0,-5,-5,0,5,5,5,5,0,-5,-10,0,5,5,5,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20],"k":[-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20]}
def post(p,b):
 req=urllib.request.Request(ENV_URL+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(req)as res:return json.load(res)
 except urllib.error.HTTPError as e:sys.exit(f"{p}: HTTP {e.code}")
def board_of(fen):
 board={}
 for i,row in enumerate(fen.split()[0].split("/")):
  file=0
  for c in row:
   if c.isdigit():file+=int(c)
   else:board["abcdefgh"[file]+str(8-i)]=c;file+=1
 return board
def eval_board(board,fen):
 sc=0;wtm=fen.split()[1]=="w"
 for sq,pc in board.items():
  r,f=int(sq[1])-1,"abcdefgh".index(sq[0]);idx=r*8+f
  pv=V[pc.lower()];pst=PST.get(pc.lower(),[0]*64)
  if pc.isupper():sc+=pv+pst[idx]
  else:sc-=pv+pst[63-idx]
 return sc if wtm else-sc
def sim_move(board,mv,fen):
 nb=board.copy();pc=nb.get(mv[:2],"")
 if mv[2:4]in nb:del nb[mv[2:4]]
 nb[mv[2:4]]=mv[4].upper()if len(mv)==5 and fen.split()[1]=="w"else(mv[4].lower()if len(mv)==5 else pc)
 if mv[:2]in nb:del nb[mv[:2]]
 if pc.lower()=="p"and mv[0]!=mv[2]:
  ep=mv[2]+mv[1]
  if ep in nb and nb[ep].lower()=="p":del nb[ep]
 return nb
def mk_fen(board,wtm):
 rows=["".join(board.get(chr(97+j)+str(8-i)," ")for j in range(8))for i in range(8)]
 return"/".join("".join(str(len(list(g)))if k else"".join(g)for k,g in __import__("itertools").groupby(r,lambda x:x==" "))for r in rows)+" "+("b"if wtm else"w")+" - - 0 1"
def search(board,fen,legal,depth,a,b):
 if depth==0:return eval_board(board,fen),None
 best=None;wtm=fen.split()[1]=="w"
 moves=sorted(legal,key=lambda m:(len(m)>4,V.get(board.get(m[2:4],"x").lower(),0)),reverse=True)
 for mv in moves:
  nb=sim_move(board,mv,fen);nfen=mk_fen(nb,wtm);nlegal=post("/legal",{"fen":nfen}).get("legal_moves",[])
  if not nlegal:sc=20000
  else:sc,_=search(nb,nfen,nlegal,depth-1,-b,-a)
  sc=-sc
  if sc>a:a=sc;best=mv
  if a>=b:break
 return a,best
while True:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  board=board_of(g["fen"]);_,mv=search(board,g["fen"],g["legal_moves"],2,-99999,99999)
  g=post("/move",{"game":g["game"],"move":mv or g["legal_moves"][0]})
