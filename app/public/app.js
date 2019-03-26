// This function gets search results from the search api and fills the results area
onSearchClick = function() {
    // Setup
    var baseUrl = 'http://localhost:3000';
    var hitsLabel = document.getElementById('num-hits');
    var searchResults = document.getElementById('search-hits');
    var term = document.getElementById('txt-search').value
    var match = document.getElementById('txt-match').value
    var lastTerm = document.getElementById('cur-term')
    var nextButton = document.getElementById('next-page')
    var prevButton = document.getElementById('prev-page')

    // Check if this is a new search term
    if (term != lastTerm.value)
    {
        searchResults.start = 1;
        lastTerm.value = term;
    }

    // Get  search results using search api
    fetch(baseUrl.concat('/search?term='+ term + '&match_term=' + match.toString().trim() + '&offset=' + (searchResults.start-1).toString()))
    .then(response => {
        return response.json();
    })
    .then(data => {
        // Update results count
        hitsLabel.innerHTML = searchResults.start + " - " + Math.min(data.hits.total,(searchResults.start + 9));
        hitsLabel.innerHTML = hitsLabel.innerHTML + " of " + data.hits.total.toString() + " Results";
        nextButton.hidden = (data.hits.total < (searchResults.start + 10));
        prevButton.hidden = (searchResults.start == 1);
        searchResults.innerHTML = "";

        // Load results list
        for (var i=0; i < data.hits.hits.length; i++) {
            var li = document.createElement("li");
            li.innerHTML = writeOutJSON(data.hits.hits[i]._source);
            searchResults.appendChild(li);
        }
    })
    .catch(err => {
        console.log(err);
        hitsLabel.value = err;
    })
}


// This function gets the next 10 results for a search
nextPage = function() {
    var searchResults = document.getElementById('search-hits');
    searchResults.start = searchResults.start + 10;
    onSearchClick();
    window.scrollTo(0, 0);
}

// This function gets the previous 10 results for a search
prevPage = function() {
    var searchResults = document.getElementById('search-hits');
    searchResults.start = Math.max(0, searchResults.start - 10);
    onSearchClick();
    window.scrollTo(0, 0);
}


// This function writes out the result JSON in a prettier format
writeOutJSON = function(input) {
    var output = "";
    for (var property in input) {
        if (input[property] == null) {
            // Do nothing
        }
        else if (typeof(input[property]) == "object") {
            output += "<p><b>" + property + "</b>: " +  writeOutJSON(input[property]) + "</p>";
        }
        else {
            output += "<p><b>" + property + "</b>: " +  "<i>" + input[property] + "</i></p>";
        }
    }
    return output;
}
