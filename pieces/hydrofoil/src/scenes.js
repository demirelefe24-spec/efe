// =====================================================================
//  SCENES — hidrofoil. World coordinates 1080x1920; TT on 1s. One slow push in era 1 is the only camera move.
//  Colour code: L green, W red, v blue, D orange, ρ teal, S purple, C_L gold; yellow = the moment L = W.
// =====================================================================
const QL = MC.green, QW = MC.red, QV = MC.blue, QD = MC.orange, QR = MC.teal, QSA = MC.purple, QCL = MC.gold, QY = MC.yellow;

// ---- the tracker: q = v / v₁ (v₁ = take-off speed). Everything that grows with speed reads it; L/W = q² until take-off.
const Q_KEYS = [[0, 0], [1.5, 0], [7.0, 0.6], [12.0, 0.72], [17.5, 0.8], [19.4, 0.8], [22.0, 0.98], [23.49, 0.98], [23.5, 1.0], [26.5, 1.15], [30, 1.15]];
const qAt = (t = TT) => keysM(Q_KEYS, t);
const flying = (t = TT) => t >= TIMELINE.cues.slam - 1e-6;
const lwAt = (t = TT) => (flying(t) ? 1 : qAt(t) ** 2);
// distance the water has travelled past the boat (px), integrated on the frame grid so it is a pure function of TT
function flowAt(t = TT, px = 520) { let s = 0; const n = Math.round(t * FPS); for (let i = 0; i < n; i++) s += qAt(i / FPS) / FPS; return s * px; }

// ---- the counter at the top, in every era: L/W = q² (the honest value at 2 places)
// drawn after the camera (DEFER), so the push-in never zooms it off the frame; o.then(lay) runs after it is drawn
function counter(p = 1, o = {}) {
  const f = () => {
    const lw = lwAt(), done = flying();
    const toks = [mv('L', QL), mn('/'), mv('W', QW), '=', mn(done ? '1.00' : lw.toFixed(2), done ? QY : MC.white, { id: 'value' })];
    const lay = writeTex(toks, CX, 420, 84, p, { alpha: o.alpha ?? 1 });
    if (o.then) o.then(lay);
  };
  if (DEFER) DEFER.push(f); else f();
}
// a caption that is on screen between t0 and t1 (mathCard on a BackgroundRectangle, Written on at t0)
function capT(segs, t0, t1 = 1e9) {
  const f = () => { if (TT >= t0 && TT < t1) mathCard(segs, CX, 1440, 50, runS(t0, 0.9)); };
  if (DEFER) DEFER.push(f); else f();
}

