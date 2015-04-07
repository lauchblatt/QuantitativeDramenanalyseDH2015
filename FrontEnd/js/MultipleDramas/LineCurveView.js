MultipleDramas.LineCurveView = function(){
	var that = {};

  var compareSelection = "";
  var speechDistributionSelection = "";

  var init = function(){
    initListener();
  };

  var initListener = function(){
    $("#selection-speech-compare").change(speechSelectionClicked);
    $("#selection-speech-distribution").change(speechSelectionClicked);
  };

  var speechSelectionClicked = function(){
    $(that).trigger("SpeechSelectionClicked");
  };

  var renderCurve = function(distribution, catDistribution, authorDistribution){
    if(compareSelection == 'Kein Vergleich'){
      if(speechDistributionSelection == "Absolut"){
        renderCurveNormal(distribution, "Absolute Häufigkeit", "absolut");
      }
      if(speechDistributionSelection == "Relativ"){
        var distributionInPercent = distributionToPercent(distribution);
        renderCurveNormal(distributionInPercent, "Relative Häufigkeit in Prozent", "in Prozent");
      }
    }
    if(compareSelection == 'Typ'){
      if(speechDistributionSelection == "Absolut"){
        renderTypeCurve(catDistribution, "Absolute Häufigkeit");
      }
      if(speechDistributionSelection == "Relativ"){
        var catDisInPercent = distributionToPercent(catDistribution);
        renderTypeCurve(catDisInPercent, "Relative Häufigkeit in Prozent");
      }    
    }
    if(compareSelection == 'Autor'){
      if(speechDistributionSelection == "Absolut"){
        renderTypeCurve(authorDistribution, "Absolute Häufigkeit");
      }
      if(speechDistributionSelection == "Relativ"){
        var authorDisInPercent = distributionToPercent(authorDistribution);
        console.log(authorDisInPercent);
        renderTypeCurve(authorDisInPercent, "Relative Häufigkeit in Prozent");
      }  
    }
  };

  var distributionToPercent = function(distribution){
    var disToPercent = {};

    if(distribution.length === undefined){
      for(key in distribution){
        disToPercent[key] = (distribution[key]/distribution.total)*100;
      }
    }else{
      disToPercent = []; 
      for(var i = 0; i < distribution.length; i++){
        distributionObject = {};

        for(key in distribution[i]){
          distributionObject[key] = (distribution[i][key]/distribution[i].total)*100;
        }
        distributionObject.type = distribution[i].type;
        distributionObject.name = getLastNameAndFirstInitial(distribution[i].name);
        disToPercent.push(distributionObject);
      }
    }
    return disToPercent;
  };

	var renderCurveNormal = function(distribution, frequencyType, toolExtension){
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Replikenlänge in Worten");
		data.addColumn("number", 'Replikenhäufigkeit ' + toolExtension);
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
          title: 'Replikenlängenverteilung, ' + frequencyType,
          curveType: 'function',
          legend: {
          	position: 'none'
          },
          hAxis : {
          	title: 'Replikenlänge in Worten'
          },
          vAxis: {
          	title: frequencyType,
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

  var renderTypeCurve = function(typeDistribution, frequencyType){

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
          title: 'Replikenlängen, ' + frequencyType,
          curveType: 'function',
          hAxis : {
            title: 'Replikenlänge in Worten'
          },
          vAxis: {
            title: frequencyType,
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

  var setSpeechDistributionSelection = function(){
    speechDistributionSelection =  $("#selection-speech-distribution").val();
  };

  var getLastNameAndFirstInitial = function(author){
    var authorLastName = author.slice(0, author.indexOf(","));
    var commaIndex = author.indexOf(",");
    var initial = author.slice(commaIndex+1, commaIndex+3);
    author = authorLastName + "," + initial + ".";
    return author;
  };

	that.renderCurve = renderCurve;
  that.renderTypeCurve = renderTypeCurve;
  that.setSpeechDistributionSelection = setSpeechDistributionSelection;
  that.init = init;
  that.setSpeechCompareSelection = setSpeechCompareSelection;

	return that;
};