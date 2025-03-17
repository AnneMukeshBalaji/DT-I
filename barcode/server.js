const express = require("express");
const mysql = require("mysql");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// MySQL Database Connection
const db = mysql.createConnection({
    host: "localhost",
    user: "root", 
    password: "LUFFYstar@#0139803",
    database: "barcode"
});

db.connect(err => {
    if (err) {
        console.error("Database connection failed: " + err.message);
    } else {
        console.log("Connected to MySQL database.");
    }
});

// API to fetch product by barcode (Fixed table and column names)
app.get("/api/products/:barcode", (req, res) => {
    const barcode = req.params.barcode;
    const query = "SELECT barcode, name, price FROM product WHERE barcode = ?"; 
    
    db.query(query, [barcode], (err, result) => {
        if (err) {
            console.error("Database query error:", err);
            return res.status(500).json({ error: "Internal Server Error" });
        }
        if (result.length === 0) {
            return res.status(404).json({ message: "Product not found" });
        }
        res.json(result[0]);
    });
});

// Start the server
app.listen(3000, () => {
    console.log("Server is running on port 3000");
});
