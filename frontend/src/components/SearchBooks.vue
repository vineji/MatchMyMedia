<template>
    <div>
        <form @submit.prevent>
            <input
            type="text"
            placeholder="Search Movies"
            v-model="query"
            @input="search"
            />
            <button @click="clearQuery">Clear</button>
        </form>
        <button @click="toggleMedia"> Toggle Media </button>
        <div v-if="mediaList.length > 0">
            <ul>
                <li v-for="media in mediaList" :key="media.id">
                    {{ media.title || media.name}}
                    <img :src=" 'https://image.tmdb.org/t/p/original/' + media.poster_path" alt="Movie poster"  />
                    <button @click="select(media)"> Select </button>
                </li>
            </ul>
        </div>
        <div v-if="show_ChosenMedia == true">
            {{ chosenMedia.title || chosenMedia.name}}
            <img :src=" 'https://image.tmdb.org/t/p/original/' + chosenMedia.poster_path" alt="Movie poster"  />
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            query : '',
            mediaList : [],
            searchMedia : 'movie',
            show_ChosenMedia : false,
            chosenMedia : null,
            
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
                    this.mediaList = data.movies || [];
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
                    this.mediaList = data.shows || [];
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
            this.search();
        },
        clearQuery(){
            this.query = '';
            this.mediaList = [];
        },
        select(media){
            this.show_ChosenMedia = true;
            this.chosenMedia = media;
            this.clearQuery();
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