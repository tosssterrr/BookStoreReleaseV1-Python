new Vue({
        el: '#personal_app',
        data: {
            personal_data: {}
        },
        created: function() {
            const vm = this;
            axios.get('/accounts/auth/users/me/')
                .then(function(response) {
                    console.log(response.data)
                    vm.personal_data = response.data
                })
        }
    }

)