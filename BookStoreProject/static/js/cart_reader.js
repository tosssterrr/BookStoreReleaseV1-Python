var paramsString = document.location.search;
var searchParams = new URLSearchParams(paramsString);


new Vue({
        el: '#cart_app',
        data: {
            cart_data: {},
            order_data: {}
        },
        created: function() {
            const vm = this;
            cart_data = JSON.parse(localStorage.getItem('cart'));
            order_data = {
                'total_qty': 0,
                'total_price': 0,
            }
            console.log(cart_data)
            vm.cart_data = cart_data

            for (key in this.cart_data) {
                order_data['total_qty'] += parseInt(this.cart_data[key]['qty'])
                order_data['total_price'] = String(parseFloat(order_data['total_price']) + parseFloat(this.cart_data[key]['total_price']))
            }
            console.log(order_data)
            localStorage.setItem('order', JSON.stringify(order_data));
            vm.order_data = order_data
        }
    }

)