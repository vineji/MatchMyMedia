<template>
    <div v-if="isVisible" class="modal-container">
        <div class="modal">
            <div class="modal-header">
                <p>Recommended books for: {{ mediaType }} - {{ mediaName }}</p>
                <button @click="close" class="close-button">Close</button>
            </div>
            <ul class="list-container">
                <li class="books_li" v-for="book in recommendedBooks" :key="book.title">
                    <img :src="book.image" class="book_image">
                    <div class="books_li_container">
                        <div class="books_li_div">
                            <p class="book_div_title"><b>Title: </b>{{ book.title }}</p>
                            <p><b>Published: </b>{{ book.published_date }}</p>
                            <div class="books_li_authors">
                                <p><b>Authors: </b></p>
                                <li style="padding-right: 0.3rem;" v-for="(author,index) in book.authors" :key="index">
                                    <span :style="{fontWeight : '900'}">{{ author.charAt(0) }}</span>{{ author.slice(1) }}
                                </li>
                            </div>
                            <div class="books_li_categories">
                                <p><b>Categories:</b></p>
                                <ul v-if="book.categories.length > 0" class="category_ul">
                                    <li class="rcmnd_genre" style="background-color: darkblue;" v-for="category in book.categories" :key="category">{{ category }}</li>
                                </ul>
                                <ul v-else>
                                    <li  style="background-color: #9b9a9a;">Unknown</li>
                                </ul>
                            </div>
                        </div>
                        <button class="more_info">More info</button>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>
<script>
export default{
    props: ['recommendedBooks','isVisible','mediaType','mediaName'],
    methods: {
        close(){
            this.$emit('update:isVisible', false);
        }
    }
}
</script>
<style>
.modal-container{
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
.modal{
    background-color: #FBFFFE;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 75rem;
    max-width: 75rem;
    height: 40rem;
    max-height: 40rem;
    border-radius: 1rem;

}
.list-container{
    height: 30rem;
    max-height: 30rem;
    width: 65rem;
    max-width: 65rem;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    overflow-x: auto;
    gap: 1rem;
    padding-bottom: 1rem;
    padding-top: 0.5rem;

}
.modal-header{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 93%;
    margin-left: 1rem;
}
.books_li_container{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 12rem;
}
.books_li{
    display: flex;
    flex-direction: row;
    width: 18rem;
    max-width: 18rem;
    max-height: 12rem;
    font-size: 0.85rem;
    padding: 1rem;
    gap: 0.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}

.books_li:hover{
    transform: scale(1.06);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.books_li_div{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
    height: 10.5rem;

}
.books_li p{
    gap: 0;
    margin: 0;
    text-align: left;
}
.book_image{
    height: 12rem;
    width: 8rem;
    max-width: 8rem;
    border-radius: 0.3rem;
}
.category_ul{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    margin: 0;
    padding: 0;
}
.book_div_title{
    max-height: 6rem;
    overflow-y: auto;
    width: 9.5rem;
    padding-right: 0.1rem;
}

.book_div_title::-webkit-scrollbar{
    width: 3px;
}

.book_div_title::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.book_div_title::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.books_li_authors{
    width: 9.6rem;
    max-height: 2.3rem;
    overflow-y: auto;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
}
.books_li_authors p{
    padding-right: 0.3rem;
}
.books_li_authors::-webkit-scrollbar{
    width: 3px;
}

.books_li_authors::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.books_li_authors::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}

.books_li_categories{
    width: 9.6rem;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    height: 2.5rem;
    overflow-y: auto;
}
.books_li_categories::-webkit-scrollbar{
    width: 3px;
}

.books_li_categories::-webkit-scrollbar-thumb{
    background-color: #1B1B1E;
    border-radius: 1rem;
}
.books_li_categories::-webkit-scrollbar-track{
    background-color: #dcdcdc;
    border-radius: 1rem;
}
.books_li_categories p{
    padding-right: 0.3rem;
}

.rcmnd_genre{
    display: inline-block;
    color: #FBFFFE;
    padding-right: 0.3rem;
    padding-left: 0.3rem;
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
    border-radius: 0.3rem;
    max-width: 8rem;
    font-size: 0.8rem;
}
.more_info{
    align-self: center;
    justify-self: flex-end;
    width: 8rem;
    height: 1.3rem;
    background-color: #FBFFFE;
    border-radius: 0.3rem;
    border: none;
    color: #1B1B1E;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    font-size: 0.8rem;
    transition: 0.2s ease;
}

.more_info:hover{
    background-color: #41ceaa;
    transition: 0.2s ease;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.close-button{
    all: unset;
    width: 4rem;
    font-size: 1.2rem;
    border: none;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    border-radius: 0.5rem;
    color: #FBFFFE;
    background-color: #e51635;
}
.close-button:hover{
    font-weight: 600;
    background-color: #ff1538;
    transition: ease 0.3s;
    
}
</style>