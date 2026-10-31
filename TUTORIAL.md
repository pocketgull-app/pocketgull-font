# PocketGull Cognitive Walkthrough: 4 Levels in 3 Minutes

Welcome to **PocketGull**. If this repository feels like "everything all at once," start here.

In cognitive science, human working memory has a strict **4-item ceiling** (*Nelson Cowan, 2001*). When a page throws 39 font files, 16 variable axes, and deep binary specifications at you simultaneously, it creates **Extraneous Cognitive Load** (*John Sweller, 1988*)—exhausting your eyes and attention before you ever install a font.

This walkthrough uses **Progressive Disclosure**: **4 levels**, introducing **one cognitive & visual principle at a time**.

---

## Level 1: Pre-Attentive Vision & Zero Backward Eye Jumps (`< 200 ms`)

### The Cognitive Science
* **Saccades & Fixations**: Your eyes do not read smoothly; they jump across a line 3 to 4 times per second (**saccades**) and pause for ~200 milliseconds (**fixations**).
* **Prediction Error & Regressive Saccades (*Karl Friston*)**: When three different characters look like the exact same vertical stick (**`1`**, **`l`**, **`I`**) or oval (**`0`**, **`O`**), your visual cortex hits a *prediction error*. Your eye is forced to stop, jump backward (**regressive saccade**), and re-read from context. Under fatigue, stress, or motor tremor (ataxia), backward eye jumps cause rapid ocular strain.
* **Pre-Attentive Feature Detection (*Anne Treisman*)**: The primary visual cortex (`V1`) detects a diagonal slash, a curved hook, or a horizontal crossbar in **under 200 milliseconds**—before conscious thought.

### How PocketGull Applies It
| What You Read | Standard Fonts (Forced Guessing) | PocketGull (Pre-Attentive Pop-Out) | Cognitive & Clinical Benefit |
| :--- | :--- | :--- | :--- |
| **`500 mg`** | `0` and `O` share the same oval | **Slashed Zero (`0̸`)** | Your eye spots the diagonal slash in `< 200 ms`—preventing tenfold (`50` vs. `500`) dosage misreads. |
| **`1lI`** | Three identical vertical sticks | **Hooked `1`**, **Curved `l`**, **Serifed `I`** | Zero regressive saccades when reading biomarkers (`IL-6`), passwords, or URLs. |
| **`b / d`, `p / q`** | Exact mirror-image twins | **Asymmetric stem spurs & bowl bias** | Prevents rotational mirror flips in dyslexia and peripheral vision. |

---

## Level 2: Parafoveal Crowding & Salience Gating (`[!]`)

### The Cognitive Science
* **Bouma's Law of Visual Crowding (*Herman Bouma, 1970*)**: Outside the tiny 2-degree center of your gaze (the *fovea*), neighboring letters blur together if their inner counters are tight or their spacing is cramped. PocketGull uses a tall **540 UPM x-height**, open apertures, and **Louise Sloan 5:1 optotype proportions** so word shapes (*boumas*) stay recognizable in your peripheral vision.
* **Inattentional Blindness vs. Bottom-Up Salience**: Humans naturally cannot see 0-pixel invisible characters—which is why **Trojan Source** (`U+202E` right-to-left text flip) and **Fake Spaces** (`U+3164` Hangul Filler) fool even experienced reviewers.

### How PocketGull Applies It
Instead of expecting your brain to spot an invisible character, PocketGull converts hidden spoofing characters into a high-salience **`[!]` warning badge** (`uni202E.guard`), while keeping legitimate multilingual joiners silent:

| Character Category | What Your Eye Sees | Cognitive Effect |
| :--- | :--- | :--- |
| **Everyday Multilingual & Emoji Joiners** (`U+200C`, `U+200D`) | **Clean, invisible shaping** *(Zero clutter)* | **Zero false alarms**: Persian (*Rubáiyát*), Arabic, and family emoji (`👨‍👩‍👧`) read smoothly without visual noise. |
| **Trojan Source & Fake Spaces** (`U+202E`, `U+3164`, `U+E0100`) | **Visible `[!]` Warning Badge** | **Instant bottom-up salience**: Hidden direction flips or fake spaces pop out immediately in your fovea. |

---

## Level 3: Defeating Hick's Law (Pick 1 Font for 1 Job)

### The Cognitive Science
* **Hick–Hyman Law ($RT = a + b \log_2(n + 1)$)**: The time and mental effort required to make a decision increases with the number of choices. Opening a folder of 39 font files causes **choice paralysis**.

### How PocketGull Applies It
Ignore the full 39-file catalog until you need a specialty cut. **95% of users only ever need one of these three files**:

| Your Primary Task | Install This Single File | Why It Fits Your Brain & Screen |
| :--- | :--- | :--- |
| **1. Coding, Terminals & ICU Monitors** | [`fonts/ttf/PocketGullMono-Regular.ttf`](fonts/ttf/PocketGullMono-Regular.ttf) | Fixed **600-UPM grid** (columns never jitter when numbers tick), active `[!]` spoof guard, and built-in status icons (`⎇`, `⚿`, `▶︎`). |
| **2. Everyday Reading, Docs & EHR Notes** | [`fonts/ttf/PocketGull-Fineliner.ttf`](fonts/ttf/PocketGull-Fineliner.ttf) | Warm **25-UPM felt-marker corner radii** reduce harsh digital glare during long-form reading. |
| **3. Websites & Web Apps** | [`fonts/woff2/PocketGull-VF.woff2`](fonts/woff2/PocketGull-VF.woff2) | One single compressed Variable Font file covering every weight (`100`–`900`) with zero layout shift (`size-adjust: 108%`). |

---

## Level 4: Cognitive Offloading (Safety Baked Into the File)

### The Cognitive Science
* **Cognitive Offloading & Poka-Yoke (*Mistake-Proofing*)**: The safest system is one that requires **zero human vigilance**. When safety depends on a tired engineer remembering 15 command-line flags, human fatigue eventually wins.

### How PocketGull Applies It
Once you install a PocketGull font from Level 3, its binary safety guarantees happen automatically with zero configuration:
1. **Zero Executable Font Code (`instructionLength = 0`)**: Legacy TrueType bytecode programs (`fpgm`, `cvt `) are stripped at build time, so the font is a pure, inert geometric drawing.
2. **2-Byte Memory Alignment (`loca[i] % 2 == 0`)**: Every character outline lands on an even memory boundary so strict browsers (Chromium OTS) and 15-year-old hospital printers never fault.
3. **Optional 1-Line Check**: If you ever want to audit a project folder offline, run:
   ```powershell
   node scripts/scan-font-security.mjs .
   ```

---

### Where to Explore Next (At Your Own Pace)
* **Interactive Specimen in Your Browser**: Open [`index.html`](index.html) (including the **650nm Scotopic Night Mode** for zero rhodopsin bleaching in dark rooms).
* **What Every Glyph & Icon Means**: [Section 4 of `UNICODE_SECURITY_AND_PUA_SPECIFICATION.md`](standards/UNICODE_SECURITY_AND_PUA_SPECIFICATION.md#4-field-guide-what-pocketgull-glyphs-mean-on-your-machine--how-to-verify-font-safety).
* **For Fellow Font Creators & Hardware Engineers**: [`FOUNDRY_AND_HARDWARE_OEM_GUIDE.md`](standards/FOUNDRY_AND_HARDWARE_OEM_GUIDE.md).
