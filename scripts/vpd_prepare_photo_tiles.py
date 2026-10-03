"""ABANDONED transport experiment, preserved as failure evidence only.

Its Figma upload route did not work. Production used official upload_assets;
this script is not a source-recovery or supported Figma delivery entry.
"""
import pathlib, hashlib, json
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1]
src=ROOT/'.liu-visual-private/source-r4.png'
out=ROOT/'.liu-visual-private/tiles';out.mkdir(exist_ok=True)
image=Image.open(src).convert('RGB')
items=[]
def transport_tile(x,y,width,height):
    p=out/f'{x}-{y}-{width}-{height}.png'
    tile=image.crop((x,y,x+width,y+height));tile.save(p,compress_level=9)
    # Connector code limit is 50,000 characters; bound encoded image payload.
    if p.stat().st_size > 33500:
        first=width//2
        transport_tile(x,y,first,height)
        transport_tile(x+first,y,width-first,height)
    else:
        items.append({'x':x,'y':y,'width':width,'height':height,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for y in range(0,1024,128):
    for x in range(0,1536,256):
        transport_tile(x,y,256,128)
rebuilt=Image.new('RGB',image.size)
for item in items:rebuilt.paste(Image.open(item['path']),(item['x'],item['y']))
assert rebuilt.tobytes()==image.tobytes()
(out/'index.json').write_text(json.dumps({'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'dimensions':list(image.size),'pixel_reconstruction_exact':True,'items':items},indent=2),encoding='utf-8')
print({'tiles':len(items),'max_bytes':max(pathlib.Path(i['path']).stat().st_size for i in items),'pixel_reconstruction_exact':True})
