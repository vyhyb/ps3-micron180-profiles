# PrusaSlicer 3 profiles: PrintersForAnts Micron 180

An offline vendor profile repository for **PrusaSlicer 3** (alpha) for the
PrintersForAnts **Micron 180**, a small CoreXY printer running
Klipper.

It contains:

- **Printer:** Micron 180 (E3D V6, direct drive, Klipper `PRINT_START` / `PRINT_END` macros)
- **Nozzles:** 0.4 and 0.6
- **Print profiles:**
  - 0.4: 0.10mm STRUCTURAL, 0.20mm BALANCED, 0.20mm QUALITY, 0.20mm STRUCTURAL, 0.30mm STRUCTURAL
  - 0.6: 0.20mm STRUCTURAL, 0.30mm STRUCTURAL, 0.40mm DRAFT
- **Filaments:** Generic PLA, PETG, ABS, ASA and FLEX; Prusament PLA, PETG and ASA

Verified to load in PrusaSlicer 3.0.0-alpha12. The 0.4 values come from a tuned, working Micron 180; the 0.6 profiles have not been print-tested yet.

## Layout

```text
micron180-fff-offline/               # the repository (zip its contents to install)
├── manifest.json
├── vendor_indices.zip               # PrintersForAnts.idx (version history)
└── PrintersForAnts/1.0.2/
    ├── vendor.yaml                  # vendor, printer, nozzles, sheet, printer config
    ├── manifest.json                # SHA-256 of every file in this folder
    ├── preset-printer-micron.yaml
    ├── preset-print-micron.yaml
    ├── preset-tool-micron.yaml
    ├── preset-filament-*.yaml
    └── assets/                      # bed model, bed texture, thumbnail
docs/                                # how the profiles work and how to reuse them
```

## Installation

Zip the **contents** of `micron180-fff-offline/`, so that `manifest.json` is at the root of the zip.
Then add the zip as a local profile repository in PrusaSlicer 3.

The repository `manifest.json` points to `http://localhost:8000/v2/repos/printersforants`. That only
matters if you serve the repository over HTTP instead.

## Accurate print times with klipper_estimator

PrusaSlicer's time estimate does not model Klipper's motion planner exactly. For accurate times in
Mainsail, Fluidd or Moonraker, run [klipper_estimator](https://github.com/Annex-Engineering/klipper_estimator)
as a post-processing script. It reads the real limits from your printer through Moonraker and rewrites
the time estimates in the g-code.

The profiles deliberately leave this unset, because the command depends on your machine. To use it, add
it to the print profile's post-processing scripts (`post_process`):

```text
/path/to/klipper_estimator --config_moonraker_url http://<printer-ip> post-process
```

PrusaSlicer appends the g-code file path automatically. Save the result as a user preset so the
setting survives profile updates.

## Documentation

See [docs/](docs/README.md):

- [Profile format](docs/profile-format.md): how a PrusaSlicer 3 vendor bundle is built
- [Printer profile](docs/printer.md): machine settings and the Klipper macros they expect
- [Print profiles](docs/print-profiles.md): every print profile and its values
- [Filament profiles](docs/filaments.md): where the filament values come from and how to tune them
- [Adapting to your printer](docs/adapting.md): reuse this bundle for another open-source printer

## Editing

After changing any file under `PrintersForAnts/<version>/`, regenerate that folder's `manifest.json`
(the hashes). A script is in [docs/adapting.md](docs/adapting.md#5-update-hashes-and-version).

## License

[MIT](LICENSE)
