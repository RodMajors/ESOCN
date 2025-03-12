<template>
  <nav class="navbar">
      <RouterLink to="/" class="logo">ESOCN</RouterLink>

      <ul class="nav-links">
          <li class="dropdown">
              <span class="dropdown-toggle">
                  攻略
                  <span class="dropdown-arrow">▼</span>
              </span>
              <ul class="dropdown-menu">
                  <li><RouterLink to="/dungeons">副本攻略</RouterLink></li>
                  <li><RouterLink to="/trials">试炼攻略</RouterLink></li>
              </ul>
          </li>
          <li><RouterLink to="/news">每日新闻</RouterLink></li>
          <li><RouterLink to="/equipment">装备列表</RouterLink></li>
          <li><RouterLink to="/skills">技能图鉴</RouterLink></li>
          <li><RouterLink to="/buffs">增益减益</RouterLink></li>
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
  font-size: 1.1rem;
  font-family: "Microsoft YaHei", "黑体", "宋体", sans-serif;
  transition: color 0.3s ease; /* 添加颜色过渡效果 */
}

.nav-links li a:hover {
  color: #ffffff;
}

.dropdown {
  position: relative; /* 保持相对定位，但不再直接限制下拉菜单 */
}

.dropdown-toggle {
  color: #bca875;
  cursor: pointer;
  font-size: 1.1rem;
  font-family: "Microsoft YaHei", "黑体", "宋体", sans-serif;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  transition: color 0.5s ease; /* 添加颜色过渡效果 */
}

.dropdown-toggle:hover {
  color: #ffffff;
}

.dropdown-arrow {
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.dropdown:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.dropdown-menu {
  list-style: none;
  position: absolute;
  top: 100%; /* 从导航栏底部滑出 */
  left: 0; /* 对齐导航栏左侧 */
  background-color: #121113;
  padding: 0.1rem 0.1rem 0.1rem 0.1rem;
  margin: 0;
  display: none;
  opacity: 0;
  transform: translateY(-10px);
  transition: opacity 0.3s ease, transform 0.3s ease;
  z-index: 1000; /* 确保不被遮挡 */
  width: auto; /* 宽度自适应内容 */
  min-width: 150px; /* 设置最小宽度，避免太窄 */
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