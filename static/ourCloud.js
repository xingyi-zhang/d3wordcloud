var a = d3.select('svg');

var layout = d3.layout.cloud()
  .size([512, 512])   // for now has to be the power of 2 due to the rounding issue in d3.layout.cloud 
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
