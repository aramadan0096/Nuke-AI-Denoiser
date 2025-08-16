# Nuke AI Denoiser

A lightweight Nuke gizmo plus a native C++ binary to denoise noisy renders or plates directly in Nuke. The release package ships with a prebuilt C++ binary and the gizmo, so you can drop them into your setup and start working.

Screenshots will be added later.

---

## What’s included (Release)

The latest release includes the prebuilt C++ binary and the gizmo, arranged like this:

```
C:.
├───bin             # Prebuilt C++ binary (required at runtime)
└───gizmos          # Nuke gizmo(s) and assets
    └───imgs        # Icons / images used by the gizmo UI
```

Important: The C++ build binary is already compiled and included under bin. You do not need to build it yourself.
<img width="610" height="507" alt="Screenshot 2025-08-16 235815" src="https://github.com/user-attachments/assets/4066f4c2-4972-4cf3-9dad-39bde641c39e" />

---

## Requirements

- Nuke 12.0+ (tested on newer versions as well)
- OS compatible with the provided binary in bin
- Permission to load external binaries on your machine/pipeline

---

## Installation

Choose one of the following setups.

### Option 1 — Quick start from a release (recommended)

1. Download the latest release and extract it somewhere convenient (e.g., `C:\tools\Nuke-AI-Denoiser`).
2. Make the gizmo discoverable by Nuke:
   - EITHER copy the `gizmos/` folder into your Nuke profile directory:
     - Windows: `C:\Users\<you>\.nuke\gizmos\`
     - macOS: `/Users/<you>/.nuke/gizmos/`
     - Linux: `/home/<you>/.nuke/gizmos/`
   - OR keep the repo anywhere and add the path via your `~/.nuke/init.py`:
     ```python
     import nuke, os
     nuke.pluginAddPath('gizmos')  # If the repo lives inside ~/.nuke
     # OR explicitly:
     nuke.pluginAddPath(r'C:\path\to\Nuke-AI-Denoiser\gizmos')
     ```
   - You can also use NUKE_PATH to point to the repo root:
     - PowerShell:
       ```powershell
       $env:NUKE_PATH = "$env:NUKE_PATH;C:\path\to\Nuke-AI-Denoiser"
       ```
     - bash/zsh:
       ```bash
       export NUKE_PATH="$NUKE_PATH:/path/to/Nuke-AI-Denoiser"
       ```
3. Restart Nuke.

4. Most important step: set the binary location in the node UI
   - Create/Select the AI Denoiser node.
   - Open the “bin” tab.
   - Set “Bin Path” to the folder that contains the binary from the release, i.e. the bin directory you extracted.
     - Example (Windows):
       ```
       C:\path\to\Nuke-AI-Denoiser\bin
       ```
   - A screenshot of this step will be added later.

### Option 2 — Studio/pipeline pathing

If you maintain centralized tool repos:

- Keep the release structure intact on a network path, e.g. `//server/tools/Nuke-AI-Denoiser`.
- Add `.../gizmos` to Nuke’s plugin path via your studio’s `init.py`.
- In the gizmo’s “bin” tab, set “Bin Path” to the shared `.../bin` directory. Consider locking or templating this knob for artists if desired.

---

## How it works (Usage)

- Add the node:
  - Press Tab and type “AI Denoiser” (exact name may vary based on your menu setup).
- Connect inputs:
  - Plug your noisy Beauty render or plate into the main input.
  - If the gizmo exposes optional passes (e.g., albedo/normal), connect them for improved detail preservation.
- Point to the binary:
  - In the node’s “bin” tab, set “Bin Path” to the release’s bin folder (see Installation step 4).
- Adjust controls:
  - Start with defaults; then tweak Strength/Mix and any pass toggles.
  - Use the Mix/Blend knob to A/B between original and denoised to avoid over-smoothing.
- Render:
  - Proceed with your usual Write node. On farms, make sure the Bin Path is accessible from render machines.

Tip: For CG, auxiliary AOVs (albedo/normal) can significantly help maintain edges and textures. For live-action plates, subtle denoising blended back often yields the most natural results.

<img width="602" height="653" alt="Screenshot 2025-08-16 235827" src="https://github.com/user-attachments/assets/0fbf3d78-5502-4c2e-859c-1db93ac4761a" />

---

## Troubleshooting

- Node doesn’t appear in the Tab menu:
  - Verify `gizmos/` is on Nuke’s plugin path (print from `init.py` to confirm).
  - Ensure no typos in the path and that you restarted Nuke after changes.
- Binary not found / fails to load:
  - Confirm the “Bin Path” in the “bin” tab points to the correct bin folder from the release.
  - Check OS/architecture compatibility and that you have permission to load external binaries.
  - Ensure antivirus/security tools aren’t blocking the binary.
- Slow performance:
  - Reduce Strength or preview a smaller ROI.
  - Cache heavy upstream nodes or write temp EXRs for iteration.

---

## Roadmap

- Add screenshots:
  - Setting “Bin Path” in the “bin” tab
  - Node UI overview and before/after comparisons
- Presets / quality profiles

---

## License

Specify a license here if applicable.

---

## Acknowledgements

Thanks to the Nuke community for best practices around gizmo packaging and distribution.
