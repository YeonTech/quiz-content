#!/usr/bin/env python3
"""index.json + 모든 세트 파일 검증. 사용: python3 validate.py"""
import json, sys, os

errors, ids = [], set()

try:
    idx = json.load(open("index.json"))
except Exception as e:
    print("❌ index.json 파싱 실패:", e); sys.exit(1)

if not idx.get("version"):
    errors.append("index.json: version 없음")

for entry in idx.get("sets", []):
    f = entry.get("file")
    if not f or not os.path.exists(f):
        errors.append(f"세트 파일 없음: {f}"); continue
    try:
        s = json.load(open(f))
    except Exception as e:
        errors.append(f"{f}: JSON 파싱 실패 {e}"); continue
    for i, q in enumerate(s.get("questions", [])):
        qid = q.get("id", f"{f}#{i}")
        if qid in ids: errors.append(f"{qid}: id 중복")
        ids.add(qid)
        if len(q.get("choices", [])) != 4: errors.append(f"{qid}: choices가 4개 아님")
        if len(q.get("choiceExplanations", [])) != 4: errors.append(f"{qid}: choiceExplanations가 4개 아님")
        if not isinstance(q.get("answer"), int) or not (0 <= q.get("answer", -1) <= 3):
            errors.append(f"{qid}: answer는 0~3 정수여야 함")
        if not q.get("topic"): errors.append(f"{qid}: topic 비어있음")
        for k in ("prompt", "explanation"):
            if not q.get(k): errors.append(f"{qid}: {k} 비어있음")

if errors:
    print("❌ 검증 실패:")
    for e in errors: print("  -", e)
    sys.exit(1)
print(f"✅ 검증 통과 — 총 문제 {len(ids)}개")
