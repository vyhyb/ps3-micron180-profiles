# PrusaSlicer 3 profiles

Offline vendor profile repository for PrusaSlicer 3, containing profiles for the
**Micron 180** printer (Klipper firmware). The profiles were converted from the
original PrusaSlicer 2.x `.ini` configs.

## Contents

```
micron180-fff-offline/
├── manifest.json          # repository manifest (id: micron, version 2)
├── vendor_indices.zip     # vendor index (Micron.idx)
└── Micron/1.0.1/
    ├── vendor.yaml
    ├── manifest.json      # file list with SHA-256 hashes
    ├── preset-printer-micron.yaml
    ├── preset-print-micron.yaml
    ├── preset-tool-micron.yaml
    ├── preset-filament-*.yaml   # PLA, PETG, ABS, ASA, FLEX (Generic + Prusament)
    └── assets/            # bed model, bed texture, thumbnail
```

## Usage

The repository manifest points to `http://localhost:8000/v2/repos/micron`.
Serve the repository locally so that PrusaSlicer can reach it at that URL, then
add it as a profile repository in PrusaSlicer.

If you edit any file under `Micron/1.0.1/`, update its hash in
`Micron/1.0.1/manifest.json`:

```sh
sha256sum micron180-fff-offline/Micron/1.0.1/<file>
```

## License

[MIT](LICENSE)
