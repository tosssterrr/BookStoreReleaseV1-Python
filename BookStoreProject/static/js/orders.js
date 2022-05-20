var paramsString = document.location.search;
var searchParams = new URLSearchParams(paramsString);

new Vue({
        el: '#order_app',
        data: {
            orders: []
        },
        created: function() {
            const vm = this;
            var url = '/order'
            axios.get(url)
                .then(function(response) {
                    vm.orders = response.data;
                    console.log(response.data)
                })

        }
    }

)