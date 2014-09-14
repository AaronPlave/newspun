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
$.getJSON('/sources', function(sources) {
  console.log(sources);
  var engine = new Bloodhound({
    name: 'sources',
    // local: [{ name: 'NBC' }, { name: 'Washington Post' }, { name: 'New York Times' }],
    local: sources.map(function (item) {
      return {name: item.val};
    }),
    datumTokenizer: function(d) {
      return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace
  });

  engine.initialize();
  $('#typeahead').tagsinput({
    typeaheadjs: {
      name: 'sources',
      displayKey: 'name',
      valueKey: 'name',
      source: engine.ttAdapter()
    },
    freeInput: false
  });
  engine.local.forEach(function(tag) {
    $('input:eq(0)').tagsinput('add', tag.name);
  });

});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

started = false;

var goToSection = function () {
  $('html, body').stop().animate({
      scrollTop: $('#' + Backbone.history.fragment).offset().top
  }, 500, 'easeInOutExpo');
};

var AppRouter = Backbone.Router.extend ({
  routes: {
    '': function () {
      started = true;
      // Intro route
      $('section').hide();
      $('#option-proximity').hide();
      $('.navbar-nav li').hide();
      $('.navbar-nav li:eq(0)').show();
      $('.selected').removeClass('selected');
    },
    'sources': function () {
      if(!started) {this.navigate('',{trigger:true});return;}

      var type = $('header .selected').parent().data('code');

      // Sources route

      if(type === "proximity") {
        $('#option-proximity').show();
      }

      $('section#sources').show();
      $('.navbar-nav li').hide();
      $('.navbar-nav li:eq(0)').show();
      $('.navbar-nav li:eq(1)').show();
      goToSection();
    },
    'graphs': function () {
      if(!started) {this.navigate('',{trigger:true});return;}
      var items = $('input:eq(0)').tagsinput('items');
      console.log(items);
      if(items.length === 0) {
        this.navigate('sources',{trigger: true});
        return;
      }
      var type = $('header .selected').parent().data('code');
      var words = $('#option-proximity input').map(function(){return $(this).val();});
      if(type === "proximity" && (words[0] === "" || words[1] === "")) {
        this.navigate('sources',{trigger: true});
      }
      // Graphs route
      $('section#graphs').show();
      $('.navbar-nav li:eq(2)').show();

      $('#graph-location').html('');
      switch (type) {
        case 'freq':
          $.getJSON('/static/sample_freq_data.json', function (data) {
            frequency(data, items);
          });
          break;
        case 'sentiment':
          $.getJSON('/', function () {

          });
        case 'readability':
          $.getJSON('/', function () {

          });
        case 'proximity':
          $.getJSON('/', function () {

          });
        default:
          this.navigate('', {trigger: true});

      }
      goToSection();
    },
    '*x': function () {
      this.navigate('', {trigger:true});
    }
  }
});

$(document).ready(function () {
  var appRouter = new AppRouter();
  Backbone.history.start();

  $('.intro .list-group li').click(function () {
    $('.intro .list-group li').removeClass('selected');
    $(this).addClass('selected');
  })
});
