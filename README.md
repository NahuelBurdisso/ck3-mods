# AGOT Conflict Merge Patch

Hand-merged copies of files that two or three enabled mods each *fully replace*.
CK3 does not merge whole files — the last mod in load order wins outright — so
without this, the earlier mods' changes to these four files are silently gone.

Must load **LAST**. Not currently enabled in the playset.

## What is merged, and against what

Re-verified 2026-08-12 against the live 45-mod playset (index rebuilt first —
`ck3.py conflicts` reads the index, not `dlc_load.json`).

| File | Colliding mods, in load order | Merge decision |
|---|---|---|
| `common/scripted_effects/07_dlc_ep3_scripted_effects.txt` | House Founders → More Dragon Eggs → Seasons of Ice and Fire | House Founders is the trunk; Seasons' removal of the `winter_*_modifier` checks kept; More Dragon Eggs' additions kept |
| `common/on_action/child_birth_on_actions.txt` | House Founders → Seasons of Ice and Fire | superset of both, no line dropped |
| `common/coat_of_arms/template_lists/color_lists.txt` | AGOT+ → House Founders | House Founders is the trunk **except** `valyria_dark/medium/light`, where AGOT+'s named-colour rewrite wins over House Founders' raw `rgb {}` lists (marked `#AGOT+ change` in the file). Without the merge House Founders wins and that rewrite is lost |
| `common/bookmarks/challenge_characters/00_challenge_characters.txt` | Additional Models and Special Buildings → Bookmarked | Additional Models' superset plus Bookmarked's only unique entry, `egg5` (Targaryen_122). `egg1`–`egg4` are duplicates of Additional Models' named Aegon entries and are deliberately dropped |

None of the four input mods has been updated since the merges were built
(all workshop mtimes predate them), so the merges are current.

## Dropped 2026-08-12 — inputs no longer installed

| File | Needed | Status |
|---|---|---|
| `gui/interaction_menu_window.gui` | Better Barbershop + More Bloodlines | neither installed; the file no longer collides at all |
| `history/titles/agot_e_the_crownlands.txt` | Nobility of Westeros | not installed |
| `history/titles/agot_k_dragonstone.txt` | Nobility of Westeros | not installed |
| `gui/window_character.gui` | built on a Spanish-translation trunk for More Bloodlines' three hooks | **actively harmful now.** That collision is today AGOT CBO Base → [other mod] → [other mod] AGOT Compatibility, and [other mod] AGOT Compatibility is a purpose-built patch that already resolves it. Shipping a stale trunk here would clobber it |

The originals of all four are still in the old copy under
`C:/Users/nahue/Documentos/Paradox Interactive/Crusader Kings III/mod/agot_conflict_merge`.

## Brace-balance caveat

AGOT Bookmarked comments out `# 7999.4.1 = {` lines, so its files are legitimately
`{`-heavy. A merge inheriting the same offset is correct, not broken.

## Commands

    python tools/ck3.py deploy agot_conflict_merge
    python tools/ck3.py validate agot_conflict_merge
    python tools/ck3.py conflicts          # rebuild the index first if the playset changed
