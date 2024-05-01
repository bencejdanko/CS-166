const tls = require("tls")
const https = require('node:https');
const fs = require('node:fs');

const main = async () => {
    const options = {
        key: fs.readFileSync('private.pem'),
        cert: fs.readFileSync('public.pem'),
    };

    https.createServer(options, (req, res) => {
        res.writeHead(200);
        res.end('hello world\n');
    }).listen(8000);
};

main()