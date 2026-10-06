"""Review supplied actual tool excerpt plus HEAD native blobs, without browser/calls."""
import hashlib,json,subprocess
from datetime import datetime,timezone
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
SOURCE=ROOT/'.liu-visual-private/plugin_installation_20261006/ACTUAL_TOOL_PROOF.json'
PUBLIC='evidence/vpd/codex_takeover_20261003/liuxiansheng_content_transfer_20261005/plugin_installation_20261006'
EXPECTED_HEAD='c19970b76cb2e30b037c55016ceb5f54b29a887c'
OLD_SHA='e01495d31e0c5adc48317beaceb051ba46895d5ef3450a0412cf9ef21165df89'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
def blob(p):return git('show','HEAD:'+p)
def write(n,v):
 p=(OUT/n).resolve();assert p.is_relative_to(OUT);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(v if isinstance(v,bytes) else (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
raw=SOURCE.read_bytes();proof=json.loads(raw)
old_before=(OUT/'INDEPENDENT_INSTALLATION_VERIFICATION.json').read_bytes()
head=git('rev-parse','HEAD').decode().strip()
paths=['PROJECT_CONTROL_ADAPTER.json','continuity/vpd/CURRENT_TASK_LOCK.json','continuity/vpd/LATEST_CHECKPOINT.json']
native_raw={p:blob(p) for p in paths}
a,l,c=[json.loads(native_raw[p]) for p in paths]
inv=proof['actual_tool_invocation_message'];args=json.loads(inv['content']['text']);metadata=inv['metadata']
prefix=proof['actual_tool_response_prefix']
# The supplied message prefix ends inside an outer JSON string. Decode that
# string with only its delimiter added; extract complete observed fields with
# raw_decode. Never present this as a complete original provider response.
encoded=prefix.split('"text":',1)[1]
decoded_fragment=json.loads(encoded+'"')
decoder=json.JSONDecoder()
def complete_field(name):
 marker='"'+name+'":';pos=decoded_fragment.index(marker)+len(marker)
 return decoder.raw_decode(decoded_fragment[pos:])[0]
derived={k:complete_field(k) for k in ['source','task_id','stage','next_required_action']}
source=derived['source'];lock_sha=sha(native_raw[paths[1]])
checks={
 'supplied_actual_capture_HTTP200':proof['http_status']==200 and proof['evidence_kind']=='OBSERVED_EXISTING_CHATGPT_HTTP_RESPONSE_BODY_EXCERPT_NOT_ASSISTANT_SELF_REPORT',
 'actual_assistant_call_message_and_exact_readonly_path':inv['author']['role']=='assistant' and inv['recipient']=='api_tool.call_tool' and inv['status']=='finished_successfully' and args['path']=='/刘先生·视觉设计工作流/link_6ac4c007fd6881919033d63620867164/get_current_workflow' and args['args']=={},
 'actual_tool_author_and_response_id_in_raw_prefix':proof['actual_tool_response_author']=={'role':'tool','name':'api_tool.call_tool'} and prefix.startswith('{"id":"'+proof['actual_tool_response_message_id']+'","author":{"role":"tool","name":"api_tool.call_tool"'),
 'raw_prefix_complete_fields_independently_decode_to_recorded_fields':derived==proof['decoded_complete_binding_fields'],
 'actual_metadata_model_and_effort_match_record':metadata['model_slug']==metadata['resolved_model_slug']==proof['actual_chatgpt_configuration']['model_slug']=='gpt-5-6-thinking' and metadata['thinking_effort']==proof['actual_chatgpt_configuration']['thinking_effort']=='max',
 'returned_commit_repository_branch_match_HEAD':head==EXPECTED_HEAD==source['commit'] and source['repository']=='vubaoha034-hash/shenmei' and source['branch']=='visual-program-distillation-v2-photography-design-20260814',
 'returned353_375_and_lock_SHA_match_native3':source['lock_revision']==l['revision']==a['task_lock']['revision']==c['task_lock']['revision']==353 and source['checkpoint_sequence']==c['sequence']==375 and source['native_lock_sha256']==lock_sha==a['task_lock']['sha256']==c['task_lock']['sha256'],
 'returned_task_stage_and_next_match_native':derived['task_id']==l['current_task_id'] and derived['stage']==l['current_stage']==c['current_stage']==c['current_focus']==a['current_mainline']['current_visual_unit']=='LIUXIANSHENG_REFERENCE_TYPOGRAPHY_CONTENT_TRANSFER_EXPERIMENT' and derived['next_required_action']==l['next_required_action']==c['next_required_action']==a['current_mainline']['next_required_action']=='LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER',
 'only_minimum1_call_claimed':proof['verified_actual_readonly_calls_minimum']==1,
 'old_catalog_unverified_report_remains_sealed':sha(old_before)==OLD_SHA and (OUT/'INDEPENDENT_INSTALLATION_VERIFICATION.json').read_bytes()==old_before
}
native_evidence=[{'path':p,'method':'Actual HEAD Git blob; no CRLF worktree substitution','commit':head,'sha256':sha(b),'bytes':len(b)} for p,b in native_raw.items()]
public_path=ROOT/PUBLIC
public_files=[]
if public_path.is_dir():
 for p in sorted(public_path.iterdir()):
  if p.is_file():
   data=p.read_bytes();public_files.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(data),'bytes':len(data)})
