import os
import zipfile
import xml.etree.ElementTree as ET

def build_nupkg():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vs_dir = os.path.join(base_dir, "distribution", "visual-studio")
    nuspec_file = os.path.join(vs_dir, "PocketGull.Typeface.nuspec")
    targets_file = os.path.join(vs_dir, "PocketGull.Typeface.targets")
    props_file = os.path.join(vs_dir, "PocketGull.Typeface.props")
    readme_file = os.path.join(vs_dir, "README.md")
    fonts_dir = os.path.join(base_dir, "fonts", "ttf")
    
    output_nupkg = os.path.join(vs_dir, "PocketGull.Typeface.3.1.0.nupkg")
    
    font_files = [
        "PocketGullMono-Regular.ttf",
        "PocketGullMono-Bold.ttf",
        "PocketGull-Regular.ttf",
        "PocketGull-Bold.ttf",
        "PocketGull-Fineliner.ttf",
        "PocketGull-VF.ttf"
    ]
    
    print(f"Packaging {output_nupkg}...")
    with zipfile.ZipFile(output_nupkg, "w", zipfile.ZIP_DEFLATED) as z:
        # NuSpec manifest at root
        z.write(nuspec_file, arcname="PocketGull.Typeface.nuspec")
        
        # README
        if os.path.exists(readme_file):
            z.write(readme_file, arcname="README.md")
            
        # Build targets
        z.write(targets_file, arcname="build/PocketGull.Typeface.targets")
        z.write(props_file, arcname="build/PocketGull.Typeface.props")
        
        # Content & contentFiles for Visual Studio / MSBuild
        for f in font_files:
            src = os.path.join(fonts_dir, f)
            if os.path.exists(src):
                z.write(src, arcname=f"content/fonts/{f}")
                z.write(src, arcname=f"contentFiles/any/any/fonts/{f}")
            else:
                print(f"Warning: font file {src} not found!")
                
    print(f"Successfully generated {output_nupkg} ({os.path.getsize(output_nupkg):,} bytes)")

if __name__ == "__main__":
    build_nupkg()
