# Print profiles

File: `PrintersForAnts/1.0.2/preset-print-micron.yaml`

## Lineup

| Nozzle | Profile | Use it for |
|--------|---------|------------|
| 0.4 | **0.10mm STRUCTURAL** | Small, detailed parts that still need strength: 4 perimeters, 40 % grid infill |
| 0.4 | **0.20mm BALANCED** | Everyday prints: 3 perimeters, 15 % gyroid, gentler accelerations (2000/3000) |
| 0.4 | **0.20mm QUALITY** | Fast visual prints: 10 % gyroid, higher speeds and accelerations, supports on the build plate only |
| 0.4 | **0.20mm STRUCTURAL** *(default)* | Functional parts: 4 perimeters, 40 % cubic, 1 mm min shell thickness, slow first layer |
| 0.4 | **0.30mm STRUCTURAL** | Faster functional parts: 3 perimeters, 15 % grid, organic supports |
| 0.6 | **0.20mm STRUCTURAL** | Stronger and faster than 0.4 at the same layer height |
| 0.6 | **0.30mm STRUCTURAL** *(default)* | General-purpose 0.6 profile |
| 0.6 | **0.40mm DRAFT** | Large, quick parts: 2 perimeters |

The 0.4 profiles are your tuned PrusaSlicer 2.9 profiles, converted one to one. The 0.6 profiles are
new: they take Prusa MINI 0.6 geometry (0.68 mm extrusion width, thicker minimum shells) and apply the
Micron accelerations and support and bridge settings. **The 0.6 profiles have not been print-tested
yet.** Treat them as a starting point.

Print speeds are upper limits. On every move the slicer also caps speed by the filament's
`filament_max_volumetric_speed`, so a fast print profile with PETG (9 mm³/s on 0.4) prints slower
than with PLA (15 mm³/s).

## How the file is structured

```text
'*common Micron 180*'                  abstract, settings shared by every profile
 ├─ tool.nozzle_diameter == 0.4         layer height limits, file name
 └─ tool.nozzle_diameter == 0.6         layer height limits, file name

<print tree>  inherits '*common Micron 180*'
 └─ printer.model == "MICRON180"
     ├─ tool.nozzle_diameter == 0.4     support width
     │   ├─ 0.10mm STRUCTURAL @Micron 180 0.4
     │   ├─ 0.20mm BALANCED   @Micron 180 0.4
     │   ├─ 0.20mm QUALITY    @Micron 180 0.4
     │   ├─ 0.20mm STRUCTURAL @Micron 180 0.4
     │   └─ 0.30mm STRUCTURAL @Micron 180 0.4
     └─ tool.nozzle_diameter == 0.6     0.6 widths, shells, Micron accelerations
         ├─ 0.20mm STRUCTURAL @Micron 180 0.6
         ├─ 0.30mm STRUCTURAL @Micron 180 0.6
         └─ 0.40mm DRAFT      @Micron 180 0.6
```

To change something for **every** profile, edit `*common Micron 180*`. To change one nozzle, edit
that nozzle's node. To change one profile, edit its leaf.

## Per-profile values

### 0.4 nozzle