// ---- the stage: the water line and the boat (eras 0 and 4 share the framing exactly)
const WL = 1060;                // the still water line
const BX = 480;                 // the boat's centre x
const REST_DECK = WL - 70;      // deck height at rest (the hull sits 80px deep)
const LIFT_Y = 210;             // how far the boat rises when it flies
// a cambered foil section (NACA-like, 12% thick, 4% camber). Leading edge at +x (the boat runs to the right), nose up by aoa.
function foilPts(cx, cy, chord, aoa = 0, n = 40) {
  const up = [], lo = [];
  for (let i = 0; i <= n; i++) {
    const b = Math.PI * i / n, x = (1 - Math.cos(b)) / 2;   // cosine spacing: dense at both edges
    const yt = 0.6 * (0.2969 * Math.sqrt(x) - 0.126 * x - 0.3516 * x * x + 0.2843 * x ** 3 - 0.1036 * x ** 4);
    const yc = x < 0.4 ? 0.04 / 0.16 * (0.8 * x - x * x) : 0.04 / 0.36 * (0.2 + 0.8 * x - x * x);
    up.push([x, yc + yt]); lo.push([x, yc - yt]);
  }
  const P = [...up, ...lo.reverse().slice(1, -1)];
  const ca = Math.cos(aoa), sa = Math.sin(aoa);
  // x = 0 is the leading edge: map it to the right end; y up is screen up
  return P.map(([x, y]) => { const lx = (0.5 - x) * chord, ly = -y * chord; return [cx + lx * ca + ly * sa, cy - lx * sa + ly * ca]; });
}
function waterSurface(ph, al = 1) {
  ctx.save(); ctx.globalAlpha = 0.14 * al; ctx.fillStyle = MC.blueE; ctx.fillRect(0, WL, W, H - WL); ctx.restore();
  const P = []; for (let x = -20; x <= W + 20; x += 12) P.push([x, WL + 5 * Math.sin((x + ph) / 46) + 3 * Math.sin((x + ph * 1.3) / 19)]);
  showCreation(P, 1, { c: MC.blueD, w: 3, al: 0.8 * al });
  // depth ticks along the left edge (quiet, true: 50px apart)
  for (let k = 1; k <= 6; k++) segLine(70, WL + k * 50, 86, WL + k * 50, MC.greyD, 2);
}
// streaks the water leaves behind (they drift left with the flow); n per row, rows at depths dy
function wake(ph, q, rows, al = 1) {
  if (q <= 0.02) return;
  rows.forEach(([dy, len], r) => {
    for (let i = 0; i < 7; i++) {
      const x = mod(i * 190 + r * 73 - ph * (1 + r * 0.15), W + 240) - 120, l = len * clamp(q * 1.6);
      segLine(x, WL + dy, x + l, WL + dy, MC.blueD, 2.5, 1, 0.55 * al);
    }
  });
}
// the boat: deck at (bx, deckY). Returns key points (foils, CG) for arrows and bridges.
function drawBoat(bx, deckY, o = {}) {
  const hull = [[-280, 0], [330, 0], [300, 52], [215, 128], [190, 140], [-262, 140], [-280, 120]].map(([x, y]) => [bx + x, deckY + y]);
  const cabin = [[-240, 0], [-240, -80], [-100, -80], [-70, 0]].map(([x, y]) => [bx + x, deckY + y]);
  const fF = [bx + 190, deckY + 300], fR = [bx - 210, deckY + 300];   // the two foils, under their struts
  // struts and foils (drawn first: the hull covers the strut tops)
  segLine(fF[0], deckY + 130, fF[0], fF[1], MC.grey, 7); segLine(fR[0], deckY + 130, fR[0], fR[1], MC.grey, 7);
  const FF = foilPts(fF[0], fF[1], 120, 4 * DEG), FR = foilPts(fR[0], fR[1], 150, 4 * DEG);
  for (const P of [FF, FR]) { ctx.save(); polyPath(P); ctx.fillStyle = MC.greyD; ctx.fill(); ctx.strokeStyle = MC.white; ctx.lineWidth = 3.5; ctx.stroke(); ctx.restore(); }
  ctx.save(); polyPath(hull); ctx.fillStyle = MC.bg; ctx.fill(); ctx.globalAlpha = 0.07; ctx.fillStyle = MC.white; ctx.fill();
  ctx.globalAlpha = 1; ctx.strokeStyle = MC.white; ctx.lineWidth = 5; ctx.lineJoin = 'round'; ctx.stroke(); ctx.restore();
  showCreation(cabin, 1, { c: MC.grey, w: 4 });
  segLine(bx - 215, deckY - 52, bx - 125, deckY - 52, MC.greyC, 3);   // the window line
  segLine(bx - 270, deckY + 30, bx + 300, deckY + 30, MC.greyD, 2);   // a rub rail
  return { fF, fR, FF, FR, cg: [bx - 10, deckY + 70], hull };
}
// free-body arrows: W down from the CG, L up at each foil (lengths in px: W = 200, each L = 100·L/W), D back from the stern
function forces(k, o = {}) {
  const lw = o.lw ?? lwAt(), p = o.p ?? 1;
  mArrow(k.cg[0], k.cg[1], k.cg[0], k.cg[1] + 200, QW, 6, p);
  writeTex([mv('W', QW)], k.cg[0] + 36, k.cg[1] + 190, 48, p, { align: 'left' });
  if (lw > 0.01) for (const f of [k.fF, k.fR]) mArrow(f[0] + 34, f[1] - 4, f[0] + 34, f[1] - 4 - 100 * lw, QL, 6, p);
  if (lw > 0.08) writeTex([mv('L', QL)], k.fF[0] + 58, k.fF[1] - 30 - 50 * lw, 48, p, { align: 'left' });
  const dl = o.dl ?? 0;
  if (dl > 4) { const [x, y] = o.dAt; mArrow(x, y, x - dl, y, QD, 6, p); writeTex([mv('D', QD)], x - dl / 2, y - 18, 48, p); }
}

