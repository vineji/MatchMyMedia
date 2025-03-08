<template>
    <div class="page_container">
        <h1>User Dashboard</h1>
        <div class="dashboard_container">   
            <div class="user_info">
                <h2 class="user_info_header">User Information</h2>
                <ul v-if="changePassword == false"  class="user_info_list">
                    <li class="user_info_li">
                        <p><b>Username</b></p>
                        <div class="user_info_div">
                            <input class="user_info_div_input" v-model="user_data.username" :placeholder="user_data.username" :readonly="readUsername">
                            <button v-if="readUsername == true" class="change_btn" @click="changeUsername">Change</button>
                            <div class="change_div" v-else-if="readUsername == false">
                                <button @click="saveUsername" class="save_btn">Save</button>
                                <button @click="cancelUsername" class="cancel_btn">Cancel</button>
                            </div>
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>Online ID</b></p>
                        <div class="user_info_div">
                            <input class="user_info_div_input" v-model="user_data.online_id" :placeholder="user_data.online_id" :readonly="readOnlineId">
                            <button v-if="readOnlineId == true" class="change_btn" @click="changeOnlineId">Change</button>
                            <div class="change_div" v-else-if="readOnlineId == false">
                                <button @click="saveOnlineId" class="save_btn">Save</button>
                                <button @click="cancelOnlineId" class="cancel_btn">Cancel</button>
                            </div>
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>Date of Birth</b></p>
                        <div class="user_info_div">
                            <input class="user_info_div_date" v-model="user_data.DOB" :placeholder="user_data.DOB" type="date" :readonly="readDOB" max="2020-01-01">
                            <button v-if="readDOB == true" class="change_btn" @click="changeDOB">Change</button>
                            <div class="change_div" v-else-if="readDOB == false">
                                <button @click="saveDOB" class="save_btn">Save</button>
                                <button @click="cancelDOB" class="cancel_btn">Cancel</button>
                            </div>
                        </div>
                    </li>
                    <button class="change_password_btn" @click="change_password">Change Password</button>
                </ul>
                <ul v-if="changePassword == true" class="user_info_list">
                    <li class="user_info_li">
                        <p><b>Old Password</b></p>
                        <div class="user_password_div">
                            <input class="user_info_div_input" v-model="password_form.old_password" placeholder="Enter Old Password" :type="showOldPassword ? 'text' : 'password'">
                            <button class="show_password_btn" @click="show_OldPassword">{{showOldPassword ? 'Hide' : 'Show'}}</button>
                            <button class="clear_password_btn" @click="clearOldPassword">Clear</button>
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>New Password</b></p>
                        <div class="user_password_div">
                            <input class="user_info_div_input" v-model="password_form.new_password_1" placeholder="Enter New Password"  :type="showNewPassword1 ? 'text' : 'password'">
                            <button class="show_password_btn" @click="show_NewPassword1">{{showNewPassword1 ? 'Hide' : 'Show'}}</button>
                            <button class="clear_password_btn" @click="clearNewPassword1">Clear</button>
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>Confirm New Password</b></p>
                        <div class="user_password_div">
                            <input class="user_info_div_input" v-model="password_form.new_password_2" placeholder="Re-enter New Password" :type="showNewPassword2 ? 'text' : 'password'">
                            <button class="show_password_btn" @click="show_NewPassword2">{{showNewPassword2 ? 'Hide' : 'Show'}}</button>
                            <button class="clear_password_btn" @click="clearNewPassword2">Clear</button>
                        </div>
                    </li>
                    <div class="password_btn_div">
                        <button @click="updatePassword" class="update_btn">Update Password</button>
                        <button @click="cancelPassword" class="cancel_password_btn">Cancel</button>
                    </div>
                </ul>
            </div>   
            <div class="genre_book_container">
                <div class="add_genre_container">
                    <h3>Favourite Genres</h3>
                    <div class="genre_div">
                        <p>Your Genres:</p>
                        <button class="add_genre_btn" @click="openGenreModal">Add Genre</button>
                    </div>
                    <ul class="user_genre_list">
                        <li class="user_genre" style="background-color: grey;" v-if="user_data.favourite_genres.length == 0">No genres added yet</li>
                        <li v-for="genre in user_data.favourite_genres" :key="genre" class="user_genre" :style=" {backgroundColor: genre[1] } ">{{genre[0]}} <button class="delete_genre_btn" @click="deleteGenre(genre[0])">-</button></li>
                    </ul>
                </div>
                <div class="add_book_container">
                </div>
            </div>  
            <div v-if="openAddGenre == true" class="genre_modal">
                <div class="genre_modal_conatiner">
                    <h4>Add Genre</h4>
                    <div>
                        <input type="text"  placeholder="Enter your own genre"/><button>Add</button>
                    </div>
                    <p>Choose from genres below</p>
                    <ul>

                    </ul>
                </div>
            </div>    
        </div>
    </div>
