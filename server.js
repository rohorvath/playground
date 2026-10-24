const http = require("http");

const port = process.env.PORT || 3000;

const page = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Hello World</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
`;

// Plain HTTP on purpose: this demo app has no certificates. TLS is expected to be
// terminated by a reverse proxy or the hosting platform in front of it.
// nosemgrep: problem-based-packs.insecure-transport.js-node.using-http-server.using-http-server
const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
  res.end(page);
});

server.listen(port, () => {
  console.log(`Hello world app listening on http://localhost:${port}`);
});
