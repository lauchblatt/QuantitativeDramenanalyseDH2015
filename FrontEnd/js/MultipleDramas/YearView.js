MultipleDramas.YearView = function(){
	var that = {};
	var yearSelection = "";
	var yearAttribute = "";
	var compareSelection = "";

	var init = function(){
		initListener();
	};

	var initListener = function(){
		$("#selection-year").change(yearSelectionClicked);
		$("#selection-year-compare").change(yearSelectionCompareClicked);
	};

	var yearSelectionClicked = function(){
		$(that).trigger("YearSelectionClicked");
	};

	var yearSelectionCompareClicked = function(){
		$(that).trigger("YearSelectionCompareClicked");
	};

	var renderScatterChart = function(dramas, authors){
		if(compareSelection == 'Kein Vergleich'){
			renderScatterChartNormal(dramas);
		}
		if(compareSelection == 'Typ'){
			renderScatterChartType(dramas);
		}
		if(compareSelection == 'Autor'){
			renderScatterChartAuthor(dramas, authors);
		}
	};

	var renderScatterChartNormal = function(dramas){
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Jahr");
		data.addColumn("number", yearSelection);
		data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
		var array = [];
		for(i = 0; i < dramas.length; i++){
			var row = [dramas[i].year, dramas[i][yearAttribute],
			createTooltip(dramas[i])];
			array.push(row);
		}
		data.addRows(array);

		var options = {
          title: 'Epochenverlauf',
          height: 700,
          width: 1170,
          explorer: {},
          tooltip: { isHtml: true },
          hAxis: {title: 'Jahr', format: ' '},
          vAxis: {title: yearSelection},
          legend: 'none',
          chartArea:{width:'75%',height:'80%'},
          trendlines: {
				          0: {
				          	tooltip: false,
				            type: 'polynomial',
				            color: 'green',
				            lineWidth: 3,
				            opacity: 0.3,
				            showR2: false,
				            visibleInLegend: false
				          }
				        }
        };
        var optionsSlider = {
        	filterColumnLabel: 'Jahr',
        	ui: {
        		chartType: 'ScatterChart',
        		chartOptions: {
        			height: 100,
        			width: 1170,
        			chartArea:{width:'75%',height:'80%'},
        			hAxis: {title: 'Jahr', format: ' '}
        		}
        	}
        };

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('dashbord-year'));

        var rangeSlider1 = new google.visualization.ControlWrapper({
          'controlType': 'ChartRangeFilter',
          'containerId': 'controls-year1',
          'options': optionsSlider
        });

        var rangeSlider2 = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'controls-year2',
          'options': {
            'filterColumnLabel': yearSelection
          }
        });

        var chart = new google.visualization.ChartWrapper({
          'chartType': 'ScatterChart',
          'containerId': 'chart-div-year',
          'options': options
        });

        dashboard.bind(rangeSlider1, chart);
        dashboard.bind(rangeSlider2, chart);
        $("#controls-year2").fadeIn();
        dashboard.draw(data);
	};

	var renderScatterChartAuthor = function(dramas, authors){
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Jahr");
		for(var i = 0; i < authors.length; i++){
			data.addColumn("number", getLastNameAndFirstInitial(authors[i].name));
			data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
		}
		var array = [];
		var rowLength = ((authors.length*2)+1);
		for(var i = 0; i < dramas.length; i++){
			var row = [];
			for(var j = 0; j < rowLength; j++){
				row.push(null);
			}
			for(var k = 0; k < authors.length; k++){
				if(dramas[i].author == authors[k].name){
					row[0] = dramas[i].year;
					row[(k*2) + 1] = dramas[i][yearAttribute];
					row[(k*2) + 2] = createTooltip(dramas[i]);
					array.push(row);
					}
				}	
			}
		data.addRows(array);

		var options = {
          title: 'Epochenverlauf',
          height: 700,
          width: 1170,
          explorer: {},
          tooltip: { isHtml: true },
          hAxis: {title: 'Jahr', format: ' '},
          vAxis: {title: yearSelection},
          chartArea:{width:'75%',height:'80%'}
        };

        var optionsSlider = {
        	filterColumnLabel: 'Jahr',
        	ui: {
        		chartType: 'ScatterChart',
        		chartOptions: {
        			height: 100,
        			width: 1170,
        			chartArea:{width:'75%',height:'80%'},
        			hAxis: {title: 'Jahr', format: ' '}
        		}
        	}
        }

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('dashbord-year'));

        var rangeSlider1 = new google.visualization.ControlWrapper({
          'controlType': 'ChartRangeFilter',
          'containerId': 'controls-year1',
          'options': optionsSlider
        });

        var chart = new google.visualization.ChartWrapper({
          'chartType': 'ScatterChart',
          'containerId': 'chart-div-year',
          'options': options
        });

        dashboard.bind(rangeSlider1, chart);

        $("#controls-year2").fadeOut();
        dashboard.draw(data);

	};

	var renderScatterChartType = function(dramas){
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Jahr");
		data.addColumn("number", 'Komoedie');
		data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
		data.addColumn("number", 'Schauspiel');
		data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
		data.addColumn("number", 'Trauerspiel');
		data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});

		var array = [];
		for(i = 0; i < dramas.length; i++){
			if(dramas[i].type == 'Komoedie'){
				var row = [dramas[i].year, dramas[i][yearAttribute], createTooltip(dramas[i]), null, null, null, null ];
				array.push(row);
			}
			if(dramas[i].type == 'Schauspiel'){
				var row = [dramas[i].year, null, null, dramas[i][yearAttribute], createTooltip(dramas[i]), null, null];
				array.push(row);
			}
			if(dramas[i].type == 'Trauerspiel'){
				var row = [dramas[i].year, null, null, null, null, dramas[i][yearAttribute], createTooltip(dramas[i])];
				array.push(row);
			}
		}
		data.addRows(array);

		var options = {
          title: 'Epochenverlauf',
          height: 700,
          width: 1170,
          explorer: {},
          tooltip: { isHtml: true },
          hAxis: {title: 'Jahr', format: ' '},
          vAxis: {title: yearSelection},
          chartArea:{width:'75%',height:'80%'},
          trendlines: {
				          0: {
				          	tooltip: false,
				            type: 'polynomial',
				            color: 'blue',
				            lineWidth: 3,
				            opacity: 0.3,
				            showR2: false,
				            visibleInLegend: false
				          },
				          1: {
				          	tooltip: false,
				            type: 'polynomial',
				            color: 'red',
				            lineWidth: 3,
				            opacity: 0.3,
				            showR2: false,
				            visibleInLegend: false
				          },
				          2: {
				          	tooltip: false,
				            type: 'polynomial',
				            color: 'yellow',
				            lineWidth: 3,
				            opacity: 0.3,
				            showR2: false,
				            visibleInLegend: false
				          }
				        }
        };

        var optionsSlider = {
        	filterColumnLabel: 'Jahr',
        	ui: {
        		chartType: 'ScatterChart',
        		chartOptions: {
        			height: 100,
        			width: 1170,
        			chartArea:{width:'75%',height:'80%'},
        			hAxis: {title: 'Jahr', format: ' '}
        		}
        	}
        }

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('dashbord-year'));

        var rangeSlider1 = new google.visualization.ControlWrapper({
          'controlType': 'ChartRangeFilter',
          'containerId': 'controls-year1',
          'options': optionsSlider
        });

        var chart = new google.visualization.ChartWrapper({
          'chartType': 'ScatterChart',
          'containerId': 'chart-div-year',
          'options': options
        });

        dashboard.bind(rangeSlider1, chart);
        $("#controls-year2").fadeOut();
        dashboard.draw(data);
	};

	var createTooltip = function(drama){
		var divBegin = "<div class='tooltip-test'>"
		var headline = "<div>" + "'" + drama.title + "'" + " von <em>" + getLastName(drama.author) + "</em></div>";
		var year = "<div>" + "<b>Jahr: </b>" + drama.year + "</div>";
		var data = "<div>" + "<b>" + yearSelection + ": </b>" + drama[yearAttribute] + "</div>";
		var divEnd = "</div>";
		return (divBegin + headline + year + data + divEnd); 
	};

	var setYearSelection = function(){
		yearSelection = $("#selection-year").val();

		if(yearSelection == "Szenenanzahl"){yearAttribute = "number_of_scenes"};
		if(yearSelection == "Replikenanzahl"){yearAttribute = "number_of_speeches_in_drama";}
		if(yearSelection == "Sprecheranzahl"){yearAttribute = "speaker_count"};
		if(yearSelection == "Konfigurationsdichte"){yearAttribute = "configuration_density";}
		if(yearSelection == "Durchschnittliche Replikenlänge"){yearAttribute = "average_length_of_speeches_in_drama";}
		if(yearSelection == "Median Replikenlänge"){yearAttribute = "median_length_of_speeches_in_drama";}
		if(yearSelection == "Maximum Replikenlänge"){yearAttribute = "maximum_length_of_speeches_in_drama";}
		if(yearSelection == "Minimum Replikenlänge"){yearAttribute = "minimum_length_of_speeches_in_drama";}
		
	};

	var setYearCompareSelection = function(){
		compareSelection = $("#selection-year-compare").val();	
	};

	var getLastName = function(author){
		author = author.slice(0, author.indexOf(","));
		return author;
	};

	var getLastNameAndFirstInitial = function(author){
		var authorLastName = author.slice(0, author.indexOf(","));
		var commaIndex = author.indexOf(",");
		var initial = author.slice(commaIndex+1, commaIndex+3);
		author = authorLastName + "," + initial + ".";
		return author;
	};

	that.renderScatterChart = renderScatterChart;
	that.setYearSelection = setYearSelection;
	that.setYearCompareSelection = setYearCompareSelection;
	that.init = init;

	return that;
};