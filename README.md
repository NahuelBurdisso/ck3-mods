# AGOT ES Dragons Fix

Source for the CK3 mod `agot_es_dragons_fix`. Must load **last**.

## Why this exists

The Spanish translation mod `3463729959` ("AGOT Spanish-Español") overrides
`history/characters/00_agot_char_dragons.txt` in order to translate 19 dragon names, which are
hardcoded `name =` values in character history rather than localization keys — so they cannot be
translated from a `.yml`.

Its copy is built on an older AGOT. Against AGOT 0.5.1 it drops:

- the `dragon_maegor_12` block (Greyscale, mentioned status)
- 3 lair assignments — `b_high_tide`, `b_the_red_keep`, `b_blackglass_port`

This mod ships AGOT 0.5.1's file with the 19 translated names merged back in, so neither the
translation nor the content is lost. Being a local mod, Steam cannot revert it the way it reverts
hand-edits to a workshop folder.

## Translated names

Azogue, Caníbal, Fuegonegro, Sueñafuego, "Ala de Plata", Fuegoalto, Fuegodorado, Lunafuego,
Robaovejas, "Fantasma Gris", Fuegosol, "Ala del Desconocido", Bruma, "Danzarina Lunar",
Estrellacaza, Borrasca, Alba, Fuegonoche. (Meleys is spelled the same in both.)

## Regenerating after an AGOT update

AGOT owns the trunk, so this file goes stale whenever AGOT edits its dragon history. Re-merge by
splitting both source files into top-level `dragon_* = { }` blocks, then for each block key present
in both, replacing AGOT's `name =` value with the Spanish one while keeping AGOT's trailing comment.

Sources:

- trunk: `<workshop>/2962333032/history/characters/00_agot_char_dragons.txt`
- names: `<workshop>/3463729959/history/characters/00_agot_char_dragons.txt`

Verify the result against the trunk: equal line count, brace depth 0, same number of top-level
blocks, same `CASTLE = title:` count, UTF-8 BOM, LF endings.

## Commands

- Deploy:   `python tools/ck3.py deploy agot_es_dragons_fix`
- Validate: `python tools/ck3.py validate agot_es_dragons_fix`
- Enable:   `python tools/ck3.py playset add agot_es_dragons_fix`
