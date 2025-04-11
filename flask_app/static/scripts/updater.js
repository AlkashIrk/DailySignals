let socket = io();
let connected = false;

document.addEventListener('DOMContentLoaded', (event) => {
    socket.on('connect', function () {
        console.log('Connected to server');
        connected = true;
        pingSend();
    });

    socket.on('disconnect', function () {
        console.log('Disconnected from server');
        connected = false;
    });

    socket.on('update', function (data) {
        console.log(data);
        update(data);
    });
});

async function pingSend() {
    let i = 0;
    // выводит 0, затем 1, затем 2
    while (connected) {
        socket.send('ping_' + i.toString());
        socket.emit('update', window.location.pathname);
        i++;
        await sleep(5000);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function update(data) {
    for (let key of Object.keys(data)) {
        let e_id = data.id + "_" + key;
        let element = document.getElementById(e_id);
        if (element !== null) {
            if (element.dataset.value !== data[key].toString()) {
                element.dataset.value = data[key].toString();
                if (element.dataset.type === "timestamp") {
                    element.innerText = getTimeFromTimestamp(data[key]);
                } else if (element.dataset.type === "int") {
                    element.innerText = getFormatedValue(data[key]);
                } else if (element.dataset.type === "float") {
                    element.innerText = getFormatedValue(data[key]);
                } else {
                    element.innerText = data[key];
                }

                if (element.dataset.type === "baseurl") {
                    let url_key = element.dataset.url-key
                    if (element !== null) {
                        element.href = element.dataset.url + data[url_key];
                    } else {
                        element.href = element.dataset.url + data[key];
                    }
                }
            }
        }
    }
}

function getTimeFromTimestamp(unix_timestamp) {
    if (unix_timestamp === 0) {
        return "-";
    }

    let date = new Date(unix_timestamp * 1000);
    let today = date.toISOString().slice(0, 10);
    let hours = date.getHours();
    let minutes = "0" + date.getMinutes();
    let seconds = "0" + date.getSeconds();
    let formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

    let formattedDateTime = today + " " + formattedTime;
    return formattedDateTime;
}

function getFormatedValue(value) {
    let formattedValue = value.toLocaleString('en-US').replaceAll(',', ' ');
    return formattedValue;
}