var socket = io();
var connected = false;
var i = 0;

//обновление состояния toggle кнопки обновления
document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelector('#SwitchUpdate').checked = (isNeedUpdate())
});

//подписка на события ws
document.addEventListener('DOMContentLoaded', (event) => {
    //событие подключения
    socket.on('connect', function () {
        console.log('Connected to server');
        connected = true;
        i = 0;
        pingSend();
    });

    //событие отключения
    socket.on('disconnect', function () {
        console.log('Disconnected from server');
        connected = false;
        i = -10;
    });

    //событие обновления данных
    socket.on('update', function (data) {
        //console.log(data);
        update(data);
    });
});

//асинхронная отправка ping
async function pingSend() {
    // выводит 0, затем 1, затем 2
    while (connected && i>=0) {
        socket.send('ping_' + i.toString());
        //в случае необходимости запрашиваем новые данные
        if (isNeedUpdate()) {
            socket.emit('update', window.location.pathname);
        }
        i++;
        await sleep(5000);
    }
}

//асинхронный таймаут
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


//основная функция обновления времени
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

//получение даты в виде ГГГГ-ММ-ДД ЧЧ:ММ:СС из unix timestamp
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

//форматированный вывод чисел 1 000 000
function getFormatedValue(value) {
    let formattedValue = value.toLocaleString('en-US').replaceAll(',', ' ');
    return formattedValue;
}

//проверка необходимости обновления
function isNeedUpdate() {
    let status = localStorage.getItem('update');
    let value = (status === '1' || status === null);
    return value;
}

//сохранение состояния обновления в localStorage
function setUpdate() {
    if (isNeedUpdate()) {
        localStorage.setItem('update', 0);
    } else {
        localStorage.setItem('update', 1);
    }
}
