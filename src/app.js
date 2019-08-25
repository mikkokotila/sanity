const express = require('express')
const app = express()
const port = 3000

app.use(express.static('.'));

app.get('/', (req, res) => res.sendFile('login.html', { root: '.' }))

app.get('/',function(req,res) {
  res.sendFile('login.html', { root: '.'});
});


app.listen(port)