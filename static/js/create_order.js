document.onclick = event => {
    if (event.target.id == "create_order") {
        var select = document.getElementById('payment_type');
        var value = select.options[select.selectedIndex].value;
        createOrder(value);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function createOrder(payment_type) {
    console.log(csrftoken)
    cartData = getCartData()
    orderPreferences = getOrderData()
    orderData = {}
    axios.post('/order/', {
            "payment": payment_type,
            "total_price": orderPreferences['total_price']
        }, { headers: { "X-CSRFToken": csrftoken } })
        .then(function(response) {
            console.log(response.data)
            orderData = response.data
            for (order_book in cartData) {
                console.log(cartData[order_book])
                axios.post('/order_book/', {
                        "book": order_book,
                        "qty": cartData[order_book]['qty'],
                        "final_price": cartData[order_book]['total_price'],
                        "order": orderData['pk']
                    }, { headers: { "X-CSRFToken": csrftoken } })
                    .then(function(response) {
                        console.log(response.data)
                    })
            }
            localStorage.removeItem('cart');
            localStorage.removeItem('order');
            window.location.href = '/accounts/profile/orders/?id=' + orderData['pk']
        })

}

function getCartData() {
    return JSON.parse(localStorage.getItem('cart'));
}
// Записываем данные в LocalStorage
function getOrderData() {
    return JSON.parse(localStorage.getItem('order'));
}



function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}