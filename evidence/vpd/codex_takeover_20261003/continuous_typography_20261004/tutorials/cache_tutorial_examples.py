"""Private source cache for inspection; public evidence contains metadata only."""
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image
import hashlib,json,os,time

REPO=Path(__file__).resolve().parents[5]
REPORT=Path(__file__).resolve().parent
PRIVATE=REPO/'.liu-visual-private/continuous_typography_20261004/tutorials'
assert PRIVATE.resolve().is_relative_to(REPO.resolve())
PRIVATE.mkdir(parents=True,exist_ok=True)
sources=[
('glyphs_handles.png','https://glyphsapp.com/media/pages/learn/drawing-good-paths/9a15a85102-1785165118/goodpaths-1-2560x-q80.png'),
('glyphs_matching_o.png','https://glyphsapp.com/media/pages/learn/drawing-good-paths/79233e04b7-1788511575/matching-o-2560x-q80.png'),
('figma_bend.gif','https://help.figma.com/hc/article_attachments/31937315233303')]
records=[]
for name,url in sources:
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as response: raw=response.read()
    path=PRIVATE/name; path.write_bytes(raw)
    with Image.open(path) as image:
        record={'url':url,'private_path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'dimensions':list(image.size),'frames':getattr(image,'n_frames',1)}
        if name=='figma_bend.gif':
            record['decoded_inspection_frames']=[]
            for index in sorted({0,image.n_frames//2,image.n_frames-1}):
                image.seek(index); frame=PRIVATE/f'figma_bend_frame_{index:03d}.png'; image.convert('RGBA').save(frame)
                record['decoded_inspection_frames'].append({'index':index,'path':str(frame),'sha256':hashlib.sha256(frame.read_bytes()).hexdigest()})
    records.append(record)
result={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'CODEX_THREAD_ID':os.environ.get('CODEX_THREAD_ID'),
        'purpose':'private tutorial illustration/frame inspection, no design or source redistribution','sources':records}
(REPORT/'TUTORIAL_IMAGE_METADATA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
