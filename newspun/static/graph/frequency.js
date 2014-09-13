var frequency = function (raw) {

var diameter = 750,
    format = d3.format(",d"),
    color = d3.scale.category20c();

var bubble = d3.layout.pack()
    .sort(null)
    .size([diameter, diameter-100])
    .padding(1.5);

var svg = d3.select("#graph-location").append("svg")
    .attr("width", diameter)
    .attr("height", diameter-100)
    .attr("class", "bubble");

var rawData = raw;

var generate = function (raw) {
  return {children: raw.frequencies.map(function (item) {
      return {
        packageName: raw.source,
        className: item[0],
        value: item[1]
      };
  })}
};

var data = generate(rawData);
  var node = svg.selectAll(".node")
      .data(bubble.nodes(data)
      .filter(function(d) { return !d.children; }))
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  node.append("title")
      .text(function(d) { return d.className + ": " + format(d.value); });

  node.append("circle")
      .attr("r", function(d) { return d.r; })
      .style("fill", function(d) { return color(d.packageName); });

  node.append("text")
      .attr("dy", ".3em")
      .style("text-anchor", "middle")
      .style("color", "#ffffff")
      .text(function(d) { return d.className.substring(0, d.r / 3); });


d3.select(self.frameElement).style("height", diameter + "px");

};
