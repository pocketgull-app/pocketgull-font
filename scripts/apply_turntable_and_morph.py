#!/usr/bin/env python3
"""
Apply Turntable Engine & Morphological Hand Models to Studio Pages
"""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def update_page(file_name):
    target_path = ROOT_DIR / file_name
    if not target_path.exists():
        print(f"File not found: {file_name}")
        return

    with open(target_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Add scripts if not present
    if 'asl_morph_svg_data.js' not in text:
        text = text.replace('<script src="js/asl_svg_data.js"></script>',
                            '<script src="js/asl_svg_data.js"></script>\n  <script src="js/asl_morph_svg_data.js"></script>\n  <script src="js/asl_turntable_engine.js"></script>')
        print(f"  [+] Added script tags to {file_name}")

    # 2. Add container if not present
    if 'id="aslTurntableContainer"' not in text:
        text = text.replace('<div class="player-bar">',
                            '<!-- 360 Adobe-Style Turntable & ROM Kinematics -->\n        <div id="aslTurntableContainer"></div>\n\n        <div class="player-bar">')
        print(f"  [+] Added turntable container to {file_name}")

    # 3. Update renderTranscriber svgContent
    old_svg_target = """        const svgContent = (typeof ASL_SVG_DATA !== 'undefined' && ASL_SVG_DATA[char])
          ? ASL_SVG_DATA[char]
          : `<div style="font-family: var(--font-sign); font-size: 52px; display: flex; align-items: center; justify-content: center; height: 100%;">${char}</div>`;"""

    new_svg_code = """        let svgContent = '';
        if (typeof ASL_MORPH_DATA !== 'undefined' && ASL_MORPH_DATA[currentHandModel] && ASL_MORPH_DATA[currentHandModel][char]) {
          svgContent = ASL_MORPH_DATA[currentHandModel][char];
        } else if (typeof ASL_SVG_DATA !== 'undefined' && ASL_SVG_DATA[char]) {
          svgContent = ASL_SVG_DATA[char];
        } else {
          svgContent = `<div style="font-family: var(--font-sign); font-size: 52px; display: flex; align-items: center; justify-content: center; height: 100%;">${char}</div>`;
        }"""

    if old_svg_target in text:
        text = text.replace(old_svg_target, new_svg_code)
        print(f"  [+] Updated svgContent in {file_name}")

    # 4. Add card click to inspect in turntable
    card_target = """        card.innerHTML = `
          ${modelBadge}
          <div class="hand-vector-wrap">${svgContent}</div>
          <div class="hand-char-label">${char}</div>
          <div class="hand-posture-desc">${data.desc}</div>
          <div class="palm-tag">${data.palm}</div>
        `;"""

    card_replacement = """        card.innerHTML = `
          ${modelBadge}
          <div class="hand-vector-wrap">${svgContent}</div>
          <div class="hand-char-label">${char}</div>
          <div class="hand-posture-desc">${data.desc}</div>
          <div class="palm-tag">${data.palm}</div>
        `;
        card.style.cursor = 'pointer';
        card.title = `Click to inspect '${char}' in 360° Turntable & ROM Inspector`;
        card.addEventListener('click', () => {
          if (typeof GLOBAL_TURNTABLE !== 'undefined' && GLOBAL_TURNTABLE) {
            GLOBAL_TURNTABLE.setChar(char);
            document.getElementById('aslTurntableContainer')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        });"""

    if card_target in text:
        text = text.replace(card_target, card_replacement)
        print(f"  [+] Added card click listener to {file_name}")

    # 5. Update updateHandModelUI to notify turntable
    model_ui_target = """    function updateHandModelUI() {
      handCardsDisplay.classList.remove('model-sloan', 'model-alimentive', 'model-thoracic', 'model-muscular', 'model-osseous', 'model-cerebral');"""

    model_ui_replacement = """    function updateHandModelUI() {
      handCardsDisplay.classList.remove('model-sloan', 'model-alimentive', 'model-thoracic', 'model-muscular', 'model-osseous', 'model-cerebral');
      if (typeof GLOBAL_TURNTABLE !== 'undefined' && GLOBAL_TURNTABLE) {
        GLOBAL_TURNTABLE.setModel(currentHandModel);
      }"""

    if model_ui_target in text:
        text = text.replace(model_ui_target, model_ui_replacement)
        print(f"  [+] Updated updateHandModelUI in {file_name}")

    # 6. Initialize turntable
    init_target = """    renderTranscriber();
    nextQuizQuestion();"""
    init_replacement = """    renderTranscriber();
    if (typeof initASLTurntable === 'function') {
      initASLTurntable('aslTurntableContainer');
    }
    nextQuizQuestion();"""

    if init_target in text:
        text = text.replace(init_target, init_replacement)
        print(f"  [+] Added initASLTurntable to {file_name}")

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Successfully processed {file_name}!")

if __name__ == "__main__":
    update_page("asl_studio.html")
    update_page("sign_studio.html")
