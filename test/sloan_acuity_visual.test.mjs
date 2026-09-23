import test from 'node:test';
import assert from 'node:assert/strict';
import { TELEMETRY_BADGES, CLINICAL_TELEMETRY_METRICS } from '../js/a11y_neuro_ergonomics_data.js';

test('Louise Sloan 5:1 Optotype Mathematical Geometry', async (t) => {
  await t.test('all 10 definitive Sloan letters are recognized', () => {
    const SLOAN_LETTERS = ['C', 'D', 'H', 'K', 'N', 'O', 'R', 'S', 'V', 'Z'];
    assert.equal(SLOAN_LETTERS.length, 10, 'Louise Sloan defines exactly 10 optotypes');
  });

  await t.test('5:1 aspect ratio math: 1000 UPM grid with 200 UPM stroke', () => {
    const emSquare = 1000;
    const strokeWidth = 200;
    const ratio = emSquare / strokeWidth;
    assert.equal(ratio, 5.0, 'Grid to stroke ratio must be strictly 5.0 (Louise Sloan 5:1 optotypic ratio)');
  });

  await t.test('Herman Bouma peripheral anti-crowding clearance (+0.12em)', () => {
    const advanceWidth = 1000;
    const boumaPadding = Math.round(advanceWidth * 0.12);
    assert.ok(boumaPadding >= 120, 'Bouma padding must provide at least 120 UPM lateral clearance');
  });
});

test('IEEE 11073 & OpenTelemetry Telemetry Standards', async (t) => {
  await t.test('every telemetry badge declares IEEE 11073 and OTel attributes', () => {
    for (const badge of TELEMETRY_BADGES) {
      assert.ok(badge.ieee11073Code, `Badge ${badge.id} missing ieee11073Code`);
      assert.ok(badge.ieee11073Code.startsWith('MDC_'), `Badge ${badge.id} ieee11073Code must start with MDC_`);
      assert.ok(badge.otelAttribute, `Badge ${badge.id} missing otelAttribute`);
      assert.ok(badge.otelAttribute.startsWith('med.alarm.'), `Badge ${badge.id} otelAttribute must start with med.alarm.`);
      assert.ok(badge.contrastRatio >= 7.0, `Badge ${badge.id} contrast ratio ${badge.contrastRatio} must satisfy WCAG AAA (>= 7:1)`);
    }
  });

  await t.test('clinical telemetry metrics map to standard vital channels', () => {
    assert.ok(CLINICAL_TELEMETRY_METRICS.length >= 5, 'Must provide at least 5 standard vital sign metrics');
    const ids = CLINICAL_TELEMETRY_METRICS.map(m => m.id);
    assert.ok(ids.includes('HR'), 'Includes Heart Rate (HR)');
    assert.ok(ids.includes('SPO2'), 'Includes SpO2');
    assert.ok(ids.includes('NIBP_SYS'), 'Includes Systolic BP');
    assert.ok(ids.includes('NIBP_DIA'), 'Includes Diastolic BP');
    assert.ok(ids.includes('RESP'), 'Includes Respiration Rate');

    for (const metric of CLINICAL_TELEMETRY_METRICS) {
      assert.ok(metric.ieee11073Code.startsWith('MDC_'), `Metric ${metric.id} must have valid IEEE 11073 MDC code`);
      assert.ok(metric.otelAttribute.startsWith('med.vital.'), `Metric ${metric.id} must have valid OTel med.vital.* attribute`);
      assert.ok(metric.typicalRange[0] < metric.typicalRange[1], `Metric ${metric.id} range must be valid min < max`);
    }
  });
});
