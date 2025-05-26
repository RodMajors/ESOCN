<template>
    <div class="sidebar-container">
      <Pledges />
      <WeeklyTrials />
      <Vendors />
      <ServerStatus />
      <daily />
      <patch/>
    </div>
  </template>
  
  <script setup lang="ts">
  import Pledges from './Pledges.vue';
  import ServerStatus from './ServerStatus.vue';
  import WeeklyTrials from './WeeklyTrials.vue';
  import Vendors from './Vendors.vue'
  import Daily from './Daily.vue';
  import Patch from './Patch.vue';
  </script>
  
  <style scoped>
  .sidebar-container {
    display: flex;
    flex-direction: column;
    gap: 1rem; /* 仅保留间距，不添加背景或边框 */
  }
  </style>