</template>
<script>
export default{
    name:"DashboardPage",
    data() {
        return{
            user_data: {
                favourite_genres : []
            },
            password_form: {},
            csrfToken: "",
            readUsername: true,
            readOnlineId: true,
            readDOB: true,
            changePassword: false,
            showOldPassword: false,
            showNewPassword1: false,
            showNewPassword2: false,
            openAddGenre: false,
        }
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
        async fetch_user(){
            try{

                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                     },
                    credentials: "include", 
                });


                if (response.ok){
                    const data = await response.json();
                    this.user_data = data;
                    this.user_data.favourite_genres = data.favourite_genres;
                    console.log("Fetched user data");
                }

            }
            catch (error){
                console.error(`${error}`)
            }
        },
        async saveUsername(){
            try{

                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                    body: JSON.stringify({ username: this.user_data.username})
                });

                if (response.ok) {
                    console.log("Username updated successfully");
                    this.readUsername = true;
                }
            }
            catch (error){
                console.error("Error updating username:", error)
            }
        },
        changeUsername(){
            this.readUsername = false;
            this.cancelOnlineId();
            this.cancelDOB();
        },
        cancelUsername(){
            this.fetch_user();
            this.readUsername = true;
        },
        async saveOnlineId(){
            try{

                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                    body: JSON.stringify({ online_id: this.user_data.online_id})
                });

                if (response.ok) {
                    console.log("Online ID updated successfully");
                    this.readOnlineId = true;
                }
            }
            catch (error){
                console.error("Error updating online ID:", error)
            }
        },
        changeOnlineId(){
            this.readOnlineId = false;
            this.cancelUsername();
            this.cancelDOB();
        },
        cancelOnlineId(){
            this.fetch_user();
            this.readOnlineId = true;
        },
        async saveDOB(){
            try{

                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                    body: JSON.stringify({ DOB: this.user_data.DOB})
                });

                if (response.ok) {
                    console.log("DOB updated successfully");
                    this.readDOB = true;
                }
            }
            catch (error){
                console.error("Error updating DOB:", error)
            }
        },
        changeDOB(){
            this.readDOB = false;
            this.cancelUsername();
            this.cancelOnlineId();
        },
        cancelDOB(){
            this.fetch_user();
            this.readDOB = true;
        },
        change_password(){
            this.cancelUsername();
            this.cancelOnlineId();
            this.cancelDOB();
            this.changePassword = true;
        },
        cancelPassword(){
            this.password_form.old_password = "";
            this.password_form.new_password_1 = "";
            this.password_form.new_password_2 = "";
            this.changePassword = false;
        },
        async updatePassword(){
            try{
                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    credentials: "include", 
                    body: JSON.stringify({
                        action : 'change_password',
                        old_password : this.password_form.old_password,
                        new_password1 : this.password_form.new_password_1,
                        new_password2 : this.password_form.new_password_2
                    })
                });

                const data = await response.json();
                if (!response.ok) {
                    let errorMessage = Object.values(data.errors || {}).flat().join("\n");
                    throw new Error(errorMessage || "Unexpected error occured when changing password");
                }
                this.cancelPassword();
            }
            catch (error) {
                console.error("Error:", error);
                alert(error);
            }

        },
        show_OldPassword(){
            this.showOldPassword = !this.showOldPassword;
        },
        show_NewPassword1(){
            this.showNewPassword1 = !this.showNewPassword1;
        },
        show_NewPassword2(){
            this.showNewPassword2 = !this.showNewPassword2;
        },
        clearOldPassword(){
            this.password_form.old_password = '';
        },
        clearNewPassword1(){
            this.password_form.new_password_1 = '';
        },
        clearNewPassword2(){
            this.password_form.new_password_2 = '';
        },
        openGenreModal(){
            this.openAddGenre = true;
        },
        async deleteGenre(genreName){
            try
            {
                const response = await fetch("http://127.0.0.1:8000/user/",
                {    
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrfToken,
                    },
                    body: JSON.stringify({ genre_name: genreName , action: "delete_genre" }),
                    credentials: "include", 
                })
                if (!response.ok) {
                    throw new Error(`Failed to remove genre: ${response.status}`);
                }
                this.fetch_user();
            }
            catch (error){
                console.error("Error removing genre:", error);
            }
        }

    },
    async mounted() {
        await this.fetch_csrf_token();
        this.fetch_user();
    }
};
</script>
<style>

