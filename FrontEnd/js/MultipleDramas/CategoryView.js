MultipleDramas.CategoryView = function(){
	var that = {};
	var categorySelection = "";
	var categoryAttribute = "";

	var init = function(){
		initListener();
	};

	var initListener = function(){
		$("#selection-category").change(categorySelectionClicked);
	};

	var renderColumnChart = function(categories){
		var data = new google.visualization.DataTable();
        data.addColumn('string', 'Typ');
        data.addColumn('number', categorySelection);
        var array = [];
        for(var i = 0; i < categories.length; i++){
        	var row = [categories[i].type, categories[i][categoryAttribute]];
			array.push(row);
        }
        data.addRows(array);
        var options = {title:'Typ-Vergleich',
        			   height: 600,
        			   width: 1000,
				        hAxis: {
        			   	title: 'Drama-Typ'
        			   },
        			   vAxis: {
        			   	title: categorySelection
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};
        var chart = new google.visualization.ColumnChart(document.getElementById('chart-category'));

        $("#download-png-category").unbind("click");
        $("#download-png-category").on("click", function(){
          window.open(chart.getImageURI());
        });

        chart.draw(data, options);
	};

	var categorySelectionClicked = function(){
		$(that).trigger("CategorySelectionClicked");	
	};

	var setCategorySelection = function(){
		categorySelection = $("#selection-category").val();

		if(categorySelection == "Szenenanzahl"){categoryAttribute = "average_number_of_scenes"};
		if(categorySelection == "Replikenanzahl"){categoryAttribute = "average_number_of_speeches";}
		if(categorySelection == "Sprecheranzahl"){categoryAttribute = "average_number_of_speakers";}
		if(categorySelection == "Konfigurationsdichte"){categoryAttribute = "average_configuration_density";}
		if(categorySelection == "Durchschnittliche Replikenlänge"){categoryAttribute = "average_average_length_of_speeches";}
		if(categorySelection == "Median Replikenlänge"){categoryAttribute = "average_median_length_of_speeches";}
		if(categorySelection == "Maximum Replikenlänge"){categoryAttribute = "average_maximum_length_of_speeches";}
		if(categorySelection == "Minimum Replikenlänge"){categoryAttribute = "average_minimum_length_of_speeches";}

	};

	that.init = init;
	that.setCategorySelection = setCategorySelection;
	that.renderColumnChart = renderColumnChart;

	return that;
};