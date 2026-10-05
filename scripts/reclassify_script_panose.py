import os
from fontTools.ttLib import TTFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

fonts_to_cure = [
    "fonts/ttf/PocketGull-Black.ttf",
    "fonts/ttf/PocketGull-Chiseltip.ttf",
    "fonts/ttf/PocketGull-MarkerRaw.ttf"
]

def reclassify_to_script():
    print("PocketGull Typefoundry: Script/Penmanship PANOSE Reclassification")
    for f in fonts_to_cure:
        path = os.path.join(ROOT_DIR, f)
        if os.path.exists(path):
            font = TTFont(path)
            # 3 = Latin Hand Written
            font["OS/2"].panose.bFamilyType = 3
            # 4 = Felt Pen / Marker stroke type (simulated via 0-15 standard)
            font["OS/2"].panose.bSerifStyle = 0 # any
            font["OS/2"].panose.bWeight = 8 # Heavy
            font.save(path)
            print(f"  [SUCCESS] {f} updated to PANOSE Hand Written (3).")
        else:
            print(f"  [WARNING] {f} not found.")

if __name__ == "__main__":
    reclassify_to_script()
