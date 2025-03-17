let totalCost = 0; // Variable to track total cost

function fetchProduct() {
    let barcode = document.getElementById("productCode").value.trim();

    if (!barcode) {
        alert("Please enter a product code!");
        return;
    }

    fetch(`http://localhost:3000/api/products/${barcode}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Product not found");
            }
            return response.json();
        })
        .then(product => {
            let tableBody = document.getElementById("productTableBody");

            // Create a new row
            let newRow = document.createElement("tr");

            newRow.innerHTML = `
                <td>${product.barcode}</td>  
                <td>${product.name}</td>
                <td>${product.price}</td>
                <td><button class="delete-btn" ><img src="image.png" height="30" width="30"></button></td>
            `;

            // Append row to table
            tableBody.appendChild(newRow);

            // Update the total cost
            totalCost += parseFloat(product.price);
            document.getElementById("totalcost").value = totalCost.toFixed(2);

            // Add event listener to the remove button
            newRow.querySelector(".delete-btn").addEventListener("click", function () {
                removeProduct(newRow, product.price);
            });
        })
        .catch(error => {
            alert(error.message);
        });

    document.getElementById("productCode").value = "";
}

// Function to remove a product from the table and update total cost
function removeProduct(row, price) {
    row.remove(); // Remove the row from the table
    totalCost -= parseFloat(price); // Subtract price from total
    document.getElementById("totalcost").value = totalCost.toFixed(2); // Update total cost
}
