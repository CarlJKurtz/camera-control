# Camera Controller (USB Microscope)
Python tool to preview and capture images from a USB microscope for typeface reference.

## Install requirements and run
```bash
pip install -r requirements.txt
python main.py
```

## Controls
- SPACE — Capture (saves raw + grid PNG)
- G — Toggle grayscale
- S — Toggle center-square crop
- ESC — Quit

## Output
Images are saved to an folder called *output.*

## Notes
- Tested on macOS. Microscope must be connected via USB.
- If an iPhone or your Mac's camera appears first, deny that device's camera permission and re-run so the USB microscope is selected.
- Readme.md was written with the help of AI