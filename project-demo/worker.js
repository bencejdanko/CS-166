const worker = self;
let token = null;

worker.addEventListener('message', (event) => {
    console.log("Message received:", event.data);
    if (event.data === "get") {
        postMessage(token);
        console.log("Token sent:", token);
        return;
    }

    console.log("Token received:", event.data);
    token = event.data;
    console.log("Token stored: ", token);
});