// Splits the given text into text chunks separated by punctuation delimiters
function splitIntoChunks(text) {
	var minChunkSize = 0;
	var re = /[。、]/g;
	var result = new Array();
	var lastFoundPos = 0;
	var lastChoppedPos = 0;
	var match = null;
	while ((match = re.exec(text)) != null) {
		if(lastChoppedPos + minChunkSize <= match.index) {
			result.push(text.substring(lastChoppedPos, match.index + 1));
			lastChoppedPos = match.index + 1;
		}
		lastFoundPos = match.index + 1;
	}
	if(lastFoundPos < text.length) {
		result.push(text.substring(lastFoundPos));
	}
	return result;
}

// Object to arrange a series of incoming chunks in the correct order.
// E.g. 3, 2, 1 -> 1, 2, 3
var ChunkMerger = (function(callback) {

    function ChunkMerger(callback){
        this._callback = callback;
		this._receivedChunks = new Array();
		this._startIndex = 0;
    };
	
	// Ctor
	// Arguments:
	//     callback - function to call once a series of chunks is complete
	ChunkMerger.prototype.setCallback = function(callback) {
		this._callback = callback;
		}

    // Adds a new chunk
	// Arguments:
	//  index - index of the chunk in the overall array, starting from 0
	//  text - contents of the chunk, may have any type
    ChunkMerger.prototype.addChunk = function(index, text) {
		if(index < this._startIndex) {
			console.error("Input index is out of the expected bound: " 
						+ index.toString() + ", " + this._startIndex.toString());
			return;
		}
		
		index -= this._startIndex;
        for(var i = this._receivedChunks.length; i <= index; ++i) {
			this._receivedChunks.push(null);
		}
		if(this._receivedChunks[index] == null) {
			this._receivedChunks[index] = text;
		}
		else {
			console.error("Chunk #" + (index + this._startIndex).toString() + " already received");
			return;
		}
		while(this._receivedChunks.length) {
			if(this._receivedChunks[0] != null) {
				this._callback(this._receivedChunks[0]);
				this._receivedChunks.shift();
				++this._startIndex;
			}
			else {
				return;
			}
		}
		for(var i = 0; i < index; ++i) {
			if(this._receivedChunks[index] == null) {
				return;
			}
		}		
    };

    return ChunkMerger;
})();

function populateTable(data) {
	if($('#wordtable > thead > tr').length == 0)
	{
		headRow = $('<tr></tr>').append("<th>Word</th>")
								.append("<th>Reading</th>")
								.append("<th>Definition</th>")
								.append("<th>Example</th>");
		$('#wordtable > thead:last').append(headRow);
	}
	var table = $('#wordtable > tbody:last');
	data.forEach( function (element, row) {
		var row = $('<tr></tr>').addClass(row % 2 ? "odd" : "even");
		element.forEach( function (cellText, column) {
			var cell = "<td>" + cellText + "</td>";
			row.append(cell);
		});
		table.append(row);
	});
}

