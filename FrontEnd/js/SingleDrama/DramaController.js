SingleDrama.DramaController = function(){
	var that = {};

	var dramaModel = null;
	var tableDramaView = null;

	var init = function(){

		dramaModel = SingleDrama.DramaModel();
		tableDramaView = SingleDrama.TableDramaView();

		dramaModel.init();

		initListener();

	};

	var initListener = function(){
		$(dramaModel).on("ActsInfoFinished", visuAct);
	};

	var visuAct = function(event, actInfo){
		console.log(actInfo);
		tableDramaView.renderAct(actInfo);
	};

	that.init = init;

	return that;
};