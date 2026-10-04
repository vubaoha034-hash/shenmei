"""Thin CLI around pinned VTracer. Conversion only; no lettering design."""
from pathlib import Path
import argparse, io, json, sys

REPO = Path(__file__).resolve().parents[5]
DEPENDENCY = REPO/'.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages'
sys.path.insert(0,str(DEPENDENCY))
import vtracer
from PIL import Image

PARAMETERS = dict(colormode='binary',mode='spline',filter_speckle=0,
                  corner_threshold=60,length_threshold=4.0,max_iterations=10,
                  splice_threshold=45,path_precision=3)

def vectorize(source, destination, alpha=False):
    source=Path(source).resolve(); destination=Path(destination).resolve()
    if not destination.is_relative_to(REPO.resolve()):
        raise ValueError('output must remain inside this repository')
    if destination.exists(): raise FileExistsError(destination)
    raw=source.read_bytes()
    if alpha:
        with Image.open(io.BytesIO(raw)) as image:
            if 'A' not in image.getbands(): raise ValueError('alpha-mask mode requires an alpha channel')
            channel=image.getchannel('A')
            if channel.getextrema()==(255,255): raise ValueError('image is fully opaque: no alpha mask')
            mask=channel.point(lambda value: 0 if value>=128 else 255).convert('RGB')
            buffer=io.BytesIO(); mask.save(buffer,format='PNG'); raw=buffer.getvalue()
    svg=vtracer.convert_raw_image_to_svg(raw,img_format='png',**PARAMETERS)
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(svg,encoding='utf-8')
    return svg

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input'); parser.add_argument('output'); parser.add_argument('--alpha-mask',action='store_true')
    args=parser.parse_args()
    vectorize(args.input,args.output,args.alpha_mask)
    print(json.dumps({'input':str(Path(args.input).resolve()),'output':str(Path(args.output).resolve()),
                      'alpha_mask':args.alpha_mask,'parameters':PARAMETERS},ensure_ascii=False))