public_assessment={'expected_directory':PUBLIC,'exists_at_bounded_check':public_path.is_dir(),'files':public_files,'assessment':'Not present at bounded check; public installed/connected/read-only declarations not independently inspected here.' if not public_files else 'File inventory is present; contents require separately authorized bounded review before any public-claim verdict.'}
# Preserve the supplied original evidence bytes under the authorized private
# directory. It contains no network headers or profile credentials.
write('ACTUAL_TOOL_PROOF_READ_COPY.json',raw)
write('ACTUAL_TOOL_PREFIX_AND_NATIVE_READ_RECORD.json',{'input_SHA256':sha(raw),'capture_source':'Root observed HTTP200 browser response excerpt; child reviewed saved bytes only','input_bytes':len(raw),'actual_tool_invocation_message':inv,'actual_tool_response_prefix':prefix,'prefix_characters':len(prefix),'independently_decoded_complete_binding_fields':derived,'native_blobs':native_evidence,'public_evidence_bounded_inventory':public_assessment})
failed=[k for k,v in checks.items() if not v]
report={'schema':'supplemental-actual-plugin-tool-evidence-review/v1','recorded_at_utc':datetime.now(timezone.utc).isoformat(),'verdict':'PASS_RECORDED_READONLY_TOOL_PREFIX_NATIVE_BINDING_WITH_LIMITATIONS' if not failed else 'FAIL_RECORDED_TOOL_EVIDENCE_REVIEW','scope':'File-only review of Root-captured actual HTTP200 tool invocation/response prefix and current HEAD native3. This observer executed no browser or plugin call.','checks':checks,'failed_checks':failed,'actual_input':{'path':SOURCE.relative_to(ROOT).as_posix(),'sha256':sha(raw),'bytes':len(raw),'private_read_copy':'ACTUAL_TOOL_PROOF_READ_COPY.json'},'raw_read_record':'ACTUAL_TOOL_PREFIX_AND_NATIVE_READ_RECORD.json','runtime':{'environment':'ChatGPT browser conversation captured by Root','actual_call_recipient':inv['recipient'],'actual_path':args['path'],'actual_args':args['args'],'actual_invocation_message_id':inv['id'],'actual_tool_response_message_id':proof['actual_tool_response_message_id'],'actual_metadata_model_slug':metadata['model_slug'],'actual_metadata_thinking_effort':metadata['thinking_effort'],'not_claimed':'Sol/Max runtime, external cold review or a direct call by this Codex observer'},'verified_returned_fields':derived,'minimum_actual_readonly_call_evidence':1,'second_call':'UNVERIFIED; assistant self-description excluded','response_completeness':{'complete_full_HTTP_response_saved':False,'inspector_inline_body_truncation_reported':True,'raw_tool_message_prefix_characters':len(prefix),'complete_prefix_binding_fields_verified':['source','task_id','stage','next_required_action'],'not_in_saved_prefix':['S7 artwork object/SHA','reference object/SHA','acceptance/count fields','full tool message metadata/parent linkage','second actual invocation/result'],'fragment_decode_method':'Only the missing outer string delimiter was appended to parse the saved string fragment; individual already-complete fields decoded with raw_decode. This is never a reconstructed complete provider response.'},'native_source':{'HEAD':head,'files':native_evidence,'revision':353,'checkpoint':375,'raw_stage':derived['stage'],'next':derived['next_required_action'],'native_current_S7':'Existing native binding only; not a newly observed tool-response artwork field'},'installation_connection_scope':{'reported_UI':'Root reports installed sidebar and connected account; this file-only observer did not inspect browser UI.','actual_readonly':'Recorded assistant api_tool.call_tool invocation and tool-authored non-error native binding prefix support at least1 actual readonly get_current_workflow response in the captured ChatGPT conversation.','global_or_Codex_tool_exposure':'No new catalog check; old report remains true for that observer session/time.','public_evidence':public_assessment,'old_HTTP401':'Historical service-token/direct-read failures are preserved in their own scope. This evidence does not convert them to successes or imply the captured browser call failed.'},'not_verified':['Second get_current_workflow call','Complete returned S7/reference projection','Feedback save/read or durable production persistence','OAuth/token details or global installation state','Sol/Max model execution','New image/photography/Figma, pixel/taste/cold review, universal system acceptance'],'privacy':{'profile_name_email_avatar_token_OAuth_parameters_saved':False,'network_headers_saved':False},'actions':{'business_public_source_writes':0,'browser_UI_actions':0,'network_plugin_HTTP_calls':0,'other_chat_messages':0,'feedback_writes':0,'subagents':0,'tests_validators_pixels':0,'private_write_scope':OUT.relative_to(ROOT).as_posix(),'stop_after_record':True},'prior_report':{'path':'INDEPENDENT_INSTALLATION_VERIFICATION.json','sha256':OLD_SHA,'rewritten':False}}
write('SUPPLEMENTAL_ACTUAL_TOOL_EVIDENCE_REVIEW.json',report)
names=['review_actual_tool_evidence.py','ACTUAL_TOOL_PROOF_READ_COPY.json','ACTUAL_TOOL_PREFIX_AND_NATIVE_READ_RECORD.json','SUPPLEMENTAL_ACTUAL_TOOL_EVIDENCE_REVIEW.json']
inventory=[]
for n in names:
 p=OUT/n;b=p.read_bytes();inventory.append({'path':n,'sha256':sha(b),'bytes':len(b)})
write('SUPPLEMENTAL_EVIDENCE_SHA256_INDEX.json',{'files':inventory})
print(json.dumps({'verdict':report['verdict'],'report_sha256':sha((OUT/'SUPPLEMENTAL_ACTUAL_TOOL_EVIDENCE_REVIEW.json').read_bytes()),'checks':len(checks),'failed_checks':failed,'minimum_actual_call_evidence':1,'metadata_model':metadata['model_slug'],'metadata_effort':metadata['thinking_effort'],'native':'353/375','public_directory_exists':public_path.is_dir(),'old_report_unchanged':checks['old_catalog_unverified_report_remains_sealed']},ensure_ascii=False))
raise SystemExit(bool(failed))
