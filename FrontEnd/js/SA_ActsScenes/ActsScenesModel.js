ActsScenes.ActsScenesModel = function(){
	var that = {};
	var metricsActs = [];
	var metricsScenes = []

	var init = function(){
		initData()

	};

	var initData = function(){
		console.log(sa_data);
		var drama = sa_data[0];
		for(i = 0; i < drama.acts.length; i++){
			metricsActs.push(drama.acts[i].sentimentMetricsBasic)
		}
	};

	var getMetricsActs = function(){
		return metricsActs
	};


	that.init = init;
	that.getMetricsActs = getMetricsActs

	return that;
};