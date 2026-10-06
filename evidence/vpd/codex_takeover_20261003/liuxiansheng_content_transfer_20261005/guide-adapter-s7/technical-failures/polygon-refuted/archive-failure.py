import pathlib,shutil
ROOT=pathlib.Path.cwd();b=ROOT/'.liu-visual-private/s7_outline_implementation';pub=ROOT/'evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/guide-adapter-s7';failed=b/'technical-failures'/'polygon-refuted';failed.mkdir(parents=True,exist_ok=True)
for p in list(b.iterdir()):
 if p.is_file():shutil.copy2(p,failed/p.name)
shutil.copytree(failed,pub/'technical-failures'/'polygon-refuted',dirs_exist_ok=True)
add=pub.parent/'s7_technical_addendum'
for name in ['S7_PIXEL_GRID_TECHNICAL_ADDENDUM.json','pixel_grid_geometry.py','PIXEL_GRID_GEOMETRY_PROOF.json']:shutil.copy2(add/name,b/name)
