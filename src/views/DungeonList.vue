<!-- src/views/DungeonList.vue -->
<template>
  <div class="dungeon-list">
    <!-- 搜索框 -->
    <div class="search-filter">
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"   
          placeholder="请输入副本中/英文名"
          class="search-input"
        />
        <button v-if="searchQuery" @click="clearSearch" class="clear-search-btn">×</button>
      </div>
    </div>

    <!-- DLC 块 -->
    <div class="dlc-container">
      <div 
        v-for="[dlcName, dlcGroup] in filteredDlcGroups" 
        :key="dlcName" 
        class="dlc-block"
      >
        <div class="dlc-header" @click="toggleDlc(dlcName)">
          <div class="left-line" :style="{ right: `calc(50% + ${spacingMap[dlcName]}px)` }"></div>
          <div class="right-line" :style="{ left: `calc(50% + ${spacingMap[dlcName]}px)` }"></div>
          <div class="dlc-icon-wrapper">
            <img :src="dlcGroup.icon" class="dlc-icon" :alt="dlcName" />
          </div>
          <span class="dlc-name" ref="dlcNameRefs">{{ dlcName }}</span>
        </div>

        <!-- 地下城列表 -->
        <transition name="slide-down">
          <table v-if="expandedDlcs[dlcName]" class="dlc-dungeons">
            <tbody>
              <tr v-for="(dungeon, index) in dlcGroup.dungeons" :key="dungeon.enName">
                <template v-if="index % 2 === 0">
                  <td class="icon-column">
                    <DungeonImage
                      :name="dungeon.name"
                      :en-name="dungeon.enName"
                      :background="dungeon.background"
                      :is-dual="dungeon.isDual"
                      :dual-dungeons="dungeon.dualDungeons"
                    />
                  </td>
                  <td class="mystery-column">{{ dungeon.mystery }}</td>
                </template>
                <template v-else>
                  <td class="mystery-column">{{ dungeon.mystery }}</td>
                  <td class="icon-column">
                    <DungeonImage
                      :name="dungeon.name"
                      :en-name="dungeon.enName"
                      :background="dungeon.background"
                      :is-dual="dungeon.isDual"
                      :dual-dungeons="dungeon.dualDungeons"
                    />
                  </td>
                </template>
              </tr>
            </tbody>
          </table>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import dungeonsData from '../data/dungeons.json';
import DungeonImage from '../components/DungeonImage.vue';
import type { Dungeon, ProcessedDungeon, DlcGroup } from '../types/dungeon';

const router = useRouter();
const isLoading = ref(true);
const searchQuery = ref('');
const expandedDlcs = ref<{ [key: string]: boolean }>({}); // 控制每个 DLC 的展开状态
const dlcNameRefs = ref<HTMLElement[]>([]); // 存储 .dlc-name 的 DOM 引用
const spacingMap = ref<{ [key: string]: number }>({}); // 存储每个 DLC 的间距

// 处理重复地下城数据并按 DLC 分组
const dlcGroups = computed(() => {
  const dungeonMap = new Map<string, ProcessedDungeon>();
  const dlcMap = new Map<string, DlcGroup>();

  // 处理地下城数据
  (dungeonsData as Dungeon[]).forEach((dungeon: Dungeon) => {
    const nameMatch = dungeon.name.match(/^(.+?)\s+(I|II)$/);
    const enNameMatch = dungeon.enName.match(/^(.+?)\s+(I|II)$/);

    if (nameMatch && enNameMatch) {
      const baseName = nameMatch[1];
      const baseEnName = enNameMatch[1];
      const suffix = nameMatch[2];

      if (dungeonMap.has(baseEnName)) {
        const existing = dungeonMap.get(baseEnName)!;
        existing.dualDungeons.push({
          name: dungeon.name,
          enName: dungeon.enName,
          originalEnName: dungeon.enName,
        });
      } else {
        dungeonMap.set(baseEnName, {
          name: baseName,
          enName: baseEnName,
          background: dungeon.background,
          mystery: dungeon.mystery,
          isDual: true,
          dualDungeons: [{
            name: dungeon.name,
            enName: dungeon.enName,
            originalEnName: dungeon.enName,
          }],
          DLC: dungeon.DLC,
          DLCicon: dungeon.DLCicon,
          place: [],
          enplace: [],
          location: '',
          mini_level: '',
          Group_Size: '',
          Bosses: '',
          mini_Bosses: '',
          picture: '',
          des: '',
          BOSS: [],
          equipment: [],
          achievement: [],
          drop: [],
          mech: []
        });
      }
    } else {
      dungeonMap.set(dungeon.enName, {
        name: dungeon.name,
        enName: dungeon.enName,
        background: dungeon.background,
        mystery: dungeon.mystery,
        isDual: false,
        dualDungeons: [],
        DLC: dungeon.DLC,
        DLCicon: dungeon.DLCicon,
        place: [],
        enplace: [],
        location: '',
        mini_level: '',
        Group_Size: '',
        Bosses: '',
        mini_Bosses: '',
        picture: '',
        des: '',
        BOSS: [],
        equipment: [],
        achievement: [],
        drop: [],
        mech: []
      });
    }
  });

  // 按 DLC 分组
  dungeonMap.forEach((dungeon) => {
    const dlcName = dungeon.DLC;
    if (!dlcMap.has(dlcName)) {
      dlcMap.set(dlcName, {
        icon: dungeon.DLCicon,
        dungeons: [],
      });
    }
    dlcMap.get(dlcName)!.dungeons.push(dungeon);
  });

  return dlcMap;
});