| Key | 0.10mm STRUCTURAL | 0.20mm BALANCED | 0.20mm QUALITY | 0.20mm STRUCTURAL | 0.30mm STRUCTURAL |
|---|---|---|---|---|---|
| `bottom_solid_layers` | 5 | 5 | 5 | 5 | 4 |
| `bottom_solid_min_thickness` | 0 | 0 | 0 | 1 | 0 |
| `bridge_flow_ratio` | 0.85 | 0.8 | 0.8 | 0.8 | 0.8 |
| `brim_separation` | 0.1 | 0 | 0 | 0.07 | 0.07 |
| `default_acceleration` | 5000 | 2000 | 5000 | 5000 | 5000 |
| `external_perimeter_acceleration` | 0 | 0 | 0 | 1500 | 1500 |
| `external_perimeter_extrusion_width` | 0.4 | 0.42 | 0.42 | 0.45 | 0.45 |
| `external_perimeter_speed` | 40 | 40 | 80 | 40 | 40 |
| `extrusion_width` | 0.4 | 0.44 | 0.44 | 0.45 | 0.45 |
| `fill_density` | 40% | 15% | 10% | 40% | 15% |
| `fill_pattern` | grid | gyroid | gyroid | cubic | grid |
| `first_layer_acceleration` | 1000 | 1000 | 2000 | 500 | 500 |
| `first_layer_extrusion_width` | 0.4 | 0.56 | 0.56 | 0.45 | 0.45 |
| `first_layer_infill_speed` | 0 | 0 | 0 | 30 | 30 |
| `first_layer_solid_infill_speed` | – | – | – | 30 | 30 |
| `first_layer_speed` | 30 | 30 | 30 | 15 | 15 |
| `infill_acceleration` | 5000 | 4000 | 5000 | 5000 | 5000 |
| `infill_extrusion_width` | 0.4 | 0.44 | 0.44 | 0.45 | 0.45 |
| `infill_speed` | 125 | 125 | 200 | 160 | 160 |
| `ironing_flowrate` | 15% | 15% | 15% | 12% | 12% |
| `ironing_type` | top | top | top | topmost | topmost |
| `layer_height` | 0.1 | 0.2 | 0.2 | 0.2 | 0.3 |
| `min_skirt_length` | 20 | 20 | 10 | 10 | 10 |
| `perimeter_acceleration` | 2000 | 2000 | 4000 | 3000 | 3000 |
| `perimeter_extrusion_width` | 0.4 | 0.44 | 0.44 | 0.45 | 0.45 |
| `perimeter_speed` | 100 | 100 | 120 | 120 | 120 |
| `perimeters` | 4 | 3 | 3 | 4 | 3 |
| `raft_first_layer_density` | 90% | 90% | 90% | 95% | 95% |
| `seam_gap_distance` | 15% | 15% | 15% | 5% | 5% |
| `seam_position` | nearest | nearest | nearest | nearest | aligned |
| `skirts` | 2 | 3 | 2 | 2 | 2 |
| `small_perimeter_speed` | 40 | 40 | 80 | 40 | 40 |
| `solid_infill_extrusion_width` | 0.4 | 0.44 | 0.44 | 0.45 | 0.45 |
| `solid_infill_speed` | 120 | 120 | 120 | 60 | 60 |
| `support_material` | enforcers_only | enforcers_only | everywhere | enforcers_only | enforcers_only |
| `support_material_buildplate_only` | 0 | 0 | 1 | 0 | 0 |
| `support_material_contact_distance` | 0.15 | 0.15 | 0.1 | 0.1 | 0.15 |
| `support_material_style` | grid | grid | grid | grid | organic |
| `top_infill_extrusion_width` | 0.4 | 0.44 | 0.44 | 0.45 | 0.45 |
| `top_solid_infill_speed` | 50 | 50 | 80 | 50 | 50 |
| `top_solid_layers` | 6 | 6 | 6 | 5 | 4 |
| `top_solid_min_thickness` | 0 | 0 | 0 | 1 | 0 |
| `travel_acceleration` | 5000 | 3000 | 5000 | 5000 | 5000 |
| `travel_speed` | 300 | 300 | 500 | 300 | 300 |

A dash means the key is not set and the slicer default is used. All 0.4 profiles also share
`min_layer_height: 0.0375`, `max_layer_height: 0.3` and `support_material_extrusion_width: 0.44`.

### 0.6 nozzle

| Key | 0.20mm STRUCTURAL | 0.30mm STRUCTURAL | 0.40mm DRAFT |
|---|---|---|---|
| `bottom_solid_layers` | 4 | 3 | 3 |
| `external_perimeter_extrusion_width` | 0.62 | 0.68 | 0.68 |
| `external_perimeter_speed` | 40 | 35 | 35 |
| `infill_extrusion_width` | 0.62 | 0.68 | 0.68 |
| `infill_speed` | 140 | 100 | 80 |
| `layer_height` | 0.2 | 0.3 | 0.4 |
| `perimeter_extrusion_width` | 0.62 | 0.68 | 0.68 |
| `perimeter_speed` | 100 | 80 | 60 |
| `perimeters` | 3 | 3 | 2 |
| `small_perimeter_speed` | 40 | 35 | 35 |
| `solid_infill_extrusion_width` | 0.62 | 0.68 | 0.68 |
| `solid_infill_speed` | 80 | 60 | 50 |
| `top_infill_extrusion_width` | 0.5 | 0.55 | 0.6 |
| `top_solid_infill_speed` | 50 | 40 | 35 |
| `top_solid_layers` | 5 | 4 | 4 |

