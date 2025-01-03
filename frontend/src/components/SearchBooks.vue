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
            <button @click="clearQuery" class="clear_button">Clear</button>
        </form>
        <div v-if="mediaList.length > 0" class="media_list">
            <ul>
                <li v-for="media in mediaList" :key="media.id">
                    <img :src=" 'https://image.tmdb.org/t/p/original/' + media.poster_path" alt="Movie poster" class="list_img"  />
                    <div class="sub_media_list">
                        <p>{{ media.title || media.name}}</p>
                        <p>Released: {{media.release_date }}</p>
                        <p>Genre: {{ media.genre_ids }}</p>
                        <button @click="select(media)"> Select </button>
                    </div>
                </li>
            </ul>
        </div>
        <div v-if="show_ChosenMedia == true" class="chosen_media">
            <img class="chosen_media_img" :src=" 'https://image.tmdb.org/t/p/original/' + chosenMedia.poster_path" alt="Movie poster"  />
            <div class="chosen_media_info">
                <p>Title: {{ chosenMedia.title || chosenMedia.name}}</p>
                <p>Released: {{chosenMedia.release_date || chosenMedia.first_air_date }}</p>
                <p>Genre: {{ chosenMedia.genre_ids }}</p>
                <p>Overview: {{ chosenMedia.overview }}</p>
                
            </div>
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

            this.show_ChosenMedia = false;
            this.chosenMedia = null;

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
.search_container{
    display: flex;
    flex-direction: column;
    align-items: center;
}
.search{
    display: flex;
    flex-direction: row;
    gap: 1rem;
    margin-right: 5rem;
}
.search input {
    display: flex;
    align-items: flex-start;
    width: 33rem;
    height: 3rem;
    border-radius: 1rem;
    padding-left: 1rem;
    font-size: 1.2rem;
    border: #6D676E solid 2px;
    color: #6D676E;
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
.clear_button{
    all: unset;
    border: #cb0422 2px solid;
    font-weight: 700;
    font-size: 1.2rem;
    width: 6rem;
    border-radius: 0.8rem;
    height: 3rem;
    color: #cb0422;
}
.clear_button:hover{
    color: #FBFFFE;
    background-color: #cb0422;
    transition: ease 0.3s;
}

.media_list{
    margin-right: 5rem;
}

.media_list ul{
    display: flex;
    flex-direction: row;
    width: 75rem;
    max-width: 75rem;
    flex-wrap: wrap;
    justify-content: space-evenly;
    
}
.media_list li {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    width: 21rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-size: 0.8rem;
    min-height: 13rem;
    padding: 1rem;
    margin-top: 1rem;
}
.media_list button{
    width: 9rem;
}
.sub_media_list{
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    max-width: 10rem;
}
.list_img{
    height: auto;
    width: 8rem;
    max-width: 100%;
}

.chosen_media{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 3rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    width: 53rem;
    margin-right: 5rem;
    margin-top: 2rem;
    padding: 2rem;
}

.chosen_media_img{
    height: auto;
    width: 9rem;
    max-width: 100%;
}


.chosen_media_info{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: space-evenly;
    width: 40rem;
    height: 14rem;
}
.chosen_media_info p{
    gap: 0;
    margin: 0;
    text-align: left;
}


</style>