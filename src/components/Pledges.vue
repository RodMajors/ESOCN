<template>
    <div class="pledges">
      <h2>无畏者日常</h2>
      <ul>
        <li v-for="pledge in pledges" :key="pledge.enName">
          <RouterLink :to="`/dungeons/${pledge.enName}`">{{ pledge.name }}</RouterLink>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import { RouterLink } from 'vue-router';
  
  interface Pledge {
    name: string;
    enName: string;
  }
  
  const pledges = ref<Pledge[]>([
    { name: '黑暗深渊', enName: 'Dark-Abyss' },
    { name: '火焰山脉', enName: 'Fire-Mountain' },
    { name: '獠牙巢穴', enName: 'Fang-Lair' },
  ]);
  </script>
  
  <style scoped>
  .pledges {
    background-color: #101010; /* 增加背景色，突出块状感 */
    padding: 1rem; /* 内边距 */
    border-radius: 8px; /* 圆角 */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); /* 阴影 */
  }
  
  h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    margin: 0.5rem 0;
  }
  
  a {
    color: #ffcc00;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>