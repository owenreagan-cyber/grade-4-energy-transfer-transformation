// Phase 13Z — Unit 1 clickable Jeopardy-style review game deck.
// Builds a 16:9 PPTX with a fully clickable game board (5 categories x 5 values),
// question slides linking to answer/reveal slides, and "Back to Board" returns.
// No external file dependencies: everything is drawn with native shapes + text.

const pptxgen = require('pptxgenjs');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5 in, 16:9
pptx.author = 'Grade 4 Science';
pptx.title = 'Energy Detective — Unit 1 Review Game';

const W = 13.333;
const H = 7.5;

// ---------- palette ----------
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
// Slides are added in interleaved order: title(1), howto(2), board(3),
// then for each (category,value): question, answer, question, answer, ...
// so a question's number = 4 + 2*(c*N_VAL + v), and its answer = question + 1.
const qSlide = (c, v) => 4 + 2 * (c * N_VAL + v);
const aSlide = (c, v) => qSlide(c, v) + 1;

// ---------- categories ----------
const CATS = [
  { short: 'Energy & Change',      full: 'Energy Causes Change',        tag: 'CASE 1' },
  { short: 'Need for Speed',       full: 'Speed & Energy of Motion',    tag: 'CASE 2' },
  { short: 'Transfer or Transform',full: 'Transfer or Transformation',  tag: 'CASE 3' },
  { short: 'Collision Course',     full: 'Collisions',                  tag: 'CASE 4' },
  { short: "Edison's Lab",         full: 'Engineering & Edison/Latimer',tag: 'CASE 5' },
];

const VALUES = [100, 200, 300, 400, 500];

