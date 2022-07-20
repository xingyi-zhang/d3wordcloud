distractor_text = ['roman', 'menus', 'more', 'oeuvre', 'mere', 'excess', 'cam', 'cream', 'mercer', 'maneuver', 'moron', 'amazes', 'serene', 's.c', 'maneuver', 'cocoa', 'worse', 'museums', 'accuse', 'ceases', 'cosmos', 'susan', 'mar', 'sum', 'manners', 'nuance', 'newness', 'anew', 'recesses', 'noon', 'wan', 'seas', 'macon', 'nuance', 'sewer', 'ceases', 'wares', 'mover', 'vancouver', 'vera', 'mere', 'ammo', 'vernon', 'see', 'mona', 'courses', 'seen', 'maze', 'were', 'movers', 'mar', 'raccoon', 'wove', 'war', 'conan', 'ensure', 'vows', 'concur', 'cannons', 'cancer', 'waco', 'swarms', 'exxon', 'moron', 'curses', 'removes', 'mere', 'census', 'verse', 'sew', 'mess', 'roars', 'una', 'norm', 'moons', 'wearer', 'murmur', 'excuse', 'murmur', 'nora', 'murmur', 'morrow', 'now', 'excuse', 'season', 'concur', 'nonsense', 'non', 'erroneous', 'mucus', 'resource', 'recesses', 'access', 'means', 'crowe', 'soccer', 'mormon', 'renounce', 'crossover', 'accuses','now', 'scene', 'oscar', 'successors', 'nerve', 'worm', 'amorous', 'exxon', 'moves', 'scans', 'woven', 'swore', 'seams', 'eva', 'canvases', 'season', 'mass', 'newcomer', 'muse', 'ensures', 'won', 'mere', 'mcnamara', 'measures', 'sooner', 'sores', 'roars', 'scans', 'sums', 'coroner', 'move', 'excess', 'unesco', 'acumen', 'none', 'seas', 'measures', 'assumes', 'vera', 'usc', 'oversaw', 'seam', 'move', 'sewer', 'across', 'moves', 'marco', 'racer', 'execs', 'cow', 'usa', 'cruz', 'masse', 'users', 'screw', 'exec', 'crews', 'versa', 'overcame', 'nassau', 'carr', 'sorrow', 'manor', 'scares', 'armor', 'waves', 'eva', 'row', 'mourn', 'news', 'u.s.a', 'wes', 'vance', 'una', 'convene', 'overseen', 'acumen', 'senses', 'anna', 'newcomer', 'woman', 'smear', 'mascara', 'noon', 'wears', 'monaco', 'snows', 'wearer', 'warmer', 'venues', 'suarez', 'scarce', 'evan', 'sorrows', 'sonoma', 'oeuvre', 'successes', 'summons', 'screws', 'corner']
target_text = ['test_1','test_2']

target_stim = target_text.map(function(d) {
  return {text: d, size: 20, fill: 'black'};
})

distractor_stim = distractor_text.map(function(d) {
  return {text: d, size: 13 + Math.random() * 15, fill: 'gray'};
})

words = target_stim.concat(distractor_stim);

var a = d3.select('svg');

var layout = d3.layout.cloud()
  .size([1000, 500])
  .words(words)
  .padding(4)
  .rotate(0)
  .font("Impact")
  .fontSize(d => d.size)
  .on("end", draw);

layout.start();

function draw(words) {
  //d3.select(a)
  a
    .attr("width", layout.size()[0])
    .attr("height", layout.size()[1])
    .append("g")
    .attr(
      "transform",
      "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")"
    )
    .selectAll("text")
    .data(words)
    .enter()
    .append("text")
    .style("font-size", d => `${d.size}px`)
    .style("font-family", "serif")
    .attr("text-anchor", "middle")
    .attr("transform", d => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
    .attr("fill", d => d.fill)
    .text(d => d.text);
}
