var express = require('express');
var path = require('path');
var cors = require('cors');
var axios = require('axios');

var app = express();
app.use(cors());

app.get('/', async (req, res) => {
	alert("HELLO");

	/*res.send('Frontend');
	await axios.get('http://localhost:3000/display')
	.then((res) => {
		console.log("S")
		console.log((res.data));
	})
	.catch((error) => {
		console.log(error.response);
	})*/
});

app.listen(8080)
console.log("Servidor online")
