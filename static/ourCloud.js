target_stim = target_text.map(function(d,i) {
  return {text: d, size: target_size[i], fill: 'black', x: target_posi[i].x, y:target_posi[i].y, rotate: 0};
})

distractor_stim = distractor_text.map(function(d) {
  return {text: d, size: getDistractorSize(dis_size_config), fill: distractor_fill};
})

var a = d3.select('svg');

var layout = d3.layout.cloud()
  .size([400, 400])
  .words(distractor_stim)
  .targets(target_stim)
  .padding(4)
  .rotate(0)
  .font(font_type)
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
    .style("font-family", font_type)
    .attr("text-anchor", "middle")
    .attr("transform", d => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
    .attr("fill", d => d.fill)
    .text(d => d.text);
}

//the config array is [min,max,mean,sd]
function getDistractorSize(size_config){
  var size = 0
  do {
    size = randomGaussian(size_config[2],size_config[3])
  } while (size <size_config[0] || size >size_config[1])
  return ~~size
}

// SOURCE: http://www.ollysco.de/2012/04/gaussian-normal-functions-in-javascript.html
function randomGaussian(mean, standardDeviation) {
  if (randomGaussian.nextGaussian !== undefined) {
      var nextGaussian = randomGaussian.nextGaussian;
      delete randomGaussian.nextGaussian;
      return (nextGaussian * standardDeviation) + mean;
  } else {
      var v1, v2, s, multiplier;
      do {
          v1 = 2 * Math.random() - 1; // between -1 and 1
          v2 = 2 * Math.random() - 1; // between -1 and 1
          s = v1 * v1 + v2 * v2;
      } while (s >= 1 || s == 0);
      multiplier = Math.sqrt(-2 * Math.log(s) / s);
      randomGaussian.nextGaussian = v2 * multiplier;
      return (v1 * multiplier * standardDeviation) + mean;
  }
};