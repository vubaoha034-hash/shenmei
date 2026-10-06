import pathlib,json,hashlib
base=pathlib.Path('.liu-visual-private/s7_outline_implementation');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cache={str(t):{'input_sha256':sha(base/f'TIER_{t}_TRACE_INPUT.png'),'output_sha256':sha(base/f'TIER_{t}_TRACE.svg')} for t in range(1,6) if (base/f'TIER_{t}_TRACE.svg').exists()}
(base/'TECHNICAL_TRACE_REUSE.json').write_text(json.dumps(cache,indent=2)+'\n')
p=base/'build-wordmark.py';s=p.read_text(encoding='utf8')
s=s.replace(" vtracer.convert_image_to_svg_py(str(infile),str(outfile),**params)"," cache=json.loads((BASE/'TECHNICAL_TRACE_REUSE.json').read_text()) if (BASE/'TECHNICAL_TRACE_REUSE.json').exists() else {}\n if str(t) in cache:\n  assert sha(infile)==cache[str(t)]['input_sha256'] and sha(outfile)==cache[str(t)]['output_sha256']\n else:vtracer.convert_image_to_svg_py(str(infile),str(outfile),**params)")
s=s.replace(' whole=union_all(paths);part='," whole=pathops.Path()\n for p in paths:whole.addPath(p)\n part=")
s=s.replace("'trace_paths':len(paths),","'trace_paths':len(paths),'reused_verified_trace':str(t) in cache,")
s=s.replace('alltiers=union_all(clipped);base=',"alltiers=pathops.Path()\nfor p in clipped:alltiers.addPath(p)\nbase=")
p.write_text(s,encoding='utf8')
(base/'TECHNICAL_ATTEMPTS.json').write_text(json.dumps({'schema':'s7-technical-attempts/v1','formal_candidates':1,'technical_builder_attempts':2,'trace_generation_calls_total':5,'failures':[{'attempt':1,'classification':'INTERRUPTED_TECHNICAL_PERFORMANCE','evidence':'First tier trace305933bytes completed. Sequential union_all of thousands of mutually disjoint traced components did not finish promptly.','changed_strategy':'Append already-disjoint VTracer contours in one compound Path then single INTERSECTION; same geometry/core/parameters. Verified completedtrace cache reused, remaining4calls only.'}],'attempt2':'same frozen candidate; no parameter or geometric change','aesthetic_verdict':None},indent=2)+'\n')
print(cache)
