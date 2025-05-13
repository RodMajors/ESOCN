<template>
    <div class="champion-area">
      <div class="header">
        <span class="category">{{ skill.category_name }}</span>
        <span class="slottable">{{ skill.is_slottable ? '需要装配' : '被动生效' }}</span>
      </div>
      <img
        class="category-icon"
        :src="categoryIcon"
        alt="类别图标"
      />
      <h2 class="name">{{ skill.name }}</h2>
      <p class="en-name">&lt;{{ skill.en_name }}&gt;</p>
      <div class="divider"></div>
      <div class="description" v-html="parseColorTags(skill.description)"></div>
    </div>
  </template>
  <script lang="ts">
  import { defineComponent, computed } from 'vue';
  import type { PropType } from 'vue';
  import { parseColorTags } from '@/utils/parseColorTags';
  import type { ChampionSkill } from '@/utils/loadChampion';
  
  export default defineComponent({
    name: 'ChampionArea',
    props: {
      skill: {
        type: Object as PropType<ChampionSkill>,
        required: true
      }
    },
    setup(props) {
      // 计算图标路径
      const categoryIcon = computed(() => {
        switch (props.skill.category_id) {
          case 1:
            return '/background/cp/ON-icon-Champion_Magicka.png'; // 法师
          case 2:
            return '/background/cp/ON-icon-Champion_Health.png'; // 战士
          case 3:
            return '/background/cp/ON-icon-Champion_Stamina.png'; // 盗贼
          default:
            return ''; // 默认无图标
        }
      });
  
      return { parseColorTags, categoryIcon };
    }
  });
  </script>
  <style scoped>
  /* 现有样式保持不变 */
  .champion-area {
    width: 300px;
    padding: 1rem;
    background-color: #000000;
    border: 1px solid #444;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    margin: 0.5rem;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  .category {
    font-size: 0.9rem;
  }
  
  .slottable {
    font-size: 0.9rem;
  }
  
  .name {
    text-align: center;
    font-size: 1.2rem;
    margin: 0;
    color: #F6E43A;
    font-weight: 550;
  }
  
  .en-name {
    text-align: center;
    font-size: 0.9rem;
    color: #F6E43A;
    font-weight: 550;
  }
  
  .category-icon {
    display: block;
    width: 48px;
    height: 48px;
    margin: 10px auto; /* 居中并添加间距 */
  }
  
  /* 其他样式（divider, description等）不变 */
  .divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(to right, transparent, #fff, transparent);
    margin: 1rem auto;
  }
  
  .description {
    font-size: 0.9em;
    line-height: 1.5;
    text-align: center;
  }
  
  /* 响应式 */
  @media (max-width: 768px) {
    .champion-area {
      padding: 15px;
      max-width: 90%;
    }
  
    .name {
      font-size: 1.5em;
    }
  
    .en-name {
      font-size: 1em;
    }
  
    .category-icon {
      width: 48px;
      height: 48px;
    }
  }
  </style>