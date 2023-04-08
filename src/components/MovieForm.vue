<template>
    <div class="container-fluid">
        <div v-if="success" class="alert alert-success">
            <h6>File Upload Successful</h6>
        </div>

        <div v-if="fail" class="alert alert-danger">
            <li v-for="error in error_message">{{error}}</li>
        </div>
        
        <form @submit.prevent="saveMovie" id="movieForm">
                <div class="form-group mb-3">
                    <label for="title" class="form-label">Movie Title</label>
                    <input id="first" type="text" name="title" class="form-control" />
                </div>

                <div class="form-group mb-3">
                    <label for="description" class="form-label">Description</label>
                    <input id="second" type="text" name="description" class="form-control" />
                </div>

                <div class="form-group mb-3">
                    <label for="poster" class="form-label">Add Poster</label>
                    <input id="third" type="file" name="poster" class="form-control" />
                </div>

                <input type="submit" class="btn btn-primary" value="Submit">
        </form>
    </div>
      
</template>

<script setup>
    import { ref, onMounted  } from "vue";
    let csrf_token = ref("");
    let success = ref(false);
    let fail = ref(false);
    let error_message = ref('');

    onMounted(() => {
        getCsrfToken();
        success.value = false;
        fail.value = false;
    });

    function saveMovie() 
    { 
        let movieForm = document.getElementById("movieForm");
        let form_data = new FormData(movieForm);

            fetch("/api/v1/movies", {
                method: 'POST',
                body: form_data,
                headers: 
                {
                    'X-CSRFToken': csrf_token.value
                }
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {

                    let i = 0;

                    for (i in data)
                    {
                        error_message = data[i];
                    }

                    if(document.getElementById('first').value == "" || document.getElementById('second').value == "" || document.getElementById('third').value == "")
                    {
                        fail.value = true;
                    }
                    else
                    {
                        success.value = true;
                    }
                    
                    setTimeout(function() 
                    {
                        success.value = false;
                    }, 3000);

                    setTimeout(function() 
                    {
                        fail.value = false;
                    }, 3000);
                })
                .catch(function (error) {
                    console.log(error);
                });
    }

    function getCsrfToken() 
    {
        fetch('/api/v1/csrf-token')
            .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    csrf_token.value = data.csrf_token;
        })
    }
</script>