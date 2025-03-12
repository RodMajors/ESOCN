<!-- src/views/DungeonDetail.vue -->
<template>
  <div class="dungeon-detail">
    <header class="dungeon-header" :style="{ backgroundImage: `url(${dungeon?.background})` }">
      <div class="title-overlay">
        <h1>{{ dungeon?.name }}</h1>
        <p class="en-name">{{ dungeon?.enName.toUpperCase() }}</p>
      </div>
    </header>
    <main v-if="dungeon" class="dungeon-main">
      <!-- 顶部区域：图片和描述 -->
      <div class="top-section">
        <div class="content">
          <div class="dungeon-preview">
            <img v-if="dungeon.picture" :src="dungeon.picture" alt="Dungeon Picture" class="dungeon-picture" />
          </div>
          <p class="dungeon-description">{{ dungeon.des }}</p>
        </div>
        <div class="sidebar">
          <info-panel
            :dungeon="dungeon"
            icon="https://images.uesp.net/7/78/ON-mapicon-RaidDungeon.png"
            class-name="试炼"
          />
        </div>
      </div>

      <!-- 分割线 -->
      <div class="divider"></div>

      <!-- BOSS 区域 -->
      <section id="boss-section" class="boss-section">
        <div class="boss-tabs">
          <span v-for="(boss, index) in dungeon.BOSS" :key="index" @click="selectBoss(index)" :class="{ active: activeBoss === index }">
            {{ boss.name }}
          </span>
        </div>
        <transition name="fade">
          <div v-if="activeBoss !== null" class="boss-content">
            <div class="boss-info">
              <table class="boss-table">
                <tr v-if = "dungeon.BOSS[activeBoss].picture">
                  <td colspan="2">
                    <img :src="dungeon.BOSS[activeBoss].picture" alt="Boss Picture" class="boss-picture" />
                  </td>
                </tr>
                <tr>
                  <td colspan="2" class="boss-name">
                    {{ dungeon.BOSS[activeBoss].name }}<br>{{ dungeon.BOSS[activeBoss].enName }}
                  </td>
                </tr>
                <tr>
                  <td class="key-cell">种族</td>
                  <td class="value-cell">{{ dungeon.BOSS[activeBoss].species }}</td>
                </tr>
                <tr>
                  <td class="key-cell">地点</td>
                  <td class="value-cell">{{ dungeon.BOSS[activeBoss].place }}</td>
                </tr>
                <tr>
                  <td class="key-cell">生命值</td>
                  <td class="value-cell">
                    <div>普通：{{ dungeon.BOSS[activeBoss]['n-Health'] }}</div>
                    <div v-if="dungeon.BOSS[activeBoss]['v-Health']">精英：{{ dungeon.BOSS[activeBoss]['v-Health'] }}</div>
                    <div v-if="dungeon.BOSS[activeBoss].hmHealth">困难：{{ dungeon.BOSS[activeBoss].hmHealth }}</div>
                  </td>
                </tr>
                <tr>
                  <td colspan="2" class="boss-des">{{ dungeon.BOSS[activeBoss].des }}</td>
                </tr>
              </table>
            </div>
            <div class="boss-skills">
              <ul>
                <li v-for="(skill, index) in dungeon.BOSS[activeBoss].skills" :key="index" :class="index % 2 === 0 ? 'row-dark' : 'row-light'">
                  <img :src="skill.icon" alt="Skill Icon" class="skill-icon" />
                  <div class="skill-name">
                    {{ skill.name }}<br><span class="skill-en-name">&lt;{{ skill.enName }}&gt;</span>
                  </div>
                  <div class="skill-des">{{ skill.des }}</div>
                </li>
              </ul>
            </div>
          </div>
        </transition>
      </section>

      <!-- 分割线 -->
      <div class="divider"></div>

      <!-- 装备区域 -->
      <section id="equipment-section" class="equipment-section">
      <div class="equipment-list" ref="equipmentList">
        <gear-area
          v-for="set in equipmentSets"
          :key="set.enName"
          :set="set"
          :scale="scaleFactor"
        />
      </div>
    </section>

      <!-- 分割线 -->
      <div class="divider"></div>

      <!-- 成就区域 -->
      <section id="achievement-section" class="achievement-section">
        <ul>
          <li v-for="(achievement, index) in dungeon.achievement" :key="achievement.name" :class="index % 2 === 0 ? 'row-dark' : 'row-light'">
            <img :src="achievement.icon" alt="Achievement Icon" class="achievement-icon" />
            <div class="achievement-name">
              {{ achievement.name }}<br><span class="achievement-en-name">&lt;{{ achievement.enName }}&gt;</span>
            </div>
            <div class="achievement-score">{{ achievement.score }}</div>
            <div class="achievement-des">{{ achievement.des }}</div>
          </li>
        </ul>
      </section>
    </main>
    <div v-else class="not-found">
      <h2>未找到地下城</h2>
      <p>无法找到对应的地下城数据，请检查 URL 或数据文件。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch  } from 'vue';
