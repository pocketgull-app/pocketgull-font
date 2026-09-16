"""
PocketGull Math: 1-Line Matplotlib & Scientific Visualization Integration
========================================================================
Registers PocketGull Math fonts and configures publication-grade clinical
and telemetry matplotlib stylesheets.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

__version__ = "3.1.0"

_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_FONTS_DIR = os.path.abspath(os.path.join(_PACKAGE_DIR, "..", "..", "fonts", "ttf"))
_REPO_STYLES_DIR = os.path.abspath(os.path.join(_PACKAGE_DIR, "..", "matplotlib"))

def get_font_path(font_name="PocketGull-Math.ttf"):
    """Returns absolute path to specified PocketGull font."""
    bundled = os.path.join(_PACKAGE_DIR, "fonts", font_name)
    if os.path.isfile(bundled):
        return bundled
    repo_font = os.path.join(_REPO_FONTS_DIR, font_name)
    if os.path.isfile(repo_font):
        return repo_font
    user_font = os.path.join(r"c:\Users\philg\Pocketgull\pocketgull\public\fonts", font_name)
    if os.path.isfile(user_font):
        return user_font
    return None

def register_font(font_name="PocketGull-Math.ttf"):
    """Registers font into matplotlib's font manager."""
    path = get_font_path(font_name)
    if path and os.path.isfile(path):
        fm.fontManager.addfont(path)
        return True
    return False

def use(theme="dark", vector_paths=True):
    """
    1-Line Setup: Registers PocketGull Math and applies the specified style.
    
    Parameters:
    - theme: 'dark' (clinical obsidian HUD), 'light' (medical paper/journal),
             'astro' or 'astro-night' (observatory scotopic red night vision),
             'bio' or 'genomics' (bioinformatics & single-cell RNA-seq).
    - vector_paths: If True, sets svg.fonttype='path' to guarantee 100% visual
                    parity on viewers without the font installed.
    """
    register_font("PocketGull-Math.ttf")
    register_font("PocketGullMono-Regular.ttf")
    
    # Map theme aliases
    alias_map = {
        "astro": "astro-night",
        "night": "astro-night",
        "genomics": "bio",
    }
    canonical_theme = alias_map.get(theme, theme)
    style_name = f"pocketgull-{canonical_theme}.mplstyle"
    style_path = os.path.join(_PACKAGE_DIR, "styles", style_name)
    if not os.path.isfile(style_path):
        style_path = os.path.join(_REPO_STYLES_DIR, style_name)
    
    if os.path.isfile(style_path):
        plt.style.use(style_path)
    else:
        # Inline fallback configuration
        plt.rcParams['font.family'] = 'PocketGull Math'
        plt.rcParams['mathtext.fontset'] = 'custom'
        plt.rcParams['mathtext.rm'] = 'PocketGull Math'
        plt.rcParams['mathtext.it'] = 'PocketGull Math:italic'
        plt.rcParams['mathtext.bf'] = 'PocketGull Math:bold'
        if theme == 'dark':
            plt.rcParams['figure.facecolor'] = '#09090b'
            plt.rcParams['axes.facecolor'] = '#121217'
            plt.rcParams['text.color'] = '#f4f4f5'
            plt.rcParams['axes.labelcolor'] = '#a1a1aa'
            plt.rcParams['xtick.color'] = '#a1a1aa'
            plt.rcParams['ytick.color'] = '#a1a1aa'

    if vector_paths:
        plt.rcParams['svg.fonttype'] = 'path'
    
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

# Convenience aliases
use_math = use
setup_matplotlib = use
