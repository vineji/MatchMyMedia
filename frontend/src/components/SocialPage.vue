<template>
    <div class="social_container">
        <div class="other_container">
        </div>
        <div class="user_list_container">
            <h1>Other Users</h1>
            <div class="sort_filter_container">
                <div class="sort_by_container">
                    <button class="sort_button" @click="fetch_all_user">Sort by</button>
                    <select class="sort_select" v-model="sortBy">
                        <option value="Most Common" >Most Common Genres</option>
                        <option value="Least Common" >Least Common Genres </option>
                    </select>
                </div>
                <div class="filter_by_container">
                    <button class="filter_button" @click="fetch_all_user">Filter</button>
                    <label>Min age:</label>
                    <input type="number" min="10" max="100" v-model.number="minAge">
                    <label>Max age:</label>
                    <input type="number" v-model.number="maxAge" min="10" max="100">
                    <button class="reset_button" @click="reset">Reset</button>
                </div>
            </div>
            <li class="user_box_not_found" v-if="userList.length == 0"> No users found</li>
            <li v-for="user in userList" :key="user" class="user_box">
                <div class="user_box_header">
                    <p><b>Online ID: </b>{{user.online_id}}</p>
                    <button class="add_friend_btn">Add Friend</button>
                </div>
                <p><b>Favourite genres:</b></p>
                <ul class="user_list_genre_container">
                    <li v-if="user.favourite_genres.length == 0"  class="user_list_genre" >No genres added yet</li>
                    <li v-for="genre in user.favourite_genres" :key="genre" :style="{backgroundColor: genre[1]}"  class="user_list_genre" >{{genre[0]}}</li>
                </ul>
                <button class="view_more_btn">View More</button>
            </li>
            <div class="pagination_container">
                <button :disabled="hasPrevious == false" @click="fetch_all_user(currentPage - 1)" class="pagination_button">Previous</button>
                <button :disabled="hasNext == false" @click="fetch_all_user(currentPage + 1)" class="pagination_button">Next</button>
            </div>
        </div>
        
    </div>

</template>
<script>
import { useUserStore } from '@/stores/userStore';
export default {
    data() {
        return {
            userList : [],
            csrfToken : "",
            sortBy : "Most Common",
            minAge : null,
            maxAge : null,
            currentPage: 1,
            totalPages: 1,
            hasNext: false,
            hasPrevious: false,
        }
    },
    setup(){
        const userStore = useUserStore();
        userStore.loadUser();
        return {userStore};
    },
    computed: {
        loggedUser(){
            return{
                id: this.userStore.user_id || null,
                online_id: this.userStore.online_id || null,
                favourite_genres: this.userStore.favourite_genres || [],
            }
        },
    },
    methods: {
        async fetch_csrf_token(){
            try{
                const response = await fetch("http://127.0.0.1:8000/csrf/",
                {    
                    method: "GET",
                    credentials: "include", 
                });

                if (response.ok){
                    const data = await response.json();
                    this.csrfToken = data.csrfToken;
                    console.log(`Fetched csrf token: ${this.csrfToken}`);
                }
                else{
                console.log(`Failed to fetch token, ${response.statusText}`)
                }
            }
            catch (error){
                console.error(`Error fetching token, ${error}`)
            }
        },
        async fetch_all_user(page = 1){
            try{
                const params = new URLSearchParams();
                params.append('sort', this.sortBy.toString());
                params.append('page', page.toString())

                if (this.minAge !== null){
                    params.append('minAge', this.minAge);
                }
                if (this.maxAge !== null){
                    params.append('maxAge', this.maxAge);
                }

                const response = await fetch(`http://127.0.0.1:8000/user-list/?${params.toString()}`,
                {    
                    method: "GET",
                    credentials: "include", 
                });

                if (response.ok){
                    const data = await response.json();
                    this.userList = data.user_list;
                    this.currentPage = data.current_page;
                    this.totalPages = data.total_pages;
                    this.hasNext = data.has_next;
                    this.hasPrevious = data.has_previous;
                }
                else{
                console.log(`Failed to fetch user list, ${response.statusText}`)
                }
            }
            catch (error){
                console.error(`Error fetching user list, ${error}`)
            }
        },
        reset(){
            this.minAge = null;
            this.maxAge = null;
            this.sortBy = "Most Common";
            this.fetch_all_user();
        }
    },
    mounted(){
        this.fetch_all_user();
    }
}

