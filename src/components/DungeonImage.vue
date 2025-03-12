<!-- src/components/DungeonImage.vue -->
<template>
  <div class="image-container" :class="{ 'dual-container': isDual }" @click="goToDetail()">
    <img :src="background" class="dungeon-icon" alt="Dungeon Background" />
    
    <!-- 默认名称显示 -->
    <div class="overlay">
      <div class="name-text">
        <span>{{ name }}</span>
        <br />
        <span class="en-name">{{ enName.toUpperCase() }}</span>
      </div>
    </div>

    <!-- 双重地下城悬停时显示 -->
    <div v-if="isDual" class="dual-options">
      <div 
        v-for="dungeon in dualDungeons" 
        :key="dungeon.enName" 
        class="dual-option" 
        @click.stop="goToDetail(dungeon.originalEnName)"
      >
        <span>{{ dungeon.name }}</span>
        <br />
        <span class="en-name">{{ dungeon.enName.toUpperCase() }}</span>
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
    isDual: {
      type: Boolean,
      default: false,
    },
    dualDungeons: {
      type: Array as () => { name: string; enName: string; originalEnName: string }[],
      default: () => [],
    },
    type:{
      type: String,
      required: true,
    }
  },
  setup(props) {
    const router = useRouter();

    const goToDetail = (enName?: string) => {
      const targetEnName = enName || props.enName;
      console.log(props.enName)
      const formattedName = targetEnName.toLowerCase().replace(/\s+/g, '-');
      if (props.type == "dungeon")
        router.push(`/dungeons/${formattedName}`);
      else if (props.type == "trial")
        router.push(`/trials/${formattedName}`);
      else if (props.type == "arena")
        router.push(`/arena/${formattedName}`);
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
  overflow: hidden;
  cursor: pointer; /* 提示可点击 */
}

.dungeon-icon {
  width: 100%;
  max-height: 150px;
  object-fit: cover;
  display: block;
  transition: transform 0.6s ease;
}

.image-container:hover .dungeon-icon {
  transform: scale(1.3);
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
  transition: opacity 0.3s ease;
}

.name-text {
  text-align: center;
  font-weight: 600;
  color: #ffffff;
  font-size: 1.6rem;
  text-shadow: rgb(0, 0, 0) -1px 1px 4px, rgb(0, 0, 0) -2px 2px 4px, rgb(0, 0, 0) -3px 3px 4px;
  transition: opacity 0.3s ease;
}

.en-name {
  font-size: 1rem;
  --font-sans: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

/* 双重地下城样式 */
.dual-container:hover .overlay {
  opacity: 0; /* 悬停时隐藏默认名称 */
}

.dual-options {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transform: translateY(-50%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none; /* 默认不响应点击 */
}

.dual-container:hover .dual-options {
  opacity: 1;
  pointer-events: auto; /* 悬停时启用点击 */
}

.dual-option {
  flex: 1;
  text-align: center;
  font-weight: 600;
  color: #ffffff;
  font-size: 1.6rem;
  text-shadow: rgb(0, 0, 0) -1px 1px 4px, rgb(0, 0, 0) -2px 2px 4px, rgb(0, 0, 0) -3px 3px 4px;
  cursor: pointer;
  padding: 0 10px;
  transition: transform 0.3s ease;
}

.dual-option:hover {
  transform: scale(1.1); /* 悬停时放大 */
}

.dual-option .en-name {
  font-size: 0.9rem;
}
</style>