Shared by all 0.6 profiles:

| Group | Values |
|-------|--------|
| Widths | `extrusion_width`, `first_layer_extrusion_width`: 0.68 (per-feature widths in the table above), `support_material_extrusion_width`: 0.55 |
| Shells | `top_solid_min_thickness`: 0.9, `bottom_solid_min_thickness`: 0.6 |
| Layer limits | `min_layer_height`: 0.1, `max_layer_height`: 0.45 |
| First layer | `first_layer_speed`: 25, `first_layer_infill_speed`: 30, `first_layer_solid_infill_speed`: 30, `first_layer_acceleration`: 500 |
| Accelerations | `default_acceleration`: 5000, `perimeter_acceleration`: 3000, `external_perimeter_acceleration`: 1500, `infill_acceleration`: 5000, `travel_acceleration`: 5000 |
| Infill | `fill_pattern`: grid, `fill_density`: 15 % |
| Seam | `seam_position`: nearest, `seam_gap_distance`: 15 % |
| Supports | `support_material`: enforcers_only, `support_material_style`: grid, `support_material_contact_distance`: 0.2 |
| Other | `bridge_flow_ratio`: 0.8, `brim_separation`: 0.1, `skirts`: 2, `min_skirt_length`: 10, `ironing_type`: top, `ironing_flowrate`: 15 %, `raft_first_layer_density`: 90 %, `travel_speed`: 300 |

## Shared settings (`*common Micron 180*`)

### Retraction and travel

Direct drive, short retraction with a Z hop. These are print settings in PrusaSlicer 3, and filaments do
not override them.

| Key | Value | Meaning |
|-----|-------|---------|
| `retract_length` | 0.75 | mm |
| `retract_speed` / `deretract_speed` | 50 / 30 | mm/s |
| `retract_before_travel` | 3 | Only retract for travels longer than 3 mm |
| `only_retract_when_crossing_perimeters` | 1 | Skip retraction for travels inside infill |
| `retract_layer_change` | 0 | |
| `retract_lift` | 0.4 | Z hop in mm |
| `retract_lift_above` / `retract_lift_below` | 0.2 / 500 | Z range where Z hop is used |
| `retract_restart_extra` | 0 | |
| `wipe`, `retract_before_wipe` | 0, 0 % | No wipe |
| `travel_ramping_lift`, `travel_slope`, `travel_max_lift` | 0, 0, 0 | Plain vertical Z hop |

### Walls, infill, surfaces

| Key | Value | Meaning |
|-----|-------|---------|
| `perimeter_generator` | arachne | Variable-width walls |
| `extra_perimeters`, `thin_walls` | 0, 0 | |
| `external_perimeters_first` | 0 | |
| `min_bead_width`, `min_feature_size` | 85 %, 25 % | Arachne defaults |
| `top_fill_pattern` | monotonic | |
| `top_one_perimeter_type` | none | |
| `fill_angle` | 45 | |
| `infill_overlap` | 20 % | |
| `infill_anchor` / `infill_anchor_max` | 0 / 50 | No anchors |
| `infill_every_layers`, `solid_infill_every_layers` | 1, 0 | |
| `solid_infill_below_area` | 0 | Never force small areas solid |
| `gap_fill_enabled` / `gap_fill_speed` | 1 / 40 | |
| `interface_shells` | 0 | |
| `elefant_foot_compensation` | 0.1 | mm |
| `slice_closing_radius` | 0.049 | |
| `first_layer_height` | 0.2 | All nozzles |

### Bridges and overhangs

| Key | Value |
|-----|-------|
| `thick_bridges` | 1 |
| `bridge_speed` | 60 |
| `bridge_acceleration` | 3000 |
| `over_bridge_speed` | 0 (use the normal speed) |
| `overhangs` | 1 |
| `enable_dynamic_overhang_speeds` | 0 |
| `overhang_speed_0` … `_3` | 15, 15, 20, 25 (used only if dynamic overhang speeds are enabled) |

