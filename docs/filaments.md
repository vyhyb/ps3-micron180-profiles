# Filament profiles

Files: `PrintersForAnts/1.0.2/preset-filament-<TYPE>-<Vendor>-<Name>.yaml`, one file per filament.

## Available filaments

| Profile | Nozzle / bed °C (1st layer → rest) | Fan % (min-max) | Max flow 0.4 | Max flow 0.6 |
|---------|------------------------------------|-----------------|--------------|--------------|
| Generic PLA @Micron 180 | 230 → 225 / 60 | 100-100 | 15 | 15 |
| Prusament PLA @Micron 180 | 230 → 225 / 60 | 100-100 | 15 | 15 |
| Generic PETG @Micron 180 | 245 / 85 | 30-55 | 9 | 15 |
| Prusament PETG @Micron 180 | 250 / 85 | 30-55 | 9 | 15 |
| Generic ABS @Micron 180 | 260 / 100 | 15-15 | 10 | 9 |
| Generic ASA @Micron 180 | 260 / 100 | 20-20 | 10 | 9 |
| Prusament ASA @Micron 180 | 260 / 100 | 20-20 | 10 | 9 |
| Generic FLEX @Micron 180 | 240 / 50 | 30-60 | 1.35 | 1.35 |

Max flow is `filament_max_volumetric_speed` in mm³/s. It is the most important limit in the profile,
because it caps every print speed.

Every filament is available for both nozzles under the same name. The nozzle-specific values sit in
two named variants:

```yaml
kind: filament
id: 'Generic PETG Micron180'            # no "@" in ids, see below
name: 'Generic PETG'
features:
  $.type: 'PETG'
condition: printer.model == "MICRON180" and (tool.nozzle_diameter == 0.4 or tool.nozzle_diameter == 0.6)
values:
  temperature: 245
  ...                                   # everything that is the same for both nozzles
variants:
- condition: tool.nozzle_diameter == 0.4
  name: 'Generic PETG @Micron 180'      # the name shown in PrusaSlicer
  id: ...
  values:
    filament_max_volumetric_speed: 9
    slowdown_below_layer_time: 10
- condition: tool.nozzle_diameter == 0.6
  name: 'Generic PETG @Micron 180'
  id: ...
  values:
    filament_max_volumetric_speed: 15
    slowdown_below_layer_time: 17
```

Two rules keep custom filaments working. Breaking either makes PrusaSlicer 3.0.0-alpha12 crash on start
once a user saves a custom filament based on the profile:

- **No `@` in any `id`.** PrusaSlicer treats `@` in an id as a separator and builds the variant
  identity as `<variant id>@<suffix>`. A custom preset saved from it then points to a parent that
  cannot be found.
- **Give every nozzle variant a `name`.** Custom presets inherit from the named variant the user
  selected, as in Prusa's own files (for example `Prusament PLA @MINI 0.4`).

## Where the values come from

The values are Prusa Research's PrusaSlicer 3 filament profiles, resolved for the **Prusa MINI** with a
0.4 and a 0.6 nozzle. The MINI is the closest Prusa machine: a small bed, one tool and a V6-class
hotend. The following was then removed or changed for a Klipper printer:

| Removed / changed | Why |
|-------------------|-----|
| `pressure_advance` → `disabled`, `pressure_advance_value` removed | Prusa's values are tuned for Prusa firmware. Set pressure advance in Klipper (`[extruder] pressure_advance`) or in `PRINT_START` |
| `start_filament_gcode` removed | Prusa uses Marlin-only codes there (`M900`, `M142`) |
| Filament retraction and travel overrides (`retract_*`, `deretract_speed`, `wipe`, `travel_*`) removed | Prusa's MINI values are for its Bowden setup (2.5-3 mm). The Micron is direct drive, so the print profile's 0.75 mm applies to every material |
| MMU / wipe-tower settings removed (`filament_ramming_parameters`, `filament_cooling_*`, `filament_loading_speed*`, `filament_unloading_speed*`, `filament_stamping_*`, `filament_toolchange_delay`, `filament_multitool_*`, `filament_minimal_purge_on_wipe_tower`, `filament_purge_multiplier`) | Single tool, no MMU |

Temperatures assume an all-metal E3D V6. If your hotend has a PTFE liner that reaches the heat break,
keep the nozzle at or below 240 °C, which rules out ABS and ASA.

## Tuning for your machine

1. **Flow limit.** Print a volumetric flow test and set `filament_max_volumetric_speed` to about
   80 % of the point where extrusion starts to fail. A standard V6 manages about 11-15 mm³/s for PLA.
2. **Pressure advance.** Calibrate it in Klipper. To keep one value per filament, add
   `SET_PRESSURE_ADVANCE ADVANCE=<value>` to that filament's `start_filament_gcode`.
3. **Chamber.** `chamber_temperature` and `chamber_minimal_temperature` are 0 and are passed to
   `PRINT_START` as `CHAMBER` / `CHAMBER_MIN`. If your macro does heat-soaking, raise them for ABS and ASA.
4. **Extrusion multiplier.** All 1.0 except FLEX (1.15). Calibrate per spool if needed.

## Adding another filament

