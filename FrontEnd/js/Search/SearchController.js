Search.SearchController = function(){
	var that = {};

	var dramaListModel = null;
	var dramaListView =null;
	var formsView = null;

	var init = function(){
		dramaListModel = Search.DramaListModel();
		dramaListModel.init();

		dramaListView = Search.DramaListView();
		dramaListView.init();

		formsView = Search.FormsView();

		initListener();
		formsView.init();

	};

	var initListener = function(){
		$(dramaListModel).on("DataRetrieved", updateList);
		$(dramaListModel).on("EmptyTable", emptyTable);
		$(dramaListModel).on("NoResultsFound", noResultsFound);
		$(dramaListModel).on("JSONDramaRetrieved", downloadDramaJSON);
		$(formsView).on("InputCatched", retrieveDramas);
		$(dramaListView).on("DramaClicked", analyzeDrama);
		$(dramaListView).on("AnalyseCollection", analyseCollection);
		$(dramaListView).on("DownloadJSON", startDownloadJSON);
	};

	var startDownloadJSON = function(event, dramaId){
		dramaListModel.getJSONDrama(dramaId);
	};

	var downloadDramaJSON = function(event, dramaJson){

		var data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(dramaJson));
		console.log(dramaJson.title);

		$('<a href="data:' + data + '" download="' + dramaJson.title + '.json"></a>')[0].click();

	};

	var analyseCollection = function(event, checkedDramas){
		localStorage["collection"] = JSON.stringify(checkedDramas);
	};

	var noResultsFound = function(){
		dramaListView.showNoResults();
	};

	var analyzeDrama = function(event, drama_id, title, author, year){

		//Probably not working in every browser
		window.open("drama.html?drama_id=" + drama_id, "_blank");
	};

	var updateList = function(event, listItem){
		dramaListView.renderListItem(listItem);
	};

	var retrieveDramas = function(event, input){
		dramaListModel.retrieveDramas(input);
	};

	var emptyTable = function(){
		dramaListView.emptyTable();
	}

	that.init = init;

	return that;
};