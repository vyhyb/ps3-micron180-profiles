# Adapting the bundle to your printer

This guide turns the Micron 180 bundle into a profile repository for another single-tool Klipper
printer. The example renames everything to a fictional vendor `MyVendor` and printer `MYPRINTER`.

Before you start, read [Profile format](profile-format.md). It explains the files and how variants and
conditions work.

## 1. Copy and rename

```sh
cp -r micron180-fff-offline myprinter-fff-offline
cd myprinter-fff-offline
mv PrintersForAnts MyVendor
mv MyVendor/1.0.3 MyVendor/1.0.0        # start your own version history
```

## 2. Edit vendor.yaml

| Where | What to change |
|-------|----------------|
| `kind: vendor` | `id: MyVendor`, `name: My Vendor`, `version: 1.0.0`. Keep the `features` block as it is |
| `printer_families` | `label`, `base_model`, and the `printer_config` id |
| `kind: tool` | `id` (for example `myprinter-0.4`) and the `condition` model name. Delete tools for nozzles you don't support, or add more (see step 6) |
| `kind: printer` | `name`, `id`, `model.base_model` and `model.model` (for example `MYPRINTER`). Under `features`, set `supports_XX_nozzle: true` for each nozzle you support |
| `visual` | Your own bed STL, bed texture (PNG or SVG) and thumbnail in `assets/`. Remove lines you don't have |
| `kind: printer_config` | `id`, `name`, `printer` (the printer id), `legacy_printer_model`, the default `tool` and `sheet` |

## 3. Replace the model name and name suffix in the presets

All presets select the printer with `printer.model == "MICRON180"`, and all preset names end in
`@Micron 180`:

```sh
cd MyVendor/1.0.0
sed -i 's/"MICRON180"/"MYPRINTER"/g; s/MICRON180/MYPRINTER/g; s/@Micron 180/@MyPrinter/g; s/Micron180/MyPrinter/g' *.yaml
```

Then give every variant a **new unique `id`** so it cannot collide with the Micron bundle if both are
installed. This replaces every unquoted `id:` with a random one:

```sh
python3 - <<'EOF'
import base64, os, re, glob
for f in glob.glob("*.yaml"):
    if f == "vendor.yaml":
        continue
    s = open(f).read()
    s = re.sub(r"^(\s*)id: (?!')(.+)$",
               lambda m: f"{m.group(1)}id: {base64.b64encode(os.urandom(16)).decode().rstrip('=')}",
               s, flags=re.M)
    open(f, "w").write(s)
EOF
```

Quoted ids are left alone. These are abstract presets (`'*...*'`) and filament ids such as
`'Generic PLA MyPrinter'`, which step 3 already made unique. Never put `@` into an id
(see [Filament profiles](filaments.md)).

## 4. Change the machine and print values

Go through these in order. Everything else can stay as it is to start with.

**Printer** (`preset-printer-*.yaml`), see [Printer profile](printer.md):

| Key | Set to |
|-----|--------|
| `bed_shape` | Your printable area, for example `['0x0', '250x0', '250x250', '0x250']` |
| `max_print_height` | Your Z height |
| `start_gcode` / `end_gcode` | The name and parameters of your Klipper start/end macros. Keep the prime line inside your bed |
| `machine_max_acceleration_*`, `machine_max_feedrate_*` | Your `printer.cfg` limits. They only affect time estimates |
| `thumbnails` | Sizes your web UI or screen uses |
| `printer_notes` | Your hotend and extruder |

**Print** (`preset-print-*.yaml`), see [Print profiles](print-profiles.md):

| Key | Why |
|-----|-----|
| `retract_length`, `retract_speed`, `retract_lift` (in `*common…*`) | Direct drive: 0.5-1 mm. Bowden: 2-5 mm |
| `*_acceleration` | Match what your input shaper results allow |
| `*_speed` | Start lower than the Micron values on a larger or heavier gantry |
| `elefant_foot_compensation`, `first_layer_*` | Depend on your bed and leveling |
| `gcode_label_objects` | `firmware` if you use `[exclude_object]` |
| `arc_fitting` | `disabled` if your Klipper has no `[gcode_arcs]` |
| `default_print` (printer file) | The print profile chosen by default for each nozzle |

**Filaments**: set `filament_max_volumetric_speed` for your hotend. See [Filament profiles](filaments.md).

## 5. Update hashes and version

Each version folder has a `manifest.json` listing every file with its SHA-256 hash. Regenerate it
after **any** change:

```sh
cd MyVendor/1.0.0
python3 - <<'EOF'
import hashlib, json, os
files = sorted(os.path.relpath(os.path.join(r, f), ".")
               for r, _, fs in os.walk(".") for f in fs if f != "manifest.json")
json.dump([{"filename": f, "filehash": hashlib.sha256(open(f, "rb").read()).hexdigest()} for f in files],
          open("manifest.json", "w"))
EOF
```

Write the version index and pack it:

```sh
cd ../..                                   # repository root
cat > MyVendor.idx <<'EOF'
min_slic3r_version = 3.0.0-alpha0
1.0.0 Initial version.
EOF
rm -f vendor_indices.zip && zip vendor_indices.zip MyVendor.idx && rm MyVendor.idx
```

For later releases, copy the version folder to a new number, bump `version:` in `vendor.yaml`, add a
line at the top of the `.idx` file, and regenerate `manifest.json`.

Finally, edit the repository `manifest.json` in the root: `name`, `description`, `id`, `url` and
`index_url`.

## 6. Adding a nozzle size

Example: adding a 0.25 nozzle.

1. `vendor.yaml`: add a `kind: tool` with `id: 'myprinter-0.25'`, `name: '0.25'`,
   condition `printer.model == "MYPRINTER" and printer.supports_025_nozzle`, and
   `nozzle_diameter` default `0.25`. Set `supports_025_nozzle: true` in the printer's `features`.
2. Printer file: add a `tool.nozzle_diameter == 0.25` variant with a `default_print`.
3. Print file: add a `tool.nozzle_diameter == 0.25` variant under `'*common…*'` (layer height limits,
   file name), and a nozzle node with widths and named print profiles in the print tree. Prusa's
   `preset-print-mini.yaml` has good 0.25 / 0.8 values to start from.
4. Filaments: extend each top-level `condition` and add a `tool.nozzle_diameter == 0.25` variant.

## 7. Check and install

Validate the keys against the slicer's schema (see [Profile format](profile-format.md#checking-keys-against-the-slicer)).

To install, zip the **contents** of the repository folder, so that `manifest.json` and
`vendor_indices.zip` sit at the root of the zip. Then add the zip as a local profile repository in
PrusaSlicer 3. Check that the slicer finds your profiles:

```sh
flatpak run --branch=beta --command=slic3r-app-launcher com.prusa3d.PrusaSlicer \
    --query-print-tool-filament-profiles --printer-profile "My Printer 0.4" --output out.json
```

Then slice a calibration cube and read through the start of the g-code before you print it.
