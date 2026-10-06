"""Bounded deterministic adapter: curve synthetic faces only, no contour-wide smoothing."""
import math

def smooth_synthetic_faces(path,spec,pathops):
 m=spec['source_to_final'];sx,sy,tx,ty=(m[k] for k in ['sx','sy','tx','ty'])
 polygons=[e['polygon'] for e in spec['source_coordinate_cuts']+spec['source_coordinate_intersections']]+[spec['replacement']['polygon']]
 faces=[]
 for poly in polygons:
  q=[(x*sx+tx,y*sy+ty) for x,y in poly]
  faces += list(zip(q,q[1:]+q[:1]))
 def dist(a,b):return math.hypot(a[0]-b[0],a[1]-b[1])
 def lerp(a,b,t):return tuple(x+(y-x)*t for x,y in zip(a,b))
 def eligible(a,b):
  if dist(a,b)<4:return False
  for u,v in faces:
   length=dist(u,v)
   def inline(p):
    deviation=abs((v[0]-u[0])*(p[1]-u[1])-(v[1]-u[1])*(p[0]-u[0]))/length
    t=((p[0]-u[0])*(v[0]-u[0])+(p[1]-u[1])*(v[1]-u[1]))/(length*length)
    return deviation<0.035 and -0.002<t<1.002
   if inline(a) and inline(b):return True
  return False
 def split(points,t):
  rows=[points]
  while len(rows[-1])>1:rows.append([lerp(a,b,t) for a,b in zip(rows[-1],rows[-1][1:])])
  return [r[0] for r in rows],[r[-1] for r in rows[::-1]]
 def trim(points,ta,tb):
  _,rest=split(points,ta);part,_=split(rest,(tb-ta)/(1-ta));return part
 output=pathops.Path();records=[]
 for contour in path.contours:
  segs=[];start=None;cur=None
  for cmd,pts in contour.segments:
   if cmd=='moveTo':start=cur=pts[0]
   elif cmd in ('lineTo','curveTo','qCurveTo'):
    assert cmd!='qCurveTo' or len(pts)==2
    segs.append([cur,*pts]);cur=pts[-1]
   elif cmd=='closePath':
    if dist(cur,start)>0.00001:segs.append([cur,start])
  if not segs:continue
  flags=[len(q)==2 and eligible(q[0],q[-1]) for q in segs]
  if not any(flags):output.addPath(contour);continue
  lengths=[sum(dist(a,b) for a,b in zip(q,q[1:])) for q in segs]
  # A join is softened only if a synthetic face is incident. Original grain contours have no such face.
  joins=[1.5 if flags[i-1] or flags[i] else 0 for i in range(len(segs))]
  pieces=[]
  for i,q in enumerate(segs):
   ta=min(0.18,joins[i]/max(lengths[i],0.001));tb=1-min(0.18,joins[(i+1)%len(segs)]/max(lengths[i],0.001))
   pieces.append(trim(q,ta,tb))
  output.moveTo(*pieces[0][0])
  for i,q in enumerate(pieces):
   if flags[i]:
    a,b=q;length=dist(a,b);mid=lerp(a,b,.5)
    # The face bows by 0.65px at its center; quadratic control is twice that normal displacement.
    control=(mid[0]-(b[1]-a[1])/length*1.3,mid[1]+(b[0]-a[0])/length*1.3)
    output.quadTo(*control,*b)
    records.append({'from':segs[i][0],'to':segs[i][-1],'trimmed_from':a,'trimmed_to':b,'center_deviation_px':.65,'corner_px':1.5})
   elif len(q)==2:output.lineTo(*q[-1])
   elif len(q)==3:output.quadTo(*q[1],*q[2])
   elif len(q)==4:output.cubicTo(*q[1],*q[2],*q[3])
   nxt=pieces[(i+1)%len(segs)][0]
   if joins[(i+1)%len(segs)]:output.quadTo(*segs[i][-1],*nxt)
  output.close()
 return output,{'schema':'s5-synthetic-local-curves/v1','synthetic_faces_matched':len(records),'faces':records,'nonrandom':True,'unchanged_source_contours_outside_incident_joins':True,'aesthetic_verdict':None}
