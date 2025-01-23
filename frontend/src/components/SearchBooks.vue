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
            <ul class="media_list_ul">
                <li class="media_list_li" v-for="media in mediaList" :key="media.id">
                    <img :src=" 'https://image.tmdb.org/t/p/original/' + media.poster_path" alt="Movie poster" class="list_img"  />
                    <div class="sub_media_list">
                        <ul class="sub_media_list_ul">
                            <li><b>Title: </b>{{ media.title || media.name}}</li>
                            <li><b>Released: </b>{{media.release_date || media.first_air_date || "Not specified"}}</li>
                            <li><b>Genres: </b></li>
                            <ul v-if="media.genre_ids.length > 0" class="genre_list">
                                <li class="genre" v-for="id in media.genre_ids" :key="id" :style="{backgroundColor: getGenreColor(id)}"> {{ getGenreName(id) }}</li>
                            </ul>
                            <ul v-else class="genre_list">
                                <li class="genre" style="background-color: #9b9a9a;">Unknown</li>
                            </ul>

                        </ul>
                        <button @click="select(media)" class="media_list_button"> Select </button>
                    </div>
                </li>
                <li class="pagination_control">
                    <button @click="this.showPageMultiplier--">Previous</button>
                    <button @click="changePage((this.showPages * this.showPageMultiplier) - 5)">{{(this.showPages * this.showPageMultiplier) - 5}}</button>
                    <button @click="changePage((this.showPages * this.showPageMultiplier) - 4)">{{(this.showPages * this.showPageMultiplier) - 4}}</button>
                    <button @click="changePage((this.showPages * this.showPageMultiplier) - 3)">{{(this.showPages * this.showPageMultiplier) - 3}}</button>
                    <button @click="changePage((this.showPages * this.showPageMultiplier) - 2)">{{(this.showPages * this.showPageMultiplier) - 2}}</button>
                    <button @click="changePage((this.showPages * this.showPageMultiplier) - 1)">{{(this.showPages * this.showPageMultiplier) - 1}}</button>
                    <button @click="changePage(this.showPages * this.showPageMultiplier)">{{(this.showPages * this.showPageMultiplier)}}</button>
                    <button @click="this.showPageMultiplier++">Next</button>
                </li>
            </ul>
        </div>
        <div v-if="show_ChosenMedia == true" class="chosen_media">
            <img class="chosen_media_img" :src=" 'https://image.tmdb.org/t/p/original/' + chosenMedia.poster_path" alt="Movie poster"  />
            <div class="chosen_media_info">
                <p><b>Title: </b>{{ chosenMedia.title || chosenMedia.name}}</p>
                <p><b>Released: </b> {{chosenMedia.release_date || chosenMedia.first_air_date }}</p>
                <ul v-if="chosenMedia.genre_ids.length > 0" class="chosen_genre_list">
                    <p><b>Genres: </b> </p>
                    <li class="chosen_genre" :style="{backgroundColor: getGenreColor(id)}" v-for="id in chosenMedia.genre_ids" :key="id">{{ getGenreName(id) }}</li>
                </ul>
                <p class="overview"><b>Overview: </b> {{ chosenMedia.overview }}</p>
                
            </div>
        </div>
    </div>
</template>
<script>
import { useGenreStore } from '@/stores/genreStore';



