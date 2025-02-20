<template>
    <div v-if="isVisible" class="modal-container">
        <div class="modal">
            <div class="modal-header">
                <p>Recommended Books</p>
                <button @click="close" class="close-button">Close</button>
            </div>
            <ul class="list-container">
                <li class="books_li" v-for="book in recommendedBooks" :key="book.title">
                    <img :src="book.image" class="book_image">
                    <div class="books_li_div">
                        <p><b>Title: </b>{{ book.title }}</p>
                        <p><b>Published: </b>{{ book.published_date }}</p>
                        <p><b>Categories:</b></p>
                        <ul v-if="book.categories.length > 0" class="category_ul">
                            <li class="genre" style="background-color: darkblue;" v-for="category in book.categories" :key="category">{{ category }}</li>
                        </ul>
                        <ul v-else>
                            <li  style="background-color: #9b9a9a;">Unknown</li>
                        </ul>
                        <button>More info</button>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>
<script>
export default{
    props: ['recommendedBooks','isVisible'],
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
    width: 65rem;
}
.books_li{
    display: flex;
    flex-direction: row;
    width: 18rem;
    max-width: 18rem;
    max-height: 12rem;
    font-size: 0.8rem;
    padding: 1rem;
    gap: 0.7rem;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.books_li_div{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.4rem;
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
</style>