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


function deleteOrderByPk(pk){
    var orderPk = pk;
    var url = "/order/" + pk
    console.log(pk)
    axios.delete(url, {'headers': {"X-CSRFToken": csrftoken}})
    .then(function(response){
    console.log(response.status)
    if (response.status=204){
    window.location.href = '/accounts/profile/order_delete_done'
    }


    })
}

document.onclick = event => {
    if (event.target.id.includes('delete')) {
        pk = event.target.id.split(" ")[1]
        deleteOrderByPk(pk)
    }
}
