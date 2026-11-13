# GUI 1.19 Patch (`gui119`)

Repairs GUI files that mods in the playset ship for a *different* CK3 version than
the one installed. The game is 1.19.0.6 ("Scribe"); several mods have
already moved to 1.20, and a few never left 1.18.

Nothing here is new content. Every file is either vanilla 1.19 script or another
mod's own file with its 1.20-only parts taken out, re-shipped from a mod that loads
last so it wins the override chain.

## What it fixes

### `gui/interaction_menu_window.gui` — 132 errors per run

**Better Barbershop** (playset 77, `supported_version="1.*.*"`) ships the **CK3 1.20**
copy of this file. It calls the puppet data functions — `GetAvailablePuppets`,
`IsPuppetViewActive`, `GetSelectedPuppetType`, type `PuppetInteractionsFilter` —
none of which exist in 1.19.0.6. Because it loads after everything else, the whole
character interaction menu is built from 1.20 script on a 1.19 engine.

It is plain 1.20 vanilla besides, so it also silently drops everything **AGOT** adds
to this file: `agot_interaction_knight_tree_button`,
`agot_interaction_dragon_tree_button`, `agot_interaction_dragon_edit_button` and the
`AGOTGetNameNoTooltip` name call. Those three buttons are missing in game right now.

The base here is therefore **A Game of Thrones' own 1.19.0.6 file**, not vanilla's,
with Better Barbershop's one real change kept: `button_barbershop` loses its
`visible = "[Character.CanCustomizePortrait]"` gate, so the barbershop button still
shows for every character. The diff against AGOT's file is that single line.

Note the wildcard: `1.*.*` matches anything, so a version audit can never flag this
mod. Declared versions are unreliable in both directions.

### `gui/custom_gui/gui119_situation_types.gui` — 62 errors per run

**AGOT: Seasons of Ice and Fire** (playset 26) replaces
`gui/window_the_great_steppe.gui` with a 789-line copy; vanilla's is 1169 lines and
is the only place that declares `icon_situation_phase_effect_item` and
`icon_situation_phase_effect_participant_group_item`. With those gone, every vanilla
file that uses them errors: `cooltip.gui`, `window_tgp_dynastic_cycle.gui`,
`window_silk_road.gui`, `window_situation_sub_region.gui`.

Both types are re-declared verbatim in a file of our own, so no file is replaced.
If a future update makes Seasons of Ice and Fire ship the full file again, this one
has to go or the types will be defined twice.

### `gui/preload/gui119_fonts.gui` — 6 warnings per run

**AGOT More Dragon Eggs** (playset 20) asks for a `Font_Size_Huge` template in
`gui/custom_gui/mde_gui/dragonpit_single_viewer.gui`. CK3 1.19 defines Tiny (13),
Small (15), Medium (18) and Big (23) — there is no Huge, so the dragonpit counters
fall back to the default size. Added at 28, continuing the progression.

### `gui/00_interactive_map_coa.gui` — 36 errors per run

**More Interactive Vassals** (playset 59, copied from version 5.7) adds a cardinal
icon to the three realm CoA map types. It is a 1.20 feature: the icon asks
`Title.HasClericalElector` and its scripted gui uses `any_clerical_elector_title`,
neither of which exists in 1.19.0.6. This is MIV's file with those three
`flowcontainer` blocks removed (108 lines) and nothing else changed.

### `gui/event_windows/gr_book_event_window.gui` — 14 errors per run

**Grand Remembrance** (playset 35, copied from version 1.10.0) draws the folio portrait
twice and switches between them on `ShouldStylizeDeadPortrait( Character.Self )`, the
1.20 "Stylize Deceased Characters" setting. On 1.19 neither `visible` parses, so both
portraits draw on top of each other. Here the plain one is `visible = yes` and the
painted one `visible = no`; two lines differ from GR's file.

### `gui/decision_view_widgets/decision_view_widget_nht_reinforce_barony.gui` — 44 errors per run

**More Lifestyles** (playset 62, copied from version 1.3.0) wrote this widget against
1.20, where the `create_holy_order` controller's data type is called
`DecisionViewWidgetSelectBarony`. In 1.19.0.6 it is still
`DecisionViewWidgetCreateHolyOrder`:

| 1.20 (mod) | 1.19 (here) |
|---|---|
| `HasCurrentTitle` | `HasCurrentCapital` |
| `GetCurrentTitle` | `GetCurrentCapital` |
| `HasValidTitles` | `HasValidBaronies` |

The mod's tooltip loc key embeds the 1.20 name as well, so the widget points at our
own `GUI119_NHT_REINFORCE_BARONY_SELECT_HOLDING_TOOLTIP` (English and Spanish).

These three are full copies of another mod's file. When that mod updates, compare its
version with the one recorded above and rebuild the copy, or the patch will silently
pin an old file.

## Load order

Must load **after** every mod named above. Anywhere at the end of the playset is fine.

## Not fixed here

- **Extended Outliner** (78) replaces `gui/hud_outliner.gui` with a 1.18-era copy,
  which drops AGOT's dragon pins (`agot_dragon_pin_icon`, `agot_dragon_pin_name`,
  `agot_dragon_pin_relation` and the `IsCharacterDragon` guards). Silent — no error
  in the log, pinned dragons just render as ordinary characters.
- **Of Ash and Oaths** (53) has 29 broken lines in `zz_aao_story_l_english.yml`:
  literal newlines inside quoted loc values, which CK3's reader cannot parse.
- **AGOT Legend Seeds Updated** (50) defines `legend_tywin_lannister` twice in its
  own `legends_l_english.yml`.
- **Advanced Cheat Menu** (41) is enabled but its workshop folder is gone. Needs a
  re-subscribe in Steam, or removal from the playset.
