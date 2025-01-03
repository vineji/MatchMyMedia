import { defineStore } from "pinia";

export const useGenreStore = defineStore('genre',{
    state: () => ({
        genreMap: {
            12 : ["Adventure", "#FFFF00"], // VIBRANT YELLOW
            14 : ["Fantasy", "#8A2BE2"],   // BLUE VIOLET
            16 : ["Animation", "#FFD700"], // GOLD
            18 : ["Drama", "#FFFFFF"],     // BLACK
            27 : ["Horror", "#8B0000"],    // DARK RED
            28 : ["Action", "#FF0000"],    // RED
            35 : ["Comedy", "#FFA500"],    // ORANGE
            36 : ["Adventure", "#FFFF00"],
            37 : ["Adventure", "#FFFF00"],
            53 : ["Adventure", "#FFFF00"],
            80 : ["Adventure", "#FFFF00"],
            99 : ["Adventure", "#FFFF00"],
        }
    })
})