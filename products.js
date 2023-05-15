const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const getSearchButton = document.getElementById("search");
    getSearchButton.onclick = searchButtonOnClick;

    const getSaveButton = document.getElementById("save");
    getSaveButton.onclick = productFormOnSubmit;
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const searchProduct = document.getElementById("searchInput");
   

    const url = 'http://127.0.0.1:5000/search?name='+`${searchProduct.value}`;
    fetch(url)
    .then(response => response.json())  
    .then(json => {
        const data = json;
        
        var table = document.getElementById("results");
        while (table.firstChild) {
            table.firstChild.remove();
        }

        data.reverse();
        data.forEach(item => {
            var row = table.insertRow(0);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            var cell6 = row.insertCell(5);

            cell1.innerHTML = item["_id"];
            cell2.innerHTML = item["name"];
            cell3.innerHTML = item["production_year"];
            cell4.innerHTML = item["price"];
            cell5.innerHTML = item["color"];
            cell6.innerHTML = item["size"];
        });
      })
    // END CODE HERE
}

productFormOnSubmit = (event) => {
    // BEGIN CODE HERE
    const getName = document.getElementById("inputName");
    const getYear = document.getElementById("inputYear");
    const getPrice = document.getElementById("inputPrice");
    const getColor = document.getElementById("inputColor");
    const getSize = document.getElementById("inputSize");

    const res = new XMLHttpRequest();
    res.open("POST", `http://127.0.0.1:5000/add-product`);
    res.onreadystatechange = () => {
        if (res.readyState == 4) {
            if (res.status == 200) {
                alert(res.responseText);
                getName.value="";
                getYear.value="";
                getPrice.value="";
                getColor.value="";
                getSize.value="";
            }
        }
    };
    res.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    res.send(JSON.stringify({
        name: getName.value,
        production_year: parseInt(getYear.value),
            price: parseInt(getPrice.value),
            color: parseInt(getColor.value),
            size: parseInt(getSize.value)
     }))
    
    // END CODE HERE
}
