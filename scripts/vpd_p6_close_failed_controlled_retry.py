#!/usr/bin/env python3
"""Close the consumed Doufang B controlled retry as a placement blocker.

Records the failed formal retry and the successful nested diagnostic probe, then
restores fail-closed P6 authority. No raster upload or Figma write occurs here.
"""
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOW='2026-09-14T01:27:00Z'
LOCK=ROOT/'continuity/vpd/CURRENT_TASK_LOCK.json'
CP=ROOT/'continuity/vpd/LATEST_CHECKPOINT.json'
ADAPTER=ROOT/'PROJECT_CONTROL_ADAPTER.json'
LEDGER=ROOT/'continuity/vpd/state_ledger/system_validation.jsonl'
FORMAL_RECEIPT_REL='evidence/vpd/figma_upload_relay/receipts/P6-DOUFANG-B-LIVE-20260914-03.json'
NESTED_RECEIPT_REL='evidence/vpd/figma_upload_relay/receipts/P6-NESTED-PLACEMENT-PROBE-20260914-01.json'
BLOCKER_REL='evidence/vpd/p6_authority_repair_v1/DOUFANG_B_CONTROLLED_RETRY_PLACEMENT_BLOCKER_20260914.json'
OLD_STATUS='VPD_P6_RELAY_PLACEMENT_PROTOCOL_VERIFIED_DOUFANG_B_RETRY_READY'
NEW_STATUS='VPD_P6_RELAY_UPLOAD_PASS_PLACEMENT_MISMATCH_BLOCKED'
OLD_ACTION='RUN_LIVE_DOUFANG_B_RELAY'
NEW_ACTION='RESOLVE_P6_RELAY_PLACEMENT_MISMATCH_NO_REUPLOAD'
UPLOAD_HASH='23926508e3fc10dd61e9df883e018e721cb7cc1f'
OBSERVED_HASH='7f57313e7409ff16d76ab867893a1229a5769962'
NESTED_HASH='1c9cbf9a9fe1017a3f44eeed563562db8222c889'
SOURCE_SHA='78137a59779a37f08b4df3aef23164d115cc61afb443610b6f6eb066e99671d9'

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def digest(p): return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def eh(e): return hashlib.sha256(json.dumps(e,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    lock,cp,adapter=read(LOCK),read(CP),read(ADAPTER)
    formal=read(ROOT/FORMAL_RECEIPT_REL); nested=read(ROOT/NESTED_RECEIPT_REL)
    assert lock['revision']==27 and lock['status']==OLD_STATUS and lock['next_required_action']==OLD_ACTION
    assert cp['sequence']==49 and cp['status']==OLD_STATUS and cp['next_required_action']==OLD_ACTION
    assert adapter['task_lock']['revision']==27
    assert formal['status']=='UPLOAD_PASS' and formal['http_status']=='200' and formal['node_id']=='12:12'
    assert formal['source_sha256']==SOURCE_SHA and formal['response']['imageHash']==UPLOAD_HASH
    assert nested['status']=='UPLOAD_PASS' and nested['http_status']=='200' and nested['node_id']=='44:3'
    assert nested['response']['imageHash']==NESTED_HASH
    assert lock['p6_integrated_design']['bound_count']==1
    assert [f['bound'] for f in lock['p6_integrated_design']['frames']]==[True,False,False,False]

    blocker={
      'schema_version':'vpd-p6-relay-placement-blocker/v2',
      'status':'BLOCKED_AFTER_CONTROLLED_RETRY',
      'scope':'FORMAL_DOUFANG_B_RETRY_CONSUMED_NO_FURTHER_FORMAL_REUPLOAD',
      'figma_file_key':'uyDxOoN1iNDPpEHTKSUWg1',
      'node_id':'12:12',
      'receipt':{'path':FORMAL_RECEIPT_REL,'sha256':digest(ROOT/FORMAL_RECEIPT_REL)},
      'upload_imageHash':UPLOAD_HASH,
      'observed_imageHash':OBSERVED_HASH,
      'image_store_contains_upload_hash':False,
      'stop_required':True,
      'frozen_source_sha256':SOURCE_SHA,
      'controlled_retry':{
        'receipt_status':'UPLOAD_PASS','http_status':200,'fresh_mint_targetNodeId':'12:12',
        'source_identity_verified':True,'formal_node_changed':False
      },
      'nested_probe':{
        'node_id':'44:3','parent_frame_id':'44:2',
        'receipt':{'path':NESTED_RECEIPT_REL,'sha256':digest(ROOT/NESTED_RECEIPT_REL)},
        'returned_imageHash':NESTED_HASH,'node_fill_hash':NESTED_HASH,
        'image_store_present':True,'verdict':'PASS_NESTED_TARGET_PLACEMENT'
      },
      'established':[
        'A fresh node-targeted mint explicitly returned targetNodeId 12:12 for the formal controlled retry.',
        'The frozen Doufang B source identity matched the freeze SHA-256 and relay returned HTTP 200 / UPLOAD_PASS.',
        'The returned formal imageHash was still absent from the current Figma file image store and node 12:12 retained its previous imageHash.',
        'A separate Frame-nested diagnostic target 44:3 successfully committed its probe image into the same Figma file image store and updated its IMAGE/FILL hash.',
        'Therefore generic nested-node placement failure is ruled out; the unresolved cause is specific to the Doufang B source path or formal node 12:12 state/semantics.'
      ],
      'not_established':[
        'Whether the failure is caused by properties/history of formal node 12:12.',
        'Whether the 422265-byte JPEG source triggers a Figma MCP placement defect despite transport acceptance.',
        'Whether a backend transaction identity/caching defect maps repeated identical source bytes to the same noncommitted imageHash.'
      ],
      'next_diagnostic':'UPLOAD_EXACT_FROZEN_DOUFANG_B_SOURCE_TO_ISOLATED_SCRATCH_TARGET_NO_FORMAL_NODE_WRITE',
      'recorded_at':NOW
    }
    write(ROOT/BLOCKER_REL,blocker); blocker_sha=digest(ROOT/BLOCKER_REL)

    lock['revision']=28
    lock['preserved_prior_revision']={'revision':27,'git_blob_sha':None,'note':'Revision 27 authorized exactly one controlled Doufang B retry after same-file placement-protocol verification; that retry has now been consumed.'}
    lock['p6_integrated_design']['status']='UPLOAD_PASS_PLACEMENT_MISMATCH_BLOCKED'
    lock['figma_upload_relay']['status']='UPLOAD_PASS_PLACEMENT_MISMATCH_BLOCKED'
    lock['current_stage']='The single authorized Doufang B controlled retry was consumed: fresh upload_assets mint explicitly targeted 12:12 and relay returned HTTP 200 / UPLOAD_PASS for the frozen source, yet the returned imageHash remained absent from the Figma file image store and node 12:12 retained the old hash. A Frame-nested scratch probe 44:3 succeeded end-to-end, ruling out generic nested-node placement failure. Formal reupload is stopped; Tea A/B remain untouched. Next diagnosis must use the exact frozen Doufang B source on an isolated scratch target, never the formal node.'
    lock['status']=NEW_STATUS; lock['next_required_action']=NEW_ACTION
    lock['completed_this_revision']=[
      'consumed the one authorized controlled Doufang B retry with fresh targetNodeId 12:12',
      'verified frozen source SHA-256 and HTTP 200 / UPLOAD_PASS receipt',
      'verified returned formal imageHash is absent from current file image store and 12:12 retained old hash',
      'verified Frame-nested scratch target 44:3 placement passes end-to-end',
      'ruled out generic nested-node placement failure and restored fail-closed authority'
    ]
    lock['updated_at']=NOW
    lock['input_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    lock['blockers']=[
      'The single authorized formal Doufang B retry was consumed without observable Figma file commit/placement.',
      'No further formal 12:12 reupload is authorized until exact-source scratch diagnosis separates source-specific from node-specific failure.',
      'Tea A/B remain blocked until Doufang B binding passes.',
      'Historical ledger prefix preserved with three known event-hash defects; not recertified.'
    ]
    lock.pop('relay_placement_protocol_probe',None)
    lock['relay_placement_blocker']={'path':BLOCKER_REL,'sha256':blocker_sha}
    lock['diagnostic_next_required_action']='UPLOAD_EXACT_FROZEN_DOUFANG_B_SOURCE_TO_ISOLATED_SCRATCH_TARGET_NO_FORMAL_NODE_WRITE'
    write(LOCK,lock); lock_sha=digest(LOCK)

    cp['sequence']=50; cp['recorded_at']=NOW; cp['current_focus']=lock['current_stage']
    for x in ['p6_doufang_B_controlled_retry_consumed_placement_failed','p6_nested_target_probe_pass']:
        if x not in cp['completed']: cp['completed'].append(x)
    cp['blocked']=list(lock['blockers']); cp['next_required_action']=NEW_ACTION
    cp['relay']['status']='UPLOAD_PASS_PLACEMENT_MISMATCH_BLOCKED'; cp['status']=NEW_STATUS
    cp['task_lock']={'path':'continuity/vpd/CURRENT_TASK_LOCK.json','sha256':lock_sha}
    cp['requirements']['p6_integrated_design']['status']='UPLOAD_PASS_PLACEMENT_MISMATCH_BLOCKED'

    adapter['vpd_system_goal_authority']['checkpoint']=NEW_STATUS
    adapter['vpd_system_goal_authority']['next_required_action']=NEW_ACTION
    adapter['task_lock']['revision']=28; adapter['task_lock']['sha256']=lock_sha

    raw=LEDGER.read_bytes(); lines=raw.splitlines(); prev=json.loads(lines[-1].decode())
    assert prev['event_id']==cp['ledger_tails']['system_validation']['event_id'] and prev['event_hash']==cp['ledger_tails']['system_validation']['event_hash']
    event={'schema_version':'upcp-state-ledger-event/v1','event_id':'EVT-VPD-P6-CONTROLLED-RETRY-PLACEMENT-FAILED-20260914-001','event_type':'P6_DOUFANG_B_CONTROLLED_RETRY_CONSUMED_PLACEMENT_FAILED_NESTED_PROBE_PASS','stream_id':'system_validation','project_id':'visual-aesthetic-vpd','task_id':'VPD-SYSTEM-LEVEL-HOLDOUT-TRANSFER-VALIDATION-V1','previous_event_id':prev['event_id'],'previous_event_hash':prev['event_hash'],'recorded_at':NOW,'input_remote_head':lock['input_commit'],'lock_sha256':lock_sha,'scope':'FORMAL_RETRY_STOP_EXACT_SOURCE_SCRATCH_DIAGNOSIS_NEXT','blocker':{'path':BLOCKER_REL,'sha256':blocker_sha},'next_required_action':NEW_ACTION}
    event['event_hash']=eh(event)
    if raw and not raw.endswith(b'\n'): raw+=b'\n'
    raw+=(json.dumps(event,ensure_ascii=False,separators=(',',':'))+'\n').encode(); LEDGER.write_bytes(raw)
    cp['ledger_tails']['system_validation']={'event_id':event['event_id'],'event_hash':event['event_hash']}
    write(CP,cp); write(ADAPTER,adapter)
    assert read(CP)['task_lock']['sha256']==digest(LOCK)
    assert read(ADAPTER)['task_lock']['sha256']==digest(LOCK)

if __name__=='__main__': main()
