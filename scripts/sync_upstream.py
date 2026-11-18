#!/usr/bin/env python3
"""tampermonkey 技能上游同步脚本。

用法:
    python scripts/sync_upstream.py --check       # 只报漂移 + 跑锚点，不写盘
    python scripts/sync_upstream.py               # 检测并同步有更新的来源，随后跑锚点
    python scripts/sync_upstream.py --anchors     # 只跑锚点校验（离线，用 vendor/ 现况）
    python scripts/sync_upstream.py --force <id>  # 强制重拉指定来源（可多个）

配置只读 manifest.json。三类 source（type 字段）:
  mirror     local_dir 是上游子树的整目录镜像。取 ref 最新 commit，与 pinned_sha 不同
             则下载 tarball、解出 subpath、整体替换 local_dir（文本保持上游字节，不做
             换行归一）。自研的 references/guide-index.md 在 local_dir 之外，不被覆盖。
  reference  只落 vendor_files 列出的仓库根相对文件到 vendor/<id>/，作锚点与 diff 对照，
             不进分发面。逐文件经 raw / API / 镜像 三通道取，缺一即判失败。
  npm        取 dist-tags.latest 版本，registry tarball 里抽 vendor_files 落 vendor/<id>/。

anchors: 每条 = 自研正文的断言 → 上游某文件里必须逐字命中的 needle 集合。
         同步后与 --anchors 都会逐条校验；未命中报 ANCHOR-BROKEN、退出码 1，
         提示据 claims 人工改写正文。漂移检测与锚点校验相互独立。

网络: 直连 api.github.com / raw.githubusercontent.com / codeload / registry.npmjs.org
      失败时自动经镜像前缀（默认 https://gh-proxy.com，环境变量 TMSKILL_MIRROR 覆盖，
      置空关闭）。GITHUB_TOKEN/GH_TOKEN 若存在则附带以提升限额。

约束: 只写 vendor/、local_dir（镜像）、manifest.json（pinned_*/last_synced）、SYNCLOG.md。
      自研文件（SKILL.md、README.md、NOTICE.md、references/guide-index.md、references 其余、
      templates、examples、scripts）一律不碰。
"""
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import date
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

SKILL_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = SKILL_ROOT / "manifest.json"
SYNCLOG = SKILL_ROOT / "SYNCLOG.md"
VENDOR = SKILL_ROOT / "vendor"
TIMEOUT = 40
MIRROR_BASE = os.environ.get("TMSKILL_MIRROR", "https://gh-proxy.com").rstrip("/")


def _out(msg: str = "", err: bool = False) -> None:
    stream = sys.stderr if err else sys.stdout
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    print(msg, file=stream)


def _headers(json_accept: bool = True) -> dict:
    h = {"User-Agent": "tampermonkey-skill-sync"}
    if json_accept:
        h["Accept"] = "application/vnd.github+json"
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def api_json(path: str):
    if requests is None:
        return None
    url = f"https://api.github.com/{path}"
    cands = [url] + ([f"{MIRROR_BASE}/{url}"] if MIRROR_BASE else [])
    for u in cands:
        try:
            r = requests.get(u, headers=_headers(), timeout=TIMEOUT,
                             proxies={"http": None, "https": None})
            if r.status_code == 200:
                return r.json()
        except requests.RequestException:
            continue
    return None


def head_sha(repo: str, ref: str):
    d = api_json(f"repos/{repo}/commits/{ref}")
    if isinstance(d, dict) and d.get("sha"):
        return d["sha"]
    for remote in ([f"https://github.com/{repo}.git"]
                   + ([f"{MIRROR_BASE}/https://github.com/{repo}.git"] if MIRROR_BASE else [])):
        try:
            r = subprocess.run(["git", "ls-remote", remote, ref],
                               capture_output=True, timeout=60,
                               encoding="utf-8", errors="replace")
            ln = (r.stdout or "").strip().splitlines()
            if ln:
                return ln[0].split()[0]
        except (subprocess.SubprocessError, OSError):
            continue
    return None


