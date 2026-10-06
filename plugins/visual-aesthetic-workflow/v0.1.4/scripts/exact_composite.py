#!/usr/bin/env python3
"""Cooperating local finalizer. Preserves decoded original samples, never JPEG re-encodes.
Engineering validation is distinct from actual semantic pixel review and business acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

ROLES = {'top_text', 'main_title_text', 'right_vertical_text', 'footer_short_text', 'minimal_text_cleanup'}
SEMANTICS = ('photo', 'two_people', 'cabin', 'sunset', 'water', 'crop', 'layout')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()

def read_original(path):
    with Image.open(path) as image:
        image.load()
        if image.mode not in ('RGB', 'RGBA'):
            raise ValueError('STOP: original mode needs an explicitly verified lossless sample policy; no implicit color conversion')
        if getattr(image, 'n_frames', 1) != 1:
            raise ValueError('STOP: animated source unsupported')
        return image.copy(), dict(image.info)

def load_contract(plan, reference_path, original):
    c = plan.get('execution_contract', {})
    if plan.get('action') == 'STOP':
        raise ValueError('STOP: planner is blocked')
    expected = {'final_canvas_policy': 'EXACT_REFERENCE_DIMENSIONS', 'finalization_mode': 'MASKED_LOCAL_EDIT_OR_DETERMINISTIC_COMPOSITE', 'whole_canvas_generative_edit_as_final': False, 'outside_edit_regions_policy': 'BIT_IDENTICAL', 'generative_output_role': 'GUIDE_ONLY', 'on_exact_composite_unavailable': 'STOP'}
    if any(c.get(k) != v for k, v in expected.items()):
        raise ValueError('STOP: exact composite contract required')
    if c.get('reference_binding', {}).get('sha256') != digest(reference_path):
        raise ValueError('STOP: original file hash does not match binding')
    if c.get('reference_dimensions') != {'width': original.width, 'height': original.height}:
        raise ValueError('STOP: actual original dimensions do not match binding')
    return c

def load_masks(c, size):
    regions = c.get('editable_regions')
    if not isinstance(regions, list) or not 1 <= len(regions) <= 20:
        raise ValueError('STOP: explicit binary edit masks required')
    width, height = size
    masks, ids = [], set()
    for r in regions:
        rid = r.get('id')
        if not isinstance(rid, str) or not rid or rid in ids or r.get('role') not in ROLES:
            raise ValueError('STOP: invalid or duplicate region')
        ids.add(rid)
        vals = [r.get(k) for k in ('x', 'y', 'width', 'height')]
        if not all(type(v) is int for v in vals):
            raise ValueError('STOP: integer region bounds required')
        x, y, w, h = vals
        if x < 0 or y < 0 or w < 1 or h < 1 or x+w > width or y+h > height or (w == width and h == height):
            raise ValueError('STOP: invalid or whole-canvas edit region')
        if digest(r['mask_source']) != r.get('mask_sha256'):
            raise ValueError('STOP: binary mask file hash mismatch')
        with Image.open(r['mask_source']) as source:
            source.load()
            if source.mode != 'L' or source.size != (w, h):
                raise ValueError('STOP: mask must be a region-sized grayscale L raster, no conversion or resizing')
            mask = source.copy()
        if not set(mask.tobytes()).issubset({0, 255}) or mask.getbbox() is None:
            raise ValueError('STOP: nonempty binary mask required; no feathered outside-mask allowance')
        masks.append((r, mask))
    for r, _ in masks:
        if r['role'] == 'minimal_text_cleanup':
            parent = next((p for p in regions if p['id'] == r.get('parent_region_id') and p['role'] != 'minimal_text_cleanup'), None)
            if not parent or r['x'] < parent['x'] or r['y'] < parent['y'] or r['x']+r['width'] > parent['x']+parent['width'] or r['y']+r['height'] > parent['y']+parent['height']:
                raise ValueError('STOP: cleanup must stay inside its bound text region')
    union = Image.new('L', size, 0)
    for r, mask in masks:
        placed = Image.new('L', size, 0)
        placed.paste(mask, (r['x'], r['y']))
        union = ImageChops.lighter(union, placed)
    if union.getextrema() == (255, 255):
        raise ValueError('STOP: mask union may not replace the whole canvas')
    return masks, union

def validate(reference_path, candidate_path, plan, provenance=None, review=None, candidate_role='DETERMINISTIC_COMPOSITE'):
    original, original_info = read_original(reference_path)
    c = load_contract(plan, reference_path, original)
    _, union = load_masks(c, original.size)
    with Image.open(candidate_path) as image:
        image.load()
        result = image.copy()
        fmt = image.format
        candidate_profile = image.info.get('icc_profile')
        candidate_orientation = image.getexif().get(274, 1)
    reasons = []
    dimensions_equal = result.size == original.size
    ratio_equal = result.width * original.height == original.width * result.height
    if not dimensions_equal:
        reasons.append('EXACT_REFERENCE_DIMENSIONS_REQUIRED')
    if not ratio_equal:
        reasons.append('EXACT_ASPECT_RATIO_REQUIRED')
    if fmt != 'PNG' or result.mode != original.mode:
        reasons.append('LOSSLESS_ORIGINAL_SAMPLE_MODE_REQUIRED')
    if candidate_profile != original_info.get('icc_profile') or candidate_orientation != original.getexif().get(274, 1):
        reasons.append('ORIGINAL_COLOR_PROFILE_AND_ORIENTATION_REQUIRED')
    if candidate_role != 'DETERMINISTIC_COMPOSITE':
        reasons.append('GENERATIVE_GUIDE_CANNOT_BE_FINAL')
    changed = None
    if dimensions_equal and result.mode == original.mode:
        channels = len(original.getbands())
        a, b, allowed = original.tobytes(), result.tobytes(), union.tobytes()
        changed = sum(a[i*channels:(i+1)*channels] != b[i*channels:(i+1)*channels] for i, mask in enumerate(allowed) if mask == 0)
        if changed != 0:
            reasons.append('OUTSIDE_EDIT_MASK_PIXELS_CHANGED')
    else:
        reasons.append('OUTSIDE_MASK_DIFF_NOT_MEASURABLE')
    source_hash, result_hash, mask_hash = digest(reference_path), digest(candidate_path), canonical_hash(c['editable_regions'])
    provenance_valid = bool(provenance and provenance.get('schema') == 'deterministic-original-pixel-composite/v1' and provenance.get('reference_sha256') == source_hash and provenance.get('output_sha256') == result_hash and provenance.get('mask_manifest_sha256') == mask_hash and provenance.get('method') == 'ORIGINAL_PIXEL_COPY_WITH_MASKED_LOCAL_PATCHES')
    if not provenance_valid:
        reasons.append('DETERMINISTIC_COMPOSITE_PROVENANCE_REQUIRED')
    engineering_pass = not reasons
    # This is a scoped review assertion supplied by the carrier; it is not host enforcement or independent acceptance.
    semantic_pass = bool(review and review.get('reference_sha256') == source_hash and review.get('output_sha256') == result_hash and review.get('actual_pixels_viewed') is True and review.get('mask_scope_text_only') is True and review.get('evidence_locator') and all(review.get('checks', {}).get(k) is True for k in SEMANTICS))
    return {'schema': 'exact-composite-postconditions/v1', 'engineering_pass': engineering_pass, 'status': 'ENGINEERING_PASS_NEEDS_ACTUAL_PIXEL_REVIEW' if engineering_pass and not semantic_pass else 'SCOPED_FINAL_ELIGIBLE' if engineering_pass else 'FAIL', 'reference_dimensions': list(original.size), 'output_dimensions': list(result.size), 'exact_aspect_ratio': ratio_equal, 'outside_mask_changed_pixels': changed, 'outside_mask_tolerance': 0, 'lossless_png': fmt == 'PNG', 'reference_sha256': source_hash, 'output_sha256': result_hash, 'mask_manifest_sha256': mask_hash, 'deterministic_provenance_valid': provenance_valid, 'semantic_preservation': {k: 'REVIEW_CONFIRMED' if semantic_pass else 'REQUIRES_ACTUAL_PIXEL_REVIEW' for k in SEMANTICS}, 'review_verification': 'CARRIER_SUPPLIED_NOT_INDEPENDENTLY_VERIFIED_BY_SCRIPT', 'final_eligible': engineering_pass and semantic_pass, 'business_acceptance_changed': False, 'failures': reasons}

def compose(reference_path, output_path, plan, patches):
    if Path(reference_path).resolve() == Path(output_path).resolve():
        raise ValueError('STOP: original reference cannot be overwritten')
    if Path(output_path).suffix.lower() != '.png':
        raise ValueError('STOP: lossless PNG output required')
    original, info = read_original(reference_path)
    c = load_contract(plan, reference_path, original)
    masks, _ = load_masks(c, original.size)
    if not isinstance(patches, list) or not patches:
        raise ValueError('STOP: local patch manifest required')
    ids = [p.get('region_id') for p in patches]
    if len(set(ids)) != len(ids) or set(ids) != {r['id'] for r, _ in masks}:
        raise ValueError('STOP: each editable mask must have exactly one bound local patch')
    input_paths = [r['mask_source'] for r, _ in masks] + [p['path'] for p in patches]
    if any(Path(path).resolve() == Path(output_path).resolve() for path in input_paths):
        raise ValueError('STOP: mask and patch source files cannot be overwritten')
    result = original.copy()
    for r, mask in masks:
        patch = next(p for p in patches if p['region_id'] == r['id'])
        if patch.get('role') != 'LOCAL_TEXT_OR_TEXTURE_CANDIDATE' or digest(patch['path']) != patch.get('sha256'):
            raise ValueError('STOP: hashed local candidate required; whole-canvas generative output is GUIDE_ONLY')
        with Image.open(patch['path']) as material:
            material.load()
            if material.mode != 'RGBA' or material.size != (r['width'], r['height']):
                raise ValueError('STOP: region-sized RGBA patch required; no scaling, recrop or whole-canvas candidate')
            layer = material.copy()
        box = (r['x'], r['y'], r['x']+r['width'], r['y']+r['height'])
        base = result.crop(box)
        local = Image.alpha_composite(base.convert('RGBA'), layer).convert(original.mode)
        # Select inside the binary mask, then paste exact local samples; outside samples stay untouched.
        result.paste(Image.composite(local, base, mask), (r['x'], r['y']))
    options = {k: info[k] for k in ('icc_profile', 'exif') if k in info}
    result.save(output_path, format='PNG', **options)
    provenance = {'schema': 'deterministic-original-pixel-composite/v1', 'method': 'ORIGINAL_PIXEL_COPY_WITH_MASKED_LOCAL_PATCHES', 'reference_sha256': digest(reference_path), 'output_sha256': digest(output_path), 'mask_manifest_sha256': canonical_hash(c['editable_regions']), 'dimensions': list(original.size), 'patches': patches, 'sample_policy': 'DECODE_ONCE_COPY_ORIGINAL_RGB_OR_RGBA_NO_COLOR_TRANSFORM', 'encoding': 'PNG_LOSSLESS', 'generative_output_role': 'GUIDE_ONLY', 'host_enforced': False}
    check = validate(reference_path, output_path, plan, provenance)
    if not check['engineering_pass']:
        raise ValueError('STOP: saved output failed exact postconditions: '+str(check['failures']))
    return provenance, check

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action', choices=['compose', 'validate'])
    ap.add_argument('--reference', required=True)
    ap.add_argument('--plan', required=True)
    ap.add_argument('--report', required=True)
    ap.add_argument('--patches')
    ap.add_argument('--output')
    ap.add_argument('--candidate')
    ap.add_argument('--provenance')
    ap.add_argument('--review')
    ap.add_argument('--candidate-role', default='DETERMINISTIC_COMPOSITE', choices=['DETERMINISTIC_COMPOSITE', 'GUIDE_ONLY'])
    args = ap.parse_args()
    load = lambda path: json.loads(Path(path).read_text()) if path else None
    try:
        plan = load(args.plan)
        if args.action == 'compose':
            if not args.output or not args.patches or not args.provenance:
                raise ValueError('STOP: compose needs output, patches and provenance paths')
            provenance, check = compose(args.reference, args.output, plan, load(args.patches))
            Path(args.provenance).write_text(json.dumps(provenance, ensure_ascii=False, indent=2)+'\n')
        else:
            if not args.candidate:
                raise ValueError('STOP: candidate path required')
            check = validate(args.reference, args.candidate, plan, load(args.provenance), load(args.review), args.candidate_role)
        Path(args.report).write_text(json.dumps(check, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps(check, ensure_ascii=False))
        return 0 if check['engineering_pass'] else 2
    except Exception as error:
        report = {'status': 'STOP', 'final_eligible': False, 'error': str(error)}
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps(report, ensure_ascii=False))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
