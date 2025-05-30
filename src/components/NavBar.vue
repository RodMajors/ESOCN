<template>
  <nav class="navbar">
      <RouterLink to="/" class="logo">ESOCN</RouterLink>

      <ul class="nav-links">
          <li><RouterLink to="/dungeons">副本攻略</RouterLink></li>
          <li><RouterLink to="/trials">试炼攻略</RouterLink></li>
          <li><RouterLink to="/champions">勇士点数</RouterLink></li>
          <li><RouterLink to="/news">每日新闻</RouterLink></li>
          <li><RouterLink to="/equipment">装备列表</RouterLink></li>
          <li><RouterLink to="/skills">技能图鉴</RouterLink></li>
          <li><RouterLink to="/buffs">增益减益</RouterLink></li>
          <li><RouterLink to="/foods">烹饪食谱</RouterLink></li>
      </ul>
  </nav>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<style scoped>
.navbar {
  background-color: #121113;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height:1rem;
  border-bottom: 1px solid #948159;
  position: relative; /* 使 .navbar 成为下拉菜单的定位参考 */
}

.logo {
  font-size: 2rem;
  font-weight: bold;
  color: #bca875;
  text-decoration: none;
  font-family: "Garamond", "Centaur", "Trebuchet MS", sans-serif;
  transition: color 0.3s ease; /* 添加颜色过渡效果 */
}

.logo:hover {
  color: #ffffff;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-links li a {
  color: #bca875;
  text-decoration: none;
  font-size: 18px;
  font-family: "Einstein Futura PT Cond", impact, charcoal, sans-serif, "Microsoft YaHei", "黑体", "宋体", sans-serif;
  transition: color 0.3s ease; /* 添加颜色过渡效果 */
}

.nav-links li a:hover {
  color: #ffffff;
}

.dropdown:hover .dropdown-menu {
  display: block;
  opacity: 1;
  transform: translateY(0);
}

.dropdown-menu li {
  padding: 0.5rem 1rem;
}

.dropdown-menu li a {
  color: #bca875;
  text-decoration: none;
  font-size: 1rem;
  white-space: nowrap; /* 防止文字换行 */
  transition: color 0.3s ease; /* 添加颜色过渡效果 */
}

.dropdown-menu li a:hover {
  color: #ffffff;
}

.website-icon {
  width: 48px;
  height: 48px;
}
</style>