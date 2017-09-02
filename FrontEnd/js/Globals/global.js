var transformGermanMetric = function(name){
		switch(name) {
		    case "Polarität (gewichtet)":
		        return "polaritySentiWS";
		        break;
		    case "Polarität (Wortanzahl)":
		        return "polaritySentiWSDichotom";
		        break;
		    case "Positiv (gewichtet)":
		        return "positiveSentiWS";
		        break;
		    case "Positiv (Wortanzahl)":
		        return "positiveSentiWSDichotom";
		        break;
		    case "Negativ (gewichtet)":
		        return "negativeSentiWS";
		        break;
		    case "Negativ (Wortanzahl)":
		        return "negativeSentiWSDichotom";
		        break;
		    case "Zorn":
		        return "anger";
		        break;
		    case "Erwartung":
		        return "anticipation";
		        break;
		    case "Ekel":
		        return "disgust";
		        break;
		    case "Angst":
		        return "fear";
		        break;
		    case "Freude":
		        return "joy";
		        break;
		    case "Traurigkeit":
		        return "sadness";
		        break;
		    case "Überraschung":
		        return "surprise";
		        break;
		    case "Vertrauen":
		        return "trust";
		        break;
		    case "Emotion vorhanden":
		    	return "emotionPresent";
		    	break;
		    case "Absolut":
		        return "metricsTotal";
		        break;
		    case "Normalisiert an Anzahl aller Wörter":
		        return "metricsNormalisedLengthInWords";
		        break;
		    case "Normalisiert an Sentiment-Tragenden Wörtern":
		        return "metricsNormalisedSBWs";
		        break;
		    case "Emotionen":
		    	return "emotions";
		    	break;
		    case "Verteilung von Sentiment-Tragenden Wörtern":
		    	return "normalisedSBWs";
		    	break;
		    case "Verteilung von allen Wörtern":
		    	return "normalisedAllWords";
		    	break;
		    default:
		    	console.log(name);
		        console.log("ERROR")
		    }
	};

var getProportionDataOfUnit = function(unit){
		var metricsUnit = unit.sentimentMetricsBasic.metricsTotal;
		var polarityWeighted = [["Positiv", metricsUnit.positiveSentiWS], ["Negativ", metricsUnit.negativeSentiWS]];
		var polarityCount = [["Positiv", metricsUnit.positiveSentiWSDichotom],
		["Negativ", metricsUnit.negativeSentiWSDichotom]];
		var emotion = [["Zorn", metricsUnit.anger], ["Erwartung", metricsUnit.anticipation], 
		["Ekel", metricsUnit.disgust], ["Angst", metricsUnit.fear], ["Freude", metricsUnit.joy],
		["Traurigkeit", metricsUnit.sadness], ["Überraschung", metricsUnit.surprise],
		["Vertrauen", metricsUnit.trust]];
		var emotionPresent = [["Emotion vorhanden", metricsUnit.emotionPresent]];

		var proportionData = {}
		proportionData["normalisedSBWs"] = {};
		proportionData["normalisedSBWs"]["polaritySentiWS"] = polarityWeighted;
		proportionData["normalisedSBWs"]["polaritySentiWSDichotom"] = polarityCount;
		proportionData["normalisedSBWs"]["emotions"] = emotion;
		proportionData["normalisedSBWs"]["emotionPresent"] = emotionPresent

		
		var noPolarityWords = unit.lengthInWords - 
		(metricsUnit.positiveSentiWSDichotom + metricsUnit.negativeSentiWSDichotom);
		var noEmotionWords = unit.lengthInWords - metricsUnit.emotionPresent;

		var polarityCountCopy = polarityCount.slice();
		var emotionCopy = emotion.slice();
		var emotionPresentCopy = emotionPresent.slice();

		polarityCountCopy.push(["Keine Polarität", noPolarityWords]);
		emotionCopy.push(["Keine Emotion", noEmotionWords]);
		emotionPresentCopy.push(["Keine Emotion", noEmotionWords]);

		proportionData["normalisedAllWords"] = {};
		proportionData["normalisedAllWords"]["polaritySentiWSDichotom"] = polarityCountCopy;
		proportionData["normalisedAllWords"]["emotions"] = emotionCopy;
		proportionData["normalisedAllWords"]["emotionPresent"] = emotionPresentCopy;

		return proportionData;

	};