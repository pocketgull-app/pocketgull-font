import os
import zipfile

def build_lambda_layer():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    aws_dir = os.path.join(base_dir, "distribution", "aws")
    fonts_dir = os.path.join(base_dir, "fonts", "ttf")
    output_zip = os.path.join(aws_dir, "pocketgull-lambda-fonts.zip")

    font_files = [
        "PocketGull-Regular.ttf",
        "PocketGull-Bold.ttf",
        "PocketGull-Fineliner.ttf",
        "PocketGullMono-Regular.ttf",
        "PocketGullMono-Bold.ttf",
        "PocketGull-Math.ttf",
        "PocketGull-VF.ttf"
    ]

    fonts_conf = """<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>/opt/fonts</dir>
  <cachedir>/tmp/fonts-cache</cachedir>
  <config></config>
</fontconfig>
"""

    print(f"Creating AWS Lambda Layer archive: {output_zip}...")
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        # Fontconfig configuration for AWS Lambda /opt mount
        z.writestr("fontconfig/fonts.conf", fonts_conf)

        # OFL License
        ofl_path = os.path.join(base_dir, "OFL.txt")
        if os.path.exists(ofl_path):
            z.write(ofl_path, arcname="OFL.txt")

        # Fonts placed into /fonts/ so Lambda mounts them to /opt/fonts/
        for f in font_files:
            src = os.path.join(fonts_dir, f)
            if os.path.exists(src):
                z.write(src, arcname=f"fonts/{f}")
                print(f"  + Added fonts/{f}")

    size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print(f"Generated {output_zip} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    build_lambda_layer()
