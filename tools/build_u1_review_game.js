// Phase 13Z — Unit 1 clickable Jeopardy-style review game deck.
// Thin config wrapper over the shared review_game_lib.js generator.

const path = require('path');
const { buildDeck } = require('./review_game_lib.js');

const CATS = [
  { short: 'Energy & Change',      full: 'Energy Causes Change',        tag: 'CASE 1' },
  { short: 'Need for Speed',       full: 'Speed & Energy of Motion',    tag: 'CASE 2' },
  { short: 'Transfer or Transform',full: 'Transfer or Transformation',  tag: 'CASE 3' },
  { short: 'Collision Course',     full: 'Collisions',                  tag: 'CASE 4' },
  { short: "Edison's Lab",         full: 'Engineering & Edison/Latimer',tag: 'CASE 5' },
];

// type: 'MC' (options + ans index) | 'TEAM' (ansText accepted answer)
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

buildDeck({
  outPath: path.resolve(__dirname, '..', 'production', 'review', 'unit-01', 'unit1-review-game.pptx'),
  meta: { author: 'Grade 4 Science', title: 'Energy Detective — Unit 1 Review Game' },
  text: {
    kicker: 'UNIT 1 REVIEW',
    bigTitle: 'ENERGY DETECTIVE',
    subtitle: 'Crack the Vault \u00B7 A Jeopardy-Style Review Game',
    subsub: 'Energy Transfer & Transformation \u00B7 5 cases \u00B7 25 clues \u00B7 30 minutes',
    monogram: 'ED',
    howtoTitle: 'How to Play',
    howtoSteps: [
      '1.  Split into teams and open the game board.',
      '2.  Choose a category and a dollar value, then click the tile.',
      '3.  Read the clue together and discuss your answer.',
      '4.  Click \u201CReveal Answer\u201D to check the correct answer.',
      '5.  Click \u201C\u25C0 Board\u201D to return and pick the next tile.',
      '6.  Track points and unlock a digit on your squad scorecard.',
    ],
    boardTitle: 'The Case Board',
    boardSubline: 'Click any tile to open the clue.',
    boardFooter: '30-minute class game \u00B7 Unit 1 review \u00B7 no external files',
    revealBtn: 'REVEAL ANSWER',
    backBtn: '\u25C0 BACK TO BOARD',
    clueAgain: 'See the clue again',
  },
  cats: CATS,
  values: [100, 200, 300, 400, 500],
  questions: Q,
  finalChallenge: null,
});
