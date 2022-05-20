var paramsString = document.location.search;
var searchParams = new URLSearchParams(paramsString);
var search_book = searchParams.get('search');

new Vue({
    el: '#books_app',
    data: {
        books: []
    },
    created: function(){
        const vm = this;
        var url = '/book/'
        axios.get('/book/')
        .then(function (response){
        vm.books = response.data;
        })

    }
}

)