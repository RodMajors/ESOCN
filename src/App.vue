<template>
  <div class="app-container">
    <NavBar />
    <div class="content-wrapper">
      <main class="main-content">
        <router-view />
      </main>
      <aside class="sidebar">
        <SideBar />
      </aside>
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import NavBar from './components/NavBar.vue';
import Footer from './components/Footer.vue';
import SideBar from './components/SideBar.vue';
</script>

<style> /* 无 scoped */
:root {
  --text-color: #C5C29E;
  font-family: "Microsoft YaHei","黑体","宋体",sans-serif;  
}

body {
  color: var(--text-color);
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-wrapper {
  display: flex;
  flex: 1;
}

/* App.vue 的 <style> 部分 */
.main-content {
  flex: 3.5;
  background-color: #000000;
  margin: 1rem;
  border-radius: 8px;
}

.sidebar {
  flex: 1;
  margin: 1rem 1rem 1rem 0;
  /* 移除以下样式以取消 sticky 效果 */
  /* position: sticky; */
  /* top: 20px; */
  /* align-self: flex-start; */
}
</style>