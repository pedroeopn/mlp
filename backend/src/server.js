require("dotenv").config();
const express = require("express");
const cors = require("cors");
require("./config/database");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Routes

app.get("/", (req, res) => {
  res.send("CuidarBem API is running");
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
