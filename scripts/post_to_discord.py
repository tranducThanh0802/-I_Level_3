#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Đẩy các cuộc trao đổi của agent (workspace/ + reviews/) ra Discord, real-time.
- Bàn giao giữa các con + verdict phản biện  -> phòng "agent trao đổi" (webhook_agents)
- Câu hỏi lên người (mục Câu hỏi lên người)   -> phòng "agent ↔ user" (webhook_user)
Chỉ đăng tin MỚI (nhớ trạng thái trong .discord_state.json), không spam lại.

Chạy:
  python3 scripts/post_to_discord.py          # đăng các tin mới
  python3 scripts/post_to_discord.py --test   # gửi 1 tin chào vào 2 phòng để kiểm tra
  python3 scripts/post_to_discord.py --reset   # quên trạng thái (sẽ đăng lại từ đầu)
"""
import os, re, sys, json, time, glob, hashlib, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(ROOT, "scripts", "discord_config.json")
STATE = os.path.join(ROOT, "scripts", ".discord_state.json")
WS = os.path.join(ROOT, "agent-team", "workspace")
RV = os.path.join(ROOT, "agent-team", "reviews")

# mỗi agent: (tên hiển thị, màu thanh embed)
IDENTITIES = {
    "spec-drafter": ("📋 PO-agent", 0x8A5CF6), "po-agent": ("📋 PO-agent", 0x8A5CF6),
    "soat-spec": ("🔍 Soát spec", 0x0EA5A5), "soát spec": ("🔍 Soát spec", 0x0EA5A5),
    "senior-uiux": ("👀 Senior UI/UX", 0xD69200), "senior": ("👀 Senior UI/UX", 0xD69200),
    "ui-ux": ("🎨 UI/UX", 0xEC4899), "uiux": ("🎨 UI/UX", 0xEC4899),
    "fixbug": ("🐛 Fix bug", 0xE05353), "fix bug": ("🐛 Fix bug", 0xE05353), "fix-bug": ("🐛 Fix bug", 0xE05353),
    "reviewer": ("⚖️ Reviewer", 0x6366F1),
    "test": ("🧪 Test", 0x17A05A), "dev": ("📱 Dev", 0x2F6FEB),
    "po(người)": ("🧑 PO (người)", 0xB08900), "po (người)": ("🧑 PO (người)", 0xB08900), "po": ("🧑 PO (người)", 0xB08900),
}
DEFAULT_ID = ("🤖 Agent", 0x7A8794)


def identity(name):
    n = (name or "").strip().lower()
    for key, val in IDENTITIES.items():
        if key in n:
            return val
    return DEFAULT_ID


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def parse_frontmatter(text):
    fm = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
    return fm


def section(text, title_contains):
    """Lấy các dòng thuộc mục '## <title>' cho tới heading tiếp theo."""
    lines = text.splitlines()
    out, grab = [], False
    for ln in lines:
        if ln.startswith("## "):
            grab = title_contains.lower() in ln.lower()
            continue
        if ln.startswith("#"):
            grab = False
            continue
        if grab and ln.strip():
            out.append(ln)
    return out


_RX_EMAIL = re.compile(r"\b([A-Za-z0-9._%+\-])[A-Za-z0-9._%+\-]*@([A-Za-z0-9.\-]+)\b")
_RX_SECRET = re.compile(r"(https://\S*discord\S*/api/webhooks/\S+)|(\bAKIA[0-9A-Z]{16}\b)|(\bAIza[0-9A-Za-z\-_]{35}\b)|(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,})")


def redact(s):
    s = _RX_SECRET.sub("[ẨN-SECRET]", s or "")
    s = _RX_EMAIL.sub(r"\1***@\2", s)  # che phần đầu email trước khi gửi ra ngoài
    return s


def post(url, username, content, color=None):
    content = redact(content)
    payload = {"username": username[:80]}
    if color is not None:
        payload["embeds"] = [{"description": content[:4000], "color": color}]
    else:
        payload["content"] = content[:1900]
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "AgentTeam-Webhook/1.0 (+local)"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status
    # Discord trả 204 khi thành công


def key(*parts):
    return hashlib.md5("||".join(parts).encode("utf-8")).hexdigest()


def main():
    cfg = load_json(CFG, {})
    wa, wu = cfg.get("webhook_agents"), cfg.get("webhook_user")
    if not wa or not wu:
        print("Thiếu webhook trong scripts/discord_config.json"); return

    if "--reset" in sys.argv:
        if os.path.exists(STATE):
            os.remove(STATE)
        print("Đã xoá trạng thái. Lần chạy tới sẽ đăng lại từ đầu.")
        return

    if "--test" in sys.argv:
        post(wa, "🤖 Agent Team", "✅ Kết nối phòng **agent trao đổi** thành công.")
        time.sleep(0.4)
        post(wu, "🤖 Agent Team", "✅ Kết nối phòng **agent ↔ user** thành công. Câu hỏi cho bạn sẽ hiện ở đây.")
        print("Đã gửi 2 tin test. Kiểm tra Discord.")
        return

    seen = set(load_json(STATE, []))
    sent = 0

    # 1) workspace: bàn giao -> phòng agents ; câu hỏi -> phòng user
    for f in sorted(glob.glob(os.path.join(WS, "*.md"))):
        base = os.path.basename(f)
        if base.upper() == "README.MD":
            continue
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        fm = parse_frontmatter(text)
        task = fm.get("task", base)

        for ln in section(text, "Bàn giao"):
            m = re.match(r"^\s*-\s*(?:\[[^\]]*\]\s*)?(.*)$", ln)
            body = (m.group(1) if m else ln).strip()
            if not body:
                continue
            sender = re.split(r"→|->", body)[0]
            sender = re.sub(r"^\s*\d{4}-\d\d-\d\d[\d:\s]*", "", sender).strip()
            k = key("ws-hand", base, body)
            if k in seen:
                continue
            name, color = identity(sender)
            post(wa, name, f"**[{task}]** {body}", color)
            seen.add(k); sent += 1; time.sleep(0.4)

        for ln in section(text, "Câu hỏi"):
            m = re.match(r"^\s*-\s*\[( |x|X)\]\s*(.*)$", ln)
            if not m:
                continue
            done, q = m.group(1).lower() == "x", m.group(2).strip()
            k = key("ws-q", base, q)
            if k in seen or done:
                if done:
                    seen.add(k)
                continue
            blocking = "[CHẶN]" in q.upper() or "CHẶN" in q
            prefix = "🔴 **CÂU HỎI CHO BẠN**" if blocking else "❓ **Cần xác nhận**"
            name, color = identity(fm.get("owner_now", ""))
            if blocking:
                color = 0xE05353
            post(wu, name, f"{prefix} · `{task}`\n{q}", color)
            seen.add(k); sent += 1; time.sleep(0.4)

    # 2) reviews: verdict/status -> phòng agents
    for f in sorted(glob.glob(os.path.join(RV, "*.md"))):
        base = os.path.basename(f)
        if base.upper() == "README.MD":
            continue
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        fm = parse_frontmatter(text)
        task = fm.get("task", base)
        status = fm.get("status", "")
        verdict_by = fm.get("verdict_by", "")
        concl = section(text, "Kết luận")
        summary = concl[0].strip("- ") if concl else status
        k = key("rv", base, status, summary)
        if k in seen:
            continue
        passed = verdict_by == "machine" or "được" in summary.lower()
        icon = "✅" if passed else "🔎"
        color = 0x17A05A if passed else 0x6366F1
        post(wa, "⚖️ Reviewer", f"{icon} **Phản biện [{task}]** — {status}\n{summary}\n`reviews/{base}`", color)
        seen.add(k); sent += 1; time.sleep(0.4)

    # 3) bugs -> phòng agents, màu theo mức nặng (kiểm soát bug)
    SEV = {"crash": 0xB00020, "high": 0xE05353, "medium": 0xD69200, "low": 0x7A8794}
    for f in sorted(glob.glob(os.path.join(ROOT, "agent-team", "memory", "bugs", "*.md"))):
        base = os.path.basename(f)
        if base.upper() == "README.MD":
            continue
        with open(f, encoding="utf-8") as fh:
            fm = parse_frontmatter(fh.read())
        sev, status = fm.get("severity", ""), fm.get("status", "")
        k = key("bug", base, status, fm.get("count", ""))
        if k in seen:
            continue
        bid = fm.get("id", "")
        tag = f"{bid} · " if bid else ""
        post(wa, "🐛 Fix bug",
             f"**{tag}{fm.get('key', base)}** · mức **{sev}** · lặp {fm.get('count','?')} · {status}\n"
             f"`{fm.get('fingerprint','')}`\n`bugs/{base}`",
             SEV.get(sev.lower(), 0x7A8794))
        seen.add(k); sent += 1; time.sleep(0.4)
        # bug agent bó tay -> báo phòng hỏi-người để người nhảy vào
        if status in ("needs-human", "needs-arch", "be-side", "cant-repro"):
            kh = key("bug-human", base, status)
            if kh not in seen:
                post(wu, "🐛 Fix bug",
                     f"🙋 **BUG CẦN NGƯỜI** · {tag}`{fm.get('key', base)}` (mức {sev})\n"
                     f"{fm.get('stuck_reason','(xem file)')}\n"
                     f"Nhận: sửa `bugs/{base}` → assignee=tên bạn, status=in-progress.",
                     0xE05353)
                seen.add(kh); sent += 1; time.sleep(0.4)

    # 4) specs -> phòng agents, màu theo trạng thái (kiểm soát spec)
    ST = {"draft": 0x7A8794, "reviewing": 0xD69200, "approved": 0x17A05A,
          "building": 0x2F6FEB, "done": 0x6366F1}
    for f in sorted(glob.glob(os.path.join(ROOT, "agent-team", "specs", "*.md"))):
        base = os.path.basename(f)
        if base.upper() == "README.MD":
            continue
        with open(f, encoding="utf-8") as fh:
            fm = parse_frontmatter(fh.read())
        status = fm.get("status", "")
        k = key("spec", base, status, fm.get("version", ""))
        if k in seen:
            continue
        emoji = "✅" if status == "approved" else "📝"
        post(wa, "📋 PO-agent",
             f"{emoji} **Spec [{fm.get('feature', base)}]** → **{status}** (v{fm.get('version','?')})\n`specs/{base}`",
             ST.get(status.lower(), 0x7A8794))
        seen.add(k); sent += 1; time.sleep(0.4)

    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(sorted(seen), fh)
    print(f"Đã đăng {sent} tin mới ra Discord." if sent else "Không có tin mới.")


if __name__ == "__main__":
    main()
