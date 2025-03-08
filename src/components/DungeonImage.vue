<!-- src/components/DungeonImage.vue -->
<template>
    <div class="image-container" @click="goToDetail">
      <img :src="background" class="dungeon-icon" alt="Dungeon Background" />
      <div class="overlay">
        <div class="name-text">
          <span>{{ name }}</span>
          <br />
          <span class="en-name">{{ enName.toUpperCase() }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default defineComponent({
    name: 'DungeonImage',
    props: {
      name: {
        type: String,
        required: true,
      },
      enName: {
        type: String,
        required: true,
      },
      background: {
        type: String,
        required: true,
      },
    },
    setup(props) {
      const router = useRouter();
  
      const goToDetail = () => {
        const formattedName = props.enName.toLowerCase().replace(/\s+/g, '-');
        router.push(`/dungeon/${formattedName}`);
      };
  
      return {
        goToDetail,
      };
    },
  });
  </script>
  
  <style scoped>
  .image-container {
    position: relative;
    width: 100%;
    overflow: hidden; /* 防止放大时溢出 */
  }
  
  .dungeon-icon {
    width: 100%;
    max-height: 150px;
    object-fit: cover;
    display: block;
    transition: transform 0.6s ease; /* 图片缩放动画 */
  }
  
  .image-container:hover .dungeon-icon {
    transform: scale(1.3); /* 鼠标悬停时放大1.2倍 */
  }
  
  .overlay {
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 80%;
    display: flex;
    align-items: center;
    justify-content: center;
    transform: translateY(-50%);
    transition: background-color 0.5s ease; /* 不透明度动画 */
  }

  .name-text {
    text-align: center;
    font-weight: 600;
    color: #ffffff;
    font-size: 1.6rem;
    text-shadow: rgb(0, 0, 0) -1px 1px 4px, rgb(0, 0, 0) -2px 2px 4px, rgb(0, 0, 0) -3px 3px 4px;
    transition: transform 0.5s ease;
  }
  
  .image-container:hover .name-text {
    transform: scale(0.9); /* 文字放大1.1倍 */
  }
  
  .en-name {
    font-size: 1rem;
    --font-sans: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  }
  </style>