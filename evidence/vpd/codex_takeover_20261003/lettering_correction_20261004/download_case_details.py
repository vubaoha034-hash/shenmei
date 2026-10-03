from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image
import hashlib, json

ROOT=Path(__file__).resolve().parent
PRIVATE=ROOT.parents[3]/'.liu-visual-private/lettering_case_sources_20261004'
PRIVATE.mkdir(parents=True,exist_ok=True)
urls=[
 ('heytea_02_structure.gif','https://cdn1.foundertype.com/Public/Uploads/wechat_images/16698128276387525bbe2d18.65068592.gif'),
 ('heytea_06_terminals.gif','https://cdn1.foundertype.com/Public/Uploads/wechat_images/1669812839638752673259f5.32072469.gif'),
 ('hanyi_white_rabbit_specimen.png','https://hanyi.com.cn/adminlte/ueditor/image/20230118/1674037099296934.png'),
 ('hanyi_white_rabbit_start.png','https://hanyi.com.cn/adminlte/ueditor/image/20230118/1674037228660424.png'),
 ('hanyi_white_rabbit_end.png','https://hanyi.com.cn/adminlte/ueditor/image/20230118/1674037233524777.png'),
 ('hanyi_white_rabbit_openings.png','https://hanyi.com.cn/adminlte/ueditor/image/20230118/1674037274468158.png')
]
records=[]
for name,url in urls:
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as response: data=response.read()
    path=PRIVATE/name
    if path.exists(): raise FileExistsError(path)
    path.write_bytes(data)
    with Image.open(path) as im: dimensions=list(im.size); format=im.format; frames=getattr(im,'n_frames',1)
    r={'url':url,'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'dimensions':dimensions,'format':format,'frames':frames,'usage':'reference pixel observation only; not a font or production asset'}
    records.append(r); print(json.dumps(r,ensure_ascii=False),flush=True)
(ROOT/'CASE_IMAGE_TOOL_EVIDENCE_02.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
