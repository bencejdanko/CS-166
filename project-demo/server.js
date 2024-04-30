const tls = require("tls")
const https = require('node:https');

const getPublicKey = async () => {
    const options = {
        name: 'RSA-OAEP',
        modulusLength: 2048,
        publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
        hash: { name: 'SHA-256' },
    };

    const keys = await crypto.subtle.generateKey(
        options,
        true,
        ['encrypt', 'decrypt'],
    );

    const publicKey = await crypto.subtle.exportKey('spki', keys.publicKey);
    const privateKey = await crypto.subtle.exportKey("pkcs8", keys.privateKey);

    let body = btoa(String.fromCharCode(...new Uint8Array(publicKey)));
    body = body.match(/.{1,64}/g).join('\n');

    let public = `-----BEGIN PUBLIC KEY-----\n${body}\n-----END PUBLIC KEY-----`;

    body = btoa(String.fromCharCode(...new Uint8Array(privateKey)));
    body = body.match(/.{1,64}/g).join('\n');

    let private = `-----BEGIN PRIVATE KEY-----\n${body}\n-----END PRIVATE KEY-----`;

    return { public, private };

};

const main = async () => {
    let keys = await getPublicKey();

    const options = {
        key: keys.private,
        cert: keys.public,
    };

    https.createServer(options, (req, res) => {
        res.writeHead(200);
        res.end('hello world\n');
    }).listen(8000);
};

main()