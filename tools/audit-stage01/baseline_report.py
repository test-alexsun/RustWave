"""Render measured baseline only. Missing measurement is BLOCKED, never guessed."""
from inventory import DOC, OUT, read, table
from pathlib import Path
import hashlib
import json
import statistics

RAW=DOC/'benchmarks/raw'


def main():
    source=RAW/'baseline.json'
    text='# Go baseline — local Docker Desktop\n\nPinned GoWave `d709bad01dc0ceacb20012a3afdf528eddfd061f`. Corrected LF archive: 1772/1772 Git blobs verified; original CRLF attempt retained in [archive report](../audit/ARCHIVE_INTEGRITY.md).\n\n'
    text+='''## Environment and method

Windows host, Docker Desktop 4.97.0 / Engine 29.9.2, WSL Linux amd64, 4 logical CPUs and 4,046,016,512 bytes VM RAM. This is an empty-instance idle baseline, not a throughput/load/capacity test and not a prediction for the 1-vCPU/<1-GiB VPS. VPS not used. Background services remain enabled with zero users/nodes; no concurrent audit build/test workload during measurements.

Reproduce: build the **unmodified upstream Dockerfile** from blob-verified raw/source-lf with COMMIT_SHA pinned, tag rustwave-audit01:upstream-lf, then `python tools/audit-stage01/benchmark.py`. Script creates only its own internal Docker network, an idle Bun HTTP probe sidecar on the internal network (no published ports), 1-CPU/256-MiB nonroot read-only app containers, 1-CPU/512-MiB PostgreSQL container with disposable tmpfs, and removes them after completion. No production volumes or databases are mounted.

Three independent fresh application/database starts per mode. PostgreSQL database is recreated between trials after stopping the prior app. Startup = host monotonic duration from docker start invocation to first HTTP 200 health, including Docker startup/exec/probe overhead; it is not an instrumented pure server.Run duration. PG startup is measured separately to pg_isready. After 20-s warmup, a nominal 30-s idle window samples cgroup v2 usage_usec; CPU = delta / actual monotonic seconds × 100, where 100% is one core. Backend RSS = /proc/1/status VmRSS; cgroup memory.current includes process/cache/tmpfs. PG cgroup values include all DB workers; PG PID1 RSS alone is not total DB RSS. Sampling itself has small docker exec/process overhead. No confidence interval or loaded-dataset claim from n=3.

SQLite is embedded in the Go process: its allocator/cache work is inside backend RSS/CPU. A separate SQLite daemon memory number would be fictitious; recorded as no separate process, not zero incremental cost. PG backend and DB are measured separately and are never conflated into a single backend value. DB tmpfs and memory cache differ from disk-backed production storage.

'''
    if source.exists():
        b=json.loads(read(source))
        text+=f'UTC start: {b["utc_start"]}. Image ID `{b["image"]}`.\n\n'
        text+='## Measured idle results\n\n'
        rows=[]
        for mode,trials in b['modes'].items():
            for i,t in enumerate(trials,1):
                db=t['database']
                rows.append([mode,i,f'{t["startup_seconds"]:.3f}',f'{t["backend_rss_bytes"]/2**20:.2f}',f'{t["backend_cgroup_bytes"]/2**20:.2f}',f'{t["backend_cpu_percent"]:.3f}',f'{db["cgroup_bytes"]/2**20:.2f}' if mode=='postgres' else 'in-process',f'{db["cpu_percent"]:.3f}' if mode=='postgres' else 'in-process',f'{t["idle_seconds"]:.2f}'])
        text+=table(['DB','Trial','Startup s','Backend RSS MiB','Backend cgroup MiB','Backend CPU %','DB cgroup MiB','DB CPU %','Window s'],rows)
        text+='\nMedians: '+ '; '.join(f'{mode}: startup {statistics.median(t["startup_seconds"] for t in trials):.3f} s, backend RSS {statistics.median(t["backend_rss_bytes"] for t in trials)/2**20:.2f} MiB, backend CPU {statistics.median(t["backend_cpu_percent"] for t in trials):.3f}%' for mode,trials in b['modes'].items())+'.\n'
        text+=f'\nPostgreSQL startup (separate, one observation): {b.get("pg_startup_seconds",0):.3f} s. Image size from docker image inspect Size: **{b["image_bytes"]:,} bytes / {b["image_bytes"]/2**20:.2f} MiB**, local cumulative image size (not registry compressed transfer or shared-disk reclaim size).\n'
        text+='\n## Runtime smoke observations (Go only)\n\n'
        rows=[]
        for mode,trials in b['modes'].items():
            t=trials[0]
            for path,res in t['http_smoke'].items():rows.append([mode,'GET '+path,res['status'],res.get('headers',{}).get('content-type',res.get('headers',{}).get('Content-Type',''))])
            for key in ('head','metrics_unauthorized','metrics_authorized','metrics_health','metrics_wrong_method'):
                res=t[key];rows.append([mode,key,res['status'],res.get('headers',{}).get('content-type',res.get('headers',{}).get('Content-Type',''))])
        text+=table(['DB','Request','Status','Content-Type'],rows)
        text+='\nMetrics disabled smoke: '+json.dumps(b.get('metrics_disabled',{}))+'. Connection failure is the expected wrong-method metrics behavior; it is not a successful JSON status. These small smoke checks do not replace the full static/metrics differential matrices.\n'
        text+='\nComplete measured counters: [baseline-measurements.json](../audit/baseline-measurements.json). Only synthetic empty-instance resource counters are published; HTTP bodies and authentication material are omitted.\n\n'
        public={k:v for k,v in b.items() if k!='modes'}
        public['modes']={m:[{k:v for k,v in t.items() if k not in ('http_smoke','head','metrics_unauthorized','metrics_authorized','metrics_health','metrics_wrong_method')} for t in ts] for m,ts in b['modes'].items()}
        # Keep derived public fixture summaries, not HTTP bodies or auth material.
        (OUT/'baseline-measurements.json').write_text(json.dumps(public,indent=2)+'\n',encoding='utf-8')
    else:
        text+='## Status\n\nBLOCKED / NOT_RUN: corrected-image runtime measurements have not completed. No RSS/CPU/startup values are inferred.\n'
    rows=[]
    for name in ('lf-gowave','gowave-image'):
        p=RAW/name
        if p.exists(): rows.append([name,p.stat().st_size,f'{p.stat().st_size/2**20:.2f}',hashlib.sha256(p.read_bytes()).hexdigest()])
    text+='\n## Binary artifacts\n\n'+table(['Artifact','Bytes','MiB','SHA-256'],rows)
    text+='\nlf-gowave is the standalone CGO_ENABLED=0 Go 1.27.3-bookworm build with -trimpath -ldflags="-s -w". gowave-image is copied from the final unmodified upstream Dockerfile image (adds version/channel/commit link flags, Alpine build stage). They are distinct build artifacts; do not assume byte identity. Commands/exit codes are in [COMMANDS](../audit/COMMANDS.md). Compiler/base-image versions and digest evidence are preserved with the execution ledger.\n'
    (DOC/'benchmarks/GO_BASELINE.md').write_text(text,encoding='utf-8')
    print('baseline report', 'measured' if source.exists() else 'pending')


if __name__=='__main__': main()
