 /*
  For local development, use mkcert: mkcert example.com 32kb.dev localhost 127.0.0.8080 ::1
  */
const cert = await Deno.readTextFile(`example.com+4.pem`)
const key = await Deno.readTextFile(`example.com+4-key.pem`)

Deno.serve({ 
  cert: cert, 
  key: key,
  port: 8080,
}, handler)

function handler(request: Request) {
  const url = new URL(request.url)
}