export default 
{
    data() {
        return {
            query : '',
            mediaList : [],
            searchMedia : 'Movie',
            show_ChosenMedia : false,
            chosenMedia : null,
            currentPage : 1,
            totalPages : 1,
            showPages : 6,
            showPageMultiplier : 1,
        };
    },
    computed: {
        genreStore(){
            return useGenreStore();
        }
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
                    const response = await fetch(`http://localhost:8000/search-movie/?title=${this.query}&page=${this.currentPage}`);

                    if (!response.ok){
                        throw new Error('Failed to fetch data');
                    }
                    const data = await response.json();
                    this.mediaList = data.movies || [];
                    this.currentPage = data.current_page || 1;
                    this.totalPages = data.total_pages || 1;
                }
                catch (error){
                    console.error('error catching data', error)
                }
            }
            else if (this.searchMedia == "TV Show"){
                try{
                    const response = await fetch(`http://localhost:8000/search-show/?title=${this.query}&page=${this.currentPage}`);

                    if (!response.ok){
                        throw new Error('Failed to fetch data');
                    }
                    const data = await response.json();
                    this.mediaList = data.shows || [];
                    this.currentPage = data.current_page || 1;
                    this.totalPages = data.total_pages || 1;
                }
                catch (error){
                    console.error('error catching data', error)
                }
            }
        },
        toggleMedia(media){
            this.currentPage = 1;
            this.searchMedia = media;
            this.search();
        },
        clearQuery(){
            this.currentPage = 1;
            this.query = '';
            this.mediaList = [];
            this.chosenMedia = null;
            this.show_ChosenMedia = false;
        },
        select(media){
            this.show_ChosenMedia = true;
            this.chosenMedia = media;
            this.mediaList = [];
            this.query = media.title || media.name
            this.currentPage = 1;
        },
        getGenreName(id){
            return this.genreStore.getGenreById(id);

        },
        getGenreColor(id){
            return this.genreStore.getGenreColorById(id);
        },
        changePage(pageNumber){
            this.currentPage = pageNumber;
            this.search();
        },
    },};
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

.media_list_ul{
    display: flex;
    flex-direction: row;
    width: 75rem;
    max-width: 75rem;
    flex-wrap: wrap;
    justify-content: flex-start;
    gap: 1.7rem;
    margin-left: 5rem;
    
}
.media_list_li {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    width: 21rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-size: 0.8rem;
    min-height: 13rem;
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
}
.media_list_button{
    margin-top: 1rem;
    width: 9rem;
    min-height: 1.5rem;
    height: 1.5rem;
    max-height: 1.5rem;
    background-color: #FBFFFE;
    border-radius: 0.3rem;
    border: none;
    color: #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    font-size: 0.8rem;

}
.media_list_button:hover{
    background-color: #41ceaa;
    transition: 0.2s ease;

}

.sub_media_list{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    height: 12rem;
    
    
}
.sub_media_list_ul{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    width: 9rem;
    max-width: 9rem;
    height: 10rem;
    text-align: left;
    gap: 0.3rem;
    padding: 0;
    margin: 0;
}

.pagination_control{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-evenly;
    align-items: center;
    width: 22rem;
    border-radius: 1rem;
    height: 15rem;
    max-height: 15rem;
    gap: 0.5rem;
}
.pagination_control button{
    height: 5rem;
    width: 5rem;
}



.genre_list{
    display: flex;
    flex-wrap: wrap;
    gap: 0.2rem;
    justify-content: flex-start;
    align-items: flex-start;
    width: 10rem;
    max-width: 10rem;
    padding: 0;
    margin: 0;
    font-size: 0.8rem;
    overflow-y: auto;
    scrollbar-width: 1px;
    scrollbar-color:  #1B1B1E #dcdcdc;
}

.genre_list::-webkit-scrollbar{
    width: 3px;
}

.genre_list::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.genre_list::-webkit-scrollbar-track{
    background-color: #dcdcdc;
}

.genre{
    color: #FBFFFE;
    padding-right: 0.4rem;
    padding-left: 0.4rem;
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
    border-radius: 0.3rem;
    
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
.overview{
    height: 7rem;
    overflow-y: auto;
}
.overview::-webkit-scrollbar{
    width: 4px;
}

.overview::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.overview::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.chosen_media_info p{
    gap: 0;
    margin: 0;
    text-align: left;
}
.chosen_genre_list{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
    align-items: center;
    width: 40rem;
    max-width: 40rem;
    padding: 0;
    gap: 0.5rem;
    margin-top: 1rem;
}
.chosen_genre{
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
    padding-left: 0.6rem;
    padding-right: 0.6rem;
    border-radius: 0.5rem;
    color: white;
}



</style>