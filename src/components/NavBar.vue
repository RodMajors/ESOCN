<template>
  <nav class="navbar">
    <RouterLink to="/" class="logo">ESOCN</RouterLink>
    <ul class="nav-links">
      <li><RouterLink to="/dungeons">副本攻略</RouterLink></li>
      <li><RouterLink to="/news">每日新闻</RouterLink></li>
      <li><RouterLink to="/equipment">装备列表</RouterLink></li>
      <li><RouterLink to="/skills">技能图鉴</RouterLink></li>
      <li><RouterLink to="/buffs">buff效果</RouterLink></li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.navbar {
  background-color: #121113;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #948159;
}

.logo {
  font-size: 2rem;
  font-weight: bold;
  color: #BCA875;
  text-decoration: none; /* 移除下划线 */
  font-family:"Garamond", "Centaur", 'Trebuchet MS', sans-serif ;
}

.logo:hover {
  color: #ffffff; /* 悬停时变金色，与其他链接一致 */
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-links li a {
  color: #BCA875;
  text-decoration: none;
  font-size: 1.1rem;
  font-family: "Microsoft YaHei","黑体","宋体",sans-serif;
}

.nav-links li a:hover {
  color: #ffffff;
}
</style>