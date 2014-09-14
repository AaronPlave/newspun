var readability = function (data) {

  var margin = {top: 40, right: 20, bottom: 30, left: 40},
      width = 750
      height = 400

  var formatPercent = d3.format("r");

  var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);

  var y = d3.scale.linear()
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickFormat(formatPercent);

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return "<strong>Readability Score:</strong> <span style='color:red'>" + d.readability_score + "</span>";
    })

  var svg = d3.select("#graph-location").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.call(tip);

  //d3.tsv("data.tsv", type, function(error, data) {
    x.domain(data.map(function(d) { return d.source; }));
    y.domain([0, d3.max(data, function(d) { return d.readability_score; })]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("fill", "white")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .attr("fill", "white")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .attr("fill", "white")
        .style("text-anchor", "end")
        .text("Readability Score");

    svg.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.source); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.readability_score); })
        .attr("height", function(d) { return height - y(d.readability_score); })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)

  //});

  function type(d) {
    d.readability_score = +d.readability_score;
    return d;
  }
  $('#graph-legend').html('Calculated using <a href="http://en.wikipedia.org/wiki/Gunning_fog_index">Gunning fog index</a>. Lower values are easier to read.');

};
