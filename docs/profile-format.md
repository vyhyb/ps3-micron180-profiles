# PrusaSlicer 3 profile format

PrusaSlicer 2.x used one big `.ini` bundle per vendor. PrusaSlicer 3 uses a **repository** of YAML files
instead, with conditional variants. This page explains the parts you need to understand and edit the
Micron bundle.

## Repository layout

```text
micron180-fff-offline/              # repository root (zip this folder's contents to install)
├── manifest.json                   # repository manifest: id, name, URLs
├── vendor_indices.zip              # contains <Vendor>.idx: version history + min slicer version
└── PrintersForAnts/                # one folder per vendor id
    └── 1.0.2/                      # one folder per vendor version
        ├── manifest.json           # every file in this folder with its SHA-256 hash
        ├── vendor.yaml             # vendor, printers, tools (nozzles), sheets, printer configs
        ├── preset-printer-*.yaml   # machine settings
        ├── preset-tool-*.yaml      # tool-print presets (per-tool overrides; empty here)
        ├── preset-print-*.yaml     # print (process) settings
        ├── preset-filament-*.yaml  # one file per filament
        └── assets/                 # bed model (STL), bed texture, thumbnail
```

`<Vendor>.idx` inside `vendor_indices.zip` is a plain text file:

```text
min_slic3r_version = 3.0.0-alpha0
1.0.2 Description of this version.
1.0.1 Description of the previous version.
```

The version folder, `version:` in `vendor.yaml` and the top line of the `.idx` file must all match.

## vendor.yaml

`vendor.yaml` holds several YAML documents separated by `---`, one per object:

| `kind` | Purpose | Micron example |
|--------|---------|----------------|
| `vendor` | Vendor id and name, the **feature** schema with defaults, printer families | `id: PrintersForAnts` |
| `sheet` | Print surfaces | `pei_smooth` |
| `tool` | A nozzle the printer can use, with its `condition` | `micron-0.4`, `micron-0.6` |
| `printer` | A printer model: `model`/`base_model`, feature overrides, bed assets | `micron180`, model `MICRON180` |
| `printer_config` | A ready-made configuration of a printer (default tool and sheet) shown in the wizard | `micron180-cfg` |

**Features** are typed flags declared in the `vendor` block with a default value, for example
`supports_06_nozzle`. A `printer` lists only the features that differ from the defaults. The Micron
sets `supports_04_nozzle` and `supports_06_nozzle` to `true`. Each tool checks its feature in its
condition:

```yaml
kind: tool
id: 'micron-0.6'
name: '0.6'
condition: printer.model == "MICRON180" and printer.supports_06_nozzle
features:
  nozzle_diameter:
    default: 0.6
```

## Presets: values, variants, conditions

Every preset file uses the same pattern:

```yaml
kind: print                 # printer | print | filament | tool_print
id: <unique id>             # stable id; names starting with * are abstract (never shown)
inherits: ['*parent*']      # optional, values are merged in this order
condition: <expr>           # optional, the preset only exists when this is true
values: {...}               # settings for this node
variants:                   # optional child nodes
- condition: <expr>
  id: <unique id>
  name: <shown name>        # a node with a name becomes a selectable preset
  values: {...}
  variants: [...]
```

How PrusaSlicer resolves a preset:

- Values are merged from the top down. A child's values override its parent's, and `inherits` is
  applied before the node's own values.
- A node whose `condition` is false is skipped, together with all its children.
- Every node with a `name` becomes a preset the user can pick.

Conditions are evaluated against the selected hardware:

| Expression | Example |
|------------|---------|
| `printer.model`, `printer.base_model` | `printer.model == "MICRON180"` |
| `printer.<feature>` | `printer.supports_06_nozzle` |
| `tool.nozzle_diameter`, `tool.nozzle_high_flow` | `tool.nozzle_diameter == 0.6` |
| `sheet.type` | `sheet.type == "pei_textured"` |
| Operators | `==`, `!=`, `=~ /regex/`, `!~`, `and`, `or`, `!` |

`id` values are arbitrary unique strings. Prusa uses 22-character base64 strings. Keep an id stable once
it has been published, because user presets and projects refer to it.

## Where settings live

In PrusaSlicer 3 some settings moved compared with PrusaSlicer 2.x:

- **Retraction, wipe and travel lift** (`retract_*`, `deretract_speed`, `wipe`, `travel_*`) are now
  **print** settings. Filament presets can override them.
- **`min_layer_height` / `max_layer_height`** are print settings, set per nozzle.
- **`support_material`** is now an enum, `none` / `enforcers_only` / `everywhere`. It replaces the
  old `support_material` + `support_material_auto` pair.
- Printer **`default_print`** selects the print profile that is chosen by default for each nozzle.

## Checking keys against the slicer

The slicer can export its full option schema, with types, enum values and defaults:

```sh
flatpak run --branch=beta --command=slic3r-app-launcher com.prusa3d.PrusaSlicer \
    --export-config-schema schema.json
```

Every key in `values:` must exist in that schema. A key that belongs to another section, such as a
print key in a filament preset, must list that section in its `overrides_in`. To list the profiles the
slicer actually loads for a printer configuration:

```sh
... --query-print-tool-filament-profiles --printer-profile "Micron 180 0.4" --output out.json
```
