MultipleDramas.AuthorView = function(){
	var that = {};
	var authorSelection = "";
	var authorAttribute = "";

	var init = function(){
		initListener();
	};

	var initListener = function(){
		$("#selection-author").change(authorSelectionClicked);
	};

	var authorSelectionClicked = function(){
		$(that).trigger("AuthorSelectionClicked");
	};

	var renderBarChart = function(authors){
		var data = new google.visualization.DataTable();
		data.addColumn("string", "Autor");
		data.addColumn("number", authorSelection);
		data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
		authors.sort(sort_by(authorAttribute,true));
		var array = [];
		for(i = 0; i < authors.length; i++){
			var row = [getLastNameAndFirstInitial(authors[i].name), authors[i][authorAttribute],
			createTooltip(authors[i])];
			array.push(row);
		}
		data.addRows(array);

		var estimatedHeight = authors.length * 30;
		if(estimatedHeight < 300){
			estimatedHeight = 300;
		}

		var options = {title:'Autorenvergleich',
        			   height: estimatedHeight,
        			   tooltip: { isHtml: true },
        			   chartArea:{width:'55%',height:'90%'},
				        hAxis: {
        			   	title: authorSelection
        			   },
        			   animation: {
                   	   	duration: 700,
                   	   },
        			   vAxis: {
        			   	baseline: 0
        			   }};

        // Create a dashboard.
        var dashboard = new google.visualization.Dashboard(
            document.getElementById('dashbord-author'));

        // Create a range slider, passing some options
        var barChartRangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'filter-author',
          'options': {
            'filterColumnLabel': authorSelection
          }
        });

        var barChart = new google.visualization.ChartWrapper({
          'chartType': 'BarChart',
          'containerId': 'chart-author',
          'options': options
        });

        $("#download-png-author").unbind("click");
        $("#download-png-author").on("click", function(){
          window.open(barChart.getChart().getImageURI());
        });

        dashboard.bind(barChartRangeSlider, barChart);

        // Draw the dashboard.
        dashboard.draw(data);
	};

	var setAuthorSelection = function(){
		authorSelection = $("#selection-author").val();

		if(authorSelection == "Szenenanzahl"){authorAttribute = "average_number_of_scenes"};
		if(authorSelection == "Replikenanzahl"){authorAttribute = "average_number_of_speeches";}
		if(authorSelection == "Sprecheranzahl"){authorAttribute = "average_number_of_speakers";}
		if(authorSelection == "Konfigurationsdichte"){authorAttribute = "average_configuration_density";}
		if(authorSelection == "Durchschnittliche Replikenlänge"){authorAttribute = "average_average_length_of_speeches";}
		if(authorSelection == "Median Replikenlänge"){authorAttribute = "average_median_length_of_speeches";}
		if(authorSelection == "Maximum Replikenlänge"){authorAttribute = "average_maximum_length_of_speeches";}
		if(authorSelection == "Minimum Replikenlänge"){authorAttribute = "average_minimum_length_of_speeches";}
	};

	var getLastNameAndFirstInitial = function(author){
		var authorLastName = author.slice(0, author.indexOf(","));
		var commaIndex = author.indexOf(",");
		var initial = author.slice(commaIndex+1, commaIndex+3);
		author = authorLastName + "," + initial + ".";
		return author;
	};

	var createTooltip = function(author){
		var divBegin = "<div class='tooltip-test'>"
		var authorDiv = "<div>" + "<b>" + author.name + "</b>" + "</div>";
		var data = "<div>" + "<b>" + authorSelection + ": </b>" + author[authorAttribute] + "</div>";
		var dramas = "<div><b>Dramen:</b> ";
		for(var i = 0; i < author.titles.length; i++){
			dramas = dramas + "'" + author.titles[i] + "'" + " ,";
		}
		dramas = dramas.substring(0, dramas.length - 1);
		dramas = dramas + "</div>";
		var divEnd = "</div>";
		return (divBegin + authorDiv + data + dramas + divEnd); 
	};

	var sort_by = function(field, reverse, primer){

   		var key = primer ? 
        function(x) {return primer(x[field])} : 
       	function(x) {return x[field]};

   		reverse = !reverse ? 1 : -1;

   		return function (a, b) {
       	return a = key(a), b = key(b), reverse * ((a > b) - (b > a));
     	} 
	};

	that.renderBarChart = renderBarChart;
	that.setAuthorSelection = setAuthorSelection;
	that.init = init;

	return that;
};