// ---------- questions ----------
// type: 'MC' (options + ans index) | 'TEAM' (ansText accepted answer)
// explain: short reasoning line shown on the answer slide
const Q = [
  // CASE 1 — Energy Causes Change
  [
    { v:100, type:'MC', q:'Energy is the ability to ____.',
      opts:['disappear quietly','cause a change','stay exactly the same','become invisible'],
      ans:1, explain:'Energy is the ability to cause change.' },
    { v:200, type:'MC', q:'A light turns on and a fan starts to spin. How do we know energy was involved?',
      opts:['We can see energy itself moving','Energy is only involved when something makes a sound','The objects changed on their own','We observe the changes and use them as evidence'],
      ans:3, explain:'A change we observe is our evidence that energy was involved.' },
    { v:300, type:'TEAM', q:'What is evidence? Give one example from class.',
      ansText:'Something we observe that helps us explain what happened. Example: the light turned on (a change I saw).',
      explain:'Observation helps us explain; the change is the evidence.' },
    { v:400, type:'TEAM', q:'Energy itself cannot be seen. How do scientists know it is involved?',
      ansText:'They observe changes and use the changes as evidence.',
      explain:'We can\u2019t see energy, but we can see the changes it causes.' },
    { v:500, type:'MC', q:'A battery, a stretched rubber band, and a ball held up high all have what in common?',
      opts:['They are all moving fast','They all have stored energy that can cause a change later','They all make sound right away','They have no energy'],
      ans:1, explain:'Stored energy can cause a change later.' },
  ],
  // CASE 2 — Speed & Energy of Motion
  [
    { v:100, type:'TEAM', q:'The energy an object has while it is moving is called ____.',
      ansText:'energy of motion',
      explain:'A moving object has energy of motion.' },
    { v:200, type:'MC', q:'A car drives slowly through a parking lot and then fast on the highway. When does the car have more energy of motion?',
      opts:['When it is moving fast','When it is moving slowly','It is the same the whole time','It has none on the highway'],
      ans:0, explain:'For the SAME object, faster motion means more energy of motion.' },
    { v:300, type:'TEAM', q:'For the SAME object, what does faster speed mean for its energy of motion?',
      ansText:'More energy of motion (it can cause a bigger change).',
      explain:'Same object, faster speed \u2192 greater change \u2192 more energy of motion.' },
    { v:400, type:'MC', q:'The same ball rolls down a low ramp and a high ramp. On which ramp will the ball most likely have more energy of motion at the bottom?',
      opts:['The high ramp, because the ball moves faster','The low ramp, because it is closer to the ground','Both ramps, because it is the same ball','Neither ramp, because ramp height does not matter'],
      ans:0, explain:'A higher ramp makes the ball move faster at the bottom.' },
    { v:500, type:'TEAM', q:'In Ramp It Up!, you measured how far the cup moved. What did you INFER from that measurement?',
      ansText:'The same ball moving faster has more energy of motion (a greater change means more energy).',
      explain:'We measure the change and infer the energy of motion.' },
  ],
  // CASE 3 — Transfer or Transformation
  [
    { v:100, type:'TEAM', q:'Energy moving from place to place or object to object is called ____.',
      ansText:'energy transfer',
      explain:'Transfer = energy moves.' },
    { v:200, type:'TEAM', q:'Energy changing from one form to another is called ____.',
      ansText:'energy transformation',
      explain:'Transformation = energy changes form.' },
    { v:300, type:'MC', q:'Warm water warms a cooler cup. The heat moves, but it stays heat. This is ____.',
      opts:['transfer only','transformation only','neither','both'],
      ans:0, explain:'The heat moves but does not change form, so it is transfer only.' },
    { v:400, type:'MC', q:'A flashlight changes stored energy in the battery into light, and energy also moves through the wires to the bulb. Which is happening?',
      opts:['transfer only','transformation only','neither','both transfer and transformation'],
      ans:3, explain:'The form changes AND the energy moves, so it is both.' },
    { v:500, type:'TEAM', q:'A tapped cup makes a sound, and a paper strip across the room moves even though nothing touched it. What does the moving paper show?',
      ansText:'That sound transferred energy (the receiver changed).',
      explain:'The paper changed, which shows energy reached it \u2014 transfer.' },
  ],
  // CASE 4 — Collision Course
  [
    { v:100, type:'TEAM', q:'What is a collision?',
      ansText:'Two objects coming together with impact.',
      explain:'A collision is two objects hitting with impact.' },
    { v:200, type:'MC', q:'A moving marble hits a still marble, and the still marble rolls away. What happened?',
      opts:['The still marble made its own energy','The moving marble\u2019s energy disappeared','Energy of motion transferred to the still marble','No energy was involved'],
      ans:2, explain:'The moving marble\u2019s energy of motion transferred to the still marble.' },
    { v:300, type:'TEAM', q:'After a crash, the cars stop. Did the energy disappear? Explain.',
      ansText:'No. Energy transferred to the target, and some became sound.',
      explain:'Energy does not disappear in a collision.' },
    { v:400, type:'MC', q:'A rolling car hits a target and stops; the target moves. What does this change tell us?',
      opts:['The energy disappeared','Energy of motion transferred from the car to the target','The target made its own energy','No energy was involved'],
      ans:1, explain:'Energy of motion transferred from the car to the target.' },
    { v:500, type:'TEAM', q:'In Crash Lab, the SAME car from a higher ramp moved the target farther. What does this show?',
      ansText:'A faster car has more energy of motion (a greater change).',
      explain:'Greater change is evidence of more energy of motion.' },
  ],
  // CASE 5 — Edison's Lab
  [
    { v:100, type:'TEAM', q:'The things a good design must do are called ____.',
      ansText:'criteria',
      explain:'Criteria are what a good design must do.' },
    { v:200, type:'TEAM', q:'The limits on materials, time, and safety are called ____.',
      ansText:'constraints',
      explain:'Constraints are the limits on a design.' },
    { v:300, type:'MC', q:'An engineer builds a design, tests it, and it does not work well. What should they do next?',
      opts:['Give up, because the design is useless','Ignore the result and keep the design the same','Remove the result from the notebook','Use the test result as evidence to improve and test again'],
      ans:3, explain:'Test results \u2014 even failures \u2014 are useful evidence to improve.' },
    { v:400, type:'MC', q:'Which sentence about Thomas Edison is true?',
      opts:['He invented the very first light bulb','He worked completely alone and never tested ideas','His bulb never needed to be improved by anyone else','He improved earlier light bulb designs and tested many materials'],
      ans:3, explain:'Edison improved earlier designs and tested many materials.' },
    { v:500, type:'TEAM', q:'How did Lewis Latimer improve the light bulb?',
      ansText:'He made a stronger, more durable filament (and improved the wire-to-filament connection).',
      explain:'Latimer\u2019s filament was stronger and lasted longer.' },
  ],
];

// ============================================================ helpers
function bg(slide, color) {
  slide.addShape(pptx.ShapeType.rect, { x:0, y:0, w:W, h:H, fill:{ color }, line:{ type:'none' } });
}

