Speeches.SpeechesLineView = function(){
	var that = {};
  var disSelection = "";
  var currentDrama_id = 0;

  var init = function(){
    initListener();
    initId();
    initLinks();
  };

  var setSelection = function(){
    disSelection = $("#selection-speech-distribution").val();

  };

  var initListener = function(){
    $("#selection-speech-distribution").change(selectionClicked);
  };

  var selectionClicked = function(){
    $(that).trigger("SelectionClicked");
  };

	var renderRelative = function(distribution){

		var data = new google.visualization.DataTable();
		data.addColumn("number", "Replikenlänge in Worten");
		data.addColumn("number", 'Replikenhäufigkeit in Prozent');
		var array = [];
		for(var key in distribution){
			var row = [parseInt(key), distribution[key]];
			array.push(row);
		}
		data.addRows(array);

		var options = {
		  height: 700,
		  width: 1170,
		  animation: {
		  	duration: 1000
		  },
		  chartArea:{width:'75%',height:'80%'},
          title: 'Replikenlängenverteilung, Relative Häufigkeit in Prozent',
          curveType: 'function',
          legend: {
          	position: 'none'
          },
          hAxis : {
          	title: 'Replikenlänge in Worten'
          },
          vAxis: {
          	title: 'Relative Häufigkeit in Prozent',
            baseline: 0
          }
        };

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('curve-dashbord'));

        var rangeSlider1 = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'curve-controls1',
          'options': {
            'filterColumnLabel': 'Replikenlänge in Worten'
          }
        });

        var rangeSlider2 = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'curve-controls2',
          'options': {
            'filterColumnLabel': 'Replikenhäufigkeit in Prozent'
          }
        });

        var chart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'curve-chart',
          'options': options
        });

        dashboard.bind(rangeSlider1, chart);
        dashboard.bind(rangeSlider2, chart);

        var chart_div = document.getElementById('curve-chart');

        $("#download-png-curve").unbind("click");
        $("#download-png-curve").on("click", function(){
          //chart_div.innerHTML = '<img src="' + chart.getChart().getImageURI() + '">';

          window.open(chart.getChart().getImageURI());
          
          //render(distribution);

        });

        dashboard.draw(data);
	};

    var renderAbsolute = function(distribution){

    var data = new google.visualization.DataTable();
    data.addColumn("number", "Replikenlänge in Worten");
    data.addColumn("number", 'Replikenhäufigkeit absolut');
    var array = [];
    for(var key in distribution){
      var row = [parseInt(key), distribution[key]];
      array.push(row);
    }
    data.addRows(array);

    var options = {
      height: 700,
      width: 1170,
      animation: {
        duration: 1000
      },
      chartArea:{width:'75%',height:'80%'},
          title: 'Replikenlängenverteilung, Absolute Häufigkeit',
          curveType: 'function',
          legend: {
            position: 'none'
          },
          hAxis : {
            title: 'Replikenlänge in Worten'
          },
          vAxis: {
            title: 'Absolute Häufigkeit',
            baseline: 0
          }
        };

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('curve-dashbord'));

        var rangeSlider1 = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'curve-controls1',
          'options': {
            'filterColumnLabel': 'Replikenlänge in Worten'
          }
        });

        var rangeSlider2 = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'curve-controls2',
          'options': {
            'filterColumnLabel': 'Replikenhäufigkeit absolut'
          }
        });

        var chart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'curve-chart',
          'options': options
        });

        dashboard.bind(rangeSlider1, chart);
        dashboard.bind(rangeSlider2, chart);

        var chart_div = document.getElementById('curve-chart');

        $("#download-png-curve").unbind("click");
        $("#download-png-curve").on("click", function(){
          //chart_div.innerHTML = '<img src="' + chart.getChart().getImageURI() + '">';

          window.open(chart.getChart().getImageURI());
          
          //render(distribution);

        });

        dashboard.draw(data);
  };

  var getSelection = function(){
    return disSelection;
  };

  var initId = function(){
    var params = window.location.search
    console.log("hello World");
    console.log(params);
    currentDrama_id = (params.substring(params.indexOf("=") + 1));
  };

  var initLinks = function(){
    $("#link-overall").attr("href", "drama.html?drama_id=" + currentDrama_id);
    $("#link-matrix").attr("href", "matrix.html?drama_id=" + currentDrama_id);
    $("#link-drama").attr("href", "singledrama.html?drama_id=" + currentDrama_id);
    $("#link-drama-actSceneAnalysis").attr("href", "singledrama.html?drama_id=" + currentDrama_id + "#act-scene-table");
    $("#link-drama-actStatistic").attr("href", "singledrama.html?drama_id=" + currentDrama_id + "#act-statistic");
    $("#link-drama-sceneStatistic").attr("href", "singledrama.html?drama_id=" + currentDrama_id + "#scene-statistic");
    $("#link-speakers").attr("href", "speakers.html?drama_id=" + currentDrama_id);
    $("#link-speaker-table").attr("href", "speakers.html?drama_id=" + currentDrama_id + "#speaker-table");
    $("#link-speeches-dominance").attr("href", "speakers.html?drama_id=" + currentDrama_id  + "#speeches-dominance");
    $("#link-speaker-statistic").attr("href", "speakers.html?drama_id=" + currentDrama_id  + "#speaker-statistic");
    $("#link-speaker-relations").attr("href", "speakers.html?drama_id=" + currentDrama_id  + "#speaker-relations");
    $("#link-speeches").attr("href", "speeches.html?drama_id=" + currentDrama_id);
    $("#link-histogram").attr("href", "speeches.html?drama_id=" + currentDrama_id + "#histogram");
    $("#link-curve-diagram").attr("href", "speeches.html?drama_id=" + currentDrama_id + "#curve-diagram");
  };

	that.renderRelative = renderRelative;
  that.setSelection = setSelection;
  that.getSelection = getSelection;
  that.init = init;
  that.renderAbsolute = renderAbsolute;

	return that;
};