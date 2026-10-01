// Shared clickable Jeopardy-style review-game generator (Phases 13Z + 13AA).
// Draws a 16:9 PPTX with a 5x5 clickable board, question -> reveal -> board
// navigation, optional simple arrow-chain diagrams, and an optional final
// challenge slide pair. No external file dependencies.

const pptxgen = require('pptxgenjs');

const W = 13.333;
const H = 7.5;

// ---------- palette (shared product family: navy / teal / warm accent) ----------
const NAVY   = '0F1B2E';
const NAVY2  = '182741';
const PANEL  = '22314E';
const GOLD   = 'F2B233';
const GOLD_D = 'C88A1E';
const TEAL   = '2EC4B6';
const TEAL_D = '1E8C82';
const PAPER  = 'FFFFFF';
const PAPER2 = 'EEF2F7';
const INK    = '1B2A41';
const MUTED  = '5B6B84';
const GREEN  = '2F9E5B';
const GREEN2 = 'E5F4EC';

// ---------- fonts ----------
const F_TITLE = 'Cambria';
const F_BODY  = 'Arial';

// ---------- slide map ----------
const SL_TITLE = 1;
const SL_HOWTO = 2;
const SL_BOARD = 3;
const N_CAT = 5, N_VAL = 5;
// Slides are added interleaved: title(1), howto(2), board(3), then for each
// (category,value): question, answer. Optional final challenge Q/A follow.
const qSlide = (c, v) => 4 + 2 * (c * N_VAL + v);
const aSlide = (c, v) => qSlide(c, v) + 1;
const finalQSlide = () => 4 + 2 * N_CAT * N_VAL;       // 54
const finalASlide = () => finalQSlide() + 1;            // 55

