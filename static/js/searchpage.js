var paramsString = document.location.search;
var searchParams = new URLSearchParams(paramsString);
var search_book = searchParams.get('name') ? searchParams.get('name') : '';

new Vue({
    el: '#books_search',
    data: {
        books: [],
        searchparams: {},
        categories: [],
    },
    created: function(){
        const vm = this;
        var url = '/book/?name=' + search_book
        var minp = searchParams.get('min') ? searchParams.get('min') : ''
        var maxp = searchParams.get('max') ? searchParams.get('max') : ''
        url += '&max_price=' + maxp + '&min_price=' + minp
        var miny = searchParams.get('minyear') ? searchParams.get('minyear') : ''
        var maxy = searchParams.get('maxyear') ? searchParams.get('maxyear') : ''
        url += '&max_year=' + maxy + '&min_year=' + miny
        var author = searchParams.get('author') ? searchParams.get('author') : ''
        url += '&author__name=' + author
        var category = searchParams.get('category')
        if (category !== 'Все' && category !== null){
        url += '&category__name=' + category
        }
        else if (category == null || category == ''){
        var category = 'Все'
        }
        categories = []
        axios.get('/category/')
        .then(function (response){
        for (var i = 0; i < response.data.length; i++){
        if(response.data[i].name !== category){categories.push(response.data[i])}
        else{categories.unshift({name:'Все', slug: null, 'id': null})}
        }
        vm.categories = categories
        })
        axios.get(url)
        .then(function (response){
        vm.books = response.data;
        searchdict = {
            'search': search_book,
            'minp': minp,
            'maxp': maxp,
            'miny': miny,
            'maxy': maxy,
            'author': author,
            'category': category
        }
        vm.searchparams = searchdict;
        })
    }
}

)