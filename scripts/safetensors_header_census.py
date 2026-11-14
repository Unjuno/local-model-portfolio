#!/usr/bin/env python3
"""Anonymous, bounded Safetensors header census. Never reads tensor payload bytes.

Input is the already audited R61 source list, not mutable Hub main. This tool
counts serialized tensor elements, including buffers, not independently proven
unique trainable parameters. It never grants access or changes catalog gates.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import struct
import urllib.parse
import urllib.request

MAX_HEADER = 4 * 1024 * 1024
DTYPE_BYTES = {'F64':8,'F32':4,'F16':2,'BF16':2,'I64':8,'I32':4,
               'I16':2,'I8':1,'U64':8,'U32':4,'U16':2,'U8':1,'BOOL':1,
               'F8_E4M3':1,'F8_E5M2':1,'F8_E4M3FN':1}
EXPECTED = {'transformer':7,'text_encoder':2,'prompt_upsampler':4,
            'text_connector':1,'vae':1}
REPO = 'PrunaAI/P-H3-Image'
REVISION = '7f98acef503cf2bcfba821a78cb1cf1a9928b2df'


def allowed_url(url: str) -> bool:
    p = urllib.parse.urlsplit(url)
    h = (p.hostname or '').lower()
    return (p.scheme == 'https' and not p.username and not p.password
            and p.port in (None,443)
            and (h in ('huggingface.co','hf.co')
                 or h.endswith('.huggingface.co') or h.endswith('.hf.co')))


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed_url(newurl):
            raise ValueError('Redirect outside official HTTPS Hub/CDN hosts')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def validate_file_path(path: str) -> None:
    p = PurePosixPath(path)
    if p.is_absolute() or '..' in p.parts or '\\' in path or str(p) != path:
        raise ValueError('Unsafe or noncanonical repository path')
    if not path.endswith('.safetensors'):
        raise ValueError('Only Safetensors metadata is supported')


def read_exact_range(response, start: int, end: int, total: int) -> bytes:
    """Reject ignored/truncated/expanded HTTP ranges before consuming a body."""
    length = end - start + 1
    try:
        if response.status != 206:
            raise ValueError('Expected HTTP 206; refusing body of non-range response')
        expected = f'bytes {start}-{end}/{total}'
        if response.headers.get('Content-Range') != expected:
            raise ValueError('Content-Range differs from pinned byte interval/size')
        if response.headers.get('Content-Encoding','identity') != 'identity':
            raise ValueError('Encoded range response cannot prove byte interval')
        cl = response.headers.get('Content-Length')
        if cl is not None and int(cl) != length:
            raise ValueError('Content-Length differs from requested interval')
        result = response.read(length)
        if len(result) != length:
            raise ValueError('Truncated header range')
        return result
    finally:
        response.close()


def _unique_object(pairs):
    d = {}
    for key, value in pairs:
        if key in d:
            raise ValueError('Duplicate JSON key')
        d[key] = value
    return d


def inspect_header(raw: bytes, data_bytes: int) -> dict:
    if not raw or len(raw) > MAX_HEADER or type(data_bytes) is not int or data_bytes < 0:
        raise ValueError('Invalid header or payload extent')
    def no_constant(value):
        raise ValueError('Nonfinite JSON number')
    obj = json.loads(raw, object_pairs_hook=_unique_object, parse_constant=no_constant)
    if not isinstance(obj, dict):
        raise ValueError('Header must be a JSON object')
    spans, names, dtypes = [], [], Counter()
    for name, entry in obj.items():
        if name == '__metadata__':
            if not isinstance(entry, dict) or not all(isinstance(v,str) for v in entry.values()):
                raise ValueError('Invalid freeform metadata')
            continue
        if not isinstance(entry, dict):
            raise ValueError('Invalid tensor entry')
        shape, dtype, offsets = entry.get('shape'), entry.get('dtype'), entry.get('data_offsets')
        if dtype not in DTYPE_BYTES:
            raise ValueError('Unknown or packed dtype; cannot infer parameter count')
        if not isinstance(shape,list) or len(shape)>32:
            raise ValueError('Invalid tensor dimensions')
        count = 1
        for size in shape:
            if type(size) is not int or size < 0 or size > 2**63-1:
                raise ValueError('Nonintegral or invalid tensor dimension')
            count *= size
            if count > 2**63-1:
                raise ValueError('Tensor element count out of supported range')
        if (not isinstance(offsets,list) or len(offsets)!=2
                or any(type(n) is not int or n<0 for n in offsets)):
            raise ValueError('Invalid tensor offsets')
        begin, end = offsets
        if end < begin or end > data_bytes or end-begin != count*DTYPE_BYTES[dtype]:
            raise ValueError('Offsets, dtype and shape disagree')
        spans.append((begin,end))
        names.append(name)
        dtypes[dtype] += count
    if not names:
        raise ValueError('No serialized tensors')
    cursor = 0
    for begin, end in sorted(spans):
        if begin != cursor:
            raise ValueError('Payload holes or overlapping tensors')
        cursor = end
    if cursor != data_bytes:
        raise ValueError('Tensor offsets do not cover full advertised payload')
    return {'tensor_count':len(names),'stored_elements':sum(dtypes.values()),
            'dtype_elements':dict(dtypes),'tensor_names':names,
            'header_sha256':hashlib.sha256(raw).hexdigest()}


def aggregate(rows: list[dict]) -> dict:
    seen, components = set(), {}
    for row in rows:
        component, result = row['component'], row['summary']
        for name in result['tensor_names']:
            key = (component,name)
            if key in seen:
                raise ValueError('Duplicate tensor name within component shards')
            seen.add(key)
        c = components.setdefault(component, {'file_count':0,'tensor_count':0,
                                              'stored_elements':0,'dtype_elements':{}})
        c['file_count'] += 1
        c['tensor_count'] += result['tensor_count']
        c['stored_elements'] += result['stored_elements']
        for dtype, n in result['dtype_elements'].items():
            c['dtype_elements'][dtype] = c['dtype_elements'].get(dtype,0)+n
    return {'components':components,'stored_elements_upper_bound':sum(
        c['stored_elements'] for c in components.values()),
        'unique_trainable_parameters_verified':False}


def census(source_path: Path, fetch=None) -> dict:
    source = json.loads(source_path.read_text(encoding='utf-8'))['preservation_original']
    if source['preferred_source_repo'] != REPO or source['immutable_source_revision'] != REVISION:
        raise ValueError('Unexpected source identity or revision')
    files = [f for f in source['source_files'] if f['path'].endswith('.safetensors')]
    if Counter(f['path'].split('/')[0] for f in files) != EXPECTED or len(files)!=15:
        raise ValueError('Full five-component/15-file source coverage not established')
    if len({f['path'] for f in files}) != 15:
        raise ValueError('Duplicate file paths')
    if sum(f['bytes'] for f in files) != 99_797_308_280:
        raise ValueError('Pinned source physical byte inventory changed')
    opener = urllib.request.build_opener(SafeRedirect())
    rows, acquired = [], 0
    for file in files:
        path, size = file['path'], file['bytes']
        validate_file_path(path)
        if not re.fullmatch(r'[0-9a-f]{64}', file.get('lfs_sha256') or ''):
            raise ValueError('Missing publisher payload hash; cannot pin source')
        def get(start, end):
            if fetch is not None:
                return fetch(path,start,end,size)
            query=urllib.parse.urlencode({'metadata_interval':f'{start}-{end}'})
            url=f'https://huggingface.co/{REPO}/resolve/{REVISION}/{urllib.parse.quote(path)}?{query}'
            req=urllib.request.Request(url, headers={
                'Range':f'bytes={start}-{end}','Accept-Encoding':'identity',
                'User-Agent':'portfolio-header-census/1.0'})
            return read_exact_range(opener.open(req,timeout=20),start,end,size)
        prefix = get(0,7)
        header_size = struct.unpack('<Q', prefix)[0]
        if not 2 <= header_size <= MAX_HEADER or 8+header_size >= size:
            raise ValueError('Invalid or oversized header size')
        raw = get(8,7+header_size)
        result = inspect_header(raw,size-8-header_size)
        acquired += 8+header_size
        rows.append({'component':path.split('/')[0],'file':path,'file_bytes':size,
                     'source_payload_sha256':file['lfs_sha256'],
                     'header_metadata_bytes_read':8+header_size,'summary':result})
    totals = aggregate(rows)
    for row in rows:
        del row['summary']['tensor_names']
    return {'schema_version':1,'source_manifest':str(source_path),
            'repo_id':REPO,'revision':REVISION,
            'observed_utc':datetime.now(timezone.utc).isoformat(),
            'status':'HEADER_CENSUS_COMPLETE','file_count':len(rows),
            'application_metadata_bytes_read':acquired,
            'tensor_payload_bytes_requested':0,'full_file_sha256_verified':False,
            'catalog_parameter_gate_changed':False,'download_approved':False,
            'source_header_verification_not_owner_license_approval':True,
            'external_dependency_closure_verified':False,
            'stored_elements_include_buffers_and_possible_ties':True,
            **totals,'files':rows}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--live',action='store_true',help='Read public metadata ranges only')
    args=p.parse_args()
    if not args.live:
        p.error('--live is required; no network reads by default')
    try:
        result=census(args.source)
    except Exception as exc:
        result={'schema_version':1,'status':'BLOCKED','error_type':type(exc).__name__,
                'reason':str(exc)[:350],'catalog_parameter_gate_changed':False,
                'download_approved':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('CENSUS_JSON='+json.dumps(result,ensure_ascii=False,separators=(',',':')))
    if result['status']!='HEADER_CENSUS_COMPLETE':
        raise SystemExit(1)

if __name__=='__main__':
    main()
