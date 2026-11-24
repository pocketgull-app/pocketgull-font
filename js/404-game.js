const STEPS = [
  { label: '20/80', size: 132 },
  { label: '20/60', size: 108 },
  { label: '20/40', size: 84 },
  { label: '20/25', size: 62 },
  { label: '20/20', size: 48 }
];

const DIRECTIONS = [
  { key: 'right', deg: 0 },
  { key: 'down', deg: 90 },
  { key: 'left', deg: 180 },
  { key: 'up', deg: 270 }
];

let stepIdx = 0;
let currentDir = 'right';

const svgEl = document.getElementById('landolt-svg');
const readoutEl = document.getElementById('acuity-readout');
const feedbackEl = document.getElementById('acuity-feedback');
const solvedEl = document.getElementById('acuity-solved');
const resetBtn = document.getElementById('reset-acuity-btn');
const againBtn = document.getElementById('again-acuity-btn');
const dirBtns = document.querySelectorAll('.dir-btn');

function pickDirection(exclude) {
  const choices = DIRECTIONS.filter((d) => d.key !== exclude);
  return choices[Math.floor(Math.random() * choices.length)].key;
}

function render() {
  if (!svgEl || !readoutEl || !feedbackEl || !solvedEl) return;

  if (stepIdx >= STEPS.length) {
    readoutEl.textContent = '20/20 • Calibrated';
    feedbackEl.textContent = 'Optotype lens calibrated cleanly.';
    solvedEl.classList.remove('hidden');
    return;
  }

  solvedEl.classList.add('hidden');
  const step = STEPS[stepIdx];
  const dirObj = DIRECTIONS.find((d) => d.key === currentDir) ?? DIRECTIONS[0];

  svgEl.setAttribute('width', String(step.size));
  svgEl.setAttribute('height', String(step.size));
  svgEl.style.transform = `rotate(${dirObj.deg}deg)`;
  svgEl.style.transition = 'transform 0.2s ease, width 0.2s ease, height 0.2s ease';

  readoutEl.textContent = `${step.label} • Step ${stepIdx + 1} / ${STEPS.length}`;
}

function submitGuess(dirKey) {
  if (stepIdx >= STEPS.length) return;
  if (dirKey === currentDir) {
    stepIdx++;
    if (stepIdx < STEPS.length) {
      currentDir = pickDirection(currentDir);
      if (feedbackEl) feedbackEl.textContent = `✓ Clear! Advancing to ${STEPS[stepIdx].label}…`;
    }
    render();
  } else {
    if (feedbackEl) feedbackEl.textContent = 'Not quite that direction — take your time and try again.';
  }
}

function resetGame() {
  stepIdx = 0;
  currentDir = pickDirection('');
  if (feedbackEl) feedbackEl.textContent = 'Which way is the gap facing?';
  render();
}

dirBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    const dir = btn.getAttribute('data-dir');
    if (dir) submitGuess(dir);
  });
});

document.addEventListener('keydown', (e) => {
  const map = {
    ArrowUp: 'up',
    ArrowDown: 'down',
    ArrowLeft: 'left',
    ArrowRight: 'right'
  };
  const dir = map[e.key];
  if (dir) {
    e.preventDefault();
    submitGuess(dir);
  }
});

resetBtn?.addEventListener('click', resetGame);
againBtn?.addEventListener('click', resetGame);

resetGame();
