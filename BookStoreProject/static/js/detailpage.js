var paramsString = document.location.search;
var searchParams = new URLSearchParams(paramsString);
var id = searchParams.get("id")
new Vue({
    el: '#books_current',
    data: {
        book: {}
    },
    created: function(){
        const vm = this;
        axios.get('/book/'+ id + '/')
        .then(function (response){
        vm.book = response.data
        })
    }
}

)