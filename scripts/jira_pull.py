#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jira_pull — KÉO thông tin "dùng agent" từ Jira (board AIP555 / fixVersion) để làm BẰNG CHỨNG A3/A6.
Chỉ ĐỌC (read-only). Chỉ thư viện chuẩn (urllib) — KHÔNG thêm thư viện (tránh nhóm cấm-tự-quyết).

CẦN (bạn tự cấp, 1 lần):
  cp scripts/.env.jira.example scripts/.env.jira   rồi điền JIRA_TOKEN.
  Token = Personal Access Token: jira.apero.vn -> avatar -> Profile -> Personal Access Tokens -> Create token.
  scripts/.env.jira đã gitignore — KHÔNG commit token (A8).

Chạy:
  python3 scripts/jira_pull.py                       # kéo version mặc định trong .env (4.3.4)
  python3 scripts/jira_pull.py --version 4.3.4       # chỉ định version
  python3 scripts/jira_pull.py --jql 'project=AIP555 AND fixVersion="4.3.4"'

Kết quả: tóm tắt in ra màn hình + ghi log từng ticket vào agent-team/intake/jira-<version>.jsonl
(dùng làm dẫn chứng: "chỉ 1 dòng, hỏi chạy việc gì").
"""
import os, sys, json, base64, statistics
import urllib.request, urllib.error, urllib.parse
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = os.path.join(ROOT, "scripts", ".env.jira")
OUTDIR = os.path.join(ROOT, "agent-team", "intake")

_KEYS = ("JIRA_BASE_URL", "JIRA_AUTH", "JIRA_TOKEN", "JIRA_EMAIL", "JIRA_PROJECT",
         "JIRA_BOARD", "JIRA_FIX_VERSION", "JIRA_SPRINT", "JIRA_AGENT_LABEL",
         "JIRA_AGENT_ASSIGNEE", "JIRA_JQL")


def load_env(path):
    cfg = {}
    try:
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    for k in _KEYS:                       # biến môi trường (nếu có) đè lên file
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    return cfg


def auth_header(cfg):
    tok = (cfg.get("JIRA_TOKEN") or "").strip()
    if not tok:
        return None
    if (cfg.get("JIRA_AUTH") or "bearer").lower() == "basic":
        raw = f"{(cfg.get('JIRA_EMAIL') or '').strip()}:{tok}".encode()
        return "Basic " + base64.b64encode(raw).decode()
    return "Bearer " + tok


def api(cfg, path):
    url = cfg["JIRA_BASE_URL"].rstrip("/") + path
    req = urllib.request.Request(url, headers={
        "Authorization": auth_header(cfg),
        "Accept": "application/json",
        "User-Agent": "AgentTeam-JiraPull/1.0",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        try:
            return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f%z")
        except Exception:
            return None


def search(cfg, jql):
    issues, start = [], 0
    while True:
        q = urllib.parse.urlencode({
            "jql": jql, "startAt": start, "maxResults": 100,
            "fields": "summary,status,assignee,reporter,created,resolutiondate,labels,issuetype,priority,resolution",
        })
        data = api(cfg, "/rest/api/2/search?" + q)
        batch = data.get("issues", [])
        issues += batch
        start += len(batch)
        if not batch or start >= data.get("total", 0):
            break
    return issues


def main():
    args = sys.argv[1:]
    cfg = load_env(ENV)
    if "--version" in args:
        cfg["JIRA_FIX_VERSION"] = args[args.index("--version") + 1]
    if "--sprint" in args:
        cfg["JIRA_SPRINT"] = args[args.index("--sprint") + 1]
    if "--jql" in args:
        cfg["JIRA_JQL"] = args[args.index("--jql") + 1]
    cfg.setdefault("JIRA_BASE_URL", "https://jira.apero.vn")
    cfg.setdefault("JIRA_PROJECT", "AIP555")
    cfg.setdefault("JIRA_FIX_VERSION", "4.3.4")

    if not cfg.get("JIRA_TOKEN"):
        print("⚠️ Chưa có token. Chạy: cp scripts/.env.jira.example scripts/.env.jira  rồi điền JIRA_TOKEN.")
        print("   (jira.apero.vn -> avatar -> Profile -> Personal Access Tokens -> Create token)")
        return 1

    sprint = (cfg.get("JIRA_SPRINT") or "").strip()
    if cfg.get("JIRA_JQL"):
        jql = cfg["JIRA_JQL"]
    elif sprint:                          # ưu tiên sprint (AIP555 dùng sprint, không dùng fixVersion)
        clause = f"sprint = {sprint}" if sprint.isdigit() else f'sprint = "{sprint}"'
        jql = clause + " ORDER BY resolutiondate ASC"
    else:
        jql = f'project = {cfg["JIRA_PROJECT"]} AND fixVersion = "{cfg["JIRA_FIX_VERSION"]}" ORDER BY resolutiondate ASC'
    print(f"▶ JQL: {jql}")

    try:
        issues = search(cfg, jql)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")[:300]
        except Exception:
            pass
        if e.code in (401, 403):
            print(f"⛔ Auth {e.code}: token sai/hết hạn/không đủ quyền. Kiểm JIRA_TOKEN & JIRA_AUTH. {body}")
        elif e.code == 400:
            print(f"⛔ JQL/version sai (400). Kiểm JIRA_FIX_VERSION / JIRA_PROJECT. {body}")
        else:
            print(f"⛔ Jira lỗi {e.code}. {body}")
        return 1
    except (urllib.error.URLError, OSError) as e:
        print(f"⛔ Không nối được {cfg['JIRA_BASE_URL']} ({e}). Cần mạng nội bộ / VPN Apero?")
        return 1

    os.makedirs(OUTDIR, exist_ok=True)
    ver = cfg["JIRA_FIX_VERSION"]
    log_path = os.path.join(OUTDIR, f"jira-{ver}.jsonl")
    by_status, by_assignee, cycles = {}, {}, []
    resolved = agent_total = agent_resolved = 0
    agent_label = (cfg.get("JIRA_AGENT_LABEL") or "").lower()
    agent_assignee = (cfg.get("JIRA_AGENT_ASSIGNEE") or "").lower()

    with open(log_path, "w", encoding="utf-8") as f:
        for it in issues:
            fld = it.get("fields", {})
            st = (fld.get("status") or {}).get("name", "?")
            cat = ((fld.get("status") or {}).get("statusCategory") or {}).get("key", "")
            asg = (fld.get("assignee") or {}).get("displayName") or "(chưa giao)"
            labels = [l.lower() for l in (fld.get("labels") or [])]
            created, resd = parse_dt(fld.get("created")), parse_dt(fld.get("resolutiondate"))
            by_status[st] = by_status.get(st, 0) + 1
            by_assignee[asg] = by_assignee.get(asg, 0) + 1
            if resd:
                resolved += 1
                if created:
                    cycles.append((resd - created).total_seconds() / 3600.0)
            is_agent = ((agent_label and agent_label in labels) or
                        (agent_assignee and agent_assignee in asg.lower()))
            if is_agent:
                agent_total += 1
                if resd:
                    agent_resolved += 1
            f.write(json.dumps({
                "key": it.get("key"), "status": st, "category": cat, "assignee": asg,
                "labels": fld.get("labels"), "created": fld.get("created"),
                "resolved": fld.get("resolutiondate"),
                "type": (fld.get("issuetype") or {}).get("name"), "is_agent": is_agent,
            }, ensure_ascii=False) + "\n")

    n = len(issues)
    print(f"\n📊 Version {ver} · {n} ticket   (log: {os.path.relpath(log_path, ROOT)})")
    print(f"   Đã resolve: {resolved}/{n}" + (f" ({resolved * 100 // n}%)" if n else ""))
    print("   Theo trạng thái:")
    for s, c in sorted(by_status.items(), key=lambda x: -x[1]):
        print(f"     - {s}: {c}")
    print("   Theo người nhận (top 12):")
    for a, c in sorted(by_assignee.items(), key=lambda x: -x[1])[:12]:
        print(f"     - {a}: {c}")
    if cycles:
        print(f"   Cycle time (tạo→resolve): trung vị {statistics.median(cycles):.1f}h · TB {statistics.mean(cycles):.1f}h")
    if agent_label or agent_assignee:
        print(f"   🤖 Agent ({agent_label or agent_assignee}): {agent_total} ticket, resolve {agent_resolved}" +
              (f" ({agent_resolved * 100 // agent_total}%)" if agent_total else ""))
    else:
        print("   (Đặt JIRA_AGENT_LABEL hoặc JIRA_AGENT_ASSIGNEE trong .env để tách riêng phần agent làm.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
