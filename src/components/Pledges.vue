<template>
    <div class="pledges">
      <h2>无畏者日常</h2>
      <ul>
        <li v-for="pledge in pledges" :key="pledge.enName">
          <DungeonImage class = 'dungeon'
                  :name="pledge.name"
                  :en-name="pledge.enName"
                  :background="pledge.background"
          />
        </li>
      </ul>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import { RouterLink } from 'vue-router';
  import DungeonImage from '../components/DungeonImage.vue'; // 导入新组件
  
  interface Pledge {
    name: string;
    enName: string;
    background: string;
  }
  
  const pledges = ref<Pledge[]>([
    { name: '獠牙巢穴', enName: 'fang-lair', background: 'https://images.uesp.net/9/93/ON-load-Fang_Lair.jpg'},
    { name: '唤鳞者之巅', enName: 'Scalecaller-Peak', background: 'https://images.uesp.net/2/23/ON-load-Scalecaller_Peak.jpg' },
    { name: '白金塔', enName: 'white-gold-tower', background: 'https://images.uesp.net/b/b0/ON-load-White-Gold_Tower.jpg' },
  ]);
  </script>
    
  <style scoped>
  .pledges {
    background-color: #101010; /* 增加背景色，突出块状感 */
    border-radius: 8px; /* 圆角 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); /* 阴影 */
    max-height: 305px;
  }
  .dungeon{
    max-height: 80px ;
    cursor: pointer;
  }
  h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    padding: 0 0 0 1rem; /* 内边距 */
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    margin-top: 0.15rem;
  }
  
  a {
    color: #ffcc00;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>