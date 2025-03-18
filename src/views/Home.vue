<template>
    <div class="home">
      <h1>ESOCN</h1>
      <p>这里是主页，探索副本攻略、每日新闻和装备列表吧！</p>
    </div>
  </template>
  
  <script setup lang="ts">
  // 暂时无需逻辑
  </script>
  
  <style scoped>
  .home {
    padding: 2rem;
    text-align: center;
  }
  
  h1 {
    color: #f1c33c;
    font-size: 60px;
    text-transform: uppercase;
    -webkit-text-fill-color: rgba(0, 0, 0, 0);
    background-image: -webkit-linear-gradient(top, rgba(241, 195, 60, 0.533), rgba(195, 134, 0, 0.933)), url(https://esossl-a.akamaihd.net/uploads/textures/gold.jpg);
    background-clip: text, text
  }
  </style>