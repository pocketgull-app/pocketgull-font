# PocketGull Typography for MATLAB

The `theme_pocketgull.m` function brings **PocketGull's Louise Sloan 5:1 optotypic legibility** and **ISMP clinical character disambiguation** to MATLAB plots, telemetry monitors, and biomedical instrumentation figures.

## Installation

Add this directory to your MATLAB search path:

```matlab
addpath('path/to/pocketgull-font/distribution/matlab');
savepath;
```

Ensure the PocketGull font files from `fonts/ttf/` are installed on your operating system (or installed via Winget: `winget install PocketGull.Typeface`).

## Usage

Call `theme_pocketgull()` after creating your plot:

```matlab
% 1. Create a plot
t = 0:0.01:10;
v = sin(2*pi*0.1*t) .* exp(-0.15*t);
plot(t, v, 'LineWidth', 2, 'Color', [0.08, 0.72, 0.65]);

title('0.10 Hz Respiratory Sinus Arrhythmia Telemetry');
subtitle('Louise Sloan 5:1 optotypic clarity & ISMP character disambiguation');
xlabel('Time (seconds)');
ylabel('ECG Amplitude (mV)');

% 2. Apply PocketGull theme
theme_pocketgull();
```

### Scotopic 650nm Red Mode (Night Shift / OLED Preservation)

```matlab
theme_pocketgull('Mode', 'scotopic');
```
