<template>
    <div class="social_container">
        <div class="other_container">
            {{ userList }}
        </div>
        <div class="user_list_container">
            <h1>Other Users</h1>
            <div class="sort_filter_container">
                <div class="sort_by_container">
                    <button class="sort_button" @click="fetch_all_user">Sort by</button>
                    <select class="sort_select" v-model="sortBy">
                        <option value="Most Common" >Most Common</option>
                        <option value="Least Common" >Least Common</option>
                    </select>
                </div>
                <div class="filter_by_container">

                </div>
            </div>
            
            <li v-for="user in this.userList" :key="user" class="user_box">
                <div class="user_box_header">
                    <p><b>Online ID: </b>{{user.online_id}}</p>
                    <button class="add_friend_btn">Add Friend</button>
                </div>
                <p><b>Genres:</b></p>
                <ul class="user_list_genre_container">
                    <li v-if="user.favourite_genres.length == 0"  class="user_list_genre" >No genres added yet</li>
                    <li v-for="genre in user.favourite_genres" :key="genre" :style="{backgroundColor: genre[1]}"  class="user_list_genre" >{{genre[0]}}</li>
                </ul>
                <button class="view_more_btn">View More</button>
            </li>
        </div>
        
    </div>

</template>
<script>
import { useUserStore } from '@/stores/userStore';
export default {
    data() {
        return {
            userList : {},
            sortBy : "Most Common"
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
        async fetch_all_user(){
            try{
                const response = await fetch("http://127.0.0.1:8000/user-list/",
                {    
                    method: "GET",
                    credentials: "include", 
                });

                if (response.ok){
                    const data = await response.json();
                    this.userList = data.user_list;
                }
                else{
                console.log(`Failed to fetch user list, ${response.statusText}`)
                }
            }
            catch (error){
                console.error(`Error fetching user list, ${error}`)
            }
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
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
}
.user_box_header p{
    margin: 0;
    padding: 0;
    text-align: left;
    font-size: 1.2rem;
    width: 30rem;
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
    width: 18rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}
.filter_by_container{
    width: 19rem;
    display: flex;
    flex-direction: row;
    background-color: aqua;
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
    font-size: 1.2rem;
    height: 2.5rem;
    padding-right: 1rem;
    padding-left: 1rem;
    border: 2px solid #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
</style>