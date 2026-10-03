#!/usr/bin/env python3
"""EXPERIMENTAL FAILED CLI carrier; not the live production review entry.

Uses the signed-in Codex account, no model API key or paid external compute.
Raw logs stay private; publish only non-sensitive evidence and final judgments.
Actual task CLI failed TLS. The working fork-none carrier and its runtime
collector are documented in REUSE_FINAL.md. CLI results never auto-promote.
"""
import argparse, datetime, hashlib, json, os, pathlib, shutil, subprocess, tempfile

PROMPT = '''你是独立中文品牌海报审稿人。这是全新的项目外审核上下文。
只看本消息与4张实际附件。不要浏览仓库、历史聊天、记忆或其他文件；不得执行文件读取/检索命令，不得调用子代理。必要时只可查看本次附件像素。
附件顺序：1=校准正样本P；2=校准负样本N；3=指定参考R；4=匿名检验作品T。
P的刘先生认可范围仅为整体图文层级、字标和文字系统，摄影并未通过；N被真人整体否决，字标印刷味过强、标题与摄影割裂。校准仅帮助理解实际偏好，不降低专业要求。
T的真人结论与过去AI结论均隐藏。T没有参与校准。R只学习上半横版广告的视觉机制，下半墙面示意不进入成品。禁止照搬R品牌、独特字形或水印。
任务：1536×1024、3:2横版平面茶产品海报，品牌“茶作”，准确文案“一杯茶，慢下来”（保留文案，不添加售价、功效、产地等事实）。一杯茶、干茶、鲜叶和木托盘。设计须从茶作字形自身建立识别性，独立叶子/装饰贴到普通字体旁边不成立。照片、中文字标、辅助文字和图文关系都看实际像素；工程身份检查由执行者另做，单靠此视觉输入无法证明隐藏图层/字节保护，应记UNKNOWN。
先给出可见事实，再判断技术文字/画幅与设计品质。字标完成度、图文关系、品牌辨识、整体完成度、指定参考差距分别给具体区域证据与优先问题；可以相对样本比较，但无须泛化数字评分。
标准：AI_PASS仅意味着达到内部交付审核标准，绝不代表刘先生认可；关键字形/图文/整体问题未解决应AI_FAIL；看不到任一必要附件请UNABLE_TO_EVALUATE。
不得因为流程完成或候选投入多而宽松。只输出JSON，包含 task_id（由下方给定）、version、pixels_seen、verdict、observations（至少5条含区域与可见证据）、technical（text_readback、aspect、hidden_source_protection='UNKNOWN'）、design（wordmark、image_text_relation、brand_identity、completion、reference_gap）、priority_problems、calibration_comparison、personal_fit=null、human_verdict='HIDDEN_PENDING'。
'''

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(); p.add_argument('--positive',required=True);p.add_argument('--negative',required=True);p.add_argument('--reference',required=True);p.add_argument('--target',required=True);p.add_argument('--out',required=True);p.add_argument('--version',required=True);p.add_argument('--task-id',required=True);p.add_argument('--timeout',type=int,default=120);args=p.parse_args()
    if not 1<=args.timeout<=300:raise ValueError('REVIEW_TIMEOUT_OUT_OF_BOUNDS')
    out=pathlib.Path(args.out).resolve()
    private=pathlib.Path(__file__).resolve().parents[1]/'.liu-visual-private'
    if not out.is_relative_to(private.resolve()):raise ValueError('RAW_CLI_LOGS_MUST_STAY_PRIVATE')
    out.mkdir(parents=True,exist_ok=True)
    cold=pathlib.Path(tempfile.mkdtemp(prefix='vpd-cold-review-'))
    images=[]
    for n,src in zip(['P.png','N.png','R.jpg','T.png'],[args.positive,args.negative,args.reference,args.target]):
        dst=cold/n;shutil.copyfile(src,dst);images.append(dst)
    prompt=PROMPT+'\ntask_id='+args.task_id+'\nversion='+args.version+'\n'
    (out/'PROMPT.txt').write_text(prompt,encoding='utf-8')
    command=['codex','exec','--ignore-user-config','--skip-git-repo-check','-C',str(cold),'-s','read-only','-m','gpt-6.1-sol','-c','model_reasoning_effort="max"','--json','--color','never','-o',str(out/'review.raw.txt')]
    for f in images: command.extend(['-i',str(f)])
    command.append('-')
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    exit_code=-1
    with (out/'private-log.jsonl').open('w',encoding='utf-8') as f:
        try:
            r=subprocess.run(command,input=prompt,encoding='utf-8',stdout=f,stderr=subprocess.STDOUT,timeout=args.timeout)
            exit_code=r.returncode
        except subprocess.TimeoutExpired:
            f.write(json.dumps({'type':'error','message':'BOUNDED_REVIEW_TIMEOUT'})+'\n')
    raw=(out/'review.raw.txt').read_text(encoding='utf-8') if (out/'review.raw.txt').exists() else ''
    try: result=json.loads(raw.removeprefix('```json').removesuffix('```').strip())
    except json.JSONDecodeError: result={'verdict':'UNABLE_TO_EVALUATE','error':'NON_JSON_OR_NO_FINAL_RESPONSE','raw_saved':bool(raw)}
    log=(out/'private-log.jsonl').read_text(encoding='utf-8')
    prohibited=[];tool_reads=[];thread=None
    for line in log.splitlines():
        try: event=json.loads(line)
        except json.JSONDecodeError: continue
        if event.get('type')=='thread.started': thread=event.get('thread_id')
        item=event.get('item',{})
        if item.get('type') in ['command_execution','mcp_tool_call']: tool_reads.append(item)
        if item.get('type')=='command_execution' or ('mcp' in item.get('type','') and item.get('tool')!='view_image'):prohibited.append(item.get('type'))
    if prohibited: result={'verdict':'UNABLE_TO_EVALUATE','error':'REVIEW_CONTEXT_READ_SCOPE_VIOLATED','review_before_scope_audit':result}
    if exit_code!=0 or result.get('pixels_seen')!=['P','N','R','T']:
        result={'verdict':'UNABLE_TO_EVALUATE','error':'EXIT_OR_REQUIRED_PIXEL_EVIDENCE_FAILED','unverified_reviewer_output':result}
    # CLI configuration requests are not actual model/isolation proof. This
    # branch never promotes a raw answer; the live fork-none collection path
    # performs runtime turn-context, spawn and four ImageView audits separately.
    if result.get('verdict') in ['AI_PASS','AI_FAIL']:
        result={'verdict':'UNABLE_TO_EVALUATE','error':'CLI_RUNTIME_AUDIT_NOT_VERIFIED','unverified_reviewer_output':result}
    result.update(reviewer={'carrier':'FRESH_EXTERNAL_CODEX_EXEC','model_requested':'gpt-6.1-sol','effort_requested':'max','thread_id':thread},reviewed_at=stamp,input_bindings=[{'neutral_id':n,'sha256':sha(f)} for n,f in zip(['P','N','R','T'],images)],isolation={'fresh_process':True,'outside_project_directory':True,'ignore_user_config':True,'creator_history_provided':False,'test_human_verdict_provided':False,'prior_ai_verdict_provided':False,'tool_read_scope_violations':prohibited,'image_attachments':4,'verified':False,'actual_model_setting_verification':'UNVERIFIED_NOT_PROMOTABLE'},exit_code=exit_code)
    (out/'REVIEW.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'verdict':result.get('verdict'),'result':str(out/'REVIEW.json'),'exit_code':exit_code,'thread_id':thread},ensure_ascii=False))
if __name__=='__main__': main()
