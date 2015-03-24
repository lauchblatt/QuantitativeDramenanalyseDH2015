Matrix.MatrixController = function(){
	var that = {};

	var matrixView = null;
	var matrixModel = null;

	var init = function(){
		matrixView = Matrix.MatrixView();
		matrixModel = Matrix.MatrixModel();
		initListener();

		matrixModel.init();
	};

	initListener = function(){
		$(matrixModel).on("ModelInitFinished", buildTable);
	};

	buildTable = function(){
		matrixView.init();
	};

	that.init = init;

	return that;
};