// 筛选后的 DLC 分组并倒序
const filteredDlcGroups = computed(() => {
  const filteredMap = new Map<string, DlcGroup>();

  dlcGroups.value.forEach((group: DlcGroup, dlcName: string) => {
    let filteredDungeons = group.dungeons;
    if (searchQuery.value) {
      filteredDungeons = filteredDungeons.filter(dungeon =>
        dungeon.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        dungeon.enName.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    }
    if (filteredDungeons.length > 0) {
      filteredMap.set(dlcName, {
        icon: group.icon,
        dungeons: filteredDungeons,
      });
    }
  });

  // 将 Map 转换为数组并倒序返回，同时初始化展开状态
  const groups = [...filteredMap.entries()].reverse();
  groups.forEach(([dlcName]) => {
    if (!(dlcName in expandedDlcs.value)) {
      expandedDlcs.value[dlcName] = true; // 默认展开
    }
  });
  return groups;
});

// 切换 DLC 展开状态
const toggleDlc = (dlcName: string) => {
  expandedDlcs.value[dlcName] = !expandedDlcs.value[dlcName];
};

const clearSearch = () => {
  searchQuery.value = '';
};

// 计算每个 DLC 名称的间距
const updateSpacing = () => {
  if (dlcNameRefs.value.length > 0) {
    dlcNameRefs.value.forEach((el) => {
      const dlcName = el.textContent || '';
      const textLength = dlcName.length; // 根据字符数计算
      const baseSpacing = 40; // 基础间距
      const additionalSpacing = textLength * 5; // 每个字符增加 5px 间距（可调整）
      spacingMap.value[dlcName] = baseSpacing + additionalSpacing;
    });
  }
};

onMounted(() => {
  isLoading.value = false;
  updateSpacing(); // 初次加载时计算间距
});
</script>

<style scoped>
.dungeon-list {
  max-width: 1200px;
  margin: 0 auto;
}

.search-filter {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  gap: 2rem;
}

.search-container {
  position: relative;
  flex: 0.99;
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #292929;
  border-radius: 4px;
  background-color: #121113;
  color: #fff;
}

.clear-search-btn {
  font-size: 130%;
  position: absolute;
  right: -1rem;
  top: 50%;
  transform: translateY(-50%);
  background-color: transparent;
  color: #EEEEEE;
  border: none;
  cursor: pointer;
}

/* DLC 块样式 */
.dlc-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dlc-block {
  border-radius: 8px;
  overflow: hidden;
}

.dlc-header {
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  position: relative; /* 为线条定位提供参考 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.dlc-header:hover .dlc-icon {
  width: 60px; /* 鼠标悬停时放大图标 */
  height: 60px;
  transition: width 0.3s ease, height 0.3s ease;
}

.dlc-header:hover .dlc-name {
  font-size: 1.4rem; /* 鼠标悬停时放大字体 */
  transition: font-size 0.3s ease;
}

.dlc-icon-wrapper {
  display: inline-block;
}

.dlc-icon {
  width: 50px;
  height: 50px;
  object-fit: contain;
  transition: width 0.3s ease, height 0.3s ease; /* 平滑过渡 */
  position: relative;
  z-index: 1; /* 确保图标在线条之上 */
}

.left-line {
  position: absolute;
  top: 50%; /* 相对于 .dlc-header 的中间 */
  height: 2px;
  transform: translateY(-50%);
  left: 0;
  background: linear-gradient(to left, white, transparent);
}

.right-line {
  position: absolute;
  top: 50%; /* 相对于 .dlc-header 的中间 */
  height: 2px;
  transform: translateY(-50%);
  right: 0;
  background: linear-gradient(to right, white, transparent);
}

.dlc-name {
  display: block;
  margin-top: 0.5rem;
  color: #ffffff;
  font-size: 1.3rem;
  text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 2px 4px, rgb(80, 80, 80) 1px 3px 4px;
  font-weight: 600;
  transition: font-size 0.3s ease; /* 平滑过渡 */
}

/* 地下城列表样式 */
.dlc-dungeons {
  width: 100%;
  border-collapse: collapse;
  overflow: hidden;
}

td {
  padding: 0.5rem;
  text-align: center;
  vertical-align: middle;
}

.icon-column {
  cursor: pointer;
  width: 50%;
  padding: 0;
  position: relative;
}

.mystery-column {
  width: 50%;
  text-align: center;
  color: #e0e0e0; /* 浅灰色文字，与白色区分 */
  font-size: 1.1rem; /* 略大字体 */
  font-weight: 500; /* 中等粗细 */
  text-shadow: 0 0 4px rgba(255, 215, 0, 0.8), 0 0 8px rgba(255, 215, 0, 0.5); /* 金色发光效果 */
  border-radius: 4px; /* 圆角 */
  padding: 0.5rem 1rem; /* 增加内边距 */
  transition: transform 0.2s ease, text-shadow 0.2s ease; /* 悬停过渡 */
}

.mystery-column:hover {
  transform: scale(1.05); /* 轻微放大 */
  text-shadow: 0 0 6px rgba(255, 215, 0, 1), 0 0 12px rgba(255, 215, 0, 0.7); /* 增强发光 */
}

/* 过渡动画 */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>