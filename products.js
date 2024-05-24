const api = "http://127.0.0.1:5000";

window.onload = () => {
  // BEGIN CODE HERE
  document
    .querySelector(".btn-primary")
    .addEventListener("click", searchButtonOnClick);
  document
    .querySelector("form")
    .addEventListener("submit", productFormOnSubmit);
  // END CODE HERE
};

searchButtonOnClick = () => {
  // BEGIN CODE HERE
  const searchInput = document.querySelector(".input-group input").value;
  const tbody = document.querySelector("table tbody");
  tbody.innerHTML = "";
  if (!searchInput) return;

  fetch(`${api}/search?name=${encodeURIComponent(searchInput)}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error fetching product data: " + response.statusText);
      }
      return response.json();
    })
    .then((product) => {
      console.log(product[0]);
      const row = document.createElement("tr");
      row.innerHTML = `
                <td>${product[0]._id}</td>
                <td>${product[0].name}</td>
                <td>${product[0].production_year}</td>
                <td>${product[0].price}</td>
                <td>${product[0].color}</td>
                <td>${product[0].size}</td>
            `;
      tbody.appendChild(row);
    })
    .catch((error) => {
      console.error(error);
    });
  // END CODE HERE
};

productFormOnSubmit = (event) => {
  // BEGIN CODE HERE
  event.preventDefault();

  const productData = {
    name: document.getElementById("productName").value,
    production_year: document.getElementById("productionYear").value,
    price: document.getElementById("price").value,
    color: document.getElementById("color").value,
    size: document.getElementById("size").value,
  };

  fetch(`${api}/add-product`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify(productData),
  })
    .then((response) => {
      if (response.status === 200) {
        document.querySelector("form").reset();
        console.log("Product updated successfully");
      } else if (response.status === 201) {
        document.querySelector("form").reset();
        console.log("Product added successfully");
      } else {
        throw new Error("Error adding product: " + response.statusText);
      }
    })
    .catch((error) => {
      console.error(error);
    });
  // END CODE HERE
};