### Speeds and motion

| Key | Value | Meaning |
|-----|-------|---------|
| `max_print_speed` | 300 | Cap for automatic speeds |
| `max_volumetric_speed` | 0 | No print-level cap; the filament cap applies |
| `max_volumetric_extrusion_rate_slope_*` | 0 | |
| `solid_infill_acceleration`, `top_solid_infill_acceleration` | 0, 0 | 0 = use `default_acceleration` |
| `travel_short_distance_acceleration` | 0 | |
| `travel_speed_z` | 0 | 0 = follow `travel_speed`, capped by `machine_max_feedrate_z` |
| `first_layer_speed_over_raft`, `first_layer_acceleration_over_raft` | 30, 0 | |

### Skirt and brim

| Key | Value |
|-----|-------|
| `skirt_distance` / `skirt_height` | 3 / 1 |
| `brim_type` / `brim_width` | outer_only / 0 (brim off until you set a width) |

### Supports

| Key | Value |
|-----|-------|
| `support_material_threshold` | 30° |
| `dont_support_bridges` | 1 |
| `support_material_pattern` / `support_material_angle` | rectilinear / 0 |
| `support_material_spacing` | 1 |
| `support_material_speed` | 90 |
| `support_material_xy_spacing` | 0.6 mm |
| `support_material_with_sheath` | 0 |
| `support_material_interface_layers` | 1 |
| `support_material_bottom_interface_layers` | -1 (same as top) |
| `support_material_interface_pattern` | rectilinear |
| `support_material_interface_spacing` | 0.2 |
| `support_material_interface_speed` | 70 |
| `support_material_interface_contact_loops` | 0 |
| `support_material_bottom_contact_distance` | 0 |
| `support_material_closing_radius` | 2 |
| `support_material_enforce_layers` | 0 |
| `support_material_synchronize_layers` | 0 |
| `support_material_extruder`, `support_material_interface_extruder` | 0, 0 (current extruder) |
| `support_tree_angle` / `support_tree_angle_slow` | 40 / 25 |
| `support_tree_branch_diameter` / `_angle` / `_double_wall` | 2 / 5 / 3 |
| `support_tree_branch_distance` | 1 |
| `support_tree_tip_diameter` | 0.8 |
| `support_tree_top_rate` | 15 % |
| `raft_contact_distance` / `raft_expansion` / `raft_first_layer_expansion` | 0.1 / 1.5 / 3 |

### Output

| Key | Value | Meaning |
|-----|-------|---------|
| `gcode_label_objects` | disabled | Set to `firmware` if you use Klipper's `[exclude_object]` |
| `gcode_comments` | 0 | |
| `gcode_resolution` | 0.0125 | |
| `arc_fitting` | emit_center | Emits G2/G3. Klipper needs `[gcode_arcs]` in `printer.cfg` |
| `output_filename_format` | `{input_filename_base}_0.4n_{layer_height}mm_{printing_filament_types}_{printer_model}_{print_time}.gcode` | `0.6n` for the 0.6 nozzle |
| `default_material` | Generic PLA @Micron 180 | |

### Multi-material leftovers

`wipe_tower` (1), `wipe_tower_*`, `ooze_prevention`, `standby_temperature_delta`,
`single_extruder_multi_material_priming`, `mmu_segmented_region_max_width` and the
`*_extruder` keys are kept from the old profiles. They do nothing on a single-tool printer.

## Not carried over from PrusaSlicer 2.9

- `post_process`: the old profiles called a local `klipper_estimator` with a Moonraker URL. Add your
  own if you want accurate times in Moonraker:
  `/path/to/klipper_estimator --config_moonraker_url http://<printer-ip> post-process`
- `notes`: a personal TODO.
- `support_material_auto`: merged into the `support_material` enum (`everywhere` = automatic supports).
- Settings that were at the slicer default and that Prusa's profiles do not set either, such as fuzzy
  skin, scarf seams, ironing and spiral vase, were dropped. The slicer applies the same defaults.