function chip(slide, { x, y, w, h, text, fill, color, size=13, bold=true, link=null }) {
  if (link) slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, fill:{ color:fill }, line:{ type:'none' }, rectRadius:0.5, hyperlink:{ slide:link } });
  else slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, fill:{ color:fill }, line:{ type:'none' }, rectRadius:0.5 });
  slide.addText(text, { x, y, w, h, align:'center', valign:'middle', fontFace:F_BODY, fontSize:size, bold, color, isTextBox:true, margin:0, charSpacing:1, ...(link ? { hyperlink:{ slide:link } } : {}) });
}

function title(slide, text, { size=40, color=GOLD, y=0.55, h=0.9 } = {}) {
  slide.addText(text, { x:0.7, y, w:W-1.4, h, align:'left', valign:'middle', fontFace:F_TITLE, fontSize:size, bold:true, color, isTextBox:true, margin:0 });
}

function subline(slide, text, { size=15, color=MUTED, y=1.45, h=0.4, align='left' } = {}) {
  slide.addText(text, { x:0.7, y, w:W-1.4, h, align, valign:'middle', fontFace:F_BODY, fontSize:size, color, isTextBox:true, margin:0 });
}

// light-slide header: value chip + category chip (left) + board pill (right)
function qHeader(slide, c, v) {
  chip(slide, { x:0.7, y:0.45, w:1.1, h:0.5, text:'$'+v, fill:GOLD, color:NAVY, size:18 });
  chip(slide, { x:1.95, y:0.45, w:3.4, h:0.5, text:CATS[c].short, fill:TEAL, color:'0B2E2A', size:14 });
  chip(slide, { x:W-2.3, y:0.45, w:1.6, h:0.5, text:'\u25C0 Board', fill:PAPER2, color:INK, size:13, link:SL_BOARD });
}

// ============================================================ slides
// ---- 1. Title ----
(() => {
  const s = pptx.addSlide();
  bg(s, NAVY);
  // decorative corner seal
  s.addShape(pptx.ShapeType.ellipse, { x:W-2.6, y:-0.8, w:3.0, h:3.0, fill:{ color:PANEL }, line:{ color:GOLD, width:2 } });
  s.addText('ED', { x:W-2.6, y:-0.8, w:3.0, h:3.0, align:'center', valign:'middle', fontFace:F_TITLE, fontSize:34, bold:true, color:GOLD, isTextBox:true, margin:0 });
  s.addShape(pptx.ShapeType.ellipse, { x:-1.0, y:H-2.0, w:2.6, h:2.6, fill:{ color:PANEL }, line:{ color:TEAL, width:2 } });
  s.addText('\u26A1', { x:-1.0, y:H-2.0, w:2.6, h:2.6, align:'center', valign:'middle', fontSize:30, color:GOLD, isTextBox:true, margin:0 });

  chip(s, { x:0.7, y:1.15, w:2.3, h:0.5, text:'UNIT 1 REVIEW', fill:PANEL, color:TEAL, size:14 });
  s.addText('ENERGY DETECTIVE', { x:0.65, y:1.8, w:W-1.3, h:1.3, align:'left', valign:'middle', fontFace:F_TITLE, fontSize:76, bold:true, color:GOLD, isTextBox:true, margin:0, charSpacing:2 });
  s.addText('Crack the Vault \u00B7 A Jeopardy-Style Review Game', { x:0.7, y:3.15, w:W-1.4, h:0.7, align:'left', valign:'middle', fontFace:F_BODY, fontSize:28, color:PAPER, isTextBox:true, margin:0 });
  s.addText('Energy Transfer & Transformation \u00B7 5 cases \u00B7 25 clues \u00B7 30 minutes', { x:0.7, y:3.85, w:W-1.4, h:0.5, align:'left', valign:'middle', fontFace:F_BODY, fontSize:16, color:MUTED, isTextBox:true, margin:0 });

  chip(s, { x:0.7, y:4.85, w:2.9, h:0.75, text:'\u25B6 START GAME', fill:GOLD, color:NAVY, size:20, link:SL_BOARD });
  chip(s, { x:3.8, y:4.85, w:2.9, h:0.75, text:'How to Play', fill:PANEL, color:PAPER, size:18, link:SL_HOWTO });

  // category preview row
  const cw = 2.3, gap = 0.18, total = 5*cw + 4*gap, x0 = (W-total)/2;
  CATS.forEach((c,i) => {
    const x = x0 + i*(cw+gap);
    s.addShape(pptx.ShapeType.roundRect, { x, y:6.15, w:cw, h:0.7, fill:{ color:NAVY2 }, line:{ color:PANEL, width:1 }, rectRadius:0.14 });
    s.addText(c.short, { x, y:6.15, w:cw, h:0.7, align:'center', valign:'middle', fontFace:F_BODY, fontSize:13, bold:true, color:TEAL, isTextBox:true, margin:0 });
  });
})();

