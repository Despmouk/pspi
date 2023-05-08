const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const getSearchButton = document.getElementById("search");
    getSearchButton.onclick = searchButtonOnClick;
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const getProduct = document.getElementById("searchInput");
   
    const resultsTable = document.getElementById("results");
    
    

    var cellCount = resultsTable.rows[0].cel.length;

    //addrow
    var rowLength = resultsTable.rows.length;
    var newRow = resultsTable.insertRow(rowLength);

    for(var i=0; i<cellCount; i++){
        var newCell = newRow.insertCell(i);
        newRow.cells[0].innerHtml = rowLength;
    }
    
    

    //time.innerHTML = `${getProduct.value}`
    //resultsDiv.appendChild(time);
    // END CODE HERE
}

productFormOnSubmit = (event) => {
    // BEGIN CODE HERE

    // END CODE HERE
}
