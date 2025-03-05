<template>
  <div class="equipment-detail">
    <template v-if="set">
      <!-- 使用 GearArea 组件展示套装信息 -->
      <GearArea :set="set" />
    </template>
    <div v-else>未找到套装</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { loadEquipment } from '../utils/loadEquipment';
import GearArea from '../components/GearArea.vue'; // 引入 GearArea 组件

interface EquipmentSet {
  name: string;
  enName: string;
  place: string;
  bonuses: { [key: string]: string }; // 修复 bonuses 类型
  type: number;
  styles?: {
    武器?: { [key: string]: any };
    护甲?: { [key: string]: any };
  };
}

const route = useRoute();
const set = ref<EquipmentSet | null>(null);

onMounted(() => {
  const equipmentData = loadEquipment();
  // 将路由参数中的 - 转换回空格
  const enName = (route.params.enName as string).replace(/-/g, ' ');
  set.value = equipmentData.find((s) => s.enName === enName) || null;
  console.log('Equipment detail loaded:', set.value);
});
</script>

<style scoped>
.equipment-detail {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>