// ---- 2. How to Play ----
(() => {
  const s = pptx.addSlide();
  bg(s, NAVY);
  title(s, 'How to Play');
  const steps = [
    '1.  Split into teams and open the game board.',
    '2.  Choose a category and a dollar value, then click the tile.',
    '3.  Read the clue together and discuss your answer.',
    '4.  Click \u201CReveal Answer\u201D to check the correct answer.',
    '5.  Click \u201C\u25C0 Board\u201D to return and pick the next tile.',
    '6.  Track points and unlock a digit on your squad scorecard.',
  ];
  steps.forEach((t,i) => {
    const y = 1.7 + i*0.72;
    s.addShape(pptx.ShapeType.ellipse, { x:0.9, y:y+0.05, w:0.42, h:0.42, fill:{ color:GOLD }, line:{ type:'none' } });
    s.addText(String(i+1), { x:0.9, y:y+0.05, w:0.42, h:0.42, align:'center', valign:'middle', fontFace:F_BODY, fontSize:15, bold:true, color:NAVY, isTextBox:true, margin:0 });
    s.addText(t, { x:1.55, y, w:W-3.1, h:0.62, align:'left', valign:'middle', fontFace:F_BODY, fontSize:21, color:PAPER, isTextBox:true, margin:0 });
  });
  chip(s, { x:0.7, y:6.35, w:2.9, h:0.7, text:'\u25B6 START GAME', fill:GOLD, color:NAVY, size:20, link:SL_BOARD });
  chip(s, { x:3.8, y:6.35, w:2.9, h:0.7, text:'Back to Title', fill:PANEL, color:PAPER, size:16, link:SL_TITLE });
})();

// ---- 3. Board ----
(() => {
  const s = pptx.addSlide();
  bg(s, NAVY);
  title(s, 'The Case Board', { size:36, y:0.4, h:0.8 });
  subline(s, 'Click any tile to open the clue.', { size:14, y:1.15, h:0.35, align:'center' });

  const margin = 0.5;
  const bw = W - margin*2;          // 12.333
  const gapX = 0.18, gapY = 0.14;
  const colW = (bw - 4*gapX)/5;
  const headY = 1.7, headH = 0.68;
  const rowY = headY + headH + 0.16, rowH = 0.82;

  // header tiles
  CATS.forEach((c,i) => {
    const x = margin + i*(colW+gapX);
    s.addShape(pptx.ShapeType.roundRect, { x, y:headY, w:colW, h:headH, fill:{ color:TEAL }, line:{ type:'none' }, rectRadius:0.1 });
    s.addText(c.short, { x, y:headY, w:colW, h:headH, align:'center', valign:'middle', fontFace:F_BODY, fontSize:15, bold:true, color:'0B2E2A', isTextBox:true, margin:0.05 });
  });
  // value tiles
  for (let v=0; v<N_VAL; v++) {
    for (let c=0; c<N_CAT; c++) {
      const x = margin + c*(colW+gapX);
      const y = rowY + v*(rowH+gapY);
      const link = qSlide(c,v);
      const fill = (v % 2 === 0) ? GOLD : 'E8B13F';
      s.addShape(pptx.ShapeType.roundRect, { x, y, w:colW, h:rowH, fill:{ color:fill }, line:{ color:GOLD_D, width:1 }, rectRadius:0.1, hyperlink:{ slide:link } });
      s.addText('$'+VALUES[v], { x, y, w:colW, h:rowH, align:'center', valign:'middle', fontFace:F_BODY, fontSize:24, bold:true, color:NAVY, isTextBox:true, margin:0, hyperlink:{ slide:link } });
    }
  }
  s.addText('30-minute class game \u00B7 Unit 1 review \u00B7 no external files', { x:0, y:H-0.45, w:W, h:0.35, align:'center', valign:'middle', fontFace:F_BODY, fontSize:11, color:MUTED, isTextBox:true, margin:0 });
})();