// ============================================================ deck builder
function buildDeck(cfg) {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_WIDE';
  pptx.author = cfg.meta.author;
  pptx.title = cfg.meta.title;

  const T = cfg.text;
  const CATS = cfg.cats;
  const VALUES = cfg.values;
  const Q = cfg.questions;
  const ST = pptx.ShapeType;

  // ---------- helpers (close over the per-deck pptx instance) ----------
  function bg(slide, color) {
    slide.addShape(ST.rect, { x: 0, y: 0, w: W, h: H, fill: { color }, line: { type: 'none' } });
  }
  function chip(slide, { x, y, w, h, text, fill, color, size = 13, bold = true, link = null }) {
    if (link) slide.addShape(ST.roundRect, { x, y, w, h, fill: { color: fill }, line: { type: 'none' }, rectRadius: 0.5, hyperlink: { slide: link } });
    else slide.addShape(ST.roundRect, { x, y, w, h, fill: { color: fill }, line: { type: 'none' }, rectRadius: 0.5 });
    slide.addText(text, { x, y, w, h, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: size, bold, color, isTextBox: true, margin: 0, charSpacing: 1, ...(link ? { hyperlink: { slide: link } } : {}) });
  }
  function title(slide, text, { size = 40, color = GOLD, y = 0.55, h = 0.9 } = {}) {
    slide.addText(text, { x: 0.7, y, w: W - 1.4, h, align: 'left', valign: 'middle', fontFace: F_TITLE, fontSize: size, bold: true, color, isTextBox: true, margin: 0 });
  }
  function subline(slide, text, { size = 15, color = MUTED, y = 1.45, h = 0.4, align = 'left' } = {}) {
    slide.addText(text, { x: 0.7, y, w: W - 1.4, h, align, valign: 'middle', fontFace: F_BODY, fontSize: size, color, isTextBox: true, margin: 0 });
  }
  function qHeader(slide, c, v) {
    chip(slide, { x: 0.7, y: 0.45, w: 1.1, h: 0.5, text: '$' + v, fill: GOLD, color: NAVY, size: 18 });
    chip(slide, { x: 1.95, y: 0.45, w: 3.4, h: 0.5, text: CATS[c].short, fill: TEAL, color: '0B2E2A', size: 14 });
    chip(slide, { x: W - 2.3, y: 0.45, w: 1.6, h: 0.5, text: '\u25C0 Board', fill: PAPER2, color: INK, size: 13, link: SL_BOARD });
  }
  function renderDiagram(slide, diagram) {
    const boxes = diagram.boxes;
    const n = boxes.length;
    const totalW = W - 1.6;
    const arrowW = 0.5, gap = 0.1;
    const bw = (totalW - (n - 1) * (arrowW + 2 * gap)) / n;
    const y = diagram.y || 2.55;
    const h = diagram.h || 1.35;
    const x0 = 0.8;
    boxes.forEach((label, i) => {
      const x = x0 + i * (bw + arrowW + 2 * gap);
      const mystery = (label === '?');
      const long = label.length > 12;
      slide.addShape(ST.roundRect, {
        x, y, w: bw, h,
        fill: { color: mystery ? 'FFFFFF' : PAPER2 },
        line: mystery ? { color: GOLD_D, width: 1.5, dashType: 'dash' } : { color: 'D5DEE8', width: 1 },
        rectRadius: 0.1,
      });
      slide.addText(String(i + 1), { x, y: y - 0.3, w: bw, h: 0.26, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 11, bold: true, color: MUTED, isTextBox: true, margin: 0 });
      slide.addText(mystery ? '?' : label, {
        x, y, w: bw, h, align: 'center', valign: 'middle', fontFace: F_BODY,
        fontSize: mystery ? 30 : (long ? 11 : 14), bold: true,
        color: mystery ? GOLD_D : INK, isTextBox: true, margin: 0.04,
      });
      if (i < n - 1) {
        slide.addText('\u2192', { x: x + bw + gap, y, w: arrowW, h, align: 'center', valign: 'middle', fontSize: 22, color: TEAL_D, isTextBox: true, margin: 0 });
      }
    });
    if (diagram.caption) {
      slide.addText(diagram.caption, { x: 0.8, y: y + h + 0.04, w: totalW, h: 0.3, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 12, italic: true, color: MUTED, isTextBox: true, margin: 0 });
    }
  }

  // ---------- 1. Title ----------
  {
    const s = pptx.addSlide();
    bg(s, NAVY);
    s.addShape(ST.ellipse, { x: W - 2.6, y: -0.8, w: 3.0, h: 3.0, fill: { color: PANEL }, line: { color: GOLD, width: 2 } });
    s.addText(T.monogram, { x: W - 2.6, y: -0.8, w: 3.0, h: 3.0, align: 'center', valign: 'middle', fontFace: F_TITLE, fontSize: 34, bold: true, color: GOLD, isTextBox: true, margin: 0 });
    s.addShape(ST.ellipse, { x: -1.0, y: H - 2.0, w: 2.6, h: 2.6, fill: { color: PANEL }, line: { color: TEAL, width: 2 } });
    s.addText('\u26A1', { x: -1.0, y: H - 2.0, w: 2.6, h: 2.6, align: 'center', valign: 'middle', fontSize: 30, color: GOLD, isTextBox: true, margin: 0 });

    chip(s, { x: 0.7, y: 1.15, w: 2.3, h: 0.5, text: T.kicker, fill: PANEL, color: TEAL, size: 14 });
    s.addText(T.bigTitle, { x: 0.65, y: 1.8, w: W - 1.3, h: 1.3, align: 'left', valign: 'middle', fontFace: F_TITLE, fontSize: 76, bold: true, color: GOLD, isTextBox: true, margin: 0, charSpacing: 2 });
    s.addText(T.subtitle, { x: 0.7, y: 3.15, w: W - 1.4, h: 0.7, align: 'left', valign: 'middle', fontFace: F_BODY, fontSize: 28, color: PAPER, isTextBox: true, margin: 0 });
    s.addText(T.subsub, { x: 0.7, y: 3.85, w: W - 1.4, h: 0.5, align: 'left', valign: 'middle', fontFace: F_BODY, fontSize: 16, color: MUTED, isTextBox: true, margin: 0 });

    chip(s, { x: 0.7, y: 4.85, w: 2.9, h: 0.75, text: '\u25B6 START GAME', fill: GOLD, color: NAVY, size: 20, link: SL_BOARD });
    chip(s, { x: 3.8, y: 4.85, w: 2.9, h: 0.75, text: 'How to Play', fill: PANEL, color: PAPER, size: 18, link: SL_HOWTO });

    const cw = 2.3, gap = 0.18, total = 5 * cw + 4 * gap, x0 = (W - total) / 2;
    CATS.forEach((c, i) => {
      const x = x0 + i * (cw + gap);
      s.addShape(ST.roundRect, { x, y: 6.15, w: cw, h: 0.7, fill: { color: NAVY2 }, line: { color: PANEL, width: 1 }, rectRadius: 0.14 });
      s.addText(c.short, { x, y: 6.15, w: cw, h: 0.7, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 13, bold: true, color: TEAL, isTextBox: true, margin: 0 });
    });
  }

  // ---------- 2. How to Play ----------
  {
    const s = pptx.addSlide();
    bg(s, NAVY);
    title(s, T.howtoTitle);
    T.howtoSteps.forEach((t, i) => {
      const y = 1.7 + i * 0.72;
      s.addShape(ST.ellipse, { x: 0.9, y: y + 0.05, w: 0.42, h: 0.42, fill: { color: GOLD }, line: { type: 'none' } });
      s.addText(String(i + 1), { x: 0.9, y: y + 0.05, w: 0.42, h: 0.42, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 15, bold: true, color: NAVY, isTextBox: true, margin: 0 });
      s.addText(t, { x: 1.55, y, w: W - 3.1, h: 0.62, align: 'left', valign: 'middle', fontFace: F_BODY, fontSize: 21, color: PAPER, isTextBox: true, margin: 0 });
    });
    chip(s, { x: 0.7, y: 6.35, w: 2.9, h: 0.7, text: '\u25B6 START GAME', fill: GOLD, color: NAVY, size: 20, link: SL_BOARD });
    chip(s, { x: 3.8, y: 6.35, w: 2.9, h: 0.7, text: 'Back to Title', fill: PANEL, color: PAPER, size: 16, link: SL_TITLE });
  }

  // ---------- 3. Board ----------
  {
    const s = pptx.addSlide();
    bg(s, NAVY);
    title(s, T.boardTitle, { size: 36, y: 0.4, h: 0.8 });
    subline(s, T.boardSubline, { size: 14, y: 1.15, h: 0.35, align: 'center' });

    const margin = 0.5;
    const bw = W - margin * 2;
    const gapX = 0.18, gapY = 0.14;
    const colW = (bw - 4 * gapX) / 5;
    const headY = 1.7, headH = 0.68;
    const rowY = headY + headH + 0.16, rowH = 0.82;

    CATS.forEach((c, i) => {
      const x = margin + i * (colW + gapX);
      s.addShape(ST.roundRect, { x, y: headY, w: colW, h: headH, fill: { color: TEAL }, line: { type: 'none' }, rectRadius: 0.1 });
      s.addText(c.short, { x, y: headY, w: colW, h: headH, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 15, bold: true, color: '0B2E2A', isTextBox: true, margin: 0.05 });
    });
    for (let v = 0; v < N_VAL; v++) {
      for (let c = 0; c < N_CAT; c++) {
        const x = margin + c * (colW + gapX);
        const y = rowY + v * (rowH + gapY);
        const link = qSlide(c, v);
        const fill = (v % 2 === 0) ? GOLD : 'E8B13F';
        s.addShape(ST.roundRect, { x, y, w: colW, h: rowH, fill: { color: fill }, line: { color: GOLD_D, width: 1 }, rectRadius: 0.1, hyperlink: { slide: link } });
        s.addText('$' + VALUES[v], { x, y, w: colW, h: rowH, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 24, bold: true, color: NAVY, isTextBox: true, margin: 0, hyperlink: { slide: link } });
      }
    }
    if (cfg.finalChallenge) {
      chip(s, { x: (W - 4.2) / 2, y: rowY + N_VAL * (rowH + gapY) + 0.06, w: 4.2, h: 0.5, text: '\u2605 FINAL CHALLENGE', fill: TEAL, color: '0B2E2A', size: 16, link: finalQSlide() });
    }
    s.addText(T.boardFooter, { x: 0, y: H - 0.45, w: W, h: 0.35, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 11, color: MUTED, isTextBox: true, margin: 0 });
  }

  // ---------- question + answer slides ----------
  for (let c = 0; c < N_CAT; c++) {
    for (let v = 0; v < N_VAL; v++) {
      const item = Q[c][v];
      const qs = qSlide(c, v);
      const as = aSlide(c, v);

      // ----- QUESTION SLIDE -----
      {
        const s = pptx.addSlide();
        bg(s, PAPER);
        qHeader(s, c, v);
        s.addText(CATS[c].tag + ' \u00B7 $' + item.v, { x: 0.7, y: 1.0, w: 6, h: 0.35, align: 'left', valign: 'middle', fontFace: F_BODY, fontSize: 12, bold: true, color: MUTED, isTextBox: true, margin: 0 });

        const visual = !!item.diagram;
        if (item.type === 'MC') {
          if (visual) {
            s.addText(item.q, { x: 0.7, y: 1.4, w: W - 1.4, h: 0.75, align: 'left', valign: 'middle', fontFace: F_BODY, fontSize: 21, bold: true, color: INK, isTextBox: true, margin: 0, lineSpacingMultiple: 1.02 });
            renderDiagram(s, Object.assign({ y: 2.5, h: 1.1 }, item.diagram));
            const letters = ['A', 'B', 'C', 'D'];
            const oy = 4.05, oh = 0.52, og = 0.08;
            item.opts.forEach((op, i) => {
              const y = oy + i * (oh + og);
              s.addShape(ST.roundRect, { x: 0.7, y, w: W - 1.4, h: oh, fill: { color: PAPER2 }, line: { color: 'D5DEE8', width: 1 }, rectRadius: 0.08 });
              s.addText([{ text: letters[i] + '.  ', options: { bold: true, color: TEAL_D } }, { text: op, options: { color: INK } }],
                { x: 0.95, y, w: W - 1.9, h: oh, align: 'left', valign: 'middle', fontFace: F_BODY, fontSize: 16, isTextBox: true, margin: 0 });
            });
            chip(s, { x: (W - 3.4) / 2, y: 6.5, w: 3.4, h: 0.62, text: T.revealBtn, fill: GOLD, color: NAVY, size: 20, link: as });
          } else {
            s.addText(item.q, { x: 0.7, y: 1.45, w: W - 1.4, h: 1.35, align: 'left', valign: 'top', fontFace: F_BODY, fontSize: 26, bold: true, color: INK, isTextBox: true, margin: 0, lineSpacingMultiple: 1.05 });
            const letters = ['A', 'B', 'C', 'D'];
            const oy = 2.95, oh = 0.66, og = 0.13;
            item.opts.forEach((op, i) => {
              const y = oy + i * (oh + og);
              s.addShape(ST.roundRect, { x: 0.7, y, w: W - 1.4, h: oh, fill: { color: PAPER2 }, line: { color: 'D5DEE8', width: 1 }, rectRadius: 0.08 });
              s.addText([{ text: letters[i] + '.  ', options: { bold: true, color: TEAL_D } }, { text: op, options: { color: INK } }],
                { x: 0.95, y, w: W - 1.9, h: oh, align: 'left', valign: 'middle', fontFace: F_BODY, fontSize: 18, isTextBox: true, margin: 0 });
            });
            chip(s, { x: (W - 3.4) / 2, y: 6.55, w: 3.4, h: 0.7, text: T.revealBtn, fill: GOLD, color: NAVY, size: 20, link: as });
          }
        } else {
          if (visual) {
            s.addText(item.q, { x: 0.7, y: 1.5, w: W - 1.4, h: 1.8, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 26, bold: true, color: INK, isTextBox: true, margin: 0, lineSpacingMultiple: 1.06 });
            renderDiagram(s, Object.assign({ y: 3.65, h: 1.15 }, item.diagram));
          } else {
            s.addText(item.q, { x: 0.7, y: 1.7, w: W - 1.4, h: 2.2, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 28, bold: true, color: INK, isTextBox: true, margin: 0, lineSpacingMultiple: 1.08 });
            chip(s, { x: (W - 3.6) / 2, y: 4.15, w: 3.6, h: 0.6, text: 'TEAM CHALLENGE', fill: TEAL, color: '0B2E2A', size: 15 });
          }
          chip(s, { x: (W - 3.4) / 2, y: 6.55, w: 3.4, h: 0.7, text: T.revealBtn, fill: GOLD, color: NAVY, size: 20, link: as });
        }
      }

      // ----- ANSWER SLIDE -----
      {
        const s = pptx.addSlide();
        bg(s, PAPER);
        qHeader(s, c, v);
        s.addText(CATS[c].tag + ' \u00B7 $' + item.v + ' \u00B7 ANSWER', { x: 0.7, y: 1.0, w: 6, h: 0.35, align: 'left', valign: 'middle', fontFace: F_BODY, fontSize: 12, bold: true, color: GREEN, isTextBox: true, margin: 0 });

        s.addShape(ST.roundRect, { x: 0.7, y: 1.55, w: W - 1.4, h: 2.6, fill: { color: GREEN2 }, line: { color: 'BFE3CF', width: 1.5 }, rectRadius: 0.12 });

        let ansLine;
        if (item.type === 'MC') {
          const letters = ['A', 'B', 'C', 'D'];
          ansLine = letters[item.ans] + ' \u2014 ' + item.opts[item.ans];
        } else {
          ansLine = item.ansText;
        }
        s.addText([{ text: 'Correct answer\n', options: { bold: true, color: GREEN, fontSize: 15, breakLine: true } },
                   { text: ansLine, options: { bold: true, color: INK, fontSize: 26 } }],
          { x: 1.05, y: 1.75, w: W - 2.1, h: 2.2, align: 'left', valign: 'middle', fontFace: F_BODY, isTextBox: true, margin: 0, lineSpacingMultiple: 1.06 });

        s.addText([{ text: 'Why: ', options: { bold: true, color: MUTED } }, { text: item.explain, options: { color: MUTED } }],
          { x: 0.7, y: 4.4, w: W - 1.4, h: 0.9, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 16, italic: true, isTextBox: true, margin: 0, lineSpacingMultiple: 1.05 });

        chip(s, { x: (W - 3.4) / 2, y: 5.9, w: 3.4, h: 0.7, text: T.backBtn, fill: GOLD, color: NAVY, size: 18, link: SL_BOARD });
        chip(s, { x: (W - 3.4) / 2, y: 6.72, w: 3.4, h: 0.55, text: T.clueAgain, fill: PAPER2, color: INK, size: 14, link: qs });
      }
    }
  }

  // ---------- optional final challenge ----------
  if (cfg.finalChallenge) {
    const fc = cfg.finalChallenge;
    {
      const s = pptx.addSlide();
      bg(s, PAPER);
      chip(s, { x: 0.7, y: 0.45, w: 1.6, h: 0.5, text: 'FINAL', fill: GOLD, color: NAVY, size: 16 });
      chip(s, { x: 2.45, y: 0.45, w: 3.4, h: 0.5, text: fc.tag, fill: TEAL, color: '0B2E2A', size: 14 });
      chip(s, { x: W - 2.3, y: 0.45, w: 1.6, h: 0.5, text: '\u25C0 Board', fill: PAPER2, color: INK, size: 13, link: SL_BOARD });
      s.addText(fc.q, { x: 0.7, y: 1.35, w: W - 1.4, h: 2.6, align: 'left', valign: 'middle', fontFace: F_BODY, fontSize: 26, bold: true, color: INK, isTextBox: true, margin: 0, lineSpacingMultiple: 1.1 });
      if (fc.promptLines) {
        s.addText(fc.promptLines.map((l) => ({ text: l + '\n', options: { color: MUTED } })),
          { x: 0.7, y: 4.0, w: W - 1.4, h: 1.6, align: 'left', valign: 'top', fontFace: F_BODY, fontSize: 16, italic: true, isTextBox: true, margin: 0, lineSpacingMultiple: 1.15 });
      }
      chip(s, { x: (W - 3.4) / 2, y: 6.55, w: 3.4, h: 0.7, text: T.revealBtn, fill: GOLD, color: NAVY, size: 20, link: finalASlide() });
    }
    {
      const s = pptx.addSlide();
      bg(s, PAPER);
      chip(s, { x: 0.7, y: 0.45, w: 1.6, h: 0.5, text: 'FINAL', fill: GOLD, color: NAVY, size: 16 });
      chip(s, { x: 2.45, y: 0.45, w: 3.4, h: 0.5, text: fc.tag, fill: TEAL, color: '0B2E2A', size: 14 });
      chip(s, { x: W - 2.3, y: 0.45, w: 1.6, h: 0.5, text: '\u25C0 Board', fill: PAPER2, color: INK, size: 13, link: SL_BOARD });
      s.addShape(ST.roundRect, { x: 0.7, y: 1.35, w: W - 1.4, h: 3.1, fill: { color: GREEN2 }, line: { color: 'BFE3CF', width: 1.5 }, rectRadius: 0.12 });
      s.addText([{ text: 'Best answer\n', options: { bold: true, color: GREEN, fontSize: 15, breakLine: true } },
                 { text: fc.ansText, options: { bold: true, color: INK, fontSize: 24 } }],
        { x: 1.05, y: 1.55, w: W - 2.1, h: 2.7, align: 'left', valign: 'middle', fontFace: F_BODY, isTextBox: true, margin: 0, lineSpacingMultiple: 1.08 });
      s.addText([{ text: 'Why: ', options: { bold: true, color: MUTED } }, { text: fc.explain, options: { color: MUTED } }],
        { x: 0.7, y: 4.65, w: W - 1.4, h: 0.9, align: 'center', valign: 'middle', fontFace: F_BODY, fontSize: 16, italic: true, isTextBox: true, margin: 0, lineSpacingMultiple: 1.05 });
      chip(s, { x: (W - 3.4) / 2, y: 5.95, w: 3.4, h: 0.7, text: T.backBtn, fill: GOLD, color: NAVY, size: 18, link: SL_BOARD });
    }
  }

  pptx.writeFile({ fileName: cfg.outPath })
    .then(f => console.log('WROTE', f))
    .catch(e => { console.error('ERROR', e); process.exit(1); });
}

module.exports = { buildDeck, qSlide, aSlide, finalQSlide, finalASlide, N_CAT, N_VAL, SL_TITLE, SL_HOWTO, SL_BOARD };
