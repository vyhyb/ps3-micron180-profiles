# Printer profile: Micron 180

File: `PrintersForAnts/1.0.3/preset-printer-micron.yaml`, plus the `printer`, `tool` and `printer_config`
entries in `vendor.yaml`.

The Micron 180 is a small CoreXY printer by PrintersForAnts. It runs Klipper. This profile is for a
machine with a direct-drive extruder and an **E3D V6** hotend.

## Hardware definition (vendor.yaml)

| Item | Value | Notes |
|------|-------|-------|
| Printer model / base model | `MICRON180` | Used in every `condition:` in the bundle |
| Nozzles (tools) | `micron-0.4`, `micron-0.6` | Enabled through the `supports_04_nozzle` and `supports_06_nozzle` features |
| Default configuration | `micron180-cfg` with a 0.4 nozzle and a PEI Smooth sheet | |
| Bed assets | `micron-bed.stl`, `micron-bed-texture.png`, `micron-thumbnail.png` | In `assets/` |

## Machine settings

### Geometry

| Key | Value | Meaning |
|-----|-------|---------|
| `bed_shape` | `0x0, 173x0, 173x173, 0x173` | Printable area in mm, origin at front-left |
| `max_print_height` | `140` | Z height in mm |
| `extruder_clearance_radius` | `70` | Used by sequential printing only |
| `z_offset` | `0` | Set Z offset in Klipper, not here |

### Firmware and g-code

| Key | Value | Meaning |
|-----|-------|---------|
| `gcode_flavor` | `klipper` | |
| `use_relative_e_distances` | `1` | Relative extrusion (`M83`). Your `PRINT_START` macro must not switch to absolute E |
| `use_firmware_retraction` | `0` | Retraction comes from the print profile |
| `autoemit_temperature_commands` | `0` | The slicer adds **no** `M104`/`M140`/`M109`/`M190`. All heating is done by `PRINT_START` |
| `binary_gcode` | `0` | Plain-text g-code, as Klipper requires |
| `machine_limits_usage` | `time_estimate_only` | The limits below only affect the time estimate. Klipper's `printer.cfg` controls the real motion, so keep the two in sync |
| `thumbnails` | `64x64/PNG, 400x300/PNG` | For Mainsail/Fluidd previews |
| `remaining_times` / `silent_mode` | `0` / `0` | Marlin features; off for Klipper |
| `stuck_filament_detection` | `0` | Prusa firmware feature; off |

### Machine limits (time estimate only)

The values mirror the `[printer]` section of the Micron's Klipper `printer.cfg`:

```ini
[printer]
kinematics: corexy
max_velocity: 200
max_accel: 8000
max_z_velocity: 25
max_z_accel: 350
square_corner_velocity: 5
```

| Key | Normal | Silent | Klipper source |
|-----|--------|--------|----------------|
| `machine_max_acceleration_x` / `_y` | 8000 | 8000 | `max_accel` |
| `machine_max_acceleration_extruding` | 8000 | 8000 | `max_accel` (Klipper uses one limit for every move) |
| `machine_max_acceleration_travel` | 8000 | 8000 | `max_accel` |
| `machine_max_acceleration_retracting` | 1500 | 1500 | – |
| `machine_max_acceleration_e` | 10000 | 10000 | – |
| `machine_max_acceleration_z` | 350 | 350 | `max_z_accel` |
| `machine_max_feedrate_x` / `_y` | 200 | 200 | `max_velocity` |
| `machine_max_feedrate_z` | 25 | 25 | `max_z_velocity` |
| `machine_max_jerk_x` / `_y` | 5 | 5 | `square_corner_velocity` (closest equivalent) |
| `machine_max_jerk_z` | 0.2 | 0.2 | – |
| `machine_max_jerk_e` | 2.5 | 2.5 | – |

> **Note:** Some print profiles ask for more than Klipper allows. Travel speed is 300-500 mm/s and
> infill speed in 0.20mm QUALITY is 200 mm/s, while `max_velocity` is 200. Klipper caps every move at
> `max_velocity`, and the time estimate does the same through `machine_max_feedrate_x` / `_y`. If
> your printer allows higher speeds, raise `max_velocity` in Klipper and these feedrates together.
>
> Even with matching limits, PrusaSlicer models Klipper's motion only approximately. For exact times, see
> the klipper_estimator section in the [README](../README.md#accurate-print-times-with-klipper_estimator).

### Custom g-code

**Start g-code** passes temperatures to a Klipper `PRINT_START` macro, then draws a prime line:

```gcode
PRINT_START EXTRUDER={first_layer_temperature[initial_tool]} BED={first_layer_bed_temperature[initial_tool]} CHAMBER={chamber_temperature[initial_tool]} CHAMBER_MIN={chamber_minimal_temperature[initial_tool]}
G0 X20 Y4 F10000   ; Go to starting point
G0 Z0.4            ; Raise Z to 0.4
G91                ; Incremental positioning
G1 X100 E35 F1200  ; Primeline
G90
```

**End g-code:** `print_end    ;end script from macro`

**Before layer change:**

```gcode
;BEFORE_LAYER_CHANGE
;[layer_z]
G92 E0
```

**After layer change:**

```gcode
;AFTER_LAYER_CHANGE
;[layer_z]
```

`color_change_gcode` (`M600`) and `pause_print_gcode` (`M601`) are left at the slicer defaults. Klipper
needs macros with those names if you use colour changes or pauses.

### What the Klipper side must provide

| Macro | Required | Expected behaviour |
|-------|----------|--------------------|
| `PRINT_START` | yes | Takes `EXTRUDER`, `BED`, `CHAMBER` and `CHAMBER_MIN`. Homes, levels (optional), heats bed and nozzle and **waits** for them, and sets relative extrusion (`M83`). Must leave the head somewhere safe for the move to X20 Y4 |
| `PRINT_END` | yes | Retract, park, turn off heaters and fans, disable motors |
| `M600` | optional | Filament change (for example via `PAUSE`) |
| `M601` | optional | Pause |

`CHAMBER` and `CHAMBER_MIN` are `0` in all filament profiles. A macro that does not use them can simply
ignore the parameters.

## Settings intentionally not set

The PrusaSlicer 2 → 3 converter copied several single-extruder multi-material (MMU) settings from a Prusa
template. They have no effect on a single-tool printer and were removed: `cooling_tube_length`,
`cooling_tube_retraction`, `parking_pos_retraction`, `extra_loading_move`, `multimaterial_purging`,
`high_current_on_filament_swap`, `filament_change_time`, `single_extruder_multi_material` and
`enable_pressure_advance_during_ramming`. The slicer uses its defaults for them.