// ---- question + answer slides ----
for (let c=0; c<N_CAT; c++) {
  for (let v=0; v<N_VAL; v++) {
    const item = Q[c][v];
    const qs = qSlide(c,v);
    const as = aSlide(c,v);

    // ---------- QUESTION SLIDE ----------
    {
      const s = pptx.addSlide();
      bg(s, PAPER);
      qHeader(s, c, v);
      // category + value caption
      s.addText(CATS[c].tag + ' \u00B7 $' + item.v, { x:0.7, y:1.0, w:6, h:0.35, align:'left', valign:'middle', fontFace:F_BODY, fontSize:12, bold:true, color:MUTED, isTextBox:true, margin:0 });

      if (item.type === 'MC') {
        s.addText(item.q, { x:0.7, y:1.45, w:W-1.4, h:1.35, align:'left', valign:'top', fontFace:F_BODY, fontSize:26, bold:true, color:INK, isTextBox:true, margin:0, lineSpacingMultiple:1.05 });
        const letters = ['A','B','C','D'];
        const oy = 2.95, oh = 0.66, og = 0.13;
        item.opts.forEach((op,i) => {
          const y = oy + i*(oh+og);
          s.addShape(pptx.ShapeType.roundRect, { x:0.7, y, w:W-1.4, h:oh, fill:{ color:PAPER2 }, line:{ color:'D5DEE8', width:1 }, rectRadius:0.08 });
          s.addText([{text:letters[i]+'.  ', options:{ bold:true, color:TEAL_D }}, {text:op, options:{ color:INK }}],
            { x:0.95, y, w:W-1.9, h:oh, align:'left', valign:'middle', fontFace:F_BODY, fontSize:18, isTextBox:true, margin:0 });
        });
      } else {
        s.addText(item.q, { x:0.7, y:1.7, w:W-1.4, h:2.2, align:'center', valign:'middle', fontFace:F_BODY, fontSize:28, bold:true, color:INK, isTextBox:true, margin:0, lineSpacingMultiple:1.08 });
        chip(s, { x:(W-3.6)/2, y:4.15, w:3.6, h:0.6, text:'TEAM CHALLENGE', fill:TEAL, color:'0B2E2A', size:15 });
      }

      // reveal button
      chip(s, { x:(W-3.4)/2, y:6.55, w:3.4, h:0.7, text:'REVEAL ANSWER', fill:GOLD, color:NAVY, size:20, link:as });
    }

    // ---------- ANSWER SLIDE ----------
    {
      const s = pptx.addSlide();
      bg(s, PAPER);
      qHeader(s, c, v);
      s.addText(CATS[c].tag + ' \u00B7 $' + item.v + ' \u00B7 ANSWER', { x:0.7, y:1.0, w:6, h:0.35, align:'left', valign:'middle', fontFace:F_BODY, fontSize:12, bold:true, color:GREEN, isTextBox:true, margin:0 });

      // answer panel
      s.addShape(pptx.ShapeType.roundRect, { x:0.7, y:1.55, w:W-1.4, h:2.6, fill:{ color:GREEN2 }, line:{ color:'BFE3CF', width:1.5 }, rectRadius:0.12 });

      let ansLine;
      if (item.type === 'MC') {
        const letters = ['A','B','C','D'];
        ansLine = letters[item.ans] + ' \u2014 ' + item.opts[item.ans];
      } else {
        ansLine = item.ansText;
      }
      s.addText([{text:'Correct answer\n', options:{ bold:true, color:GREEN, fontSize:15, breakLine:true }},
                 {text:ansLine, options:{ bold:true, color:INK, fontSize:26 }}],
        { x:1.05, y:1.75, w:W-2.1, h:2.2, align:'left', valign:'middle', fontFace:F_BODY, isTextBox:true, margin:0, lineSpacingMultiple:1.06 });

      // explain line
      s.addText([{text:'Why: ', options:{ bold:true, color:MUTED }}, {text:item.explain, options:{ color:MUTED }}],
        { x:0.7, y:4.4, w:W-1.4, h:0.9, align:'center', valign:'middle', fontFace:F_BODY, fontSize:16, italic:true, isTextBox:true, margin:0, lineSpacingMultiple:1.05 });

      // buttons
      chip(s, { x:(W-3.4)/2, y:5.9, w:3.4, h:0.7, text:'\u25C0 BACK TO BOARD', fill:GOLD, color:NAVY, size:18, link:SL_BOARD });
      chip(s, { x:(W-3.4)/2, y:6.72, w:3.4, h:0.55, text:'See the clue again', fill:PAPER2, color:INK, size:14, link:qs });
    }
  }
}

// ---------- write ----------
const path = require('path');
const OUT = path.resolve(__dirname, '..', 'production', 'review', 'unit-01', 'unit1-review-game.pptx');
pptx.writeFile({ fileName: OUT })
  .then(f => console.log('WROTE', f))
  .catch(e => { console.error('ERROR', e); process.exit(1); });
