// PocketGull OpenSCAD Silkscreen and Engraving Module
// Conforms to ISMP Pin Disambiguation & High-Acuity 3D Typography

module pocketgull_label(text_str, size_mm = 2.5, depth_mm = 0.4, font_type = "PocketGull Mono:style=Bold") {
    linear_extrude(height = depth_mm, convexity = 10) {
        text(text_str, 
             size = size_mm, 
             font = font_type, 
             halign = "center", 
             valign = "center");
    }
}

// Example usage on a PCB panel or enclosure:
// difference() {
//     cube([50, 30, 2], center = true);
//     translate([0, 0, 0.8]) pocketgull_label("PIN 1: +5V  PIN 2: GND  D0: RX", size_mm = 2.0);
// }
