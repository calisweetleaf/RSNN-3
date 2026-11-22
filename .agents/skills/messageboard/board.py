#!/usr/bin/env python3
"""Somnus swarm message board: append-only JSONL, flock-guarded, shared by every lane.

  board.py post  --from LANE --kind {claim,api,blocker,done,note,request} --topic T --body TEXT
  board.py read  [--since N] [--topic T] [--kind K]
  board.py claims            # who owns which paths right now
"""
import argparse, fcntl, json, os, sys, time
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "board")
LOG = os.path.abspath(os.path.join(ROOT, "board.jsonl"))

def _append(rec):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG + ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        n = sum(1 for _ in open(LOG)) if os.path.exists(LOG) else 0
        rec = {"seq": n, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **rec}
        with open(LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
        fcntl.flock(lk, fcntl.LOCK_UN)
    return rec

def _all():
    if not os.path.exists(LOG):
        return []
    return [json.loads(l) for l in open(LOG) if l.strip()]

def main():
    p = argparse.ArgumentParser(); s = p.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("post"); a.add_argument("--from", dest="frm", required=True)
    a.add_argument("--kind", required=True, choices=["claim", "release", "api", "blocker", "done", "note", "request"])
    a.add_argument("--topic", required=True); a.add_argument("--body", required=True)
    r = s.add_parser("read"); r.add_argument("--since", type=int, default=0)
    r.add_argument("--topic"); r.add_argument("--kind")
    s.add_parser("claims")
    o = p.parse_args()
    if o.cmd == "post":
        print(json.dumps(_append({"from": o.frm, "kind": o.kind, "topic": o.topic, "body": o.body})))
    elif o.cmd == "read":
        for m in _all():
            if m["seq"] >= o.since and (not o.topic or m["topic"] == o.topic) and (not o.kind or m["kind"] == o.kind):
                print(f'[{m["seq"]}] {m["ts"]} {m["from"]} {m["kind"]} {m["topic"]}: {m["body"]}')
    else:
        own = {}
        for m in _all():
            if m["kind"] == "claim": own[m["topic"]] = m["from"]
            elif m["kind"] == "release": own.pop(m["topic"], None)
        for k, v in own.items(): print(f"{k}\t{v}")
if __name__ == "__main__":
    sys.exit(main())
