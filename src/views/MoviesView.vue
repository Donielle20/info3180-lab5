<script setup>
    import { ref, onMounted  } from "vue";

    let movies = ref([]);

    onMounted(() => {
        fetchMovies()
    });

    function  fetchMovies()
    {
        fetch("/api/v1/movies", {
                method: 'GET'
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    movies.value = data;

                    let i = 0;
                    
                    for (i in data)
                    {
                        movies.value = data[i];
                        console.log(data[i]);
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
    }
</script>

<template>
    <div class="indent">
        <h1>Movies</h1>

        <div class="separate">
            <div v-for="movie in movies" class="grid">
                <img :src="`/uploads/${movie[3]}`" alt="Movie poster" class="image"/>
                <div class="read">
                    <h2>{{movie[1]}}</h2>
                    <br>
                    <h4>{{movie[2]}}</h4>
                </div> 
            </div>
        </div>
    </div>
</template>

<style>
    h1{
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }
    .separate{
        display: grid;
        grid-template-columns: 1fr 1fr;
        row-gap: 50px;
        column-gap: 25px;
    }
    .image{
        width: 250px;
        height: 350px;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
    }
    .read{
        width: 400px;
        height: 350px;
    }
    .grid{
        display: grid;
        grid-template-columns: 260px 260px;
        border-radius: 10px;
        border-bottom: 10px;
        box-shadow: 6px 6px 5px rgb(191, 197, 199);
        border: 2px solid rgb(191, 197, 199);
        width: 700px;
    }
    .indent{
        padding: 20px;
        /* margin: 50px; */
    }
</style>