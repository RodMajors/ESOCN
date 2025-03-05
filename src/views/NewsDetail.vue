<template>
    <div class="news-detail">
      <h1>{{ news?.title }}</h1>
      <p>这是一个模板化的新闻页面。</p>
      <p>新闻ID: {{ news?.id }}</p>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  const news = ref<{ id: number; title: string } | null>(null);
  
  const newsList = [
    { id: 1, title: '新副本上线公告' },
    { id: 2, title: '服务器维护通知' },
  ];
  
  onMounted(() => {
    const id = Number(route.params.id);
    news.value = newsList.find(n => n.id === id) || null;
  });
  </script>
  
  <style scoped>
  .news-detail {
    padding: 2rem;
  }
  </style>