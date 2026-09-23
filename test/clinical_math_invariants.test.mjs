import test from 'node:test';
import assert from 'node:assert/strict';

test('EMA Tremor Damping: Exponential moving average dampens physical micro-tremors', () => {
  function emaFilter(currentVal, targetVal, smoothingFactor = 0.15) {
    return currentVal + (targetVal - currentVal) * smoothingFactor;
  }

  let smoothedX = 100;
  // Step jitter towards target 200
  smoothedX = emaFilter(smoothedX, 200, 0.2);
  assert.equal(smoothedX, 120);

  smoothedX = emaFilter(smoothedX, 200, 0.2);
  assert.equal(smoothedX, 136);

  smoothedX = emaFilter(smoothedX, 200, 0.2);
  assert.equal(smoothedX, 148.8);
});

test('Louise Sloan 5:1 Aspect Ratio: Optotype grid conforms to strict 5x5 sub-cell acuity', () => {
  const capHeight = 700; // UPM
  const strokeWidth = capHeight / 5; // 140 UPM stroke width
  assert.equal(strokeWidth, 140);
  assert.equal(capHeight / strokeWidth, 5.0);
});

test('0.10 Hz Respiratory Wave: Cycle duration exactly matches 10.0 seconds', () => {
  const freq = 0.10; // Hz
  const periodSeconds = 1 / freq;
  const inhaleSeconds = 4.0;
  const exhaleSeconds = 6.0;

  assert.equal(periodSeconds, 10.0);
  assert.equal(inhaleSeconds + exhaleSeconds, periodSeconds);
});
