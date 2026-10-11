  // SCORE BODY — hidrofoil (inside buildScore(); see kit/score-head.js). 120 BPM, D major.
  // Thin at rest, a groove that thickens with speed, the fullest bar on the climb, a hard stop at 22.0 (silence while the
  // dot hangs under W), then the loudest hit on take-off at 23.5 and a flat, warm chord as the boat flies.
  const T = TIMELINE, cu = T.cues, SIL = cu.hush, HIT = cu.slam;
  const beats = (t0, t1, step, fn) => { for (let t = t0, i = 0; t < t1 - 1e-6; t += step, i++) fn(t, i); };
  to = 'm';
  // rest: one quiet pad
  pad(0.0, 2.05, ['D3', 'A3', 'Fs4'], 0.025, { type: 'triangle', cut: 900, att: 0.6, rel: 0.3, send: 0.4 });
  // speeding up: a pad under the groove, brighter each era
  pad(2.0, 12.05, ['D3', 'A3', 'E4', 'Fs4'], 0.028, { type: 'triangle', cut: 1100, att: 0.4, rel: 0.3, send: 0.4 });
  pad(12.0, 17.55, ['B2', 'Fs3', 'D4', 'A4'], 0.022, { type: 'triangle', cut: 1300, att: 0.3, rel: 0.3, send: 0.4 });
  pad(17.5, SIL, ['G2', 'D3', 'B3', 'Fs4'], 0.034, { type: 'sawtooth', cut: 1500, att: 0.3, rel: 0.12, send: 0 });
  // the bass: on the beat from 2.0, on 8ths from the graph (the busiest stretch)
  const root = (t) => (t < 12 ? nz('D2') : t < 17.5 ? nz('B1') : nz('G1'));
  beats(2.0, 17.5, BEAT, (t, i) => bass(t, root(t) * (i % 4 === 3 ? 1.5 : 1), 0.16));
  beats(17.5, SIL - 0.2, E8, (t, i) => bass(t, root(t) * (i % 8 === 7 ? 1.5 : 1), 0.15));
  // ticks: 8ths from the foil, 16ths on the climb (the water rushing past faster)
  beats(7.0, 17.5, E8, (t, i) => noiseHit(t, 0.03, 'highpass', 7000, 0.7, i % 2 ? 0.02 : 0.035, 0.25));
  beats(17.5, SIL - 0.15, E16, (t, i) => noiseHit(t, 0.025, 'highpass', 7500, 0.7, i % 4 === 0 ? 0.04 : 0.022, 0.25));
  // plucks: the formula's Writes, the squares, the cells, ρ
  [['D4', 0], ['Fs4', E8], ['A4', BEAT]].forEach(([n, dt], i) => pluck(cu.eq + 0.1 + dt, nz(n), 0.13, -0.2 + i * 0.2, 0.5, 2600, 0.35));
  pluck(cu.v2, nz('E5'), 0.12, 0.2, 0.4, 3000, 0.3);
  pluck(cu.sq, nz('B4'), 0.12, -0.3, 0.45, 2800, 0.3);
  ['D5', 'E5', 'Fs5', 'A5'].forEach((n, i) => pluck(cu.sq2 + 0.55 + i * E8 * 0.5, nz(n), 0.11, -0.3 + i * 0.2, 0.4, 3200, 0.3));
  pluck(cu.rho, nz('Fs5'), 0.12, 0.2, 0.5, 3000, 0.3);
  // the climb: an arpeggio that rises with the dot (dry: nothing may ring into the silence)
  const arp = ['G4', 'B4', 'D5', 'Fs5', 'A5', 'B5', 'D6', 'E6'];
  beats(cu.climb, SIL - 0.2, E8, (t, i) => pluck(t, nz(arp[Math.min(arp.length - 1, Math.floor(i / 2))]), 0.08 + i * 0.004, (i % 2 ? 0.25 : -0.25), 0.18, 3600, 0));
  // take-off: a short chord stab and a sub on the hit, then a flat, warm chord under the flight; fades by the loop
  pad(HIT, HIT + 0.45, ['D3', 'A3', 'D4', 'Fs4', 'A4'], 0.12, { type: 'sawtooth', cut: 3200, att: 0.005, rel: 0.3, send: 0.5 });
  sub(HIT, 0.6);
  noiseHit(HIT, 0.5, 'lowpass', 2400, 0.8, 0.18, 0, 0.4, 300);
  pad(HIT + 0.35, 29.9, ['D3', 'A3', 'E4', 'Fs4'], 0.042, { type: 'triangle', cut: 1400, att: 0.6, rel: 2.0, send: 0.5 });
  beats(HIT + 2 * BEAT, 27.5, BEAT, (t) => bass(t, nz('D2'), 0.09));
  chime(cu.eqLW + 0.1, [nz('D5'), nz('A5'), nz('Fs6')], 0.05);
  chime(cu.home, [nz('A4'), nz('D5'), nz('Fs5')], 0.04);
  to = 's';
  // the three morphs: a soft whoosh into each
  [T.morphs[0], T.morphs[1], T.morphs[2]].forEach((tc) => sweep(tc - 0.55, tc, 0.012, 600, 3200, 0));
  // the water: a faint hiss that grows with speed until the silence, then again in flight
  sweep(2.0, 7.0, 0.006, 300, 900, -0.2);
  for (let i = 0; i < 6; i++) blip(cu.lift + i * E16, 900 + i * 90, 1200 + i * 90, 0.03, 0.02);   // L growing
