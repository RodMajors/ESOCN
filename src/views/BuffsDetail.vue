<template>
  <div class="buffs-detail">
    <BuffArea v-if="buff" :buff="buff" :isDebuff="isDebuff" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import buffsData from '@/Data/buffs.json';
import BuffArea from '@/components/BuffArea.vue';

interface Buff {
  name: string;
  enName: string;
  des: string;
}

interface BuffsData {
  buffs: Buff[];
  debuffs: Buff[];
}

const typedBuffsData = buffsData as BuffsData;
const route = useRoute();
const buff = ref<Buff | null>(null);
const isDebuff = ref(false);

onMounted(() => {
  const enName = route.params.enName as string;
  const formattedEnName = enName.replace(/-/g, ' ');
  buff.value = typedBuffsData.buffs.find(b => b.enName === formattedEnName) || null;
  if (!buff.value) {
    buff.value = typedBuffsData.debuffs.find(b => b.enName === formattedEnName) || null;
    isDebuff.value = !!buff.value; // 如果在 debuffs 中找到，标记为 debuff
  }
  if (buff.value) {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'image';
    link.href = getIconPath(buff.value.enName, isDebuff.value);
    document.head.appendChild(link);
  }
});
  const getIconPath = (enName: string, isDebuff: boolean): string => {
    const formattedName = enName.replace(/\s+/g, '_').toLowerCase();
    const prefix = isDebuff ? 'debuff' : 'buff';
    return `/esoui/art/icons/ability_${prefix}_${formattedName}.webp`;
  };


</script>

<style scoped>
.buffs-detail {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>