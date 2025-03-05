<template>
    <div class="sidebar-container">
      <Pledges />
      <ServerStatus />
    </div>
  </template>
  
  <script setup lang="ts">
  import Pledges from './Pledges.vue';
  import ServerStatus from './ServerStatus.vue';
  </script>
  
  <style scoped>
  .sidebar-container {
    display: flex;
    flex-direction: column;
    gap: 2rem; /* 仅保留间距，不添加背景或边框 */
  }
  </style>