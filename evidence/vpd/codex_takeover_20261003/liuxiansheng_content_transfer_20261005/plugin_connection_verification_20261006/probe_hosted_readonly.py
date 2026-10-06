import sys, json, hashlib, datetime, urllib.request, urllib.error, ssl
from pathlib import Path

out = Path(__file__).resolve().parent
print('READY_FOR_SITES_AUTHORIZED_SERVICE_TOKEN', flush=True)
if sys.stdin.isatty():
    import msvcrt
    characters = []
    while True:
        character = msvcrt.getwch()
        if character in ('\r', '\n'):
            break
        characters.append(character)
    config = json.loads(''.join(characters))
else:
    config = json.loads(sys.stdin.readline())
token = config.pop('token')
url = config['mcp_url']
records = []
calls = [
    {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'bounded-sites-service-readonly-verifier', 'version': '1.0'}}},
    {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list', 'params': {}},
    {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'get_current_workflow', 'arguments': {}}},
]
for rpc in calls:
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    request = urllib.request.Request(url, data=json.dumps(rpc).encode('utf-8'), method='POST', headers={
        'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'MCP-Protocol-Version': '2025-06-18', 'OAI-Sites-Authorization': 'Bearer ' + token,
    })
    record = {'time_utc': start, 'request': rpc, 'url': url, 'trusted_identity_headers_supplied_by_verifier': False}
    try:
        with urllib.request.urlopen(request, timeout=25, context=ssl.create_default_context()) as response:
            raw = response.read(300001)
            assert len(raw) <= 300000
            record.update(status=response.status, content_type=response.headers.get('Content-Type'), body_bytes=len(raw), body_sha256=hashlib.sha256(raw).hexdigest())
    except urllib.error.HTTPError as error:
        raw = error.read(300001)
        record.update(status=error.code, content_type=error.headers.get('Content-Type'), body_bytes=len(raw), body_sha256=hashlib.sha256(raw).hexdigest())
    except Exception as error:
        record.update(transport_error=type(error).__name__ + ': ' + str(error))
        raw = b''
    try:
        record['body'] = json.loads(raw.decode('utf-8'))
    except (ValueError, UnicodeError):
        record['body_text'] = raw.decode('utf-8', errors='replace')[:2000]
    records.append(record)
    print(json.dumps({k:v for k,v in record.items() if k not in ['body','body_text']}, ensure_ascii=False), flush=True)
    if record.get('status') != 200 or 'error' in record.get('body', {}):
        break
result = {
    'schema': 'bounded-sites-hosted-readonly-service-probe/v1',
    'scope': 'OFFICIAL_SITES_PROVIDED_SERVICE_TOKEN_NOT_CHATGPT_PLUGIN_CONNECTION',
    'project_id': config['project_id'], 'published_version': 3,
    'no_forged_user_identity': True, 'TLS_verification': True,
    'connection_and_oauth_not_verified': True, 'human_feedback_write_calls': 0,
    'records': records,
}
(out/'ACTUAL_HOSTED_SERVICE_READONLY_PROBE.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('SAVED_ACTUAL_HOSTED_SERVICE_READONLY_PROBE', flush=True)
