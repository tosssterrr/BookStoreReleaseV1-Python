var d = document,
    itemBox = d.querySelectorAll('.item_box'), // блок каждого товара
    cartCont = d.getElementById('cart_content'); // блок вывода данных корзины

function getCartData() {
    return JSON.parse(localStorage.getItem('cart'));
}
// Записываем данные в LocalStorage
function setCartData(o) {
    localStorage.setItem('cart', JSON.stringify(o));
    return false;
}

function addToCart_2(book) {
    var cartData = getCartData() || {},
        itemId = book.getAttribute('data-id')
    itemPrice = document.getElementById('price').getAttribute('data-id')
    itemName = document.getElementById('name').getAttribute('data-id')
    itemImg = document.getElementById('img').getAttribute('data-id')
    if (cartData.hasOwnProperty(itemId)) {
        cartData[itemId]['qty'] = parseInt(cartData[itemId]['qty']) + 1;
        cartData[itemId]['total_price'] = String(parseFloat(cartData[itemId]['price']) * cartData[itemId]['qty']);
        setCartData(cartData)
    } else {
        cartData[itemId] = {
            'name': itemName,
            'price': itemPrice,
            'img': itemImg,
            'qty': 1,
            'total_price': itemPrice,
        }
        setCartData(cartData)
    }
    console.log(cartData)
    window.location.href = '/cart/'
    return false;
}

function delCartElemByPk(pk){
    var cartData = getCartData() || {},
        itemId = pk
    if (cartData.hasOwnProperty(itemId)) {
    delete cartData[itemId]
    setCartData(cartData)
    console.log(Object.keys(cartData).length)
    if (Object.keys(cartData).length == 0){
    localStorage.removeItem('cart');
    }
    window.location.href = '/cart/'
    return false
    }
    else{
    console.log('Как ты это вызвал?')
    }
}

function updCartElemByPk(pk, qty){
    var cartData = getCartData() || {},
        itemId = pk
        newItemQty = qty
    if (cartData.hasOwnProperty(itemId)) {
    console.log('попал')
    cartData[pk]['qty'] = newItemQty;
    cartData[itemId]['total_price'] = String(parseFloat(cartData[itemId]['price']) * cartData[itemId]['qty']);
    setCartData(cartData)
    window.location.href = '/cart/'
    }
    else{
    console.log('Как ты это вызвал?')
    }
}

// Устанавливаем обработчик события на каждую кнопку "Добавить в корзину"
document.onclick = event => {
    if (event.target.id == "plus") {
        book = event.target.parentNode.parentNode.innerHTML
        addToCart_2(event.target)
    } else if (event.target.id == 'clear') {
        localStorage.removeItem('cart');
        window.location.href = '/cart/'
    } else if (event.target.id.includes('clear')){
        pk = event.target.id.split(" ")[1]
        delCartElemByPk(pk)
    } else if (event.target.id.includes('update')){
        pk = event.target.id.split(" ")[1]
        qty = d.getElementById('number '+pk).value
        console.log('pk= '+pk+' qty= '+qty)
        updCartElemByPk(pk, qty)
    }
}

