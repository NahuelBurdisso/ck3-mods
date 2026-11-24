# Route Planner Plus 1.19 Fix

Makes Route Planner Plus (`3689519233`) work on CK3 1.19. It overrides exactly one
file, `gui/window_travel_route_edit.gui`, which nothing else in the playset owns.

## What was broken

RPP's copy of the window kept a data-function shape 1.19 removed:

```
Or( TravelRouteEditWindow.IsSelectingProvinceAtEnd( TravelPlanDestination.GetIndex ),
    And( TravelRouteEditWindow.IsSelectingProvinceAtBegin( TravelPlanDestination.GetIndex ),
         IsDataModelEmpty( TravelPlanDestination.GetWaypoints ) ) )
```

at lines 135 and 435. The engine cannot parse it, so it **drops the `visible`
property entirely** — logged as

```
[E][pdx_gui_factory.cpp:934]: gui/window_travel_route_edit.gui:135 - Failed parsing
data statement '...' for property 'visible'(774)
```

With `visible` gone both widgets default to shown: the yellow "Select a province"
prompt sits permanently under every destination and every destination wears the
selection highlight, whether or not a selection is in progress.

## The fix

1.19 folded the pair into one call. `IsSelectingProvinceAt( d, w )` still covers the
slot before waypoint `w`; the slot before the destination itself — what `AtEnd` meant,
and what `AtBegin` meant while the waypoint list was empty — is now
`IsSelectingProvinceBeforeDestination( d )`. Vanilla uses exactly this pair in its own
`game/gui/window_travel_route_edit.gui` (lines 123 and 136), and they are the only two
`IsSelectingProvince*` functions left anywhere in the game directory.

RPP's other two call sites were already on the new two-argument form, which is why
only `AtEnd` appeared in the log: `Or` short-circuits and never reached `AtBegin`.

## Rebuilding

```
python tools/_rppfix.py            # report only, exit 0 == pass
python tools/_rppfix.py --write
```

from `D:/ck3`. It copies RPP's live workshop file and substitutes the two statements,
and
refuses to write unless it finds exactly 2 of them, the line count is unchanged (the
engine reports gui errors by line) and no dead call survives.

**This is a whole-file copy, so it pins RPP at the version it was built from.** Rerun
`_rppfix.py --write` after every RPP update or this mod silently reverts it. If the
statement count comes back anything but 2, RPP touched the file and the substitution
has to be re-derived rather than forced.

## Load order

Anywhere after Route Planner Plus, which sits at index 0. Nothing else owns
`window_travel_route_edit.gui`, so there is no other constraint. It is placed just
before the local patch mods at the end of the playset.
