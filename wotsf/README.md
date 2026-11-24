# AGOT: War of the Small Folk

A submod for **A Game of Thrones** (CK3 total conversion) about the human cost of war.
Counties remember what armies do to them, and the memory belongs to the land, not to the lord.

- **CK3**: 1.19.0.6 "Scribe"
- **AGOT**: 0.5.1 (workshop `2962333032`) — hard dependency, declared in `descriptor.mod`
- **Status**: Phases 1-3 implemented (suffering system + chevauchée + brotherhoods). Phase 3 has
  not yet been run in game. Phase 4 planned.

---

## What Phase 1 does

Every county that war touches gets a hidden `wotsf_suffering` score from 0 to 100.
It goes up when armies do things to the county and down only in peace.

**Gains** (all multiplied by the intensity game rule, and by 1.5 during winter):

| Source | Amount | When |
|---|---|---|
| Sack / raid completed | +15 | once, at the moment the raid resolves |
| Hostile army present | +3 | once per month, no matter how many stacks |
| Friendly army present | +1 | once per month |
| Under siege | +4 | monthly, while a siege is running in the county |
| Occupied | +2 | monthly, while `county_controller != holder` |

**Recovery**: -2 a month (-4 if the holder is `compassionate` or `just`), and only while the
county is neither occupied nor besieged **and its holder is not at war anywhere**. A lord who
keeps fighting elsewhere does not get to heal his own lands. That is the design, not a bug.

**Bands** (one county modifier at a time, never stacked):

| Band | Suffering | Modifier | Effects |
|---|---|---|---|
| 1 | 25-49 | Restless Fields | tax -10%, levies -10% |
| 2 | 50-74 | A Land in Pain | tax -25%, levies -25%, dev growth factor -50% |
| 3 | 75-100 | Scorched Earth | tax -50%, levies -60%, dev growth -0.2, control growth -0.3 |

At 0 the county is wiped clean: variables removed, modifier removed, monthly pulse stopped.

**Report**: the decision *Assess the State of the Smallfolk* (1 year cooldown, free) counts
your own counties per band. It reads `every_held_title`, never the map.

**Game rules**: `Small Folk: Suffering Intensity` (Disabled / Merciful / Canon / Brutal) and
`Small Folk: Debug Mode` (off / on, unlocks two testing decisions on your capital county).

---

## What Phase 2 does

**Order a Chevauchée** is a hostile character interaction aimed at a county your enemy holds.
You need an army of yours standing in that county and not in battle. The county cannot have been
raided in the past six months, and you must not have sworn the practice off.

For three months the county burns:

| Effect | Value |
|---|---|
| Suffering | +8/month (+4 if the defender garrisoned it) |
| Plunder to the commander | `development_level × 0.15` gold/month, halved if garrisoned |
| Dread to the commander | +0.5/month |
| County | dev growth factor -50%, county opinion -20 |
| Commander | movement speed -25% |

You pay for the order the moment you give it: clergy opinion -10 for five years, -25 piety if
your faith holds compassion a virtue, and a vassal opinion split — the compassionate, just and
paranoid think less of you, the callous, sadistic and ambitious think more.

**Escalation.** The third time you burn the same opponent's lands, a knight of your own host who
still has a conscience comes to your tent (`wotsf.0101`). Stop and you swear it off for ten years
and gain piety. Break him in front of the host and two in five walk out of your service. Hang him
and you take the trait on the spot.

**Scourge of the Smallfolk** (dread +20, vassals -10, clergy -20, mercenaries -10% to hire) is
also granted by six chevauchées inside a rolling five-year window. While the man lives, every
child of his carries -5 general opinion. Ten years of restraint erase it, or *Do Penance for the
Burned Fields* (300 piety + 150 gold) erases it now.

**The defender gets an answer** (`wotsf.0201`, once per five years). Garrison the county (halves
the raid's bite, costs you 15% of your levies for two years), promise justice (two years to pay,
or every count in your realm remembers the broken word), or do nothing (+5 suffering and the lord
who asked never forgets).

**Game rule**: `Small Folk: AI and the Chevauchée` — Never / The Cruel Only (default) / Freely.
Compassionate and just AI rulers never order one at any setting.

