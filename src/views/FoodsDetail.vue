<template>
    <div v-if="food">
        <FoodArea :food="food" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { parseColorTags } from '../utils/parseColorTags';
import type { food } from "@/types/food.ts";
import FoodArea from "@/components/FoodArea.vue";

const food = ref<food | null>(null);
const route = useRoute();
const router = useRouter();

const getFoodByEnName = async (enName: string): Promise<food | null> => {
    try {
        enName = decodeURIComponent(enName).replace(/\s+/g, '%20');
        console.log("Fetching food data for:", enName);
        const response = await fetch(`/api/foods/${enName}`);
        if (!response.ok) {
            throw new Error(`Error fetching food: ${response.statusText}`);
        }
        const data = await response.json();
        console.log("Fetched food data:", data);
        return data as food;
    } catch (error) {
        console.error("Failed to fetch food data:", error);
        return null;
    }  
};

onMounted(async () => {
    const enName = route.params.enName as string;
    const formattedEnName = enName.replace(/_/g, ' ');
    food.value = await getFoodByEnName(formattedEnName);
    console.log("Food data on mount:", food);
});


</script>

<style>

</style>