function fetchProduct() {
    let barcode = document.getElementById("productCode").value.trim(); // Fixed input ID

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

            let newRow = `<tr>
                <td>${product.barcode}</td>  
                <td>${product.name}</td>
                <td>${product.price}</td>
            </tr>`;

            tableBody.innerHTML += newRow;
        })
        .catch(error => {
            alert(error.message);
        });

    document.getElementById("productCode").value = ""; // Fixed input ID
}