---

## What Phase 3 does

A county left at **Scorched Earth** stops being a number on the map and starts producing men.

**They rise on their own.** Suffering 75 or higher gives the county about a 12% chance a month
of raising a brotherhood — half a year, on average, of a lord doing nothing. Eight may exist in
the world at once. Their leader is a real character standing in one of the county's provinces,
with a name, a face and no dynasty.

| Strength | What it costs the holder |
|---|---|
| 1-59 | tax -20%, control growth -0.25, county opinion -15 |
| 60+ | tax -35%, levies -20%, control growth -0.5, county opinion -25 |

Strength grows about 3 a month, faster in a badly hurt county and faster still if somebody is
paying them. It **falls** 4 a month once suffering drops below 50, and the band disperses on its
own below 25. Healing the county is a real answer, not a slow one.

**They make themselves felt.** Past strength 40 they take a tax cart (`wotsf.0302`) — never
killing anyone from the county, which is exactly how they keep it quiet. Past 70 there is a song
about their leader (`wotsf.0303`), and it is being sung in your hall.

**Three answers, all acting on your worst-afflicted county:**

- **Hunt Down the Brotherhood** (150 gold, once a year). A roll, not a certainty: base 20% plus
  your martial, +25 for an army already standing there, less a quarter of their strength.
  Winning hangs the leader on the road out of the county. Failing makes them stronger and the
  county watched you fail.
- **Open the Granaries** (150 gold, once a year). -25 suffering outright. Unlike everything else
  in the mod this is not touched by intensity or by winter: gold buys grain at the same rate in
  every season.
- **Treat with the Brotherhood** (150 piety). It works. Nobody hangs, the band disperses, and
  their leader may take service with you — and every proud, ambitious or brave vassal you have
  now knows you ended a rising by talking.

**Somebody else can be paying them.** *Fund the Brotherhood* costs 150 gold, is aimed at a county
of a ruler you are at war with, and **the victim is not told**. What is created is a secret, so
the vanilla machinery decides when it comes out — his spymaster, or whoever buys the hook. When
it does (`wotsf.0304`), he and every vassal he has remembers it for thirty years.

**Game rule**: `Small Folk: Brotherhoods` — None / As Written (default) / The Riverlands
(2.5× the rise rate; the cap of eight still holds).

---

## Load order

Anywhere **after AGOT**. The mod adds only new prefixed files; it replaces nothing, so its
position relative to other submods does not matter. `descriptor.mod` declares the AGOT
dependency, so the launcher will keep it below AGOT on its own.

## Compatibility

| Mod | How | Result |
|---|---|---|
| AGOT 0.5.1 | required | no file collision, no key collision, no on_action `effect` block touched |
| AGOT: Seasons of Ice and Fire | detected, optional | `has_global_variable = AGOT_seasons_is_loaded`. Nothing breaks when absent |
| Any other submod | none needed | all keys are `wotsf_`-prefixed, all files are new |

Verified with `ck3.py conflicts` against a 47-mod playset: **0 colliding files**.

### How Seasons is handled

Winter is read from the **vanilla** province modifiers `winter_mild_modifier`,
`winter_normal_modifier` and `winter_harsh_modifier`, never from a Seasons-specific key.
That means the winter multiplier works identically with or without Seasons — Seasons simply
makes winter far more frequent, so the same code produces a much harsher game. Referencing a
Seasons modifier key directly would have made the mod fail to load without it.

---

## Technical decisions

Three things the design document asked for do not exist in CK3 1.19. Each was redesigned
rather than hacked around.

### 1. The monthly pulse is per-county, not global

1.19 has **no monthly global `on_action`** — the only monthly hooks in the engine are
`on_army_monthly`, `on_faith_monthly` and the per-playable pulses. A global monthly loop over
every county would also violate the performance rule.

Instead each suffering county runs a **self-chaining hidden event** (`wotsf.0001`, scope
`landed_title`) that re-fires itself every 30 days and dies when suffering hits 0. Vanilla
precedent: `false_conversion.0002/0003`, raised from `county_on_actions.txt`.

