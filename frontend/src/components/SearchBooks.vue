<template>
    <div>
        <form>
            <input
            type="text"
            placeholder="Search Movies"
            v-model="query"
            @input="search"
            />
            <button type="submit">Search</button>
        </form>
        <div v-if="movies.length> 0">
            <ul>
                <li v-for="movie in movies" :key="movie.id">
                    {{ movie.title }}
                    <img :src=" 'https://image.tmdb.org/t/p/original/' + movie.poster_path" alt="Movie poster"  />
                </li>
            </ul>

        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            query : '',
            movies : []
        };
    },
    methods: {
        async search(){
            if (this.query.length < 2){
                return
            }

            try{
                const response = await fetch(`http://localhost:8000/api/search-movie/?title=${this.query}`);

                if (!response.ok){
                    throw new Error('Failed to fetch data');
                }
                const data = await response.json();
                this.movies = data.movies || [];
            }
            catch (error){

                console.error('error catching data', error)
            }
        }
    }
};
</script>
<style>
li{
    list-style: none;
}
img{
    height: 3cm;
    width: auto;
}
</style>