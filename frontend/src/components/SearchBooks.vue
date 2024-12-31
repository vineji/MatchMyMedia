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
        <button @click="toggleMedia">Toggle Media</button>
        <div v-if="media.length> 0">
            <ul>
                <li v-for="object in media" :key="object.id">
                    {{ object.title || object.name}}
                    <img :src=" 'https://image.tmdb.org/t/p/original/' + object.poster_path" alt="Movie poster"  />
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
            media : [],
            searchMedia : 'movie'
        };
    },
    methods: {
        async search(){
            if (this.query.length < 2){
                return
            }

            if (this.searchMedia == "movie"){
                try{
                    const response = await fetch(`http://localhost:8000/api/search-movie/?title=${this.query}`);

                    if (!response.ok){
                        throw new Error('Failed to fetch data');
                    }
                    const data = await response.json();
                    this.media = data.movies || [];
                }
                catch (error){
                    console.error('error catching data', error)
                }
            }
            else if (this.searchMedia == "tv"){
                try{
                    const response = await fetch(`http://localhost:8000/api/search-show/?title=${this.query}`);

                    if (!response.ok){
                        throw new Error('Failed to fetch data');
                    }
                    const data = await response.json();
                    this.media = data.shows || [];
                }
                catch (error){
                    console.error('error catching data', error)
                }
            }
        },
        toggleMedia(){
            if (this.searchMedia == "movie") {
                this.searchMedia = "tv";
            }
            else{
                this.searchMedia = "movie";
            }
            this.query = '';

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