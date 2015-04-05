Speeches.SpeechesLineView = function(){
	var that = {};
  var disSelection = "";

  var init = function(){
    initListener();
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

	that.renderRelative = renderRelative;
  that.setSelection = setSelection;
  that.getSelection = getSelection;
  that.init = init;
  that.renderAbsolute = renderAbsolute;

	return that;
};