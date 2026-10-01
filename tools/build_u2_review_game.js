// Phase 13AA — Unit 2 clickable Jeopardy-style review game deck.
// Thin config wrapper over the shared review_game_lib.js generator.

const path = require('path');
const { buildDeck } = require('./review_game_lib.js');

const CATS = [
  { short: 'Resource Detective', full: 'Renewable vs Nonrenewable', tag: 'FILE 1' },
  { short: 'Fossil Fuels',        full: 'Coal, Petroleum, Natural Gas', tag: 'FILE 2' },
  { short: 'Turbines & Generators', full: 'Turbine & Generator Pathways', tag: 'FILE 3' },
  { short: 'Renewable Power',     full: 'Wind, Water, Sun, Geothermal', tag: 'FILE 4' },
  { short: 'Resource Challenge',  full: 'Compare, Choose, Explain', tag: 'FILE 5' },
];

// type: 'MC' (options + ans index) | 'TEAM' (ansText). Optional diagram = arrow-chain visual.
const Q = [
  // FILE 1 — Resource Detective (renewable / nonrenewable / availability / classification)
  [
    { v:100, type:'MC', q:'A resource that can be restored as fast as it is used is called a ____.',
      opts:['renewable resource','nonrenewable resource','fossil fuel','solar cell'],
      ans:0, explain:'Renewable means it comes back as quickly as it is used.' },
    { v:200, type:'MC', q:'What is the main difference between a renewable and a nonrenewable resource?',
      opts:['Nonrenewable resources are always safer','Renewable resources cause more air pollution','Renewable resources are restored quickly, but nonrenewable resources take millions of years to form','Nonrenewable resources are restored quickly by planting trees'],
      ans:2, explain:'Renewable returns fast; nonrenewable takes millions of years.' },
    { v:300, type:'MC', q:'Coal is plentiful today, but it forms over millions of years. This shows that coal is ____.',
      opts:['renewable','nonrenewable','a biofuel','available everywhere'],
      ans:1, explain:'Abundant does NOT mean renewable.' },
    { v:400, type:'MC', q:'Propane gas is abundant in tanks today, but it takes millions of years to form underground. Propane is a ____.',
      opts:['renewable resource','biofuel','nonrenewable resource','geothermal resource'],
      ans:2, explain:'It is used faster than nature can create it.' },
    { v:500, type:'TEAM', q:'Why does it matter how quickly a resource is restored?',
      ansText:'A resource is renewable only if it comes back as fast as (or faster than) we use it.',
      explain:'Renewable or nonrenewable depends on time: how fast we use it vs. how fast it returns.' },
  ],
  // FILE 2 — Fossil Fuels (coal / petroleum / natural gas / formation / uses)
  [
    { v:100, type:'MC', q:'Which fossil fuel is a liquid formed underground that is refined into gasoline and diesel?',
      opts:['petroleum (crude oil)','coal','natural gas','uranium'],
      ans:0, explain:'Petroleum is a liquid fossil fuel refined into fuels.' },
    { v:200, type:'TEAM', q:'The three fossil fuels are coal, petroleum, and ____.',
      ansText:'natural gas',
      explain:'Coal, petroleum, and natural gas are the three fossil fuels.' },
    { v:300, type:'MC', q:'Which energy source is a fossil fuel?',
      opts:['sunlight','coal','wind','uranium'],
      ans:1, explain:'Coal is a fossil fuel formed from the remains of living things.' },
    { v:400, type:'MC', q:'Why are fossil fuels like petroleum considered nonrenewable?',
      opts:['They are made in factories every day','They are used much faster than nature can create them','They can never be completely used up','They are found everywhere on Earth\u2019s surface'],
      ans:1, explain:'We use them faster than nature can replace them.' },
    { v:500, type:'TEAM', q:'How are coal and petroleum alike? How are they different?',
      ansText:'Alike: both form from the remains of organisms over millions of years. Different: coal forms from swamp plants (solid); petroleum forms from ocean organisms (liquid).',
      explain:'All fossil fuels come from remains of living things from long ago.' },
  ],
  // FILE 3 — Turbines & Generators (pathways; coal vs nuclear shared step)
  [
    { v:100, type:'TEAM', q:'A machine with blades that spins when moving air, water, or steam pushes it is a ____.',
      ansText:'turbine',
      explain:'A turbine spins when air, water, or steam pushes its blades.' },
    { v:200, type:'MC', q:'What is the final form of energy produced by a generator?',
      opts:['electricity','sound','heat','sunlight'],
      ans:0, explain:'The generator makes electricity.' },
    { v:300, type:'MC', q:'Which machine belongs in the empty box?',
      opts:['turbine','solar cell','dam','battery'],
      ans:0, explain:'Moving air spins the turbine, which turns the generator.',
      diagram:{ boxes:['Moving air','?','Generator','Electricity'], caption:'Wind electricity pathway' } },
    { v:400, type:'MC', q:'Coal plants and nuclear plants use different fuels. What shared step do BOTH use to make electricity?',
      opts:['Both burn the fuel underground','Both use rooftop solar cells','Both use heat to turn water into steam that spins a turbine-generator','Both rely on flowing river currents'],
      ans:2, explain:'Nuclear and coal share the heat \u2192 steam \u2192 turbine \u2192 generator pathway.' },
    { v:500, type:'TEAM', q:'Look at the pathway. Explain what stays the SAME in a coal plant and a nuclear plant.',
      ansText:'Heat boils water into steam \u2192 the steam spins a turbine \u2192 the turbine turns a generator \u2192 electricity.',
      explain:'Both plants share heat \u2192 steam \u2192 turbine \u2192 generator.',
      diagram:{ boxes:['Fuel','Heat','Steam','Turbine','Generator','Electricity'], caption:'The pathway coal and nuclear share' } },
  ],
  // FILE 4 — Renewable Power (wind / hydro / solar / geothermal / location)
  [
    { v:100, type:'TEAM', q:'Hydroelectric power is electricity made from ____.',
      ansText:'moving water (usually through a dam)',
      explain:'Moving water spins a turbine connected to a generator.' },
    { v:200, type:'MC', q:'Geothermal energy relies on heat that comes from where?',
      opts:['the Sun\u2019s rays','warm ocean waves','burning fossil plants','deep inside Earth'],
      ans:3, explain:'Geothermal uses heat from inside Earth.' },
    { v:300, type:'MC', q:'A solar cell converts sunlight into what? Fill the empty box.',
      opts:['electricity','heat','wind','geothermal energy'],
      ans:0, explain:'A solar cell changes sunlight into electricity.',
      diagram:{ boxes:['Sunlight','Solar cell','?'], caption:'Solar electricity pathway' } },
    { v:400, type:'MC', q:'A mountain town has strong, steady wind every day, but it is cloudy most of the year and has no large rivers. Which renewable resource is the most reliable choice?',
      opts:['hydroelectric power','solar power','coal','wind power'],
      ans:3, explain:'Steady wind makes wind power the most reliable choice there.' },
    { v:500, type:'TEAM', q:'Why is solar power called renewable but not always available?',
      ansText:'The sun keeps shining (renewable), but solar depends on location, weather, and time of day (cloudy days, nighttime).',
      explain:'Sunlight is free and renewable, but not always available.' },
  ],
  // FILE 5 — Resource Challenge (comparison / benefit vs limitation / hybrid / synthesis)
  [
    { v:100, type:'MC', q:'A hybrid car uses two sources of energy. Which combination is common in hybrid vehicles?',
      opts:['coal and natural gas','gasoline fuel and battery power','wind and solar','uranium and water'],
      ans:1, explain:'Hybrids commonly combine gasoline and battery power.' },
    { v:200, type:'MC', q:'What is one major limitation of using solar energy?',
      opts:['It makes lots of smoke and air pollution','It needs millions of years to form','It depends on available sunlight, so less sun can limit electricity','It needs a deep underground coal mine'],
      ans:2, explain:'Solar depends on the sunlight that is available.' },
    { v:300, type:'MC', q:'Which is a major environmental cost of burning fossil fuels like coal and oil?',
      opts:['releasing smoke and air pollutants into the air','cooling Earth\u2019s oceans too fast','creating extra wind currents','using up all the sunlight'],
      ans:0, explain:'Burning fossil fuels releases smoke and air pollutants.' },
    { v:400, type:'MC', q:'A town has strong sunlight most days but very little moving water. Which energy resource would be most reliable based on availability?',
      opts:['hydroelectric power','coal power','wind power','solar power'],
      ans:3, explain:'Strong sunlight makes solar power the most reliable there.' },
    { v:500, type:'TEAM', q:'Name ONE renewable resource. Give one benefit AND one limitation, and where it works well.',
      ansText:'Example: wind \u2014 benefit: no fuel to burn; limitation: needs a windy location; works well where the wind blows steadily.',
      explain:'Any resource with a benefit, a limitation, and a good location earns full points.' },
  ],
];

