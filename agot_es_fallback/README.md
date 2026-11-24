# AGOT ES Fallback

Source for the CK3 mod `agot_es_fallback`. Must load **last**.

## Why this exists

**CK3 does not fall back to English.** If a localization key is missing in the active language, the
game draws the raw key on screen — verified 2026-08-26 with the game in `l_spanish`, which showed
`AGOT_NAME_CHARACTER_COMMA` in every character profile and `dynn_Blackfyre` for house names.

AGOT ships no `localization/spanish`, and neither do most of its submods. The translation mod
`3463729959` covers 96.5% of AGOT itself, but that still leaves 14,558 keys across the playset
with no Spanish definition at all — The Red Keep 3,651, the AGOT 0.5.1 delta 2,367, Brightboar
1,730, AGOT+ 1,318, and so on. All of them would render as raw keys.

This mod emits an `l_spanish` entry for each of those keys carrying the **English text, verbatim**.
It is not a translation and does not pretend to be one: it only converts an unreadable key into the
readable English string you would have seen before switching language.

By construction it contains **only** keys absent from every Spanish source in the playset, so it
never overrides a real translation, and it produces no duplicate-key errors.

> **This repository ships the generator only.** The generated
> `localization/spanish/zzz_es_fallback_*.yml` files are copies of other mods' English text, so
> they are not published here; run the generator against your own playset to produce them.

## Regenerating

Required whenever a mod is added, removed, or updated — new English-only keys appear as raw keys
again. The generator scans vanilla plus every mod in `dlc_load.json` plus the translation mod,
collects `english` and `spanish` (including each `localization/replace/<lang>`), and writes the
difference.

Value parsing detail that matters: a CK3 loc value ends at the **last** quote on the line, not the
second one — 180 of these values legitimately contain embedded quotes (`The outlaw "king" was...`).
Cutting at the first closing quote truncates them.

Output: `localization/spanish/zzz_es_fallback_NN_l_spanish.yml`, UTF-8 **with BOM**, LF endings,
`l_spanish:` header, 4000 keys per file.

## Verifying

- key count equals the reported missing count, and `sort | uniq -d` on the keys is empty
- re-running the scan after enabling this mod reports `MISSING in spanish : 0`
- `python tools/ck3.py validate agot_es_fallback` is clean
- in game: no raw `SCREAMING_SNAKE_CASE` strings in character profiles, house names, or tooltips

## Commands

- Deploy:   `python tools/ck3.py deploy agot_es_fallback`
- Validate: `python tools/ck3.py validate agot_es_fallback`
- Enable:   `python tools/ck3.py playset add agot_es_fallback`
