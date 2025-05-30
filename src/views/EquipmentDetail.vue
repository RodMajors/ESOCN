<template>
  <div class="equipment-detail">
    <!-- 第一个块：套装信息、图标和当前套装 -->
    <div class="detail-block" v-if="set">
      <div class="detail-container">
        <!-- 左侧信息 -->
        <div class="left-info">
          <h2>套装信息</h2>
          <div class="info-item" @click="goToDetail(set.enName)">
            <span class="label">套装名称：</span>
            <span class="value clickable">{{ set.name }}</span>
          </div>
          <div class="info-item" @click="goToDetail(set.enName)">
            <span class="label">英文名：</span>
            <span class="value clickable">{{ set.enName }}</span>
          </div>
          <div class="info-item" @click="filterByPlace(set.place)">
            <span class="label">套装出处：</span>
            <span class="value clickable">{{ set.place.split(',')[0] }}</span>
          </div>
          <div class="info-item" @click="filterByType(set.type)">
            <span class="label" >套装类型：</span>
            <span class="value clickable">{{ getTypeText(set.type) }}</span>
          </div>
          <div class="info-item">
            <span class="label">护甲类型：</span>
            <span class="value">{{ set.armor }}</span>
          </div>
          <div class="info-item">
            <span class="label">套装样式：</span>
            <span class="value">{{ set.style }}</span>
          </div>
        </div>

        <!-- 中间图标区域 -->
        <div class="icons-container">
          <img
            v-for="(icon, index) in set.styles"
            :key="index"
            :src="icon"
            class="style-icon"
            alt="Style Icon"
          />
        </div>

        <!-- 右侧当前套装 GearArea -->
        <div class="right-gear">
          <GearArea :set="set" />
        </div>
      </div>
    </div>

    <!-- 分割线区域 -->
    <div class="divider-container" v-if="set">
      <div class="divider"></div>
    </div>

    <!-- 第二个块：相关套装 -->
    <div class="related-block" v-if="set">
      <div class="related-container">
        <div class="related-header">
          <h2>相关套装</h2>
          <span class="view-all" @click="filterByPlace(set.place)">查看全部</span>
        </div>
        <div class="sets-list">
          <GearArea
            v-for="relatedSet in relatedSets"
            :key="relatedSet.enName"
            :set="relatedSet"
          />
        </div>
      </div>
    </div>

    <!-- 未找到套装 -->
    <div v-else>未找到套装</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { loadEquipment } from '../utils/loadEquipment';
import GearArea from '../components/GearArea.vue';
import { loadRelatedEquipment, getEquipmentByEnName } from '../utils/loadEquipment';
import type { EquipmentSet } from '@/types/equipment'


const route = useRoute();
const router = useRouter();
const set = ref<EquipmentSet | null>(null);
const equipmentData = ref<EquipmentSet[]>([]);

const typeMap: { [key: number]: string } = {
  1: '竞技场', 2: 'PVP', 3: '制造', 4: 'PVP', 5: 'PVP', 6: '副本', 7: 'PVP',
  8: '怪物', 9: '区域', 10: '新手', 11: '试炼', 12: '神器', 13: '怪物', 14: '怪物', 15: '职业',
};

const getTypeText = (type: number): string => {
  return typeMap[type] || '未知';
};

const styleIcons = computed(() => {
  if (!set.value?.styles) return [];
  const icons: string[] = [];

  const extractIcons = (obj: any) => {
    if (typeof obj !== 'object' || obj === null) return;
    if (obj.icon) {
      icons.push(obj.icon);
    }
    Object.values(obj).forEach(value => extractIcons(value));
  };

  extractIcons(set.value.styles);
  return icons;
});

const getIconPath = (icon: string): string => {
  const cleanPath = icon.replace(/^\/esoui\//, '').replace('.dds', '.webp');
  return cleanPath ? `../esoui/${cleanPath}` : 'https://  .placeholder.com/24';
};

const relatedSets = computed(() => {
  if (!set.value) return [];
  return equipmentData.value
    .filter(s => s.place === set.value!.place && s.enName !== set.value!.enName)
    .slice(0, 3);
});

const loadSet = async (enName: string) => {
  set.value = await getEquipmentByEnName(enName);
  if (!set.value) return;
  equipmentData.value = await loadRelatedEquipment(set.value.place.split(',')[0]);
};

// 初次加载
onMounted(async () => {
  const enName = (route.params.enName as string).replace(/_/g, ' ');
  await loadSet(enName);
});

// 监听路由变化
watch(() => route.params.enName, async (newEnName) => {
  if (newEnName) {
    const enName = (newEnName as string).replace(/_/g, ' ');
    await loadSet(enName);
  }
});

const goToDetail = (enName: string) => {
  const formattedName = enName.replace(/\s+/g, '_');
  router.push(`/equipment/${formattedName}`);
};

const filterByPlace = (place: string) => {
  router.push({ path: '/equipment', query: { place: place.split(',')[0] } });
};

const filterByType = (type: number) => {
  router.push({ path: '/equipment', query: { type: getTypeText(type) } });
};
</script>

<style scoped>
.equipment-detail {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* 第一个块：套装信息、图标和当前套装 */
.detail-block {
  background-color: #000000;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  padding: 1rem;
}

.detail-container {
  display: flex;
  justify-content: space-between;
  gap: 1rem; /* 减小间隙，从 2rem 到 1rem */
  width: 100%;
  align-items: flex-start;
}

.left-info {
  flex: 2; /* 增加宽度，从 flex: 1 到 flex: 2 */
  min-width: 0;
  padding-left: 1rem;
}

.left-info h2 {
  font-size: 1.5rem;
  color: #F6E43A;
  margin-bottom: 1rem;
}

.info-item {
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
}

.label {
  font-size: 1rem;
  color: #C5C29E;
  min-width: 80px;
}

.value {
  font-size: 1rem;
}

.clickable {
  color: #E2B502;
  cursor: pointer;
}

.clickable:hover {
  text-decoration: underline;
}

.icons-container {
  flex: 3; /* 调整比例，从 flex: 2 到 flex: 3 */
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: flex-start;
  padding-top: 1.7rem;
}

.style-icon {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.right-gear {
  flex: 0 0 auto; /* 固定宽度不变 */
  min-width: 0;
  display: flex;
  justify-content: flex-end;
}

/* 分割线区域 */
.divider-container {
  margin: 2rem 0;
}

.divider {
  width: 100%;
  height: 1px;
  background: linear-gradient(to right, transparent, #EEEEEE, transparent);
}

/* 第二个块：相关套装 */
.related-block {
  background-color: #000000;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  padding: 1rem;
}

.related-container {
  width: 100%;
}

.related-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.related-header h2 {
  font-size: 1.5rem;
  padding-left: 1rem;
  color: #F6E43A;
}

.sets-list {
  display: flex;
  width: 100%;
  justify-content: space-between;
}

.sets-list .gear-area {
  flex: 0 0 300px;
}

.view-all {
  font-size: 1rem;
  color: #C5C29E;
  cursor: pointer;
  padding-right: 1rem;
}

.view-all:hover {
  text-decoration: underline;
  color: #F6E43A;
}
</style>