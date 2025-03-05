<template>
  <div class="buff-area">
    <!-- 左上角：Buff/Debuff 类型 -->
    <div class="type-place">
      <div>
        <span class="type">{{ isDebuff ? 'Debuff' : 'Buff' }}</span>
      </div>
    </div>

    <!-- 居中内容 -->
    <div class="center-content">
      <!-- Buff 图标 -->
      <img :src="getIconPath(buff.enName)" class="buff-icon" alt="Buff Icon" loading="lazy" />

      <!-- Buff 名称和英文名 -->
      <div class="name-container">
        <span class="name">{{ buff.name }}</span>
        <br />
        <span class="en-name">&lt;{{ buff.enName }}&gt;</span>
      </div>

      <!-- 分割线 -->
      <div class="divider"></div>

      <!-- Buff 描述 -->
      <div class="description" v-html="parseColorTags(buff.des)"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { parseColorTags } from '../utils/parseColorTags';

// 定义 props
const { buff, isDebuff } = defineProps<{
  buff: {
    name: string;
    enName: string;
    des: string;
  };
  isDebuff: boolean;
}>();

// 获取图标路径，根据 isDebuff 区分 buff 和 debuff
const getIconPath = (enName: string): string => {
  const formattedName = enName.replace(/\s+/g, '_').toLowerCase();
  const prefix = isDebuff ? 'debuff' : 'buff'; // 直接使用解构的 isDebuff
  return `/esoui/art/icons/ability_${prefix}_${formattedName}.webp`;
};
</script>

<style scoped>
.buff-area {
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
  justify-content: flex-start;
  margin-bottom: 1rem;
}

.type-place .type {
  font-size: 0.9rem;
  color: #C5C29E;
}

.center-content {
  text-align: center;
}

.buff-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
}

.name-container {
  margin-bottom: 1rem;
}

.name-container .name {
  font-size: 1.2rem;
  color: #F6E43A;
}

.name-container .en-name {
  font-size: 0.9rem;
  color: #F6E43A;
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
</style>