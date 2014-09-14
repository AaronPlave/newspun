var proximity = function(data, source) {
  var width = 750,
      height = 400,
      radius = Math.min(width, height) / 2;

  var color = d3.scale.ordinal()
      .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

  var arc = d3.svg.arc()
      .outerRadius(radius - 10)
      .innerRadius(radius - 120);

  var pie = d3.layout.pie()
      .sort(null)
      .value(function(d) { return d.number; });

  var svg = d3.select("#graph-location").append("svg")
      .attr("width", width)
      .attr("height", height)
    .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  data.forEach(function(d) {
    d.number = +d.number;
  });

  var g = svg.selectAll(".arc")
      .data(pie(data))
    .enter().append("g")
      .attr("class", "arc");

  g.append("path")
      .attr("d", arc)
      .style("fill", function(d) { return color(d.data.caption); });

  g.append("text")
      .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
      .attr("dy", ".35em")
      .attr("fill", "black")
      .style("text-anchor", "middle")
      .style("font-size", "15px")
      .text(function(d) { return d.data.caption; });

  g.append("text")
      .attr("dy", ".35em")
      .attr("fill", "white")
      .style("text-anchor", "middle")
      .style("font-size", "20px")
      .text(source);
};