buildDeck({
  outPath: path.resolve(__dirname, '..', 'production', 'review', 'unit-02', 'unit2-review-game.pptx'),
  meta: { author: 'Grade 4 Science', title: 'Resource Detective — Unit 2 Review Game' },
  text: {
    kicker: 'UNIT 2 REVIEW',
    bigTitle: 'RESOURCE DETECTIVE',
    subtitle: 'Solve the Energy Source Case \u00B7 A Jeopardy-Style Review Game',
    subsub: 'Using Natural Resources for Energy \u00B7 5 files \u00B7 25 clues \u00B7 30 minutes',
    monogram: 'RD',
    howtoTitle: 'How to Play',
    howtoSteps: [
      '1.  Split into teams and open the game board.',
      '2.  Choose a category and a dollar value, then click the tile.',
      '3.  Read the clue together and discuss your answer.',
      '4.  Click \u201CReveal Answer\u201D to check the correct answer.',
      '5.  Click \u201C\u25C0 Board\u201D to return and pick the next tile.',
      '6.  Track points and unlock a clue on your squad scorecard.',
    ],
    boardTitle: 'The Resource Case Board',
    boardSubline: 'Click any tile to open the clue.',
    boardFooter: '30-minute class game \u00B7 Unit 2 review \u00B7 no external files',
    revealBtn: 'REVEAL ANSWER',
    backBtn: '\u25C0 BACK TO BOARD',
    clueAgain: 'See the clue again',
  },
  cats: CATS,
  values: [100, 200, 300, 400, 500],
  questions: Q,
  finalChallenge: {
    tag: 'THE MYSTERY TOWN',
    q: 'Final Challenge \u2014 The Mystery Town\nA town wants to switch to renewable energy. It has strong, steady wind every day, many cloudy days, no large river nearby, and no volcanic activity.',
    promptLines: [
      'Which ONE resource should this town investigate? Explain your choice.',
    ],
    ansText: 'Wind power. The town has strong, steady wind every day \u2014 so wind is reliable there.',
    explain: 'Cloudy days limit solar, no river limits hydroelectric, and no volcanic activity limits geothermal. Steady wind makes wind the best fit.',
  },
});
