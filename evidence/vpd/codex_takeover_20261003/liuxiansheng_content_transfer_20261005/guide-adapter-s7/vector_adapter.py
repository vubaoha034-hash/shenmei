import re, pathops
TOKEN=re.compile(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?')
def parse_svg_path(d, matrix=(1,0,0,1,0,0)):
    """Minimal deterministic SVG pen adapter. Supported commands are explicit."""
    tokens=TOKEN.findall(d)
    # Do not silently skip unsupported characters.
    if re.sub(r'[\s,]','',TOKEN.sub('',d)):
        raise RuntimeError('Unsupported path data syntax')
    p=pathops.Path();i=0;cmd=None;current=(0.,0.);start=(0.,0.);last_cubic=None;last_quad=None
    a,b,c,dd,e,f=matrix
    def point(pt): return (a*pt[0]+c*pt[1]+e,b*pt[0]+dd*pt[1]+f)
    def numbers(n):
        nonlocal i
        if i+n>len(tokens) or any(len(t)==1 and t.isalpha() for t in tokens[i:i+n]): raise RuntimeError('Incomplete SVG path data')
        value=list(map(float,tokens[i:i+n]));i+=n;return value
    def xy(n,relative):
        values=numbers(n*2);pts=[]
        for j in range(n): pts.append((values[2*j]+(current[0] if relative else 0),values[2*j+1]+(current[1] if relative else 0)))
        return pts
    while i<len(tokens):
        if len(tokens[i])==1 and tokens[i].isalpha():
            cmd=tokens[i];i+=1
        if cmd is None: raise RuntimeError('Path has no current command')
        upper=cmd.upper();relative=cmd.islower()
        if upper=='Z':
            p.close();current=start;last_cubic=last_quad=None;cmd=None;continue
        if upper=='M':
            q=xy(1,relative)[0];p.moveTo(*point(q));current=start=q;cmd='l' if relative else 'L';last_cubic=last_quad=None
        elif upper=='L':
            q=xy(1,relative)[0];p.lineTo(*point(q));current=q;last_cubic=last_quad=None
        elif upper=='H':
            x=numbers(1)[0]+(current[0] if relative else 0);current=(x,current[1]);p.lineTo(*point(current));last_cubic=last_quad=None
        elif upper=='V':
            y=numbers(1)[0]+(current[1] if relative else 0);current=(current[0],y);p.lineTo(*point(current));last_cubic=last_quad=None
        elif upper=='C':
            q=xy(3,relative);p.cubicTo(*(v for pt in q for v in point(pt)));current=q[2];last_cubic=q[1];last_quad=None
        elif upper=='S':
            q=xy(2,relative);q0=(2*current[0]-last_cubic[0],2*current[1]-last_cubic[1]) if last_cubic is not None else current
            p.cubicTo(*(v for pt in [q0,*q] for v in point(pt)));current=q[1];last_cubic=q[0];last_quad=None
        elif upper=='Q':
            q=xy(2,relative);p.quadTo(*(v for pt in q for v in point(pt)));current=q[1];last_quad=q[0];last_cubic=None
        elif upper=='T':
            q=xy(1,relative)[0];q0=(2*current[0]-last_quad[0],2*current[1]-last_quad[1]) if last_quad is not None else current
            p.quadTo(*(v for pt in [q0,q] for v in point(pt)));current=q;last_quad=q0;last_cubic=None
        else: raise RuntimeError('Unsupported SVG command: '+cmd)
    return p
def source_matrix(value):
    if not value:return (1,0,0,1,0,0)
    match=re.fullmatch(r'\s*translate\(([^()]*)\)\s*',value)
    if match:
        v=[float(x) for x in re.split(r'[\s,]+',match.group(1).strip())]
        if len(v)==1:v.append(0.)
        if len(v)!=2:raise RuntimeError('Invalid translate')
        return (1,0,0,1,*v)
    match=re.fullmatch(r'\s*matrix\(([^()]*)\)\s*',value)
    if match:
        v=tuple(float(x) for x in re.split(r'[\s,]+',match.group(1).strip()))
        if len(v)==6:return v
    raise RuntimeError('Unsupported VTracer transform: '+value)
def union_all(paths):
    out=pathops.Path()
    for p in paths:out=pathops.op(out,p,pathops.PathOp.UNION)
    return out
def poly(points):
    p=pathops.Path();p.moveTo(*points[0])
    for q in points[1:]:p.lineTo(*q)
    p.close();return p
def rectangle(box):
    x0,y0,x1,y1=box;return poly([(x0,y0),(x1,y0),(x1,y1),(x0,y1)])
def facts(p):
    return {'bounds_source':[float(v) for v in p.bounds],'area_source':float(p.area),'contours':len(list(p.contours))}

def n(value):
    val=round(float(value),2)
    if val==0:return '0'
    return format(val,'.2f').rstrip('0').rstrip('.')
def svg_d(p):
    out=[]
    for command, points in p.segments:
        if command=='moveTo':out.append('M'+' '.join(n(v) for q in points for v in q))
        elif command=='lineTo':out.append('L'+' '.join(n(v) for q in points for v in q))
        elif command=='curveTo':
            if len(points)!=3:raise RuntimeError('Unexpected cubic sequence')
            out.append('C'+' '.join(n(v) for q in points for v in q))
        elif command=='qCurveTo':
            if len(points)<2 or points[-1] is None:raise RuntimeError('Unsupported all-off-curve quadratic sequence')
            for segment in pathops.decompose_quadratic_segment(tuple(points)):
                out.append('Q'+' '.join(n(v) for q in segment for v in q))
        elif command=='closePath':out.append('Z')
        elif command=='endPath':pass
        else:raise RuntimeError('Unsupported pathops segment: '+command)
    return ''.join(out)
def fill_path(d,color,identity):
    return '<path id="'+identity+'" fill="'+color+'" fill-rule="nonzero" d="'+d+'"/>'
