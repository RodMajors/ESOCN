<template>
    <div class="news-list">
      <h1>每日新闻</h1>
      <ul>
        <li v-for="news in newsList" :key="news.id">
          <RouterLink :to="`/news/${news.id}`">{{ news.title }}</RouterLink>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import { RouterLink } from 'vue-router';
  
  const newsList = ref([
    { id: 1, title: '新副本上线公告' },
    { id: 2, title: '服务器维护通知' },
  ]);
  </script>
  
  <style scoped>
  .news-list {
    padding: 2rem;
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