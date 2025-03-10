<!-- src/components/SkillArea.vue -->
<template>
    <div class="skill-area">
      <img :src="skill.icon" alt="skill icon" class="skill-icon" />
      <h3>{{ skill.name }}</h3>
      <p class="en-name">{{ skill.enName?.toUpperCase() }}</p>
      <hr class="divider" />
      <div class="skill-stats">
        <div class="stat-item" v-if="skill.cost">
          <span class="label">消耗:</span>
          <div class="cost-values">
            <span class="value" v-if="skill.ultimate">{{ formatCost(skill.cost, skill.ultimate) }}</span>
            <span class="value" 
              v-if="skill.magickaCost"
              v-html="parseColorTags2(skill.magickaCost + '魔力')"
            ></span>
            <span class="value" 
              v-if="skill.staminaCost"
              v-html="parseColorTags2(skill.staminaCost + '耐力')"
            ></span>
            <span class="value" 
              v-if="skill.healthCost"
              v-html="parseColorTags2(skill.healthCost + '生命')"
            ></span>
          </div>
        </div>
        <div class="stat-item">
          <span class="label">{{ skill.isChanneled ? '引导时间:' : '施法时间:' }}</span>
          <span class="value">{{ formatCastTime(skill.castTime) }}</span>
        </div>
        <div v-if = "skill.target" class="stat-item">
          <span class="label">目标:</span>
          <span class="value">{{ skill.target || '无' }}</span>
        </div>
        <div v-if = "skill.duration" class="stat-item">
          <span class="label">持续时间:</span>
          <span class="value">{{ formatDuration(skill.duration) }}</span>
        </div>
        <div class="stat-item" v-if="skill.radius">
          <span class="label">技能范围:</span>
          <span class="value">{{ formatDistance(skill.radius) }}</span>
        </div>
        <div class="stat-item" v-if="skill.maxRange">
          <span class="label">施法距离:</span>
          <span class="value">{{ formatDistance(skill.maxRange) }}</span>
        </div>
      </div>
      <hr class="divider" />
      <div class="skill-description" v-html="parseColorTags2(skill.description || '无描述')"></div>
      <div v-if="skill.newEffect" class="skill-new-effect" style = "font-weight: bold;">新效果</div>
      <div v-if="skill.newEffect" class="skill-new-effect" v-html="skill.newEffect"></div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps } from 'vue';
  import type { skills } from '@/types/skills';
  import { parseColorTags2 } from '@/utils/parseColorTags2';
  
  // 定义传入的 props 类型
  const props = defineProps<{
    skill: skills;
  }>();
  
  // 格式化消耗（检查 ultimate）
  const formatCost = (cost: number | null | undefined, ultimate: number | null | undefined) => {
    if (cost === null || cost === undefined) return '无';
    return ultimate === 1 ? `${cost} 终极点` : `${cost}`;
  };
  
  // 格式化施法/引导时间（毫秒转秒）
  const formatCastTime = (castTime: number | null | undefined) => {
    if (castTime === 0) return '瞬发';
    return castTime ? `${(castTime / 1000)} 秒` : '0 秒';
  };
  
  // 格式化持续时间（毫秒转秒）
  const formatDuration = (duration: number | null | undefined) => {
    return duration ? `${(duration / 1000)} 秒` : '0 秒';
  };
  
  // 格式化距离（厘米转米）
  const formatDistance = (distance: number | null | undefined) => {
    return distance ? `${(distance / 100)} 米` : '0 米';
  };
  </script>
  
  <style scoped>
  .skill-area {
    background-color: #000000;
    border: 1px solid #333333; /* 细边框 */
    padding: 15px;
    border-radius: 5px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
  }
  
  .skill-icon {
    display: block;
    width: 64px;
    height: 64px;
    margin: 0 auto 10px; /* 居中且与下方间距 */
    border-radius: 5px;
  }
  
  h3 {
    font-size: 18px;
    font-weight: bold;
    color: #F6E43A;
    text-align: center;
    margin: 0 0 5px;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px;
  }
  
  .en-name {
    font-size: 16px;
    color: #F6E43A;
    text-align: center;
    font-weight: bold;
    margin: 0 0 10px;
  }
  
  .divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #555555, transparent); /* 两头渐隐 */
    margin: 10px 0;
  }
  
  .skill-stats {
    margin-left: .6rem;
    margin-right: .6rem;
    flex-grow: 1; /* 占据剩余空间 */
  }
  
  .stat-item {
    display: flex;
    justify-content: space-between;
    margin: 5px 0;
  }
  
  .label {
    font-size: 14px;
    color: #e5e2b9;
    text-align: left;
  }
  
  .cost-values {
    display: flex;
    flex-direction: column; /* 设置为垂直排列 */
    align-items: flex-end; /* 右对齐 */
  }

  .value {
    font-size: 14px;
    color: #ffffff;
    text-align: right;
    margin: 2px 0; /* 添加间距，避免文字过于紧凑 */
  }
  
  .skill-description {
    font-size: 14px;
    margin-bottom: 10px;
    text-align: center;
  }
  
  .skill-new-effect {
    font-size: 14px;
    color: #55cf43; /* 绿色 */
    text-align: center;
  }
  </style>