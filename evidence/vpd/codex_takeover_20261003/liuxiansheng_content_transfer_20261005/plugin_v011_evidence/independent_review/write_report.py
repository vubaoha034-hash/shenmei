from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

out=Path(__file__).resolve().parent
repo=out.parents[1]
def load(name): return json.loads((out/name).read_text('utf-8'))
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
source=load('FINAL_SOURCE_MANIFEST.json')
run=load('RUN_SUMMARY.json')
cases=load('INDEPENDENT_CASE_RESULTS.json')
freeze=load('ROOT_FREEZE_COMPARISON.json')
old=load('OLD_SOURCE_PRESERVATION.json')
remote=load('REMOTE_NATIVE_COMPARISONS.json')
stability=load('BEFORE_AFTER_SOURCE_STABILITY.json')
commands=load('COMMAND_RESULTS.json')
assert run['tests_exit']==run['independent_exit']==run['build_exit']==0
assert cases['passed']==cases['total']==22 and cases['failed']==0
assert freeze['all_equal'] and freeze['file_count']==12 and stability['all_unchanged']
assert len(old['files'])==15 and all(x['raw_bytes_equal'] and x['published_git_equivalent'] for x in old['files'])
core=next(x for x in source['files'] if x['path'].endswith('/core.mjs'))
worker=next(x for x in source['files'] if x['path'].endswith('/worker.mjs'))
entry=next(x for x in remote['files'] if x['path'].endswith('/S7_FINAL_REUSE.md'))
transport=[]
for name in ['PLUGIN_V011_LIVE_GITHUB_READBACK.json','PLUGIN_V011_LIVE_GITHUB_DIAGNOSTIC.json']:
    record=load('parent_transport_records/'+name)
    transport.append({'path':'parent_transport_records/'+name,'sha256':digest(out/'parent_transport_records'/name),'http_status':record['http_status'],'complete_current_result':record['current'],'production_plugin_connection_verified':record['production_plugin_connection_verified'],'scope':record['scope'],'github_calls':record['github_calls']})
