# AGOT Conflict Merge Patch

Merged copies of files that several enabled mods each *fully replace*. CK3 does not
merge whole files — the last mod in load order wins outright — so without this, every
earlier mod's edits to these files are silently gone.

Must load **after every owning mod**. `agot_dd_fix` owns only
`events/agot_events/agot_scenario_defiance_of_duskendale_events.txt`, so it does not
interact with anything here and keeps its "always last" slot.

## Rebuilding — do not hand-merge

    python tools/_mergepatch.py            # report only, exit 0 == all targets pass
    python tools/_mergepatch.py --write    # regenerate all eight whole-file merges
    python tools/_ishumanfix.py            # the key-level merge -- see "Key-level" below
    python tools/_ishumanfix.py --write
    python tools/ck3.py validate agot_conflict_merge

`tools/_mergepatch.py` reads the live `dlc_load.json`, resolves each target's owners in
load order, and runs a real 3-way merge (`git merge-file`, base = first owner) once per
owning mod. Genuine overlaps auto-resolve to the later-loading mod, i.e. identically to
what the game does today. It then checks, per file: no conflict markers, brace delta equal
to the base's, no duplicated top-level key (`.txt` only), and **every owner's
unique-vs-base lines present in the output**. Nothing is written unless its checks pass.

**This patch is never an owner of its own targets.** It is filtered out of the owners list
by path. Feeding the last build's output back in is harmless only while the merge is
idempotent; the moment a new owning mod appears it duplicates the shared hunks and, because
the patch loads last, its stale copy wins the overlaps and drops the new mod's lines. That
is exactly what happened when A Time for Wolves Fix was added — 21 of its lines vanished.

**A merge pins its inputs' content at build time. Re-run after ANY owning mod updates.**
The 2026-08-12 hand-merges had gone stale exactly this way — four of the five owning mods
updated between 09-08 and 09-14.

## What is merged, and against what

Rebuilt 2026-09-14 from the live 87-mod playset. All eight: 0 conflicts, 0 lines lost.
Indices below are that playset's.

| File | Owners, in load order | Recovered by the merge |
|---|---|---|
| `common/scripted_effects/07_dlc_ep3_scripted_effects.txt` | AGOT [1] → House Founders [14] → More Dragon Eggs [19] → Seasons [25] | HF's 339-line adventurer-title rework (it comments AGOT's `adventurer_name_001..` out behind `# AGOTHF Disabled` and substitutes house-founder naming) **and** MDE's `# MDE Modified` block (returns the head dragonkeeper to court and re-pits living dragons at the new capital on title transfer). Both were dead: Seasons won the file. Seasons' own `#SEASONS MODIFIED` winter-modifier lists are kept |
| `gui/hud.gui` | AGOT [1] → More Dragon Eggs [19] → Battlefield Duel + [80] | MDE's `bottom_left_dragon_portrait = {}` widget — the HUD dragon portrait, lost to Battlefield Duel +'s 116-line reputation-stack rewrite |
| `common/coat_of_arms/template_lists/color_lists.txt` | AGOT [1] → AGOT+ [4] → House Founders [14] | AGOT+'s 38 unique lines (incl. the `valyria_dark/medium/light` named-colour rewrite), lost to House Founders |
| `common/on_action/child_birth_on_actions.txt` | AGOT [1] → House Founders [14] → Seasons [25] | HF's 4 unique lines, lost to Seasons |
| `common/bookmarks/challenge_characters/00_challenge_characters.txt` | AGOT [1] → Additional Models & Special Buildings [8] → Bookmarked [21] → A Time for Wolves Fix [22] | **`--union`, see below.** The 16 shared keys are exactly AGOT's, so all three are independent extensions of the base: AMSB +7, Bookmarked +5 (`egg1`–`egg5`, its "Main Mod Graveyard" Aegons), ATfW +12. 40 top-level entries out, no duplicate keys. ATfW loads last and would otherwise take the whole end-of-file region |
| `gfx/interface/illustrations/scripted_illustrations/ingame.txt` | AGOT [1] → Fire and Blood [3] → *(AGOT+ [4], AMSB [8] — superseded)* → Additional Models / AGOT+ Compatch [9] | F&B's 6 lines (the `fab_storms_end_throneroom.dds` scene). AGOT+ and AMSB are **not merged directly**: the compatch at [9] already is AGOT+ ∪ AMSB for this file (456 + 9 = 465 unique-vs-base exactly), so merging all three triple-counted and produced 38 657 lines from a 20 369-line base |
| `history/titles/agot_d_kingsguard.txt` | AGOT [1] → Bookmarked [21] → A Time for Wolves Fix [22] | Bookmarked's `7998.1.2` holder block, lost to ATfW's Brienne-of-Tarth entry |
| `gui/custom_gui/agot_kingsguard.gui` | AGOT [1] → Fire and Blood [3] | **`RESTORE`, not a merge.** Ships AGOT's current 877-line file verbatim. See below |