body{
    background-color: rgba(247, 244, 244, 0.944);
}

.page_container{
    display: flex;
    flex-direction: column;
    align-items: center;
}
.dashboard_container{
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 80rem;
    height: 35rem;
}

.user_info{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    background-color: #FBFFFE; 
    width: 33rem;   
    height: 27rem;
    padding: 2rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border-radius: 1.4rem;
}
.user_info_header{
    font-size: 1.8rem;
    margin: 0;
    align-self: center;
    margin-bottom: 1.5rem;
}
.user_info_list{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    width: 31rem;
    height: 24rem;
    margin: 0;
    padding: 0;
    margin-left: 1rem;
    gap: 1rem;

}
.user_info_li p{
    margin: 0;
    padding: 0;
}
.user_info_li{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.user_info_li b{
    font-size: 1.2rem;
}
.user_info_div{
    margin-top: 0.5rem;
    display: flex;
    flex-direction: row;
    width: 31rem;
    justify-content: space-between;
}
.user_info_div_input {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    font-size: 1.2rem;
    border: 3px solid #1B1B1E;
    padding-left: 0.5rem;
    padding-top: 0.6rem;
    padding-bottom: 0.6rem;
    width: 19.5rem;
    border-radius: 0.5rem;
}
.user_info_div_date{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    font-size: 1.2rem;
    border: 3px solid #1B1B1E;
    padding-left: 0.5rem;
    padding-top: 0.47rem;
    padding-bottom: 0.47rem;
    width: 19.5rem;
    border-radius: 0.5rem;

}

.user_genres{
    background-color: aliceblue;  
    width: 35rem;
}

.change_btn{
    all: unset;
    background-color: #0dc43b;
    font-size: 1.2rem;
    color: #FBFFFE;
    font-weight: 401;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.change_btn:hover{
    background-color: #0dc43bae;
}

.button_div{
    margin-top: 2rem;
}

.save_btn{
    all: unset;
    background-color: #0fb485;
    font-size: 1.1rem;
    color: #FBFFFE;
    font-weight: 401;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.save_btn:hover{
    background-color: rgba(13, 196, 144, 0.823);
}
.cancel_btn{
    all: unset;
    background-color: #e51635;
    font-size: 1.1rem;
    color: #FBFFFE;
    font-weight: 401;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.cancel_btn:hover{
    background-color: #ff1538be;
}

.change_div{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 9.5rem;
}
.change_password_btn{
    all: unset;
    margin-top: 1rem;
    height: 3rem;
    width: 10rem;
    font-size: 1.2rem;
    font-weight: 401;
    align-self: flex-start;
    color: #FBFFFE;
    background-color: #c7142f;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}

.change_password_btn:hover{
    background-color: #c7142fa8;

}

.password_btn_div{
    width: 20.4rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}

.update_btn{
    all: unset;

    height: 3rem;
    width: 10rem;
    font-size: 1.2rem;
    font-weight: 401;
    align-self: flex-start;
    color: #FBFFFE;
    background-color: #0fb485;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.update_btn:hover{
    background-color: rgba(13, 196, 144, 0.823);
}
.cancel_password_btn{
    all: unset;
    height: 3rem;
    background-color: #e51635;
    font-size: 1.2rem;
    color: #FBFFFE;
    font-weight: 401;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
    border-radius: 0.5rem;
    transition: 0.2s ease;
}
.cancel_password_btn:hover{
    background-color: #ff1538be;
}
.user_password_div{
    margin-top: 0.5rem;
    display: flex;
    flex-direction: row;
    width: 31rem;

}
.show_password_btn{
    all: unset;
    background-color: #FAA916;
    color: #FBFFFE;
    width: 3rem;
    font-weight: 401;
    font-size: 1.1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    margin-left: 0.3rem;
    transition: 0.2s ease;
}
.show_password_btn:hover{
    background-color: #faaa16b4;
}
.clear_password_btn{
    all: unset;
    background-color: #e51635;
    color: #FBFFFE;
    font-weight: 401;
    font-size: 1.1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.5rem;
    margin-left: 0.3rem;
    transition: 0.2s ease;

}
.clear_password_btn:hover{
    background-color: #e51635b9;
}
.genre_book_container{
    width: 40rem;
    display: flex;
    flex-direction: column;
    height: 31rem;
    justify-content: space-between;
}
.add_genre_container{
    width: 38rem;
    height: 13rem;
    background-color: #FBFFFE;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border-radius: 1.4rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding-left: 2rem;
}
.add_genre_container h3{
    margin-bottom: 0.7rem;
    align-self: center;
    margin-right: 2rem;

}

.add_book_container{
    width: 40rem;
    height: 17rem;
    background-color: #FBFFFE;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border-radius: 1.4rem;
}
.add_genre_btn{
    all: unset;
    font-size: 1.1rem;
    height: 2.5rem;
    font-weight: 401;
    color: #1B1B1E;
    background-color: #FAA916;
    border-radius: 0.5rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    transition: 0.2s ease;
}
.add_genre_btn:hover{
    background-color: #faaa16b9;
    color: #1b1b1ea8;
}
.genre_div{
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 36rem;
    justify-content: space-between;
}
.genre_div p {
    margin: 0;
    padding: 0;
    display: flex;
    align-items: center;
    font-size: 1.1rem;
    height: 2.5rem;
    font-weight: 401;
    color: #1B1B1E;
    background-color: #41ceaa;
    border-radius: 0.5rem;
    padding-left: 0.6rem;
    padding-right: 0.6rem;
}
.genre_modal{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    background: rgba(0,0,0,0.5);
    width: 100%;
    height: 100%;
}
.genre_modal_conatiner{
    display: flex;
    flex-direction: column;
    background-color: #FBFFFE;
    width: 36rem;
    height: 30rem;
    padding-left: 2rem;
    padding-right: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.user_genre_list{
    padding-left: 0;
    padding-top: 0.3rem;
    width: 36rem;
    max-width: 36rem;
    height: 5rem;
    max-height: 5rem;
    overflow-y: scroll;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.user_genre_list::-webkit-scrollbar{
    width: 5px;
}

.user_genre_list::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.user_genre_list::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.user_genre{
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: row;
    color: #FBFFFE;
    font-size: 1rem;
    height: 2rem;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
    border-radius: 0.3rem;
}
.delete_genre_btn{
    padding: 0;
    margin: 0;
    all: unset;
    position: absolute;
    top: -5px;
    right: -5px;
    background-color: #c7142f;
    height: 0.95rem;
    width: 0.95rem;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.9rem;
    font-size: 1.2rem;
    text-align: right;
    font-weight: 501;
}
.delete_genre_btn:hover{
    background-color: #c7142fba;
}




</style>