import { useRoute } from 'vue-router';
import trialsData from '../data/trials.json';
import type { Dungeon } from '../types/trials';
import InfoPanel from '../components/InfoPanel.vue';
import GearArea from '../components/GearArea.vue';
import { getEquipmentByEnName } from '../utils/loadEquipment';
import type { EquipmentSet } from '../types/equipment';

const route = useRoute();
const dungeon = ref<Dungeon | null>(null);
const activeBoss = ref<number | null>(0);
const activeSection = ref<string>('boss-section');
const equipmentSets = ref<EquipmentSet[]>([]);
const equipmentList = ref<HTMLElement | null>(null); // 获取装备区域的 DOM 元素
const scaleFactor = ref(1); // 缩放比例

const sections = [
  { id: 'boss-section', label: 'BOSS' },
  { id: 'equipment-section', label: '装备' },
  { id: 'achievement-section', label: '成就' },
];

onMounted(async () => {
  const dungeons: Dungeon[] = trialsData;
  const routeEnName = route.params.enName as string;
  const formattedEnName = routeEnName.replace(/-/g, ' ');
  dungeon.value = dungeons.find(d => d.enName.toLowerCase() === formattedEnName.toLowerCase()) || null;
  
  if (dungeon.value && dungeon.value.BOSS.length > 0) {
    activeBoss.value = 0;
  }

  if (dungeon.value && dungeon.value.equipment) {
    const sets = await Promise.all(
      dungeon.value.equipment.map(async (item: string) => {
        const enNameFormatted = item.replace(/\s+/g, '_');
        const set = await getEquipmentByEnName(enNameFormatted);
        return set || { enName: item, name: item, place: '', icon: '', bonuses: {}, type: 0 } as EquipmentSet;
      })
    );
    equipmentSets.value = sets;
  }
});

const selectBoss = (index: number) => {
  activeBoss.value = index;
};

const scrollToSection = (sectionId: string) => {
  activeSection.value = sectionId;
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};

// 计算缩放比例
const calculateScaleFactor = () => {
  if (equipmentList.value && equipmentSets.value.length > 0) {
    const containerWidth = equipmentList.value.offsetWidth; // 容器宽度
    const itemCount = equipmentSets.value.length; // GearArea 的数量
    if(itemCount == 4) {
      const itemWidth = 336; // 每个 GearArea 的原始宽度（根据实际宽度调整）
      const totalWidth = itemWidth * itemCount; // 所有 GearArea 的总宽度 
      const gap = 16; // 每个 GearArea 之间的间距（根据实际 gap 值调整）

      // 计算缩放比例
      const availableWidth = containerWidth - (itemCount - 1) * gap; // 可用宽度
      scaleFactor.value = Math.min(1, (availableWidth / totalWidth)); // 缩放比例
    } else if (itemCount == 8) {
      const itemWidth = 336; // 每个 GearArea 的原始宽度（根据实际宽度调整）
      const totalWidth = itemWidth * itemCount; // 所有 GearArea 的总宽度 
      const gap = 16; // 每个 GearArea 之间的间距（根据实际 gap 值调整）

      // 计算缩放比例
      const availableWidth = containerWidth - (itemCount - 1) * gap; // 可用宽度
      scaleFactor.value = Math.min(1, (availableWidth / totalWidth)*2); // 缩放比例
    }
    
    console.log(scaleFactor)

  }
};

// 页面加载时计算缩放比例
onMounted(() => {
  calculateScaleFactor();
  window.addEventListener('resize', calculateScaleFactor); // 监听窗口大小变化
});

// 监听 equipmentSets 变化
watch(equipmentSets, () => {
  calculateScaleFactor();
});


</script>

<style scoped>
.dungeon-detail {
  padding: 0;
  width: 100%;
  margin-bottom: 0.5rem;
}