// ---- era 0: the boat at rest, then speeding up; the hull ploughs and the drag grows
function sceneBoat() {
  const cu = TIMELINE.cues, q = qAt(), lw = lwAt(), ph = flowAt();
  fillAll(MC.bg);
  waterSurface(ph);
  const deck = REST_DECK - 50 * lw;   // as the foils take weight the hull sits a little higher (L < W: still in the water)
  const k = drawBoat(BX, deck);
  wake(ph, q, [[26, 70], [70, 50], [130, 36]]);
  // a bow wave: the hull pushing water aside grows with speed
  const bw = 40 * clamp(q * 1.4);
  if (bw > 1) showCreation([[BX + 300, WL + 2], [BX + 320 + bw * 0.6, WL - bw * 0.7], [BX + 345 + bw, WL + 2]], 1, { c: MC.blueD, w: 3 });
  forces(k, { p: runS(0.3, 0.8), dl: (30 + 100 * lw) * runS(cu.drag, 0.6), dAt: [BX - 285, WL + 40] });
  piHero(BX + 70, deck, 0.7, { key: 'pi', look: TT < cu.drag ? [CX, 420] : [BX - 330, WL + 40], mood: q > 0.45 ? 'wow' : 'calm' });
  counter(runS(0.0, 0.8));
  mathTag('hidrofoil');
  capT('Tekne hızlanıyor', 0.35, cu.drag + 0.5);
  capT('Gövde suyu itiyor', cu.drag + 0.5);
}
function pieceCam(era, t) {
  if (era === 0) { const ff = [BX + 190, REST_DECK - 50 * lwAt(6.4) + 300]; return push(t, TIMELINE.cues.push, 6.4, { z: 2.5, p: ff, to: [CX, 960] }); }
  return null;
}

