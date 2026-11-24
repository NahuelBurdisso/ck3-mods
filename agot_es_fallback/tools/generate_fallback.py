"""Count/generate Spanish fallback entries for keys that only exist in English.

CK3 renders the raw key when a key is missing in the active language, so every
English-only key in the playset shows as e.g. AGOT_NAME_CHARACTER_COMMA on screen.
"""
import json, re, sys
from pathlib import Path

USER = Path("D:/Documents/Paradox Interactive/Crusader Kings III")
GAME = Path("D:/SteamLibrary/steamapps/common/Crusader Kings III/game")
ES_MOD = Path("D:/SteamLibrary/steamapps/workshop/content/1158310/3463729959")
KEY = re.compile(r'^(\s*)([A-Za-z0-9_.\-]+):(\d*)\s+"(.*)$')

def scan(root, lang):
    """key -> raw value text, for every <root>/localization[/replace]/<lang>."""
    out = {}
    for base in (root / "localization", root / "localisation"):
        for sub in (base / lang, base / "replace" / lang):
            if not sub.exists():
                continue
            for f in sub.rglob("*.yml"):
                for line in f.read_text(encoding="utf-8-sig", errors="replace").splitlines():
                    m = KEY.match(line)
                    if m:
                        out[m.group(2)] = m.group(4).rstrip()
    return out

def roots():
    dlc = json.loads((USER / "dlc_load.json").read_text(encoding="utf-8-sig"))
    for rel in dlc["enabled_mods"]:
        p = USER / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8-sig", errors="replace")
        m = re.search(r'^path\s*=\s*"([^"]+)"', t, re.M)
        n = re.search(r'name\s*=\s*"([^"]+)"', t)
        if m and Path(m.group(1)).exists():
            yield (n.group(1) if n else rel), Path(m.group(1))

en, es = {}, {}
en.update(scan(GAME, "english")); es.update(scan(GAME, "spanish"))
sources = list(roots()) + [("AGOT Spanish-Español", ES_MOD)]
per_mod = {}
for name, root in sources:
    e, s = scan(root, "english"), scan(root, "spanish")
    en.update(e); es.update(s)
    per_mod[name] = (e, s)

missing = {k: v for k, v in en.items() if k not in es}
print(f"english keys total : {len(en)}")
print(f"spanish keys total : {len(es)}")
print(f"MISSING in spanish : {len(missing)}   <- these render as raw keys on screen")

blame = []
for name, (e, s) in per_mod.items():
    n = sum(1 for k in e if k in missing)
    if n:
        blame.append((n, name))
for n, name in sorted(blame, reverse=True):
    print(f"   {n:7} {name}")

if "--write" in sys.argv:
    OUT = Path("D:/ck3/mods/agot_es_fallback/localization/spanish")
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.yml"):
        f.unlink()
    def value_of(raw):
        """raw = everything after the opening quote. Cut at the LAST quote on the line."""
        j = raw.rfind('"')
        return raw[:j] if j >= 0 else raw

    items = sorted((k, value_of(v)) for k, v in missing.items())
    bad = [k for k, v in items if '"' in v]
    if bad:
        print("WARN unbalanced quotes in", len(bad), "values:", bad[:5])
    CHUNK = 4000
    for i in range(0, len(items), CHUNK):
        part = items[i:i + CHUNK]
        body = ["l_spanish:"]
        for k, v in part:
            body.append(f' {k}:0 "{v}"')
        txt = "\n".join(body) + "\n"
        (OUT / f"zzz_es_fallback_{i // CHUNK:02d}_l_spanish.yml").write_bytes(
            b"\xef\xbb\xbf" + txt.encode("utf-8"))
    print("wrote", len(items), "keys into", len(range(0, len(items), CHUNK)), "files")
