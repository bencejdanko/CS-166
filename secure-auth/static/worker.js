const worker = self;
let secret_access_token = null;
let csrf_token = null;


worker.addEventListener('message', async (event) => {
    let { method, secret_access_token_url, secret_url, secret } = event.data;
     
    if (method === "get") {

        let response = await fetch(secret_access_token_url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })

        let data = await response.json();
        secret_access_token = data.secret_access_token;

        response = await fetch(secret_url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `${secret_access_token}`
            }
        })

        if (response.status === 401) {
            let data = await response.json();
            worker.postMessage({ message: data.message });
            return;
        }

        data = await response.json();
        secret = data.secret;
        worker.postMessage({ 
            method: "get",
            secret: secret
        });

    } else if (method === "set") {
        let response = await fetch(secret_access_token_url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })

        if (response.status === 475) {
            let data = await response.json();
            worker.postMessage({ method: 'error', message: data.message });
            return;
        } else if (!response.ok) {
            worker.postMessage({ method: 'error', message: "Something went wrong" });
            return;
        }

        let data = await response.json();
        secret_access_token = data.secret_access_token;

        response = await fetch(secret_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `${secret_access_token}`
            },
            body: JSON.stringify({ secret })
        })

        worker.postMessage({ method: "set" });

    } 
});