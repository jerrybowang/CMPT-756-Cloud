const express = require('express');
const app = express();
const port = 3000;

app.use(express.static('public'));
// ++++++++++++++++++ Cookies & Securities ++++++++++++++++++ //

var cors = require("cors");
const corsOptions = {
  origin: "http://localhost:3000", // must match to frontend path
  credentials: true, //access-control-allow-credentials:true
  optionSuccessStatus: 200,
};
app.use(cors(corsOptions));
app.use(express.json());


app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
