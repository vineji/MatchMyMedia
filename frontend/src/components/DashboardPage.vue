<template>
    <div >
        <p>Dashboard</p>
        <p>{{ user_data }}</p>
    </div>
</template>
<script>
export default{
    name:"DashboardPage",
    data() {
        return{
            user_data: {},
            csrfToken: ""
        }
    },
    methods : {
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

        }

    },
    async mounted() {
        await this.fetch_csrf_token();
        this.fetch_user();
    }
};
</script>
<style>

</style>