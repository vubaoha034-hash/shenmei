from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image
import hashlib, json

REPO = Path(__file__).resolve().parents[4]
PRIVATE = REPO / '.liu-visual-private/lettering_case_sources_20261004'
PRIVATE.mkdir(parents=True, exist_ok=True)
ROOT = Path(__file__).resolve().parent
urls=[
 ('heytea_01_introduction.jpeg','https://cdn1.foundertype.com/Public/Uploads/wechat_images/16698128276387525b30c8c6.33531003.jpeg'),
 ('heytea_03_mechanism.jpeg','https://cdn1.foundertype.com/Public/Uploads/wechat_images/16698128316387525fac27e2.11410228.jpeg'),
 ('heytea_05_mechanism.jpeg','https://cdn1.foundertype.com/Public/Uploads/wechat_images/1669812838638752669c70a3.82991969.jpeg'),
 ('heytea_07_mechanism.jpeg','https://cdn1.foundertype.com/Public/Uploads/wechat_images/16698128446387526cd9fca2.93514739.jpeg'),
 ('heytea_09_mechanism.jpeg','https://cdn1.foundertype.com/Public/Uploads/wechat_images/16698128466387526e55dfe5.07263740.jpeg'),
 ('heytea_application.jpg','https://cdn1.foundertype.com/Public/Uploads/img/customcase_attach_20221130212735_1809.jpg'),
]
records=[]
for name,url in urls:
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as response: data=response.read()
    path=PRIVATE/name
    if path.exists(): raise FileExistsError(path)
    path.write_bytes(data)
    with Image.open(path) as im: dimensions=list(im.size); format=im.format
    record={'url':url,'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'dimensions':dimensions,'format':format,'usage':'reference observation only; no font download or production reuse'}
    records.append(record); print(json.dumps(record,ensure_ascii=False),flush=True)
(ROOT/'CASE_IMAGE_TOOL_EVIDENCE.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