evidence_paths=['FINAL_SOURCE_MANIFEST.json','ROOT_FREEZE_COMPARISON.json','OLD_SOURCE_PRESERVATION.json','SOURCE_DIFFS.json','REMOTE_NATIVE_COMPARISONS.json','INDEPENDENT_CASE_RESULTS.json','BEFORE_AFTER_SOURCE_STABILITY.json','COMMAND_RESULTS.json','RUN_SUMMARY.json','logs/final_source_tests.stdout.txt','logs/final_source_tests.stderr.txt','logs/independent_cases.stdout.txt','logs/independent_cases.stderr.txt','logs/build.stdout.txt','logs/build.stderr.txt','independent_cases.mjs','review_runner.py']
report={
 'schema':'vpd-plugin-v011-independent-engineering-review/v1',
 'recorded_at':datetime.now(timezone.utc).isoformat(),
 'verdict':'PASS',
 'pass_scope':'FROZEN_SOURCE_LOGIC_AND_LOCAL_BUILD_ARTIFACT_ONLY',
 'blocking_findings':[],
 'context':{'agent_task':'/root/s4_fresh_repository_entry_test','thread_id':'01a10ee8-1549-71c2-bdde-566204a0a8e5','parent_session_id':'01a0ffab-c9b7-7c40-b55b-e51535c156dd','prior_S4_publication_context_retained':True,'aesthetic_cold_review':False,'reviewed_authored_changes':'Root v0.1.1; reviewer did not edit release source','recursive_delegation':False},
 'repository':{'name':'vubaoha034-hash/shenmei','branch':'visual-program-distillation-v2-photography-design-20260814','checkout':str(repo),'native_fixed_commit':run['fixed_commit'],'native_fixed_parent':run['parent'],'legacy_fixed_commit':cases['legacy_commit'],'new_release_status_at_review':'Untracked v0.1.1 source under the authority checkout, not deployed or published by this reviewer'},
 'frozen_source':{'root_manifest_path':freeze['manifest_path'],'root_manifest_sha256':freeze['manifest_sha256'],'file_count':12,'all_12_match_actual_bytes':True,'core_sha256':core['sha256'],'worker_sha256':worker['sha256'],'before_after_27_source_files_unchanged':True,'new_source_files':source['files']},
 'old_source_preservation':{'published_baseline_commit':run['fixed_commit'],'files':15,'actual_working_bytes_equal_fixed_git_blobs':15,'before_after_raw_sha_unchanged':True,'copied_baseline_core_sha256':'4c51a64df0a7da97058134683780759b62af21f6c1c56f8901f7f035113034a5','details':'OLD_SOURCE_PRESERVATION.json'},
 'reviewed_change':{'core':'Only two authorized entry paths, preserve canonical native entry projection equality and SHA; return entryRef from snapshot and its bound path; initialize 0.1.1','worker':'Only User-Agent and GET homepage version labels changed to 0.1.1; HTTP/auth/feedback dispatch unchanged','package_and_tests':'Default test includes all three test files; initialization expectation 0.1.1; local byte-identical baseline import removes parent-source import dependency','unchanged_guards':['canonical repository/branch and native task identity','native lock SHA/revision plus checkpoint/adapter mirrors','locked mainline ID and pinned policy hashes','roadmap/evidence SHA and safe repository paths','trusted runtime identity plus authorization; caller identity cannot override','HEAD/expected commit drift rejection','recorded pixel evidence is not reexecuted or human acceptance','no artwork generation, business-state writes, training/scheduling or automatic promotion']},
 'native_recovery':{'current':cases['observations']['current'],'legacy':cases['observations']['legacy'],'entry_sha256':entry['remote_sha256'],'new_entry_actual_bytes_read':True,'three_native_files_bound_to_actual_fixed_lock_sha':True,'correct_unique_next_action':'LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER','current_human_acceptance':'PENDING','promotion_allowed':False,'original_0_1_0_current_status':409,'original_0_1_0_error':'Current reuse entry mismatch'},
 'tests':{'final_source_suite':{'passed':40,'failed':0,'exit_code':0,'source_files':['core.test.mjs','worker.test.mjs','entry.test.mjs'],'log':'logs/final_source_tests.stdout.txt'},'independently_authored_real_git_blob_cases':{'passed':22,'failed':0,'exit_code':0,'results':'INDEPENDENT_CASE_RESULTS.json','coverage':['actual current S7 350/372','actual legacy S4 344/366','old source regression reproduced','entry byte tamper','coherent unknown entry with correct own SHA','allowed entry projection mismatch','coherent mainline tamper','repository path traversal','native lock hashes and identity/action mismatches','HEAD drift and wrong expected commit','missing/unauthorized/caller supplied identity','non-authorizing transfer plan','built core and built HTTP worker actually read S7','built adapter immutable URL/version/cache behavior with mock transport']},'local_storage_tests':'Synthetic test-only SQLite files confined below this private review directory; no production D1 or genuine feedback writes'},
 'build':{'exit_code':0,'cwd':str(out/'build_copy'),'source_snapshot':'source_snapshot/v0.1.1','artifact':'build_copy/dist/server/index.js','artifact_core':'build_copy/dist/server/core.mjs','emitted_worker_core_and_hosting_match_frozen_sources':True,'built_worker_imports_and_executes_new_core':True,'built_worker_current_native_revision':350,'built_worker_checkpoint_sequence':372,'built_initialize_and_homepage_version':'0.1.1','scope':'Actual local build and executed artifact; no Site deployment, hosted MCP call or production auth verified'},
 'actual_remote_read':{'connector':'GitHub fetch_file','commit':run['fixed_commit'],'successful_fixed_commit_reads':4,'all_4_bytes_equal_local_git_blob':True,'files':remote['files'],'initial_path_parameter_errors':2,'one_bounded_parameter_correction':'First two requests omitted vpd; corrected from actual source PATHS. Original 404 responses retained in raw_remote/00.json and 01.json. No further remote retries.'},
 'transport_limitation':{'parent_local_real_network_records':transport,'complete_new_worker_real_github_readback':False,'hosted_production_MCP_verified':False,'production_identity_and_header_stripping_verified':False,'production_feedback_persistence_verified':False,'not_retried':True,'note':'Connector reads prove the four fixed remote native/entry bytes exist; they do not establish worker production transport or hosted identity. Root local network readback/diagnostic each returned 502; diagnostic lock read timed out at 15 seconds.'},
 'not_checked':['Site deployment or live hosted tool connection','production owner/private audience enforcement and trusted header stripping','production D1 feedback write/read','default test in Site mirror without authoritative 3e6/4d Git objects','new Drive/Figma/image calls or pixel/aesthetic review','full history validator','time/cost savings or learned general taste quality'],
 'write_boundary':{'sole_write_root':str(out),'native_public_source_business_writes':False,'production_feedback_writes':False,'deployment_or_publication':False,'drive_figma_image_calls':0,'business_state_and_artwork_acceptance_modified':False},
 'actual_tools_and_commands':{'GitHub_connector_reads':6,'GitHub_successful_reads':4,'figma':0,'drive':0,'imagegen':0,'native_full_validator':0,'commands':commands,'method':'Source/Git-blob reads, SHA256 comparisons, Node tests and isolated build; write only private evidence'},
 'evidence':[{'path':path,'sha256':digest(out/path)} for path in evidence_paths],
 'release_gate':'No blocking engineering findings in the exact reviewed frozen source and local build. Root can use this bounded review for its authorized deployment decision; production connection and transport remain unverified. This report supplies no aesthetic, human-acceptance or deployment PASS.'
}
destination=out/'REPORT.json'
destination.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps({'report':str(destination),'sha256':digest(destination),'verdict':report['verdict'],'scope':report['pass_scope'],'source_files':12,'tests':'40/40','independent_cases':'22/22','hosted_MCP_verified':False},ensure_ascii=False,indent=2))
