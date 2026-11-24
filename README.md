# CK3 mods

My Crusader Kings III mods, one folder per mod. They target CK3 1.19 and the
[A Game of Thrones](https://steamcommunity.com/sharedfiles/filedetails/?id=2962333032) (AGOT)
total conversion. Each folder has its own README with the details.

## Content mods

| Folder | What it is |
|---|---|
| [`wotsf`](wotsf) | **AGOT: War of the Small Folk.** A submod about the human cost of war: counties remember what armies do to them. Suffering system, chevauchée and brotherhoods. |
| [Battle Chronicles](https://github.com/NahuelBurdisso/battle-chronicles) | Turns battles into narrated moments. Lives in its own repository. |
| [`bc_spike`](bc_spike) | The throwaway spike that proved the engine hooks Battle Chronicles is built on. |

## Compatibility and fix patches

Running a large AGOT playset means fixing what other mods break for each other. These patches
contain merged or corrected copies of vanilla and third-party mod files, as compatibility patches do;
the original work belongs to its authors.

| Folder | What it fixes |
|---|---|
| [`agot_conflict_merge`](agot_conflict_merge) | Merged copies of files that several mods each fully replace. CK3 does not merge whole files, so without it the last mod in load order silently wins. Built by a script, not by hand. |
| [`gui119`](gui119) | Repairs GUI files that mods ship for a different CK3 version than the one installed. |
| [`rpp_119_fix`](rpp_119_fix) | Makes Route Planner Plus work on CK3 1.19 by fixing one window. |
| [`agot_es_dragons_fix`](agot_es_dragons_fix) | Restores dragon history entries that the Spanish translation mod drops because it was built on an older AGOT. |
| [`agot_es_fallback`](agot_es_fallback) | Generator that fills every localization key missing in Spanish with its English text, because CK3 shows raw keys instead of falling back. Generator only. |

## Tooling

| Folder | What it is |
|---|---|
| [`claude_eyes`](claude_eyes) | A telemetry submod that dumps game state to the debug log so an AI assistant can read a running campaign. |

The CLI used to scaffold, validate, deploy and index these mods lives in
[ck3-modding-workspace](https://github.com/NahuelBurdisso/ck3-modding-workspace).

## Installing a mod

Copy the mod folder into `Documents/Paradox Interactive/Crusader Kings III/mod/` together with a
`.mod` pointer file (the folder's `descriptor.mod` plus a `path=` line), then enable it in your playset.
The READMEs state where each one must sit in the load order.