## Key-level merges — a collision with no file collision

Built by **`tools/_ishumanfix.py`**, not `_mergepatch.py`, and it is a different failure
mode. Every target above is a file several mods ship at the *same path*. This one is the
opposite: the owners ship **differently named files**, so nothing is overwritten and a
collision scan by filename reports zero — yet CK3 keeps only the **last definition of a
duplicate top-level key**, so the last-loading owner still silently wins and the others'
edits die. Filename collisions are therefore a lower bound on conflicts; duplicate
definition keys have to be diffed separately.

| Key | Defined by | Recovered |
|---|---|---|
| `is_human` | AGOT [1] `00_agot_character_triggers.txt` → Great Councils [5] `zzz_Great_Councils_replaced_triggers.txt` → DireWolves [6] `dw_direwolf_character_triggers.txt` | Both single-line additions. GC's `NOT = { has_character_flag = zzz_great_councils_disable }` and DireWolves' `NOT = { has_trait = direwolf }` are each built on AGOT's 20-line base and neither contains the other, so whichever loads last erases the other's. Losing the DireWolves line makes **direwolves count as human**; losing GC's kills its per-character opt-out. Output 22 lines, 0 conflicts |

Shipped at `common/scripted_triggers/zzz_merge_is_human.txt`. The builder **discovers its
owners** — it scans every enabled mod's `common/scripted_triggers/` for a top-level
`is_human`, so a new mod defining it is picked up by re-running rather than by editing a
list. Same guarantees as `_mergepatch.py`: base is the first owner in load order, real
`git merge-file` 3-way, and it refuses to write unless there are no conflict markers, the
brace delta is 0, every owner's unique-vs-base line is in the output, and the result
defines **exactly one** top-level key. Extracting a block counts braces with comments
stripped, or a commented-out `}` would end it early.

This also means Great Councils' load position no longer matters for `is_human`; it sits at
[5] (before DireWolves) as belt-and-braces, so even with this patch disabled the direwolf
line survives and only GC's opt-out flag is lost.

## `RESTORE` — when a later mod ships a stale snapshot

Fire and Blood [3] ships a 508-line `agot_kingsguard.gui`. AGOT's is 877. F&B's only
line not in AGOT's is `blockoverride "replace_councillor"` — AGOT moved that button into
a `block "replace_councillor"` default inside the councillor template and dropped the 7
redundant per-slot overrides F&B still carries. The file contains **zero** `fab_`/F&B
tokens: it is an accidental leftover, not content.

Merging is the wrong tool here. F&B's diff-vs-base *is* a revert, so a 3-way merge would
delete 187 of AGOT's lines. `RESTORE` ships the base verbatim and asserts the stale owner
adds nothing outside a declared allowlist — if F&B ever puts real content in that file the
check fails and the entry must be removed and merged properly.

## `--union` — when every owner only appends

`00_challenge_characters.txt`'s three non-base owners each append new top-level entries at
the end of the file. That is one overlapping hunk, and `--theirs` gives it entirely to the
latest loader. `--union` keeps every side. It is only safe because of the
duplicate-top-level-key check: if two owners edited the *same* key, union would emit it
twice, CK3 would keep one, and the check fails the build.

## BOM

Write the BOM convention of the file the game loads **today** (the last owner), not the
base's. AGOT ships `color_lists.txt` with no BOM but House Founders, which currently wins
it, ships one — matching the base instead makes `ck3.py validate` warn and CK3 log
`lexer.cpp:306` every load.

## Dropped 2026-08-12 — inputs no longer installed

`gui/interaction_menu_window.gui` (Better Barbershop + More Bloodlines),
`history/titles/agot_e_the_crownlands.txt` and `agot_k_dragonstone.txt` (Nobility of
Westeros). Originals are in the old copy under
`C:/Users/nahue/Documentos/Paradox Interactive/Crusader Kings III/mod/agot_conflict_merge`.

**`gui/window_character.gui` must never come back here.** That collision is now
AGOT CBO Base → [other mod] → [other mod] AGOT Compatibility, and [other mod] AGOT
Compatibility is a purpose-built patch that already resolves it; a trunk shipped here
would clobber it. It is also the file behind the DireWolves↔CBO load crash.

## Brace balance — count real braces only

The brace check strips `#` line comments first (but not a `#` inside a double-quoted
string — CK3 format codes look like `default_format = "#high;italic"`). Without that,
commented-out script makes every file look unbalanced: AGOT's `ingame.txt` reads `+102`
raw and `+0` for real, and AGOT Bookmarked's commented-out `# 7999.4.1 = {` lines were the
classic false hit. With comments stripped every owner and every merge is `+0`, so the
check is now a genuine assertion rather than "matches the base's arbitrary offset".