The chain **is** the registry. `wotsf_active_counties` (a global variable list) mirrors it for
the report and for the phase-3 world caps. Nothing in the mod ever iterates the map.

### 2. Army presence is read from the commander, and enrols in the same hook

The design offered two paths: scan armies from a global tick (A), or check counties for armies
(B). Path B alone **cannot bootstrap** — a county nobody has reached yet is not in the registry,
so it is never scanned, so it never enters the registry.

The mod hooks `on_army_monthly` instead. An army scope has **no location link** in 1.19
(`army_commander`, `army_owner` and `involved_combat_side` are the only army event targets),
but the commanding character stands in the army's province, which is how vanilla `bp2_yearly.4030`
reads it. So `scope:army.army_commander.location.county` is the army's county, and the one hook
both enrols the county and charges it. No scan anywhere.

Multiple stacks in one county are deduplicated by per-county monthly claim variables
(`wotsf_army_claim_hostile` / `_friendly`), cleared once a month by the tick.

### 3. Chevauchée is county + commander modifiers, driven by an interaction

`add_army_modifier` **does not exist** in 1.19, so the design's "army modifier" is not
implementable. The chevauchée is a county modifier plus a countdown variable on the county, and a
`movement_speed` character modifier on the commander. The countdown is ticked by the Phase 1
county pulse, so Phase 2 adds **no new loop**.

A CK3 **decision cannot point at a county**. The only vehicle in 1.19 that lets the player pick
one is a character interaction with `target_type = title`, so the order is sent at the enemy
ruler with one of their counties as the target — the same machinery as
`revoke_title_interaction`. It is hostile and cannot be refused (`auto_accept = yes`); the
recipient still gets the popup, and `wotsf.0201` gives them something to do about it.

### 4. Two design points that 1.19 cannot deliver

Both were escalated and replaced with the author's approval rather than hacked around.

**"Your main army loses numbers."** There is no effect in 1.19 that damages or removes men from
a raised army — `remove_commander` is the only army-scope effect there is. Replaced with
*garrison + levy cost*: the defender posts men in the county (a county modifier that halves both
the suffering and the plunder) and pays for it with `levy_size -15%` and
`levy_reinforcement_rate -25%` on himself for two years. The troops leave the line the same way;
they just do it through a modifier instead of a casualty count.

**"The third chevauchée in the same war."** `scope:war` cannot be stored in a variable: the war
object is destroyed at war end, and a stored reference would dangle. The escalation counter is
keyed to the **opponent** instead. In play it reads identically, and it survives the peace — a
second war against the same neighbour continues the count, which is arguably more honest.

### 5. Birthday, birth and death hooks go through sub-on_actions

`on_birthday`, `on_birth_child` and `on_death` are hooked by declaring a private
`wotsf_on_birthday` / `wotsf_on_birth_child` / `wotsf_on_death` and listing it under
`on_actions = { }`. This is the exact pattern AGOT itself uses on those keys
(`agot_knight_on_actions.txt`, `agot_ub_on_actions.txt`), which proves the list merges in this
playset. `wotsf.0120` bails on one `has_trait` check, so every character who is not a Scourge
costs a single trait read per birthday.

### 6. Brotherhoods add no loop of their own

They are ticked by the Phase 1 county pulse — the same 30-day self-chaining event that counts
suffering down. The spawn roll, the strength growth, the flavour events and even the check for
*"is the leader still alive?"* all happen inside `wotsf_county_tick_effect`. No new `on_action`
was hooked in Phase 3, and a county that has never suffered still costs the same two variable
reads it cost in Phase 1.

### 7. The tier modifiers have no duration, so every exit is funnelled

A duration-less county modifier is only removed by something removing it. A county that healed
to 0 with a band still on it would carry `wotsf_brotherhood_modifier` for the rest of the game.
Every way a brotherhood can end — hunted, parleyed, starved of recruits, or the county simply
healing — goes through `wotsf_end_brotherhood_effect`, including a guarded call inside
`wotsf_clear_county_effect`. The chevauchée cooldown went the other way for the same reason: it
is a modifier *with* a duration precisely so nothing has to remember to expire it.