Copy the closest existing file and change `id` (no `@`), the top-level `name`, the variant `name`s,
`features.$.type` and the values. Keep the `@Micron 180` suffix in the variant names so they don't
clash with other vendors' filaments. Give each variant a new unique `id`. Then update the version `manifest.json` (see [Adapting](adapting.md#5-update-hashes-and-version)).

## Full value reference (shared values)

Values that are the same for both nozzles. A dash means the key is not set and the slicer default is used.

| Key | Generic ABS | Generic ASA | Prusament ASA | Generic FLEX | Generic PETG | Prusament PETG | Generic PLA | Prusament PLA |
|---|---|---|---|---|---|---|---|---|
| `bed_temperature` | 100 | 100 | 100 | 50 | 85 | 85 | 60 | 60 |
| `bridge_fan_speed` | 25 | 30 | 30 | 80 | 50 | 50 | 100 | 100 |
| `chamber_minimal_temperature` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `chamber_temperature` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `cooling` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `cooling_perimeter_transition_distance` | 10 | 10 | 10 | – | 10 | 10 | 10 | 10 |
| `cooling_slowdown_logic` | uniform_cooling | uniform_cooling | uniform_cooling | uniform_cooling | uniform_cooling | uniform_cooling | uniform_cooling | uniform_cooling |
| `disable_fan_first_layers` | 4 | 4 | 4 | 3 | 3 | 3 | 1 | 1 |
| `enable_dynamic_fan_speeds` | – | – | – | 0 | – | – | – | – |
| `end_filament_gcode` | ; Filament-specific end gcode | ; Filament-specific end gcode | ; Filament-specific end gcode | ; Filament-specific end gcode | ; Filament-specific end gcode | ; Filament-specific end gcode | ; Filament-specific end gcode | ; Filament-specific end gcode |
| `extrusion_multiplier` | 1 | 1 | 1 | 1.15 | 1 | 1 | 1 | 1 |
| `fan_always_on` | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `fan_below_layer_time` | 30 | 20 | 20 | 100 | 20 | 20 | 100 | 100 |
| `filament_abrasive` | – | – | – | 0 | – | – | – | – |
| `filament_colour` | '' | '' | '' | #008000 | '' | '' | '' | '' |
| `filament_cost` | 45.10 | 45.10 | 35.28 | 40 | 19.99 | 29.99 | 19.99 | 27.99 |
| `filament_density` | 1.04 | 1.07 | 1.07 | 1.22 | 1.27 | 1.27 | 1.24 | 1.24 |
| `filament_diameter` | 1.75 | 1.75 | 1.75 | 1.75 | 1.75 | 1.75 | 1.75 | 1.75 |
| `filament_infill_max_crossing_speed` | – | – | – | 0 | 0 | 0 | 0 | 0 |
| `filament_infill_max_speed` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `filament_max_volumetric_speed` | – | – | – | 1.35 | – | – | 15 | 15 |
| `filament_notes` | '' | '' | '' | – | '' | '' | '' | '' |
| `filament_shrinkage_compensation_xy` | 0% | 0% | 0% | 0% | – | – | – | – |
| `filament_shrinkage_compensation_z` | 0% | 0% | 0% | 0% | – | – | – | – |
| `filament_soluble` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `filament_spool_weight` | 278 | 278 | 278 | 0 | 278 | 278 | 278 | 278 |
| `filament_type` | ABS | ASA | ASA | FLEX | PETG | PETG | PLA | PLA |
| `filament_vendor` | Generic | Generic | Prusa Polymers | Generic | Generic | Prusa Polymers | Generic | Prusa Polymers |
| `first_layer_bed_temperature` | 100 | 100 | 100 | 50 | 85 | 85 | 60 | 60 |
| `first_layer_temperature` | 260 | 260 | 260 | 240 | 245 | 250 | 230 | 230 |
| `full_fan_speed_layer` | 0 | 0 | 0 | 0 | 5 | 5 | 3 | 3 |
| `idle_temperature` | – | – | – | 70 | – | – | – | – |
| `max_fan_speed` | 15 | 20 | 20 | 60 | 55 | 55 | 100 | 100 |
| `min_fan_speed` | 15 | 20 | 20 | 30 | 30 | 30 | 100 | 100 |
| `min_print_speed` | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 |
| `pressure_advance` | disabled | disabled | disabled | disabled | disabled | disabled | disabled | disabled |
| `slowdown_below_layer_time` | 20 | 20 | 20 | 10 | – | – | – | – |
| `temperature` | 260 | 260 | 260 | 240 | 245 | 250 | 225 | 225 |

Nozzle-specific values:

| Filament | 0.4 variant | 0.6 variant |
|----------|-------------|-------------|
| Generic / Prusament PLA | `filament_max_volumetric_speed: 15` (shared), `slowdown_below_layer_time: 15` | `slowdown_below_layer_time: 18` |
| Generic / Prusament PETG | `filament_max_volumetric_speed: 9`, `slowdown_below_layer_time: 10` | `filament_max_volumetric_speed: 15`, `slowdown_below_layer_time: 17` |
| Generic ABS, Generic / Prusament ASA | `filament_max_volumetric_speed: 10`, `filament_infill_max_crossing_speed: 0` | `filament_max_volumetric_speed: 9`, `filament_infill_max_crossing_speed: 100` |
| Generic FLEX | – | – |
