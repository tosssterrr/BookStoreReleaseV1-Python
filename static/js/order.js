var paramsString = document.location.search;
var searchParams = new URLSearchParams(paramsString);
var id = searchParams.get("id")

new Vue({
        el: '#order_app',
        data: {
            order: {},
            order_books: []
        },
        created: function() {
            const vm = this;
            var url = '/order/' + id
            axios.get(url)
                .then(function(response) {
                    vm.order = response.data;
                    console.log(response.data)
                })
            var url_2 = '/books_order/'+ id;
            axios.get(url_2)
                .then(function(response){
                    vm.order_books = response.data
                    console.log(response.data)
                })
        }
    }

)