import json,hashlib,copy,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE='evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/'
EP=BASE+'plugin_reference_repair_20261006/'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def ref(p):return {'path':p,'sha256':digest(p)}
def write(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
parent='8bf1d47144db96573f33e218122058ac975850c5'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==parent
lock=read('continuity/vpd/CURRENT_TASK_LOCK.json')
assert lock['revision']==354 and lock['next_required_action']=='LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER'
old=read(BASE+'NATIVE_PLUGIN_INSTALLED_READONLY_VERIFIED_RECEIPT_20261006.json')
assert old['status']==lock['status']
out=copy.deepcopy(old)
refs={r['path']:copy.deepcopy(r) for r in out['artifact_refs']}
added=[]
for p in (ROOT/EP).rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts:
  rel=p.relative_to(ROOT).as_posix(); refs[rel]=ref(rel);added.append(rel)
for p in (ROOT/'plugins/visual-aesthetic-workflow/v0.1.2').rglob('*'):
 if p.is_file() and 'dist' not in p.parts and '__pycache__' not in p.parts:
  rel=p.relative_to(ROOT).as_posix();refs[rel]=ref(rel);added.append(rel)
for rel in ['START_HERE.md','plugins/visual-aesthetic-workflow/REQUEST_REFERENCE_RUNTIME.json']:
 refs[rel]=ref(rel);added.append(rel)
out['artifact_refs']=list(refs.values())
out['completed_this_revision']=['同一私有插件运行0.1.2与Site第4版实际发布，新增请求级参考草稿，原生任务、摄影、版本及真人结论不变','真实ChatGPT工具目录刷新、原生重新连接与新聊天调用通过；原聊天仍内部错误，全部失败及取证截断边界保存','源码独立工程审核55项与13探针通过；保存新入口、实际版本、必要依赖和未验证视觉收益，不作成品或审美通过']
out['plugin_reference_repair']={'authorization':ref(EP+'REQUEST_AND_DIAGNOSIS.json'),'runtime':ref('plugins/visual-aesthetic-workflow/REQUEST_REFERENCE_RUNTIME.json'),'deployment':ref(EP+'HOSTED_DEPLOYMENT.json'),'actual_call':ref(EP+'CHATGPT_REAL_CALL.json'),'old_chat_failures':ref(EP+'ORIGINAL_CHAT_ERRORS.json'),'independent_source_review':ref(EP+'independent_review_EXECUTION_EVIDENCE.json'),'source_commit':'535a61558e3154b644f60b7b643566a94f1ea86f','mainline_reference_rebound':False,'artwork_generated':False,'aesthetic_improvement_verified':False}
assert out['worker_continuation']==old['worker_continuation']
for p in ['plugins/visual-aesthetic-workflow/CURRENT_RELEASE.json','plugins/visual-aesthetic-workflow/CONNECTION_VERIFICATION.json','continuity/vpd/codex_takeover_20261003/S7_FINAL_REUSE.md']:
 assert (ROOT/p).read_bytes()==subprocess.check_output(['git','show',parent+':'+p],cwd=ROOT)
for p in (ROOT/'plugins/visual-aesthetic-workflow/v0.1.1').rglob('*'):
 if p.is_file() and 'dist' not in p.parts:
  rel=p.relative_to(ROOT).as_posix()
  try: original=subprocess.check_output(['git','show',parent+':'+rel],cwd=ROOT,stderr=subprocess.DEVNULL)
  except subprocess.CalledProcessError: continue
  assert p.read_bytes()==original,rel
write(BASE+'NATIVE_PLUGIN_REQUEST_REFERENCE_VERIFIED_RECEIPT_20261006.json',out)
print(json.dumps({'prepared_receipt':BASE+'NATIVE_PLUGIN_REQUEST_REFERENCE_VERIFIED_RECEIPT_20261006.json','artifact_refs':len(refs),'new_refs':len(added),'worker_unit_unchanged':True,'outer_budget':out['budget'],'old_release_and_entry_unchanged':True,'receipt_sha256':digest(BASE+'NATIVE_PLUGIN_REQUEST_REFERENCE_VERIFIED_RECEIPT_20261006.json')},ensure_ascii=False))
