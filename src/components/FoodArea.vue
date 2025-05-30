<template>
    <div class="food-area" v-if="food">
        <div class="type-place">
            <div>
                <span class="type" :style="{ color: getTypeColor(food.specializedItemTypeText) }">{{food.specializedItemTypeText}}</span>
                <br>
                <span class="place">{{ food.canBeCrafted ? "可制造" : "不可制造" }}</span>
            </div>
            <div>
                <span class="place" :style="{ color: getQualityColor(food.quality) }">{{ food.quality }}</span>
            </div>
            
        </div>
        <div class="center-content">
            <img :src="food.icon" alt="Food Icon" class="food-icon">
        </div>
        <div class="name-container" :style="{ color: getQualityColor(food.quality) }">
            <span class="name">{{ food.name }}</span>
            <br>
            <span class="en-name">&lt;{{ food.enName.toUpperCase() }}&gt;</span>
        </div>
        <div class="divider"></div>
        <div 
            class="description"
            v-html="parseColorTags(food.description)"
        ></div>
        <br>
        <div v-if="food.ingredients" class="ingredients-column">
            <div class="ingredients">制作原料：</div>
            <span 
                class="ingredients"
                v-for="(index, ingredient) in food.ingredients"
                :key="index"
            >
            {{ ingredient }}({{ index }})
            </span>
        </div>
    </div>
</template>

<script lang="ts">
import { ref, onMounted, computed, watch, defineComponent} from "vue";
import { useRouter, useRoute } from "vue-router";
import { parseColorTags } from '../utils/parseColorTags';
import type { food } from "@/types/food.ts";

export default defineComponent({
    name: 'FoodArea',
    props: {
        food: {
            type: Object as () => food,
            required: true
        }
    },
    setup(props) {
        const getQualityColor = (quality: string): string => {
            switch (quality) {
                case '传说':
                    return '#DCC55F';
                case '优良':
                    return '#6BC34B';
                case '普通':
                    return '#6BC34B';
                case '上乘':
                    return '#6797EC';
                case '史诗':
                    return '#9B4AE5'; // Gold color for Legendary
                default:
                    return '#FFFFFF'; // Default to white if unknown
            }
        };
        const getTypeColor = (type: string): string => {
            switch (type) {
                case '肉类餐食' :
                case '水果餐食' :
                case '蔬菜餐食' :
                case '酒精饮料' :
                case '茶饮料' :
                case '补品饮料' :
                    return '#6BC34B'; // Tomato color for Food
                case '小吃餐食':
                case '蔬菜炖肉餐食':
                case '甜点餐食':
                case '利口酒饮料':
                case '酊剂饮料':
                case '甜果汁茶饮料' :
                    return '#6797EC'; // SteelBlue for Drink
                case '精致餐食':
                case '蒸馏物饮料':
                    return '#9B4AE5'; // LimeGreen for Potion
                case '饮品':
                case '独特餐食':
                    return '#DCC55F'; // Default to white if unknown
                default:
                    return '#FFFFFF'; // Default to white if unknown
            }
        };

        return {
            getQualityColor,
            getTypeColor,
            parseColorTags
        };
    },
    
});



</script>

<style>
.food-area {
  width: 300px;
  padding: 1rem;
  background-color: #000000;
  border: 1px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  margin: 0.5rem;
}

.type-place {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.type-place .type,
.type-place .place {
  font-size: 0.9rem;
  color: #C5C29E;
}

.center-content {
  text-align: center;
}

.food-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
}

.name-container {
  margin-bottom: 1rem;
  text-align: center;
}

.name-container .name {
  font-size: 1.2rem;
}

.name-container .en-name {
  font-size: 0.9rem;
}

.divider {
  width: 100%;
  height: 1px;
  background: linear-gradient(to right, transparent, #fff, transparent);
  margin: 1rem auto;
}

.description {
  font-size: 0.9rem;
  color: #C5C29E;
  text-align: center;
}

.ingredients-column{
    margin: auto;
    
    text-align: center;
}

.ingredients{
    font-size: 14px;
    color: #55cf43; /* 绿色 */
    text-align: center;
}


</style>