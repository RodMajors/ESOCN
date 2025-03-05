<template>
  <div class="dungeon-detail">
    <h1>{{ dungeon?.name }} 攻略</h1>
    <p>这是一个模板化的副本攻略页面。</p>
    <p>英文名称: {{ dungeon?.enName }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

// 定义副本数据的类型
interface Dungeon {
  id: number;
  name: string;
  enName: string;
}

const route = useRoute();
const dungeon = ref<Dungeon | null>(null);

onMounted(async () => {
  const response = await fetch('/src/data/dungeons.json');
  const dungeons: Dungeon[] = await response.json();
  const enName = route.params.enName as string;
  dungeon.value = dungeons.find(d => d.enName === enName) || null;
});
</script>

<style scoped>
.dungeon-detail {
  padding: 2rem;
}
</style>