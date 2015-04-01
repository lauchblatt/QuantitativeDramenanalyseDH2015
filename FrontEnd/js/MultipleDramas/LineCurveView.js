MultipleDramas.LineCurveView = function(){
	var that = {};

  var compareSelection = "";

  var init = function(){
    initListener();
  };

  var initListener = function(){
    $("#selection-speech-compare").change(speechSelectionCompareClicked);
  };

  var speechSelectionCompareClicked = function(){
    $(that).trigger("SpeechSelectionCompareClicked");
  };

  var renderCurve = function(distribution, catDistribution, authorDistribution){
    if(compareSelection == 'Kein Vergleich'){
      renderCurveNormal(distribution);
    }
    if(compareSelection == 'Typ'){
      renderTypeCurve(catDistribution);
    }
    if(compareSelection == 'Autor'){
      renderTypeCurve(authorDistribution);
    }
  };

	var renderCurveNormal = function(distribution){
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Replikenlänge in Worten");
		data.addColumn("number", 'Replikenhäufigkeit');
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
          title: 'Replikenlängen, Absolute Häufigkeit',
          curveType: 'function',
          legend: {
          	position: 'none'
          },
          hAxis : {
          	title: 'Replikenlänge'
          },
          vAxis: {
          	title: 'Absolute Häufigkeit',
            baseline: 0
          }
        };

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('curve-dashbord'));

        var rangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'curve-controls',
          'options': {
            'filterColumnLabel': 'Replikenlänge in Worten'
          }
        });

        var chart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'curve-chart',
          'options': options
        });

        $("#download-png-curve").unbind("click");
        $("#download-png-curve").on("click", function(){
          window.open(chart.getChart().getImageURI());
          //drawChartAct(actInfo);
        });

        dashboard.bind(rangeSlider, chart);

        dashboard.draw(data);
	};

  var renderTypeCurve = function(typeDistribution){

    var data = new google.visualization.DataTable();

    data.addColumn("number", "Replikenlänge in Worten");
    for(var i = 0; i < typeDistribution.length; i++){
      if(typeDistribution[i].type !== undefined){
        data.addColumn("number", typeDistribution[i].type);
      }
      if(typeDistribution[i].name !== undefined){
        data.addColumn("number", typeDistribution[i].name)
      }
    }

    var presentLengths = [];
    for(var i = 0; i < typeDistribution.length; i++){
      for(var key in typeDistribution[i]){
          if(presentLengths.indexOf(key) == -1 && !isNaN(key)){
            presentLengths.push(key);
          }
      }
    }
    var array = [];
    for(var i = 0; i < presentLengths.length; i++){
      var row = [parseInt(presentLengths[i])];
      for(var j = 0; j < typeDistribution.length; j++){
        if(typeDistribution[j][presentLengths[i]] !== undefined){
          row.push(typeDistribution[j][presentLengths[i]]);
        }else{
          row.push(null);
        }
      }
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
          title: 'Replikenlängen, Absolute Häufigkeit',
          curveType: 'function',
          hAxis : {
            title: 'Replikenlänge'
          },
          vAxis: {
            title: 'Häufigkeit',
            baseline: 0
          }
        };

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('curve-dashbord'));

        var rangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'curve-controls',
          'options': {
            'filterColumnLabel': 'Replikenlänge in Worten'
          }
        });

        var chart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'curve-chart',
          'options': options
        });

        $("#download-png-curve").unbind("click");
        $("#download-png-curve").on("click", function(){
          window.open(pieChart.chart().getImageURI());
        });

        dashboard.bind(rangeSlider, chart);

        dashboard.draw(data);
  };

  var setSpeechCompareSelection = function(){
    compareSelection = $("#selection-speech-compare").val();  
  };

	that.renderCurve = renderCurve;
  that.renderTypeCurve = renderTypeCurve;
  that.init = init;
  that.setSpeechCompareSelection = setSpeechCompareSelection;

	return that;
};