
var words = [{'text': 'me', 'weight': 153}, {'text': 'beautiful', 'weight': 227}, {'text': 'great', 'weight': 114}, {'text': 'oliver', 'weight': 125}, {'text': 'love', 'weight': 383}, {'text': 'name', 'weight': 148}, {'text': 'this', 'weight': 159}, {'text': 'time', 'weight': 142}, {'text': 'story', 'weight': 250}, {'text': 'yor', 'weight': 151}, {'text': 'chalamet', 'weight': 203}, {'text': 'call', 'weight': 181}, {'text': 'characters', 'weight': 111}, {'text': 'year', 'weight': 138}, {'text': 'it', 'weight': 263}, {'text': 'armie', 'weight': 133}, {'text': 'the', 'weight': 372}, {'text': 'hammer', 'weight': 166}, {'text': 'by', 'weight': 117}, {'text': 'elio', 'weight': 179}];
$('#keywords').jQCloud(words);

// progressbar.js@1.0.0 version is used
// Docs: http://progressbarjs.readthedocs.org/en/1.0.0/

var bar = new ProgressBar.Line(container, {
  strokeWidth: 4,
  easing: 'easeInOut',
  duration: 1400,
  color: '#F8D220',
  trailColor: '#eee',
  trailWidth: 1,
  svgStyle: {width: '100%', height: '100%'},
  text: {
    style: {
      // Text color.
      // Default: same as stroke color (options.color)
      color: '#999',
      position: 'absolute',
      right: '0',
      top: '30px',
      padding: 0,
      margin: 0,
      transform: null
    },
    autoStyleContainer: false
  },
  from: {color: '#F8D220'},
  to: {color: '#ED6A5A'},
  step: (state, bar) => {
    bar.setText(Math.round(bar.value() * 100) + ' %');
  }
});

// bar.animate(1.0);  // Number from 0.0 to 1.0


function AppViewModel(name="Call Me by Your Name",url="https://resizing.flixster.com/p_ipwfC-wfF2aVudG27Ng0kFwt4=/206x305/v1.bTsxMjQ4MjQwMjtqOzE3NjQ5OzEyMDA7NjQ4Ozk2MA"){
  var self = this;
  self.progressStatus = ko.observable('not begin yet');
  self.movieTitle = ko.observable(name);
  self.movieImg = ko.observable(url);
  self.movieUrl = ko.observable("");
  self.Naive = ko.observable("");
  self.Logis = ko.observable("");
  self.onEnter = function(d,e){
    e.keyCode===13 &&self.progressStatus('Fetching data...')&& self.searchMovie(self.movieUrl());
    return true;
  };
  self.searchMovie = function(url){
    bar.animate(0.3);
    setTimeout(function(){
      self.progressStatus('Analyzing data...')
      bar.animate(0.6);
    },1500);
    $.ajax({
      type:'POST',
      url:'/',
      dataType: 'json',
      data:{"url":url},
      async: true,
      success:function(data){
        self.movieTitle(data['title']);
        self.movieImg(data['imgurl']);
        self.Naive(data['scores'][0]);
        self.Logis(data['scores'][1]);
        console.log(data['words']);
        $('#keywords').jQCloud('update',data['words'],{delay:100,autoResize: true, shape:'rectangular'});//
        bar.animate(1.0);
        self.progressStatus('Result is out!!!');
        self.movieUrl("");
      },
      fail:function(){
        alert('fail to fetch data');
      }
    });
  };

  };

ko.applyBindings(new AppViewModel("Call Me By Your Name","https://resizing.flixster.com/p_ipwfC-wfF2aVudG27Ng0kFwt4=/206x305/v1.bTsxMjQ4MjQwMjtqOzE3NjQ5OzEyMDA7NjQ4Ozk2MA"));
