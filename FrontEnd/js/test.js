var initGoogleCharts = function(){
		// Load the Visualization API and the piechart package.
      	setTimeout(function(){google.load('visualization', '1', {'callback': continueInit, 
      		'packages':['corechart', 'controls']})}, 0);
	};

var genderArray = [];
var heritageArray = [];
var birthYearArray = [];
var deathYearArray = [];
var arrivalYearArray = [];

initGoogleCharts();

var continueInit = function(){
	keys = []

	male = 0;
	female = 0;
	abstammung = {};
	geburtsjahr = {};
	todesjahr = {};
	ankunftsjahr = {};

	for(var i = 0; i < testData.length; i++){
		male = male + testData[i].geschlecht.m
		female = female + testData[i].geschlecht.w
		
		for(abstammungsTyp in testData[i].abstammung){
			if(abstammung[abstammungsTyp] == undefined){
				abstammung[abstammungsTyp] = testData[i].abstammung[abstammungsTyp];
			}else{
				abstammung[abstammungsTyp] = abstammung[abstammungsTyp] + testData[i].abstammung[abstammungsTyp]
			}
		}

		for(geburtsjahrTyp in testData[i].geburtsjahr){
			if(geburtsjahr[geburtsjahrTyp] == undefined){
				geburtsjahr[geburtsjahrTyp] = testData[i].geburtsjahr[geburtsjahrTyp];
			}else{
				geburtsjahr[geburtsjahrTyp] = geburtsjahr[geburtsjahrTyp] + testData[i].geburtsjahr[geburtsjahrTyp]
			}
		}

		for(todesjahrTyp in testData[i].todesjahr){
			if(todesjahr[todesjahrTyp] == undefined){
				todesjahr[todesjahrTyp] = testData[i].todesjahr[todesjahrTyp];
			}else{
				todesjahr[todesjahrTyp] = todesjahr[todesjahrTyp] + testData[i].todesjahr[todesjahrTyp]
			}
		}
		if(testData[i].ankunft.year != null){
			console.log(testData[i]["ankunft"]["year"]);
			if(ankunftsjahr[testData[i]["ankunft"]["year"]["$numberLong"]] == undefined){
				ankunftsjahr[testData[i]["ankunft"]["year"]["$numberLong"]] = 1;
			}else{
				ankunftsjahr[testData[i]["ankunft"]["year"]["$numberLong"]] = ankunftsjahr[testData[i]["ankunft"]["year"]["$numberLong"]] + 1;
			}
		}else{
		
		}
	}
	genderArray = [['Gender', 'Count'],['Male', male],['Female', female]];
	heritageArray.push(["Heritage", "Count"]);
	birthYearArray.push(["BirthYear", "Count"]);
	deathYearArray.push(["DeathYear", "Count"]);
	arrivalYearArray.push(["ArrivalYear", "Count"]);

	
	for (typ in abstammung){
		heritageArray.push([typ, abstammung[typ]]);
	}

	for (jahr in geburtsjahr){
		birthYearArray.push([jahr, geburtsjahr[jahr]]);
	}

	for (jahr in todesjahr){
		deathYearArray.push([jahr, todesjahr[jahr]]);
	}

	for (jahr in ankunftsjahr){
		arrivalYearArray.push([jahr, ankunftsjahr[jahr]]);
	}
	console.log(arrivalYearArray);
	$("#pie-metric").change(drawPieChart);
	drawPieChart();
};

	var drawPieChart = function(){

			var name = "";

			var dataTable = [];

			var selection = $("#pie-metric-selection").val();
			if(selection == "Gender"){
				dataTable = genderArray;
				name = selection;
			}
			if(selection == "Descent"){
				dataTable = heritageArray;
				name = selection;
			}

			if(selection == "Birth year"){
				dataTable = birthYearArray;
				name = selection;
			}

			if(selection == "Death year"){
				dataTable = deathYearArray;
				name = selection;
			}

			if(selection == "Arrivel"){
				dataTable = arrivalYearArray;
				name = selection;
			}

			var data = google.visualization.arrayToDataTable(dataTable);
	        var options = {
			  height: 600,
	      		width: 1000,
	      		chartArea:{width:'70%',height:'75%'},
	          	title: name,
	          	is3D: true,
	          	animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }
	        	};
	        var chart = new google.visualization.PieChart(document.getElementById('genderPie'))
	        chart.draw(data, options);
		};
