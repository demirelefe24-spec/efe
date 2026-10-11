// =====================================================================
//  ERAS, BRIDGES — hidrofoil (read by kit/morph.js). Three shape morphs, one hard cut (the slam at 23.5s).
// =====================================================================
const ERA_BG = [MC.bg, MC.bg, MC.bg, MC.bg, MC.bg];
const BRIDGES = [
  // the front foil under the hull -> the big foil section
  { tc: 7.0, A: () => ({ P: foilPts(BX + 190, REST_DECK - 50 * lwAt(6.4) + 300, 120, 4 * DEG), c: MC.white }), B: () => ({ P: FOIL, c: MC.white }) },
  // the lift arrow -> the L of the equation
  { tc: 12.0, A: () => ({ P: resample(arrowPoly(L_ARROW.x, L_ARROW.y0, L_ARROW.y0 - L_ARROW.len), true, 12), c: QL }), B: () => ({ P: eqBox('L'), c: QL }) },
  // the square on 2v -> the area under the parabola
  { tc: 17.5, A: () => ({ P: resample(SQ2, true, 12), c: QV }), B: () => ({ P: PARA_AREA, c: QL }) },
];
