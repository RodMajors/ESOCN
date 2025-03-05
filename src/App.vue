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
  font-family: "宋体",Simsun;
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

.main-content {
  flex: 3.5;
  background-color: #101010;
  margin: 1rem;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
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