def _fetch_repo_file(repo: str, ref: str, rel: str):
    """取仓库根相对文件 rel 的原始字节：contents API → raw → 镜像 raw。返回 bytes 或 None。"""
    d = api_json(f"repos/{repo}/contents/{rel}?ref={ref}")
    if isinstance(d, dict) and d.get("encoding") == "base64" and d.get("content"):
        try:
            return base64.b64decode(d["content"])
        except Exception:
            pass
    if requests is None:
        return None
    raw = f"https://raw.githubusercontent.com/{repo}/{ref}/{rel}"
    for u in ([raw] + ([f"{MIRROR_BASE}/{raw}"] if MIRROR_BASE else [])):
        try:
            r = requests.get(u, headers=_headers(json_accept=False),
                             timeout=TIMEOUT, proxies={"http": None, "https": None})
            if r.status_code == 200:
                return r.content
        except requests.RequestException:
            continue
    return None


def npm_latest(pkg: str):
    if requests is None:
        return None, None
    for u in ([f"https://registry.npmjs.org/{pkg}"]
              + ([f"{MIRROR_BASE}/https://registry.npmjs.org/{pkg}"] if MIRROR_BASE else [])):
        try:
            d = requests.get(u, timeout=TIMEOUT, proxies={"http": None, "https": None}).json()
            v = d["dist-tags"]["latest"]
            return v, d["time"][v][:10]
        except Exception:
            continue
    return None, None


def download_npm_files(pkg: str, version: str, wanted: list[str]):
    """下载 npm tarball，抽出 wanted 文件（package/ 前缀下的仓库根相对路径）。"""
    url = f"https://registry.npmjs.org/{pkg}/-/{pkg.split('/')[-1]}-{version}.tgz"
    if requests is None:
        return {}
    data = None
    for u in ([url] + ([f"{MIRROR_BASE}/{url}"] if MIRROR_BASE else [])):
        try:
            r = requests.get(u, timeout=300, stream=True,
                             proxies={"http": None, "https": None})
            if r.status_code == 200:
                data = r.content
                break
        except requests.RequestException:
            continue
    if not data:
        return {}
    import io
    got = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            rel = "/".join(m.name.split("/")[1:])
            if rel in wanted:
                got[rel] = tf.extractfile(m).read()
    return got


# ---------------------------------------------------------------- mirror 下载

def mirror_tarball_replace(repo: str, ref: str, subpath: str, dest: Path):
    base = f"https://github.com/{repo}/archive/refs/heads/{ref}.tar.gz"
    if requests is None:
        return None
    for url in ([base] + ([f"{MIRROR_BASE}/{base}"] if MIRROR_BASE else [])):
        try:
            r = requests.get(url, timeout=600, stream=True,
                             proxies={"http": None, "https": None})
            r.raise_for_status()
            import io
            buf = io.BytesIO(r.content)
            with tempfile.TemporaryDirectory() as tmp:
                ex = Path(tmp) / "x"
                ex.mkdir()
                with tarfile.open(fileobj=buf, mode="r:gz") as tf:
                    tf.extractall(ex, filter="data")
                top = next(ex.iterdir())
                src = top / subpath if subpath else top
                if not src.is_dir():
                    continue
                n = sum(1 for p in src.rglob("*") if p.is_file())
                if n == 0:
                    continue
                if dest.exists():
                    bak = dest.with_name(dest.name + ".old")
                    shutil.rmtree(bak, ignore_errors=True)
                    dest.rename(bak)
                    try:
                        shutil.copytree(src, dest)
                    except OSError:
                        bak.rename(dest)
                        raise
                    shutil.rmtree(bak, ignore_errors=True)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(src, dest)
                return n
        except (requests.RequestException, tarfile.TarError, OSError):
            continue
    return None


# ---------------------------------------------------------------- source 同步

