var gVar;

function init() {

	var searchBox = document.getElementById('searchText'),
		$sBoxObj = $(searchBox),
		$asObj = $('#autoSuggestDiv');

	searchBox.addEventListener('input',function(e){
		
		var searchQuery = e.target.value,
			asQueryObj = getWordAtPosition(searchQuery,e.target.selectionStart);

		$asObj.hide();
		resetResults('Your software libraries search results will appear here!');

		if (e.target.value.slice(-1) != ' ' && $.trim(e.target.value) != '' && $.trim($asObj.text()) != asQueryObj.word)
		{	
			if(asQueryObj.partial_word.length >= 3) 
			{
				autoSuggest(e.target,asQueryObj);
			}
		}
	});

	$asObj.css('top',($sBoxObj.offset().top + $sBoxObj.outerHeight()).toString()+'px');

	function acceptAutoSuggest() {
		var currentQuery = $sBoxObj.val(),
			cursorPos = searchBox.selectionStart,
			curwordObj = getWordAtPosition(currentQuery,cursorPos),
			asText = $.trim($asObj.text());

		$sBoxObj.val(currentQuery.replace(curwordObj.word,asText));

		searchBox.selectionStart = curwordObj.end + asText.length - curwordObj.word.length;
		searchBox.selectionEnd = curwordObj.end + asText.length - curwordObj.word.length;	

		setTimeout(function(){
	        $sBoxObj.focus();
	    }, 1);

		$asObj.hide();
	}

	$(document).keydown(function(e) {

		if($('#searchText').is(':focus'))
		{
			var keynum;
			
			if(window.event) 
			{ // IE					
            	keynum = e.keyCode;
            }
            else if(e.which)
            { // Netscape/Firefox/Opera					
            	keynum = e.which;
            }
            
	    	if(keynum == 13) 
	    	{ // Enter key is pressed
	        	sendSearchRequest();
	        	return;
	    	}
	    	else if(keynum == 9 || keynum == 39)
	    	{
	    		if($asObj.css('display') != 'none')
				{
	    			acceptAutoSuggest();
	    			if(keynum == 9)
	    				e.preventDefault();
	    		}
	    	}    
        }
	    
	});

	$('#searchButton').click(function(i,obj){
		sendSearchRequest();
	});

	setTimeout(function(){
        $sBoxObj.focus();
    }, 1);

    $asObj.click(function(){
		acceptAutoSuggest();
	});

}

function getWordAtPosition(inputString, cPosition) {
	var i = cPosition,
		j = cPosition,
		wordObj = {};

	while(i > 0 && inputString[i-1] != ' ') {
		i--;
	}

	while(j < inputString.length && inputString[j] != ' ') {
		j++;
	}

	wordObj['word'] = inputString.slice(i,j);
	wordObj['start'] = i;
	wordObj['end'] = j;
	wordObj['partial_word'] = inputString.slice(i,cPosition);

	return wordObj;
}

function autoSuggest(inputObj,asWordObj) {
	var $sBoxObj = $(inputObj),
		$asObj = $('#autoSuggestDiv'),
		asFixedLeft = $sBoxObj.offset().left + parseInt($sBoxObj.css('padding-left').replace('px','')),
		asFixedOffset = parseInt($sBoxObj.css('padding-left').replace('px','')),
		asOffset = $('#asSizeCheck')
						.css('display','none')
						.css('color','#fff')
						.css('position','absolute')
						.css('font-size',$sBoxObj.css('font-size'))
						.css('width','auto')
						.html($sBoxObj.val().slice(0,asWordObj.start))
						.width();

		asOffset = asWordObj.start > 0 ? asOffset : asOffset - 2; 

		$asObj.css('left',(asFixedLeft+asOffset+1).toString()+'px');
	$.ajax({
		type: "GET",
		url: URL,
		data: {'q': asWordObj.word, 'as': 'true'},
		success: function(data) {
			
			console.log(data);
			if(data.length > 0)
			{
				if(data[0] != asWordObj.word)
				{
					cleanPartialWord = asWordObj.partial_word.replace(/\W+/g,'');
					if(data[0].indexOf(cleanPartialWord) != -1)
					{
						$asObj.html('&nbsp;'+cleanPartialWord+'<b>'+data[0].replace(cleanPartialWord,'')+'</b>'+'&nbsp;')
					}
					else
					{
						$asObj.html('&nbsp;'+data[0]+'&nbsp;')
					}
					$asObj.show();
				}
			}
		}
	})
}

function resetResults(msg) {
	var resultsContainer = $('#searchResults');
	resultsContainer.empty();
	$('#searchMetrics').empty();
	resultsContainer.append($('<h2/>').html(msg));
}

function sendSearchRequest() {
	var queryText = $("#searchText").val(),
		searchResults = [],
		ndcgValues = [];

	$('#autoSuggestDiv').hide();
	
	if($.trim(queryText) == '')
		return;

	var startTime = new Date().getTime();
	$('.search-option img').show();

	$.ajax({
		type: "GET",
		url: URL,
		data: {'q': queryText, 'os': $('#targetOSSelect').val(), 'lang': $('#languageSelect').val()}, 
		success: function(data) {
			console.log(JSON.stringify(data));
			gVar = data;
			$('.search-option img').hide();
			if(data){
			    try{
			        searchResults = data["results"];
			        ndcgValues = data["ndcg_values"];	        
			    }
			    catch(e){
			        alert(e); 
			    }
			}
			else
			{
				resetResults('No results found for '+queryText+'.');
				return;
			}
			var endTime = new Date().getTime();

			resultsContainer = $('#searchResults');
			resultsContainer.empty();
			var resultRow,
				urlTitle = '',
				url = '',
				resultsHeader = $('<div/>').append(
									$('<h3/>')
										.html("Results for <i>"+queryText+"</i> : ")
										.addClass('results-header')
								);
			resultsContainer.append(resultsHeader);

			for(var i = 0; i < searchResults.length; i++) {
				
				url = searchResults[i]['url'];
				urlTitle =  searchResults[i]['title'].length == 0 ? url.replace('http://','') : searchResults[i]['title'];
				
				var resultRow = $('<div/>').append(
											$('<label/>')
												.append($('<a/>').html(urlTitle).attr('href',url).addClass(''))
												.addClass('result-title')
								),
					snippetText = '',
					snippetRow = $('<p/>').addClass('result-snippet');

				if(searchResults[i]["snippet"].length > 0)
				{
					for(var j=0; j < searchResults[i]["snippet"].length; j++)
					{
						snippetText += searchResults[i]["snippet"][j] + '...';
					}
					snippetText = snippetText.slice(0,250)+'...';
					snippetRow.html(snippetText);

					resultRow.append(snippetRow)
				}

				$(resultRow).hide().appendTo(resultsContainer).fadeIn(i*100);
				//resultsContainer.append(resultRow);
			}

			var execTime = (endTime - startTime)/1000,
				execTimeHTML = "<h4>Retrieval time : "+execTime.toString()+' s</h4>',
				ndcgHTML = '',
				headerHTML = '<h3>Search Metrics</h3><br>';

			if(ndcgValues.length > 0)
			{
				ndcgHTML = "<h4>NDCG @ 10 : "+ndcgValues[ndcgValues.length-1]+"</h4>";
			}

			metricsContainer = $('#searchMetrics');
			metricsContainer.empty();
			$metricRow = $('<div/>').html(headerHTML+execTimeHTML+ndcgHTML);
			metricsContainer.append($metricRow);

			$('#searchText').blur();
		}
	})
}