// ---- era 1: the foil section, close up. The flow bends over it and leaves pointing down; L grows up.
const FC = [CX, 960], FCH = 640, FAOA = 6 * DEG;
const FOIL = foilPts(FC[0], FC[1], FCH, FAOA);
const L_ARROW = { x: CX + 20, y0: 930, len: 300 };
// a fat arrow outline (the bridge shape for L)
function arrowPoly(x, y0, y1, sw = 13, hw = 34, hl = 70) { return [[x - sw, y0], [x + sw, y0], [x + sw, y1 + hl], [x + hw, y1 + hl], [x, y1], [x - hw, y1 + hl], [x - sw, y1 + hl]]; }
// one streamline at offset d from the foil's centre line; lp = how developed the lift (and the downwash) is
function streamPts(d, lp) {
  const P = [], A = 46 * Math.exp(-Math.abs(d) / 200), Dn = 70 * Math.exp(-Math.abs(d) / 300) * lp, sg = (z) => 1 / (1 + Math.exp(-z));
  for (let x = 60; x <= 1020; x += 12) {
    const u = (x - FC[0]) / (FCH / 2);
    const bump = d < 0 ? -A * Math.exp(-((u * 0.9) ** 2)) : 0.4 * A * Math.exp(-(u * u));
    const down = Dn * sg((-u - 0.6) * 3) * (1 + Math.max(0, -u - 1) * 0.8) - 0.35 * Dn * sg((u - 0.6) * 3);
    P.push([x, FC[1] + d + bump + down]);
  }
  return P;
}
function sceneFoil() {
  const cu = TIMELINE.cues, lp = runS(cu.lift, 1.2), ph = flowAt();
  fillAll(MC.bg);
  const A = axes2({ at: FC, u: 100, x: [-4.6, 4.6], y: [-4, 4], p: 0 });
  numberPlane(A, { p: 1, al: 0.5, step: 1, sub: 2 });
  // the streamlines: drawn on from upstream (the right), dashes drifting left with the water
  const sp = runS(cu.flow, 1.0);
  [-280, -210, -140, -70, 70, 140, 210, 280].forEach((d, i) => {
    const P = streamPts(d, lp), Q = subPath([...P].reverse(), lagged(sp, i % 4, 4, 0.4));
    if (Q.length < 2) return;
    ctx.save(); ctx.strokeStyle = QV; ctx.globalAlpha = 0.6; ctx.lineWidth = 3.5; ctx.lineCap = 'round';
    ctx.setLineDash([30, 22]); ctx.lineDashOffset = -ph * 0.9;
    ctx.beginPath(); Q.forEach(([x, y], j) => (j ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.stroke(); ctx.restore();
  });
  // the foil and its angle of attack (chord line vs the flow)
  ctx.save(); polyPath(FOIL); ctx.fillStyle = MC.greyD; ctx.fill(); ctx.strokeStyle = MC.white; ctx.lineWidth = 5; ctx.lineJoin = 'round'; ctx.stroke(); ctx.restore();
  const le = [FC[0] + FCH / 2 * Math.cos(FAOA), FC[1] - FCH / 2 * Math.sin(FAOA)], ap = runS(cu.flow + 0.4, 0.8);
  ctx.save(); ctx.setLineDash([10, 9]);
  segLine(le[0], le[1], le[0] + 110, le[1], MC.greyC, 2.5, ap);
  segLine(le[0], le[1], le[0] + 110 * Math.cos(FAOA), le[1] - 110 * Math.sin(FAOA), MC.greyC, 2.5, ap);
  ctx.restore();
  angleArc(le[0], le[1], 95, 0, -FAOA, MC.greyC, ap, 3);
  writeTex([mv('α', MC.greyC)], le[0] + 70, le[1] - 26, 36, ap);
  // L: water pushed down, the foil pushed up
  if (lp > 0) mArrow(L_ARROW.x, L_ARROW.y0, L_ARROW.x, L_ARROW.y0 - L_ARROW.len, QL, 9, lp);
  writeTex([mv('L', QL)], L_ARROW.x + 40, L_ARROW.y0 - L_ARROW.len + 40, 64, runS(cu.lift + 0.6, 0.6), { align: 'left' });
  const dp = runS(cu.down, 0.8);
  [[200, 1090], [270, 1150]].forEach(([x, y], i) => mArrow(x + 60, y - 30, x, y, QV, 5, lagged(dp, i, 2)));
  piHero(860, 1400, 0.85, { key: 'pi', look: TT < cu.lift ? FC : [L_ARROW.x, L_ARROW.y0 - L_ARROW.len], mood: TT > cu.lift + 0.8 ? 'wow' : 'calm' });
  counter();
  mathTag('foil kesiti');
  capT('Foil suyu aşağı iter', cu.flow, cu.down);
  capT('Su da foili yukarı iter', cu.down);
}

// ---- era 2: the lift equation; v² as an area: twice the speed, four times the lift
const EQ = [mv('L', QL, { id: 'L' }), '=', { frac: [[mn('1')], [mn('2')]], id: 'half' }, mv('ρ', QR, { id: 'rho' }), mv('v', QV, { sup: '2', id: 'v' }), mv('S', QSA, { id: 'S' }), mv('C', QCL, { sub: 'L', id: 'C' })];
const EQ_Y = 650, EQ_SIZE = 110;
function eqBox(id, pad = 14) {
  const L = texLayout(EQ, EQ_SIZE), x0 = CX - L.w / 2, its = L.items.filter((g) => g.id === id);
  const a = Math.min(...its.map((g) => g.x)) + x0 - pad, b = Math.max(...its.map((g) => g.x + g.w)) + x0 + pad;
  const t = EQ_Y - EQ_SIZE * 0.78 - pad, u = EQ_Y + EQ_SIZE * 0.12 + pad;
  return resample([[a, t], [b, t], [b, u], [a, u]], true, 12);
}
const SQ1 = [[150, 960], [290, 960], [290, 1100], [150, 1100]], SQ2 = [[480, 820], [760, 820], [760, 1100], [480, 1100]];
function sceneFormula() {
  const cu = TIMELINE.cues;
  fillAll(MC.bg);
  counter();
  const lay = writeTex(EQ, CX, EQ_Y, EQ_SIZE, runS(cu.eq, 1.0), {
    dim: {},
  });
  // the legend under it, quiet
  writeText([{ s: 'ρ', c: QR, it: true }, { s: ' yoğunluk    ', c: MC.greyC }, { s: 'v', c: QV, it: true }, { s: ' hız    ', c: MC.greyC }, { s: 'S', c: QSA, it: true }, { s: ' foil alanı', c: MC.greyC }], CX, 770, 40, runS(cu.eq + 0.7, 0.8));
  // Indicate v² (and later ρ): a there-and-back scale on the term, redrawn on top
  const ind = (id, t0) => { const b = texBox(lay, id), u = (TT - t0) / 0.6; if (!b || u <= 0 || u >= 1) return; const k = indicateS(u, 0.3); ctx.save(); ctx.translate(b.cx, b.cy); ctx.scale(k, k); ctx.translate(-b.cx, -b.cy); ctx.fillStyle = MC.bg; ctx.fillRect(b.x0 - 4, b.y0 - 4, b.x1 - b.x0 + 8, b.y1 - b.y0 + 8); ctx.restore(); ctx.save(); ctx.translate(b.cx, b.cy); ctx.scale(k, k); ctx.translate(-b.cx, -b.cy); lay.items.filter((g) => g.id === id).forEach((g) => { ctx.font = fontM(g.size, { it: g.it }); ctx.fillStyle = g.c; ctx.fillText(g.ch, g.x, g.y); }); ctx.restore(); };
  ind('v', cu.v2); ind('rho', cu.rho);
  // v² as an area: the square on v holds one L; the square on 2v holds four
  const s1 = runS(cu.sq, 0.8), s2 = runS(cu.sq2, 0.9);
  showCreation(SQ1, s1, { c: QV, w: 5, closed: true, fill: 0.16, fillC: QL });
  writeTex([mv('L', QL)], 220, 1052, 60, runS(cu.sq + 0.4, 0.5));
  writeTex([mv('v', QV)], 220, 1160, 54, runS(cu.sq + 0.3, 0.5));
  mArrow(320, 1030, 440, 1030, MC.grey, 4, runS(cu.sq2 - 0.25, 0.5));
  showCreation(SQ2, s2, { c: QV, w: 5, closed: true, fill: 0.16, fillC: QL });
  cellGrid(SQ2, 2, QL, 0.6 * runS(cu.sq2 + 0.4, 0.4), 2.5);
  const cl = runS(cu.sq2 + 0.55, 0.8);
  [[550, 911], [690, 911], [550, 1051], [690, 1051]].forEach(([x, y], i) => writeTex([mv('L', QL)], x, y, 60, lagged(cl, i, 4, 0.5)));
  writeTex([mn('2', MC.white), mv('v', QV)], 620, 1165, 54, runS(cu.sq2 + 0.3, 0.5));
  // ρ: water against air
  writeTex([mv('ρ', QR, { sub: 'su' }), '≈', mn('800'), { sp: 0.1 }, mv('ρ', QR, { sub: 'hava' })], CX, 1290, 64, runS(cu.rho + 0.1, 0.9));
  piHero(860, 1400, 0.85, { key: 'pi', look: TT < cu.sq ? [CX, EQ_Y] : TT < cu.rho ? [620, 960] : [CX, 1270], mood: TT > cu.sq2 + 0.8 && TT < cu.rho ? 'wow' : 'calm' });
  mathTag('kaldırma kuvveti');
  capT('Hız iki katı → kaldırma dört katı', cu.eq + 0.2, cu.rho);
  capT('Su, havadan ~800 kat yoğun', cu.rho);
}

// ---- era 3: the L–v graph. L/W = (v/v₁)²: the parabola climbs to the W line at v = v₁.
const GO = [170, 1250], GUX = 560, GUY = 500, GX1 = 1.17;
const gTo = (x, y) => [GO[0] + x * GUX, GO[1] - y * GUY];
const PARA_AREA = (() => { const P = [gTo(0, 0)]; for (let i = 0; i <= 40; i++) { const x = GX1 * i / 40; P.push(gTo(x, x * x)); } P.push(gTo(GX1, 0)); return resample(P, true, 14); })();
function sceneGraph() {
  const cu = TIMELINE.cues, q = qAt(), lw = q * q;
  fillAll(MC.bg);
  counter();
  const A = axes2({ at: GO, ux: GUX, uy: GUY, x: [0, 1.25], y: [0, 1.4], p: 0 });
  numberPlane(A, { p: runS(17.5, 1.0), al: 0.6, step: 0.5, sub: 2 });
  axes2({ at: GO, ux: GUX, uy: GUY, x: [0, 1.25], y: [0, 1.4], ext: 0.08, p: runS(cu.axes, 0.8), step: 0.5, tick: 9 });
  const lb = runS(cu.axes + 0.5, 0.5);
  writeTex([mv('v', QV)], gTo(1.33, 0)[0], GO[1] - 24, 48, lb);
  writeTex([mv('v', QV, { sub: '1' })], gTo(1, 0)[0], GO[1] + 50, 40, lb);
  writeTex([mv('L', QL), mn('/'), mv('W', QW)], GO[0] + 26, gTo(0, 1.45)[1] + 10, 44, lb, { align: 'left' });
  // the parabola (what the square became) and the weight line
  graphM(A, (x) => x * x, 0, GX1, runS(cu.curve, 0.9), { c: QL, w: 6, area: 0.14 });
  ctx.save(); ctx.setLineDash([16, 12]);
  segLine(gTo(0, 1)[0], gTo(0, 1)[1], gTo(1.25, 1)[0], gTo(1.25, 1)[1], QW, 4, runS(cu.wline, 0.7));
  ctx.restore();
  writeTex([mn('1', MC.grey)], GO[0] - 22, gTo(0, 1)[1] + 12, 36, runS(cu.wline, 0.6), { align: 'right' });
  writeTex([mv('W', QW)], gTo(1.25, 1)[0] - 6, gTo(1.25, 1)[1] - 22, 48, runS(cu.wline + 0.3, 0.6));
  // the dot rides the curve with the tracker
  const dp = runS(cu.climb - 0.3, 0.4);
  if (dp > 0) { const [x, y] = gTo(q, lw); dropLines(A, q, lw, { y: true, al: 0.6 * dp }); trackDot(x, y, QL, { al: dp, r: 13 }); }
  const P = gTo(q, lw), hush = TT >= cu.hush;
  piHero(860, 1400, 0.85, { key: 'pi', look: TT < cu.climb ? gTo(0.6, 0.36) : P, mood: hush ? 'wow' : 'calm' });
  mathTag('L – v');
  capT([{ s: 'L', c: QL, it: true }, { s: ', ' }, { s: 'v', c: QV, it: true }, { s: '² ile büyür' }], 17.95, cu.hush);
  capT([{ s: 'L', c: QL, it: true }, { s: ' = ' }, { s: 'W', c: QW, it: true }, { s: ' olunca…' }], cu.hush + 0.1);
}

// ---- era 4: L = W. The hull jumps clear; only the foils stay in the water. The opening frame, changed.
function sceneFly() {
  const cu = TIMELINE.cues, q = qAt(), ph = flowAt(), lw0 = qAt(cu.slam - 0.02) ** 2;
  fillAll(MC.bg);
  waterSurface(ph);
  const rise = springMove(cu.slam, 50 * lw0, LIFT_Y, SPRING.snappy), deck = REST_DECK - rise;
  const k = drawBoat(BX, deck);
  // where the struts cut the surface: two small V wakes; deeper streaks at foil depth
  for (const f of [k.fF, k.fR]) showCreation([[f[0] - 30, WL - 2], [f[0], WL + 6], [f[0] + 24, WL - 8]], 1, { c: MC.blueD, w: 3 });
  wake(ph, q, [[18, 46], [k.fF[1] - WL + 30, 60]], 0.9);
  const dl = springMove(cu.slam, 30 + 100 * lw0, 40, SPRING.smooth);
  forces(k, { lw: 1, dl, dAt: [k.fR[0] - 40, k.fR[1] + 10] });
  piHero(BX + 70, deck, 0.7, { key: 'pi', look: TT < cu.eqLW ? [CX, 420] : [BX + 300, WL], mood: 'happy', hop: (TT - cu.slam) / 0.5 });
  counter(1, { then: (lay) => { const vb = texBox(lay, 'value'); if (vb) flashAt(vb.cx, vb.cy, (TT - cu.slam) / 0.45, MC.yellowP, 46, 5); } });
  const ep = runS(cu.eqLW, 0.9);
  writeTex([mv('L', QL), '=', mv('W', QW)], CX, 560, 90, ep);
  segLine(CX - 110, 586, CX + 110, 586, QY, 4, runS(cu.eqLW + 0.6, 0.6));
  mathTag('hidrofoil');
  capT('Gövde sudan çıkar', cu.slam + 0.45, cu.eqLW + 0.6);
  capT('Direnç düşer', cu.eqLW + 0.6, cu.home);
  capT('Kanat suda, gövde havada', cu.home);
}
