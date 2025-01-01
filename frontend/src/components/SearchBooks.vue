<template>
    <div class="search_container">
        <form @submit.prevent class="search">
            <div class="search_button_div">
                <button @click="toggleMedia('Movie')"
                :class="{active: searchMedia === 'Movie'}"
                class="movie_button"
                > Movies </button>

                <button @click="toggleMedia('TV Show')"
                :class="{active: searchMedia === 'TV Show'}"
                class="show_button"
                > TV Shows  </button>
            </div>

            <input
            type="text"
            :placeholder="'Search ' + searchMedia"
            v-model="query"
            @input="search"
            />
            <button @click="clearQuery">Clear</button>
        </form>
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
            searchMedia : 'Movie',
            show_ChosenMedia : false,
            chosenMedia : null,
            
        };
    },
    methods: {
        async search(){
            if (this.query.length < 2){
                return
            }

            if (this.searchMedia == "Movie"){
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
            else if (this.searchMedia == "TV Show"){
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
        toggleMedia(media){
            this.searchMedia = media;
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
.search_container{
    display: flex;
    flex-direction: column;
    align-items: center;
}

li{
    list-style: none;
}
img{
    height: 3cm;
    width: auto;
}
.search{
    display: flex;
    flex-direction: row;
    gap: 1rem;
}
.search input{
    width: 33rem;
    height: 2.8rem;
    border-radius: 1rem;
    padding-left: 1rem;
    font-size: 1.2rem;
}
.search_button_div{
    background-color: #FBFFFE;
    border: #FAA916 solid 2px;
    height: 3rem;
    border-radius: 1rem;
    overflow: hidden;
}
.search_button_div button{
    all: unset;
    background-color: #FBFFFE;
    color: #FAA916;
    height: 3rem;
    padding-left: 1rem;
    padding-right: 1rem;
    cursor: pointer;
    font-weight: 500;
    font-size: 1.2rem;
}
.movie_button{
    border-top-right-radius: 0.8rem;
    border-bottom-right-radius: 0.8rem;
}
.show_button{
    border-top-left-radius: 0.8rem;
    border-bottom-left-radius: 0.8rem;
}

.search_button_div button.active{
    background-color: #FAA916;
    color: #FBFFFE;
    transition: ease 0.3s;
    
}


</style>