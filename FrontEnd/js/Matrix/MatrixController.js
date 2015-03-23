Matrix.MatrixController = function(){
	var that = {};

	var matrixView = null;
	var matrixModel = null;

	var init = function(){
		matrixView = Matrix.MatrixView();
		matrixModel = Matrix.MatrixModel();

		matrixModel.init();
	};

	that.init = init;

	return that;
};