//обновление стиля
var tradeOffStatus = 'table-warning';

//подписка на события ws
document.addEventListener('DOMContentLoaded', (event) => {
    //событие обновления данных
    socket.on('update', function (data) {
        updateTradeStatus(data);
    });
});

//основная функция обновления стиля
function updateTradeStatus(data) {
    let key = 'is_trade';
    let e_id = data.id + "_" + key;
    let row_id = "row_" + data.id;

    let element = document.getElementById(row_id);
    if (element !== null) {
        let old_value = element.dataset[key];
        let new_value = data[key].toString();
        if (old_value !== new_value) {
            element.dataset[key] = new_value;
            if (data[key]) {
                removeStyle(row_id, tradeOffStatus);
            } else {
                addStyle(row_id, tradeOffStatus);
            }
        }
    }
}

//добавляем стиля
function removeStyle(id, style) {
    let element = document.getElementById(id);
    if (element !== null) {
        element.classList.remove(style);
    }
}

//убираем стиль стиля
function addStyle(id, style) {
    let element = document.getElementById(id);
    if (element !== null) {
        element.classList.add(style);
    }
}

