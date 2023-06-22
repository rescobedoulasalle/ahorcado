const fs = require('fs');
const path = require('path');
const express = require('express');
const readline = require('readline');

const app = express();
app.use(express.static('pub'));
app.use(express.json());

app.listen(3000, () => {
  console.log('Escuchando en: http://localhost:3000');
});

app.get('/', (request, response) => {
  const titulo = fs.readFileSync(path.resolve(__dirname, 'preguntas', 'programacion.txt'), 'utf8')
    .split('\n')[0];

  fs.readFile(path.resolve(__dirname, 'juego.html'), 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      response.status(500).send('Error al leer el archivo HTML.');
      return;
    }

    const html = data.replace('{{ titulo }}', titulo);
    response.send(html);
  });
});

app.get('/jugar', (request, response) => {
	const preguntas = [];
  
	const readInterface = readline.createInterface({
	  input: fs.createReadStream(path.resolve(__dirname, 'preguntas', 'programacion.txt')),
	  crlfDelay: Infinity
	});
  
	const readLines = async () => {
	  for await (const line of readInterface) {
		const [pregunta, respuesta] = line.split('|');
		preguntas.push({ pregunta, respuesta });
	  }
  
	  response.json(preguntas);
	};
  
	readLines().catch((error) => {
	  console.error(error);
	  response.status(500).send('Error al leer el archivo de preguntas.');
	});
});
