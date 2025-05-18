<template>
    <div class="buffs-list">
      <table>
        <tbody>
          <tr
            v-for="(buff, index) in allBuffs"
            :key="buff.enName"
            :class="index % 2 === 0 ? 'row-dark' : 'row-light'"
            @click="goToDetail(buff.enName)"
          >
          <td class="icon-column">
            <img :src="getIconPath(buff.enName, buff.isDebuff)" class="buff-icon" alt="Buff Icon" loading="lazy" />
          </td>
            <td class="name-column">{{ buff.name }}</td>
            <td class="en-name-column">&lt;{{ buff.enName }}&gt;</td>
            <td class="des-column" v-html="parseColorTags(buff.des)"></td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue';
  import { useRouter } from 'vue-router';
  import buffsData from '@/Data/buffs.json'; // 使用 @ 表示 src 目录
  import { parseColorTags } from '@/utils/parseColorTags';
  
  // 定义 Buff 接口，添加 isDebuff 用于区分
  interface Buff {
    name: string;
    enName: string;
    des: string;
    isDebuff?: boolean; // 添加标记
  }
  
  // 定义 JSON 文件结构
  interface BuffsData {
    buffs: Buff[];
    debuffs: Buff[];
  }
  
  // 类型断言
  const typedBuffsData = buffsData as BuffsData;
  
  const router = useRouter();
  
  // 合并 buffs 和 debuffs，并添   isDebuff 标记
  const allBuffs = computed(() => {
    const buffsWithType = typedBuffsData.buffs.map(buff => ({ ...buff, isDebuff: false }));
    const debuffsWithType = typedBuffsData.debuffs.map(debuff => ({ ...debuff, isDebuff: true }));
    return [...buffsWithType, ...debuffsWithType];
  });
  
  // 获取图标路径，根据 isDebuff 区分 buff 和 debuff
  const getIconPath = (enName: string, isDebuff: boolean = false): string => {
    if (enName == "Empower") {
      return '/esoui/art/icons/ability_buff_major_empower.webp'
    }
    const formattedName = enName.replace(/\s+/g, '_').toLowerCase();
    const prefix = isDebuff ? 'debuff' : 'buff';
    return `/esoui/art/icons/ability_${prefix}_${formattedName}.webp`;
  };
  
  // 跳转到详情页
  const goToDetail = (enName: string) => {
    const formattedName = enName.replace(/\s+/g, '-');
    router.push(`/buffs/${formattedName}`);
  };
  </script>
  
  <style scoped>
  .buffs-list {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    background-color: #101010;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  }
  
  td {
    padding: 0.5rem;
    text-align: center;
    border-bottom: 1px solid #444;
    vertical-align: middle;
  }
  
  .icon-column {
    width: 10%;
    padding: 0 0.5rem 0 1rem;
  }
  
  .buff-icon {
    width: 48px;
    height: 48px;
    object-fit: contain;
  }
  
  .name-column {
    width: 20%;
  }
  
  .en-name-column {
    font-family: "Centaur", 'Trebuchet MS', sans-serif ;
    width: 25%;
  }
  
  .des-column {
    width: 45%;
    text-align: left;
  }
  
  .row-dark {
    background-color: #1A1A1A;
  }
  
  .row-light {
    background-color: #262626;
  }
  
  tr {
    cursor: pointer;
  }
  
  tr:hover {
    background-color: #333333;
  }
  </style>