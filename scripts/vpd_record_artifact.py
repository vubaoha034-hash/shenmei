"""Bind real Figma/export evidence to the existing native takeover receipt."""
import argparse,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from visual_memory.vpd_task_lock import digest
TASK='VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def ref(p):return {'path':p,'sha256':digest(ROOT/p)}
def dump(p,v):
 q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 a=argparse.ArgumentParser();a.add_argument('--version',type=int,required=True);a.add_argument('--node',required=True);a.add_argument('--status',required=True);a.add_argument('--next',required=True);a.add_argument('--review',action='store_true');a.add_argument('--review-path');a.add_argument('--artifact',action='append',default=[]);a.add_argument('--receipt-name',default='EXECUTION_RECEIPT.json');args=a.parse_args()
 assert pathlib.Path(args.receipt_name).name==args.receipt_name
 n=args.version;assert n in [1,2,3]
 d=f'evidence/vpd/codex_takeover_20261003/v{n}/'
 f=load(d+'EXPORT_FIDELITY.json');rb=load(d+'FIGMA_READBACK.json')
 assert f['protected_pixels_changed']==0 and f['design_pixels_equal_raw_figma']
 assert rb['node_id']==args.node and rb['source_layer']['locked']
 assert rb['actual_source_bytes_readback']['sha256']==f['source']['sha256']
 texts=[x['characters'] for x in rb.get('text_nodes',[])] or [x['text'] for x in rb.get('descendants',[]) if x.get('type')=='TEXT']
 assert ''.join(texts)=='一杯茶，慢下来'
 vectors=rb.get('vector_count',sum(x.get('type')=='VECTOR' for x in rb.get('descendants',[])));assert vectors>=16
 tech={'task_id':TASK,'version':n,'source_sha256':f['source']['sha256'],'dimensions':f['dimensions'],'overlay_envelopes':f['overlay_envelopes'],'source_layer_unchanged':True,'protected_pixels_changed':0,'protected_pixels_compared':f['protected_pixels_compared'],'source':f['source'],'export':f['final_delivery_export'],'raw_figma_export':f['raw_figma_export'],'figma_readback':ref(d+'FIGMA_READBACK.json'),'trace':ref(d+'TOOL_TRACE.json'),'figma':{'file_key':'uyDxOoN1iNDPpEHTKSUWg1','node_id':args.node,'url':'https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id='+args.node.replace(':','-')},'fidelity_compensation':ref(d+'EXPORT_FIDELITY.json'),'editable_vector_count':vectors,'text_readback':texts,'actual_source_bytes_readback':rb['actual_source_bytes_readback'],'hidden_background_recovery':False}
 dump(d+'TECHNICAL_CHECK.json',tech)
 receipt={'task_id':TASK,'status':args.status,'next_required_action':args.next,'budget':{'formal_versions_used':n,'revisions_used':n-1},'technical_check':ref(d+'TECHNICAL_CHECK.json'),'artifact_refs':[ref(d+f) for f in ['TECHNICAL_CHECK.json','EXPORT_FIDELITY.json','FIGMA_READBACK.json','TOOL_TRACE.json']]+[ref(f'evidence/vpd/codex_takeover_20261003/chazuo-wordmark-v{n}.svg')],'tool_operations':{'photo_generations':0,'wordmark_image_generations':0,'official_figma_upload_assets_source':1 if n==1 else 0,'formal_version':n},'human_verdict':'PENDING'}
 if args.review:receipt['pixel_review']=ref(args.review_path or d+'PIXEL_REVIEW.json');receipt['artifact_refs'].append(receipt['pixel_review'])
 receipt['artifact_refs'] += [ref(p) for p in args.artifact]
 target=d+args.receipt_name
 if (ROOT/target).exists() and load(target)!=receipt:raise ValueError('IMMUTABLE_RECEIPT_WOULD_BE_OVERWRITTEN')
 dump(target,receipt)
 print(json.dumps({'receipt':ref(target),'technical':ref(d+'TECHNICAL_CHECK.json')}))
if __name__=='__main__':main()
