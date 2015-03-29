Speeches.SpeechesDistributionView = function(){
	var that = {};

	var render = function(scenesInfo){

		var data = new google.visualization.DataTable();
		data.addColumn("string", "Replik");
		data.addColumn("number", 'Replikenlänge in Worten');
		var array = [];
		var iterator = 0;
		for(act = 0; act < scenesInfo.length; act++){
			for(scene = 0; scene < scenesInfo[act].length; scene++){
				if(scenesInfo[act][scene].speeches !== undefined){
					for(speech = 0; speech < scenesInfo[act][scene].speeches.length; speech++){
						var row = [getSpeechInfo(act, scene, speech, scenesInfo[act][scene].speeches[speech]), 
						scenesInfo[act][scene].speeches[speech]['length']];
						array.push(row);
						iterator++;
					}
				}
			}
		}
		data.addRows(array);

		var options = {
		  height: 700,
		  width: 1170,
		  animation: {
		  	duration: 1000
		  },
		  legend: {
          	position: 'none'
          },
          hAxis : {
          	title: 'Replikenlänge'
          },
          vAxis: {
          	title: 'Häufigkeit'
          },
		  chartArea:{width:'75%',height:'80%'},
          title: 'Histogramm - Häufigkeitsverteilung der Replikenlängen'
        };

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('distribution-dashbord'));

        var rangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'distribution-controls',
          'options': {
            'filterColumnLabel': 'Replikenlänge in Worten'
          }
        });

        var chart = new google.visualization.ChartWrapper({
          'chartType': 'Histogram',
          'containerId': 'distribution-chart',
          'options': options
        });

        dashboard.bind(rangeSlider, chart);

        dashboard.draw(data);

	};

	var getSpeechInfo = function(actNumber, sceneNumber, speechNumber, speech){
		var info = "Sprecher: " + speech.speaker + ", " + (actNumber + 1) + ". Akt, " + (sceneNumber + 1) + ". Szene, " 
		+ (speechNumber + 1) + ". Replik";
		return info;
	};

	that.render = render;

	return that;
};