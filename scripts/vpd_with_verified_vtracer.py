"""Restore the fixed upstream dependency in workspace, then run existing checks.

Does not change ACLs, validator semantics, old package files or business state.
The target remains responsible for its own authorization and state transaction.
"""
import hashlib, importlib.metadata, json, pathlib, runpy, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
WHEEL = ROOT / '.liu-visual-private/dependencies/vtracer_0_6_15_cp312/vtracer-0.6.15-cp312-cp312-win_amd64.whl'
WHEEL_SHA = 'b0f08b66734e41872d4ac343ed6d08870b3235346def3e112e10b3b2443e619e'
RESTORED = ROOT / '.liu-visual-private/dependencies/vtracer_verified_restore_20261006/site-packages'

def prepare():
    if hashlib.sha256(WHEEL.read_bytes()).hexdigest() != WHEEL_SHA:
        raise RuntimeError('Fixed upstream wheel identity changed')
    with zipfile.ZipFile(WHEEL) as z:
        names = z.namelist()
        if any(pathlib.PurePosixPath(n).is_absolute() or '..' in pathlib.PurePosixPath(n).parts for n in names):
            raise RuntimeError('Unsafe wheel member')
        if not RESTORED.exists():
            RESTORED.mkdir(parents=True)
            z.extractall(RESTORED)
        for name in names:
            if name.endswith('/'):
                continue
            if (RESTORED / name).read_bytes() != z.read(name):
                raise RuntimeError('Restored upstream member changed: ' + name)
    sys.path.insert(0, str(RESTORED))
    import vtracer
    if not pathlib.Path(vtracer.__file__).resolve().is_relative_to(RESTORED.resolve()):
        raise RuntimeError('Unexpected imported VTracer location')
    if importlib.metadata.version('vtracer') != '0.6.15':
        raise RuntimeError('Unexpected VTracer version')
    return {'upstream_version':'0.6.15', 'wheel_sha256':WHEEL_SHA,
            'actual_module':vtracer.__file__, 'all_wheel_members_equal':True,
            'upstream_modified':False, 'acl_changes':0}

if __name__ == '__main__':
    proof = prepare()
    print(json.dumps(proof), flush=True)
    if len(sys.argv) > 1:
        target = (ROOT / sys.argv[1]).resolve()
        if not target.is_relative_to(ROOT):
            raise RuntimeError('Target outside project workspace')
        sys.path.insert(0, str(ROOT))
        sys.argv = [str(target), *sys.argv[2:]]
        runpy.run_path(str(target), run_name='__main__')