def sync_source(src: dict, check_only: bool, force: bool):
    sid, stype = src["id"], src.get("type", "mirror")
    if stype == "npm":
        ver, when = npm_latest(src["package"])
        if ver is None:
            return {"id": sid, "state": "failed", "error": "registry 不可达"}
        if ver == src.get("pinned_version") and not force:
            return {"id": sid, "state": "unchanged", "version": ver}
        if check_only:
            return {"id": sid, "state": "updated", "version": ver,
                    "from": src.get("pinned_version"), "action": "npm 有新版本"}
        got = download_npm_files(src["package"], ver, src.get("vendor_files", []))
        if not got:
            return {"id": sid, "state": "failed", "error": "npm 包内未命中 vendor_files"}
        d = VENDOR / sid
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        for rel, data in got.items():
            out = d / rel.replace("/", os.sep)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        src["pinned_version"] = ver
        src["pinned_date"] = when
        src["last_synced"] = date.today().isoformat()
        return {"id": sid, "state": "updated", "version": ver,
                "files": len(got), "method": "npm"}

    repo, ref = src["repo"], src["ref"]
    sha = head_sha(repo, ref)
    if sha is None:
        return {"id": sid, "state": "failed", "error": "远端 commit 不可达"}
    if sha == src.get("pinned_sha") and not force:
        return {"id": sid, "state": "unchanged", "head": sha}

    if stype == "mirror":
        if check_only:
            return {"id": sid, "state": "updated", "head": sha,
                    "from": src.get("pinned_sha", "")[:12], "action": "可重建镜像"}
        dest = SKILL_ROOT / src["local_dir"]
        n = mirror_tarball_replace(repo, ref, src.get("subpath", ""), dest)
        if not n:
            return {"id": sid, "state": "failed", "error": "tarball 下载/替换失败"}
        src["pinned_sha"] = sha
        src["last_synced"] = date.today().isoformat()
        return {"id": sid, "state": "updated", "head": sha, "files": n,
                "method": "tarball-mirror"}

    # reference: 按 vendor_files 精确取文件（条目可为文件路径或目录前缀）
    if check_only:
        return {"id": sid, "state": "updated", "head": sha,
                "from": src.get("pinned_sha", "")[:12], "action": "可刷新 vendor 快照"}
    dest = VENDOR / sid
    want = src.get("vendor_files", [])
    if not want:
        return {"id": sid, "state": "failed", "head": sha,
                "error": "reference 源缺 vendor_files"}
    # 目录前缀条目展开：取仓库树枚举该前缀下的全部文件（如官方技能、市场版助手）
    files = list(want)
    for entry in want:
        if entry.endswith("/"):
            expanded = _tree_files_under(repo, sha, entry)
            if not expanded:
                return {"id": sid, "state": "failed", "head": sha,
                        "error": f"目录前缀 {entry} 在上游无文件"}
            files = [f for f in files if f != entry] + expanded
    written, missing = 0, []
    for rel in files:
        data = _fetch_repo_file(repo, sha, rel)
        if data is None:
            missing.append(rel)
            continue
        out = dest / rel.replace("/", os.sep)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        written += 1
    if missing:
        return {"id": sid, "state": "failed", "head": sha,
                "error": f"vendor_files 取失败: {missing[:6]}"}
    if written == 0:
        return {"id": sid, "state": "failed", "head": sha,
                "error": "vendor_files 零命中，放弃写回"}
    src["pinned_sha"] = sha
    src["last_synced"] = date.today().isoformat()
    return {"id": sid, "state": "updated", "head": sha,
            "files": written, "method": "raw-per-file"}


def _tree_files_under(repo: str, sha: str, prefix: str) -> list[str]:
    """递归树里枚举 prefix 下的文件路径。"""
    d = api_json(f"repos/{repo}/git/trees/{sha}?recursive=1")
    if not isinstance(d, dict):
        return []
    return [e["path"] for e in d.get("tree", [])
            if e.get("type") == "blob" and e["path"].startswith(prefix)]


# ---------------------------------------------------------------- 锚点校验

def anchor_path(a: dict, src: dict) -> Path:
    f = a["file"].replace("/", os.sep)
    if src.get("type") == "mirror":
        return SKILL_ROOT / src["local_dir"] / f
    return VENDOR / src["id"] / f


