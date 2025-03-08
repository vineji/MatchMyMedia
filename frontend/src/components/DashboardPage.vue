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
                            <input v-model="user_data.username" :placeholder="user_data.username" :readonly="readUsername">
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
                            <input v-model="user_data.online_id" :placeholder="user_data.online_id" :readonly="readOnlineId">
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
                            <input v-model="user_data.DOB" :placeholder="user_data.DOB" type="date" :readonly="readDOB">
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
                        <div class="user_info_div">
                            <input v-model="password_form.old_password" placeholder="Enter Old Password" type="password">
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>New Password</b></p>
                        <div class="user_info_div">
                            <input v-model="password_form.new_password_1" placeholder="Enter New Password"  type="password">
                        </div>
                    </li>
                    <li class="user_info_li">
                        <p><b>Confirm New Password</b></p>
                        <div class="user_info_div">
                            <input v-model="password_form.new_password_2" placeholder="Re-enter New Password" type="password">
                        </div>
                    </li>
                    <div class="password_btn_div">
                        <button @click="updatePassword" class="update_btn">Update Password</button>
                        <button @click="cancelPassword" class="cancel_password_btn">Cancel</button>
                    </div>
                </ul>
            </div>   
            <div class="user_genres">
                <p>genre</p>

            </div>      
        </div>
    </div>
</template>
<script>
export default{
    name:"DashboardPage",
    data() {
        return{
            user_data: {},
            password_form: {},
            csrfToken: "",
            readUsername: true,
            readOnlineId: true,
            readDOB: true,
            changePassword: false
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
    justify-content: space-evenly;
    width: 90rem;
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
    border-radius: 2rem;
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
.user_info_div input {
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



</style>