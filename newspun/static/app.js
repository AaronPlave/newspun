// jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
      if(!$('.navbar-fixed-top').hasClass('top-nav-collapse')) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
      }
    } else {
      if($('.navbar-fixed-top').hasClass('top-nav-collapse')) {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
      }
    }
});

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 500, 'easeInOutExpo');
        event.preventDefault();
    });

  var engine = new Bloodhound({
    name: 'sources',
    local: [{ name: 'NBC' }, { name: 'Washington Post' }, { name: 'New York Times' }],
    datumTokenizer: function(d) {
      return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace
  });

  engine.initialize();
  $('input').tagsinput({
    typeaheadjs: {
      name: 'sources',
      displayKey: 'name',
      valueKey: 'name',
      source: engine.ttAdapter()
    },
    freeInput: false
  });

});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