def check_anchors(cfg: dict) -> list[dict]:
    smap = {s["id"]: s for s in cfg["sources"]}
    res = []
    for a in cfg.get("anchors", []):
        src = smap.get(a["source_id"])
        if src is None:
            res.append({"anchor": a["id"], "status": "no-source", "missing": []})
            continue
        p = anchor_path(a, src)
        if not p.exists():
            res.append({"anchor": a["id"], "status": "file-missing",
                        "file": str(p.relative_to(SKILL_ROOT)).replace(os.sep, "/"),
                        "missing": ["<whole file>"]})
            continue
        text = p.read_bytes().decode("utf-8", errors="replace")
        miss = [n for n in a["needles"] if n not in text]
        res.append({"anchor": a["id"], "status": "ok" if not miss else "needle-missing",
                    "file": str(p.relative_to(SKILL_ROOT)).replace(os.sep, "/"),
                    "missing": miss, "claims": a.get("claims", [])})
    return res


# ---------------------------------------------------------------- 主流程

def main() -> int:
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        _out(__doc__)
        return 0
    check_only = "--check" in args
    anchors_only = "--anchors" in args
    force_ids = []
    if "--force" in args:
        i = args.index("--force")
        force_ids = [x for x in args[i + 1:] if not x.startswith("--")]

    try:
        cfg = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as e:
        _out(f"manifest.json 读取失败: {e}", err=True)
        return 2

    if anchors_only:
        res = check_anchors(cfg)
        return _report_anchors(res)

    if requests is None:
        _out("需要 requests 才能联网；离线仅 --anchors 可用",
             err=True)
        return 2

    results = []
    for src in cfg["sources"]:
        r = sync_source(src, check_only=check_only, force=src["id"] in force_ids)
        results.append(r)
        brief = "; ".join(f"{k}={v}" for k, v in r.items() if k not in ("id", "state"))
        _out(f"[{r['state']:>9}] {r['id']:<32} {brief}")

    if not check_only:
        MANIFEST.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8-sig")
        _append_synclog(results)

    res = check_anchors(cfg)
    rc = _report_anchors(res)
    stats = {}
    for r in results:
        stats[r["state"]] = stats.get(r["state"], 0) + 1
    _out("同步汇总: " + "; ".join(f"{k}={v}" for k, v in sorted(stats.items())))
    return max(rc, 1 if any(r["state"] == "failed" for r in results) else 0)


def _report_anchors(res: list) -> int:
    ok = sum(1 for r in res if r["status"] == "ok")
    bad = [r for r in res if r["status"] != "ok"]
    _out(f"\n锚点校验: {len(res)} 条，通过 {ok}，未通过 {len(bad)}")
    for r in bad:
        _out(f"  !! {r['anchor']} [{r['status']}] @ {r.get('file','?')} "
             f"缺 needle: {r.get('missing')}"
             + (f" | 需人工改写: {r.get('claims')}" if r.get("claims") else ""))
    if bad:
        _out("  → 上游改名/改文，本技能正文据 claims 需同步修订。")
        return 1
    return 0


def _append_synclog(results: list) -> None:
    upd = [r for r in results if r["state"] == "updated"]
    if not upd:
        return
    if not SYNCLOG.exists() or SYNCLOG.stat().st_size == 0:
        SYNCLOG.write_text(
            "# 上游同步日志\n\n"
            "| 日期 | 来源 | 动作 | 新 commit/版本 | 规模 |\n|---|---|---|---|---|\n",
            encoding="utf-8")
    with open(SYNCLOG, "a", encoding="utf-8") as f:
        for r in upd:
            ref = r.get("head") or r.get("version") or ""
            scale = f"{r['files']} 文件" if "files" in r else r.get("action", "")
            f.write(f"| {date.today().isoformat()} | `{r['id']}` | "
                    f"{r.get('method', r.get('action',''))} | `{ref[:12]}` | {scale} |\n")


if __name__ == "__main__":
    sys.exit(main())