### 8. Relief does not scale with intensity or winter

`wotsf_relieve_suffering_effect` is a separate effect rather than
`wotsf_add_suffering_effect` with a negative amount. That one multiplies by the intensity rule
and by winter, so relief would be worth half as much in the season the county needs it most and
1.5× under Brutal — backwards on both counts. Gold buys grain at the same rate all year.

### 9. The patron is a real secret, not a popup

`wotsf_fund_brotherhood_interaction` sets `popup_on_receive = no`. The victim is not told.
What the actor gains is `wotsf_secret_funding_outlaws`, and from there the vanilla secret system
decides when it comes out. Its category is diplomacy — 1.19 has no intrigue category, and
`hostile` would file the thing next to a declaration of war, which announces exactly what it is
supposed to hide.

### 10. The decisions choose the county for you

There is no dynamic county picker for decisions in 1.19; a decision's option list takes static
`item` blocks. All three brotherhood answers use `ordered_held_title` sorted by
`wotsf_county_suffering_value` and act on the worst one you hold. The localization says so
plainly rather than leaving the player to guess.

### Other constraints obeyed

- **on_actions are additive only.** `events = { }` lists merge across mods; `effect = { }` does
  not — the engine keeps exactly one and picks it alphabetically by filename. This mod never
  writes an `effect` block on a shared hook, so AGOT's own logic is untouched.
- **Variables are created late.** A county gets `wotsf_suffering` the first time something
  happens to it, and loses it the moment it heals. A quiet game costs nothing.
- **Band modifiers are stripped before the new one is added.** Two different county modifiers
  stack; re-adding the same one only refreshes it.
- **Scripted triggers take no parameters.** A scripted trigger that declares a parameter and
  never reads it fails to compile, and every call site then goes silently dead.

---

## Honest limitations

- **Suffering survives a change of owner.** This is deliberate (the land remembers), but it
  means conquering a ruined county hands you the ruin. The decision and event text says so.
- **Recovery is blocked by any war the holder is in**, even one fought on the far side of the
  continent. Intentional, but it makes long wars very punishing for the aggressor's own lands.
- **The self-chaining pulse is proven across one save/load, not across decades.** Save, reload
  and three months of play produced the full set of markers on the far side of the reload
  boundary and nothing in `error.log`. A long session has not been measured; that is owed in the
  Phase 4 balance pass.
- **Only counties with a holder participate.** Unlanded/wasteland counties are skipped entirely.
- **The world cap of eight brotherhoods is first-come.** A county that rolls while the world is
  full simply loses and re-rolls next month. There is no queue and no preference for the worst
  county, so one corner of the map can hold every band there is.
- **A brotherhood leader who is never hunted is never cleaned up.** He is a real character with
  no dynasty and no title; if the band ends by the county healing, he goes on living somewhere.
- **The patron is never forgotten.** `var:wotsf_brotherhood_patron` is not cleared when the
  patron dies. Today only the growth bonus reads it, so this is harmless.
- **There are still almost no flavour events.** The visible ones are the report, the knight
  confrontation, the defender's plea and the four brotherhood events. Phase 4 is the pool.
- **The escalation counter never resets at peace.** Keyed to the opponent, by design (see
  Technical decisions §4), but it means a grudge war can push you to the trait faster than the
  design's "three per war" reads on paper.
- **The commander who gets the plunder is picked at random** among your idle armies in the
  county. With two hosts there, the gold may land on the wrong one.
- **Nothing in Phase 3 has been observed in a running game yet.** Phase 2 has had a clean full
  cycle; the brotherhoods have not been run once. Treat every number above as intended, not
  measured.
- **The six-month chevauchée cooldown has never been watched expiring.** It is a modifier with a
  duration, so the engine owns it, but nobody has sat through one.

---

## Working on this mod

- Deploy:   `python tools/ck3.py deploy wotsf`
- Validate: `python tools/ck3.py validate wotsf`
- Enable:   `python tools/ck3.py playset add wotsf`
- Conflicts:`python tools/ck3.py conflicts`

Plan, changelog and roadmap live in `D:/ck3/docs/wotsf/`.
