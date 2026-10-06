from pathlib import Path
import json,hashlib,sys,importlib.util,xml.etree.ElementTree as ET
from PIL import Image
root=Path(r"C:/Users/Administrator/OneDrive/文档/足球/shenmei-vpd-resume-20261006");out=root/".liu-visual-private/s7_fresh_entry"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
png=out/"FIGMA_COMPLETE_S7.png";svg=out/"S7_WORDMARK.svg"
with Image.open(png) as im:
    pixel={"format":im.format,"mode":im.mode,"size":list(im.size),"sha256":sha(png),"bytes":png.stat().st_size,"rgba_sha256":hashlib.sha256(im.convert("RGBA").tobytes()).hexdigest()}
tree=ET.parse(svg);ns={"s":"http://www.w3.org/2000/svg"};paths=tree.findall(".//s:path",ns)
svg_info={"sha256":sha(svg),"bytes":svg.stat().st_size,"path_count":len(paths),"path_ids":[p.attrib.get("id") for p in paths],"has_svg_text":bool(tree.findall(".//s:text",ns)),"viewBox":tree.getroot().attrib.get("viewBox")}
deps={}
numpy_spec=importlib.util.find_spec('numpy')
for name,path in {
"bundled_python":Path(sys.executable),"Pillow":Path(Image.__file__),"bundled_numpy":Path(numpy_spec.origin).parent if numpy_spec else Path(r"C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/numpy"),
"bundled_node":Path(r"C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe"),
"bundled_sharp_package":Path(r"C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/package.json"),
"skia_pathops_binary":root/".liu-visual-private/dependencies/skia_pathops_0_9_2_abi3/site-packages/pathops/_pathops.pyd",
"vtracer_site_packages":root/".liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages",
"vector_adapter":root/"evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/guide-adapter-s7/vector_adapter.py"}.items():
    deps[name]={"path":str(path),"exists":path.exists(),"content_read":name in ["vector_adapter","bundled_sharp_package"]}
    if name=="vector_adapter":deps[name]["sha256"]=sha(path)
    if name=="bundled_sharp_package":
        meta=json.loads(path.read_text(encoding="utf-8"));deps[name]["version"]=meta["version"]
prov=json.loads((root/"evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/plugin_evidence/SOURCE_PROVENANCE.json").read_text(encoding="utf-8"))
plugin_sources=[{"path":r["path"],"expected_sha256":r["sha256"],"actual_sha256":sha(root/r["path"]),"matches":sha(root/r["path"])==r["sha256"]}for r in prov["source_files"]]
result={"pixel_identity":pixel,"svg_identity":svg_info,"dependency_existence":deps,"plugin_source_byte_bindings":plugin_sources,"no_rebuild_or_trace":True,"clean_machine_install_verified":False}
(out/"ASSET_AND_DEPENDENCY_EVIDENCE.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"png":pixel,"svg":svg_info,"deps_exist":{k:v["exists"]for k,v in deps.items()},"plugin_sources_all_match":all(x["matches"]for x in plugin_sources)},ensure_ascii=False))
