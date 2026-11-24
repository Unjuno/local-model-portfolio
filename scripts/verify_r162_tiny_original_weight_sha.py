#!/usr/bin/env python3
"""Read-only SHA256 check for publisher-pinned core model weights. No model code or downloads."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TTS=ROOT/"manifests/drafts/r162-2026-11-25-paradee13-tihon100k-core-weight-pins.candidate.json"
INK=ROOT/"manifests/drafts/r162-2026-11-25-electroglyph-inkling-heretic-v22-adapter-core.candidate.json"
def digest_file(path:Path,block:int=4*1024*1024)->str:
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda:stream.read(block),b""):
            h.update(part)
    return h.hexdigest()
def verify(directory:Path,files:list[dict],repo:str)->bool:
    passed=True
    for f in files:
        p=directory/f["path"]
        try:
            if not p.is_file():raise FileNotFoundError(str(p))
            n=p.stat().st_size
            if n!=f["bytes"]:
                print(f"FAIL {repo}/{f['path']}: bytes {n}!={f['bytes']}")
                passed=False
                continue
            actual=digest_file(p)
            if actual!=f["sha256"]:
                print(f"FAIL {repo}/{f['path']}: SHA256 differs")
                passed=False
            else:print(f"PASS {repo}/{f['path']}: {n} bytes sha256 OK")
        except OSError as ex:
            print(f"FAIL {repo}/{f['path']}: {ex}")
            passed=False
    return passed
def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--paradee-dir",type=Path,help="A directory containing onnx/ and pytorch/ from pinned Paradee v1.3")
    p.add_argument("--tihon-dir",type=Path,help="A directory containing model.safetensors from pinned TiHon")
    p.add_argument("--inkling-lora-dir",type=Path,help="A directory with adapter_model.safetensors from pinned electroglyph Inkling LoRA")
    args=p.parse_args()
    if not any((args.paradee_dir,args.tihon_dir,args.inkling_lora_dir)):
        p.error("Provide at least one model directory. This tool never downloads weights.")
    tts=json.loads(TTS.read_text(encoding="utf8"));ink=json.loads(INK.read_text(encoding="utf8"))
    src={x["id"]:x for x in tts["model_sources"]}
    okay=True
    if args.paradee_dir:okay=verify(args.paradee_dir,src["sahilmahendrakar/Paradee-8M-v1.3"]["weights"],"Paradee") and okay
    if args.tihon_dir:okay=verify(args.tihon_dir,src["ngocthien/tihon-tts"]["weights"],"TiHon") and okay
    if args.inkling_lora_dir:okay=verify(args.inkling_lora_dir,ink["core_weight_files"],"InklingARA") and okay
    print("ONLY CORE FILES CHECKED; nonweight dependencies/license/offline restore NOT certified")
    return 0 if okay else 1
if __name__=="__main__":sys.exit(main())