</script>
<style>
.social_container{
    display: flex;
    flex-direction: row;
    justify-content: space-between;

}
.other_container{
    width: 50rem;
}
.user_list_container{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    width: 60rem;

}
.user_box_not_found{
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 1.3rem;
    width: 39rem;
    padding-top: 1.5rem;
    padding-right: 1.5rem;
    padding-left: 1.5rem;
    padding-bottom: 1.5rem;
    background-color: #FBFFFE;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-size: 2rem;
    gap: 1rem;
}
.user_box{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    border-radius: 1.3rem;
    width: 39rem;
    padding-top: 1.5rem;
    padding-right: 1.5rem;
    padding-left: 1.5rem;
    padding-bottom: 0.5rem;
    background-color: #FBFFFE;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    font-size: 1.2rem;
    gap: 1rem;
}
.user_box p{
    padding: 0;
    margin: 0;
}
.user_box_header{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}
.user_box_header p{
    margin: 0;
    padding: 0;
    text-align: left;
    font-size: 1.2rem;
    width: 28rem;
}
.user_box_header b{
    padding-right: 1rem;
}
.user_list_genre_container{
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: #1B1B1E #f0efef;
    max-height: 5rem;
    gap: 0.8rem;
    width: 100%;
    padding-left: 0.1rem;
    padding-bottom: 1rem;
}
.user_list_genre_container::-webkit-scrollbar{
    width: 7px;
}

.user_list_genre_container::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.user_list_genre_container::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.user_list_genre_container p{
    padding: 0;
    margin: 0;
    text-align: left;
}
.user_list_genre{
    color: #FBFFFE;
    background-color: grey;
    padding-top: 0.3rem;
    padding-bottom: 0.3rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    border-radius: 0.6rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.add_friend_btn{
    margin: 0;
    padding: 0;
    all: unset;
    background-color: #248eff;
    color: #1B1B1E;
    font-weight: 700;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.3rem;
    font-size: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.view_more_btn{
    all: unset;
    font-size: 1rem;
    align-self: center;
    text-decoration: underline;
}
.sort_filter_container{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 42rem;
}
.sort_by_container{
    width: 16rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.sort_button{
    all: unset;
    background-color: #FAA916;
    color: #1B1B1E;
    font-size: 1.3rem;
    font-weight: 700;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}
.sort_button:hover{
    background-color: #faaa16bf;
    color: #1b1b1eb0;
}
.sort_select{
    display: flex;
    align-items: center;
    background-color: #FBFFFE;
    font-size: 1.1rem;
    width: 9rem;
    height: 2.5rem;
    border-radius: 0.5rem;
    border: 2px solid #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.filter_by_container{
    width: 24rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.filter_by_container input{
    all: unset;
    background-color: #FBFFFE;
    align-items: center;
    width: 3rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.filter_by_container label{
    font-weight: 500;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.reset_button{
    all: unset;
    margin-left: 0.9rem;
    background-color: #e51635;
    color: #FBFFFE;
    font-size: 1.3rem;
    font-weight: 700;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;

}
.reset_button:hover{
    background-color: #e51635ca;
    color: #fbfffed1;
}
.filter_button{
    all: unset;
    background-color: #41ceaa;
    color: #1B1B1E;
    font-size: 1.3rem;
    font-weight: 700;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}
.filter_button:hover{
    background-color: #41ceabd3;
    color: #1b1b1eb0;
}
.pagination_container{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 42rem;
}
.pagination_button{
    all: unset;
    font-weight: 500;
    font-size: 1.2rem;
    background-color: #FBFFFE;
    color: #1B1B1E;
    border: 3px solid #1B1B1E;
    border-radius: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}
.pagination_button:hover{
    background-color: #1B1B1E;
    color: #FBFFFE;
}
.pagination_button:disabled{
    background-color: #fbfffeb6;
    color: #1b1b1e74;
    border: 3px solid #1b1b1e74;
}
</style>