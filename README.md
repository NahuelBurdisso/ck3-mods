# AGOT Conflict Merge Patch

Merged copies of files that several enabled mods each *fully replace*. CK3 does not
merge whole files — the last mod in load order wins outright — so without this, every
earlier mod's edits to these files are silently gone.

Must load **after every owning mod**. `agot_dd_fix` owns only
`events/agot_events/agot_scenario_defiance_of_duskendale_events.txt`, so it does not
interact with anything here and keeps its "always last" slot.

## Rebuilding — do not hand-merge

    python tools/_mergepatch.py            # report only
    python tools/_mergepatch.py --write    # regenerate all five files
    python tools/ck3.py validate agot_conflict_merge

`tools/_mergepatch.py` reads the live `dlc_load.json`, resolves each target's owners in
load order, and runs a real 3-way merge (`git merge-file`, base = first owner) once per
owning mod. Genuine overlaps auto-resolve to the later-loading mod, i.e. identically to
what the game does today. It then checks, per file: no conflict markers, brace delta equal
to the base's, and **every owner's unique-vs-base lines present in the output**.

**A merge pins its inputs' content at build time. Re-run after ANY owning mod updates.**
The 2026-08-12 hand-merges had gone stale exactly this way — four of the five owning mods
updated between 09-08 and 09-14.

## What is merged, and against what

Rebuilt 2026-09-14 from the live 81-mod playset. All five: 0 conflicts, 0 lines lost.

| File | Owners, in load order | Recovered by the merge |
|---|---|---|
| `common/scripted_effects/07_dlc_ep3_scripted_effects.txt` | AGOT → House Founders [12] → More Dragon Eggs [17] → Seasons [22] | HF's 339-line adventurer-title rework (it comments AGOT's `adventurer_name_001..` out behind `# AGOTHF Disabled` and substitutes house-founder naming) **and** MDE's `# MDE Modified` block (returns the head dragonkeeper to court and re-pits living dragons at the new capital on title transfer). Both were dead: Seasons won the file. Seasons' own `#SEASONS MODIFIED` winter-modifier lists are kept |
| `gui/hud.gui` | AGOT → More Dragon Eggs [17] → Battlefield Duel + [76] | MDE's `bottom_left_dragon_portrait = {}` widget — the HUD dragon portrait, lost to Battlefield Duel +'s 116-line reputation-stack rewrite |
| `common/coat_of_arms/template_lists/color_lists.txt` | AGOT → AGOT+ [2] → House Founders [12] | AGOT+'s 38 unique lines (incl. the `valyria_dark/medium/light` named-colour rewrite), lost to House Founders |
| `common/on_action/child_birth_on_actions.txt` | AGOT → House Founders [12] → Seasons [22] | HF's 4 unique lines, lost to Seasons |
| `common/bookmarks/challenge_characters/00_challenge_characters.txt` | AGOT → Additional Models & Special Buildings [6] → Bookmarked [19] | AMSB's 47 unique lines, lost to Bookmarked. 28 top-level entries out, no duplicate keys — Bookmarked no longer ships the `egg1`–`egg4` entries the 2026-08-12 note said had to be dropped by hand |

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

## Brace-balance caveat

AGOT Bookmarked comments out `# 7999.4.1 = {` lines, so its files are legitimately
`{`-heavy. A merge inheriting the same offset is correct, not broken — which is why the
rebuild compares the merge's brace delta to the **base's**, not to zero.
