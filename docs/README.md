# Documentation

These pages describe the PrintersForAnts **Micron 180** profiles for PrusaSlicer 3. They also explain how to
reuse them as a starting point for another open-source printer, such as a Voron, a RatRig or a custom
Klipper machine.

PrusaSlicer 3 is still in alpha, and its profile format may change. Everything here was checked
against **PrusaSlicer 3.0.0-alpha12**.

| Page | What it covers |
|------|----------------|
| [Profile format](profile-format.md) | How a PrusaSlicer 3 vendor bundle is built: files, inheritance, variants, conditions |
| [Printer profile](printer.md) | The Micron 180 machine settings and the Klipper macros it expects |
| [Print profiles](print-profiles.md) | The print profiles for each nozzle, what they share and how they differ |
| [Filament profiles](filaments.md) | Where the filament values come from and what was changed for Klipper |
| [Adapting to your printer](adapting.md) | Step-by-step: turn this bundle into one for your own printer |

## Where the values come from

| Part | Source |
|------|--------|
| Printer (machine limits, g-code, bed) | The PrusaSlicer 2.9 printer profile used on a real Micron 180 (E3D V6, Klipper) |
| Print, 0.4 nozzle | Tuned PrusaSlicer 2.9 print profiles from the same machine, converted to PrusaSlicer 3 keys |
| Print, 0.6 nozzle | Prusa MINI 0.6 geometry (extrusion widths, shell thickness) combined with the Micron tuning above. Not yet print-tested |
| Filaments | Prusa Research MINI filament profiles, with Marlin-only and MMU-only settings removed |

Prusa Research's own PrusaSlicer 3 bundle was used as the reference for layout and naming, and to
check which keys are valid.