.dungeon-header {
  position: relative;
  height: 150px;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.title-overlay {
  text-align: center;
  color: #fff;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.8);
}

.title-overlay h1 {
  font-size: 2.2rem;
  text-shadow: rgb(0, 0, 0) -1px 1px 4px, rgb(0, 0, 0) -2px 2px 4px, rgb(0, 0, 0) -3px 3px 4px;
  margin: 0;
}

.en-name {
  font-size: 1.4rem;
  margin: 0.5rem 0 0;
  font-weight: 600;
  text-shadow: rgb(0, 0, 0) -1px 1px 4px, rgb(0, 0, 0) -2px 2px 4px, rgb(0, 0, 0) -3px 3px 4px;
}

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, #fff, transparent);
  margin: 1rem 0;
}

.dungeon-main {
  width: 100%;
}

.top-section {
  display: flex;
  justify-content: space-between;
  gap: 1rem; /* 减小与 sidebar 的间距 */
  padding: 0;
}

.content {
  flex: 1;
  padding: 1rem;
}

.sidebar {
  width: 350px;
  max-width: 350px;
  flex-shrink: 0;
  display: flex;
  justify-content: flex-end;
  padding: 0;
}

.dungeon-preview {
  display: flex;
  gap: 2rem; /* 增加图片与描述的间距 */
  justify-content: space-between; /* 使描述更靠近右侧 */
  margin-bottom: 2rem;
}

.dungeon-picture {
  max-height: 200px; /* 添加最大高度限制 */
  object-fit: contain; /* 保持宽高比，不拉伸 */
  display: block;
}

.dungeon-description {
  font-size: .9rem;
  letter-spacing: 1px;
  line-height: 1.5;
  white-space: pre-wrap;
  flex: 1;
}

.section-nav {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
}

.section-nav span {
  padding: 0.5rem 1rem;
  background-color: #262626;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

.section-nav span.active {
  background-color: #555555;
}

.boss-section {
  padding: 1rem;
}

.boss-tabs {
  letter-spacing:normal;
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.boss-tabs span {
  padding: 0.5rem 1rem;
  background-color: #262626;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

.boss-tabs span.active {
  background-color: #555555;
}

.boss-content {
  display: flex;
  gap: 1.2rem;
}

.boss-info {
  width: 350px;
}

.boss-table {
  width: 100%;
  border-collapse: collapse;
  background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
  border: 2px solid transparent;
  border-image: linear-gradient(to bottom right, #806f4d, #d4af37) 1;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.boss-table td {
  padding: 0.5rem;
}

.boss-picture {
  width: 100%;
  height: auto;
}

.boss-name {
  background-color: #000000;
  text-align: center;
  text-shadow: rgb(80, 80, 80) 1px 1px 3px, rgb(80, 80, 80) 1px 2px 3px, rgb(80, 80, 80) 1px 3px 3px;
  padding: 1rem;
}

.key-cell {
  background-color: #000000;
  width: 40%;
  text-align: center;
  border-right: 0.5px solid #444;
}

.value-cell {
  background-color: #101010;
  text-align: center;
}

.boss-des {
  background-color: #101010;
  text-align: center;
  font-size: 0.85rem;
  letter-spacing: 1px;
}

.boss-skills {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  flex: 1;
}

.boss-skills ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.boss-skills li {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  gap: 1rem;
}

.row-dark {
  background-color: #1a1a1a;
}

.row-light {
  background-color: #101010;
}

.skill-icon {
  width: 48px;
  height: 48px;
}

.skill-name {
  flex: 1;
}

.skill-en-name {
  font-size: 0.8rem;
}

.skill-des {
  flex: 2;
  font-size: .85rem;
}

.equipment-list {
  display: flex;
  flex-wrap: wrap; /* 允许内容换行 */
  width: 100%; /* 确保容器宽度占满父容器 */
}


.achievement-section {
  padding: 1rem;
}

.achievement-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.achievement-section li {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  gap: 1rem;
}

.achievement-icon {
  width: 48px;
  height: 48px;
}

.achievement-name {
  flex: 1;
  text-align: center;
}

.achievement-en-name {
  font-size: 0.8rem;
}

.achievement-score {
  width: 60px;
  text-align: center;
}

.achievement-des {
  flex: 2;
  font-size: 0.9rem;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.not-found {
  text-align: center;
  padding: 2rem;
  color: #888;
}

.not-found h2 {
  font-size: 1.5rem;
}
li {
  padding: 0.5rem;
  text-align: center;
  border-bottom: 0.5px solid #444;
  vertical-align: middle;
}

tr {
  border-bottom: 0.5px solid #444;
}

</style>