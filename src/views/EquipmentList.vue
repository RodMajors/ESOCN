<template>
  <div class="equipment-list">
    <!-- 搜索框 -->
    <div class="search-filter">
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="请输入装备中/英文名或者出处地点名称"
          class="search-input"
        />
        <button v-if="searchQuery" @click="clearSearch" class="clear-search-btn">×</button>
      </div>
      <button @click="toggleFilter" class="filter-btn">筛选</button>
    </div>

    <!-- 筛选区域 -->
    <transition name="slide-down">
      <div v-if="showFilter" class="filter-area">
        <div class="filter-row">
          <div class="filter-column">
            <h4>类型</h4>
            <div class="filter-options">
              <span
                v-for="type in typeOptions"
                :key="type"
                @click="toggleTypeFilter(type)"
                :class="{ active: activeTypeFilters.includes(type) }"
              >
                {{ type }}
              </span>
            </div>
          </div>
          <!-- 部件过滤暂时禁用，因为 API 不返回 styles -->
          <!--
          <div class="filter-column">
            <h4>部件</h4>
            <div class="filter-options">
              <span
                v-for="part in partOptions"
                :key="part"
                @click="togglePartFilter(part)"
                :class="{ active: activePartFilters.includes(part) }"
              >
                {{ part }}
              </span>
            </div>
          </div>
          -->
        </div>
      </div>
    </transition>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading">“他妈的这数据量也太多了...<br>——@RodMajors“</div>

    <!-- 装备列表 -->
    <transition name="slide-down">
      <table v-if="paginatedEquipment.length > 0 && !isLoading" :style="{ marginTop: showFilter ? '1rem' : '0' }">
        <tbody>
          <tr
            v-for="(set, index) in paginatedEquipment"
            :key="set.enName"
            :class="index % 2 === 0 ? 'row-dark' : 'row-light'"
          > 
            <td @click="goToDetail(set.enName)" class="icon-column">
              <img :src="set.icon" class="set-icon" alt="Set Icon"/>
            </td>
            <td class="name-column">
              <div @click="goToDetail(set.enName)" class="name-link">
                <span>{{ set.name }}</span>
                <br />
                <span class="en-name">&lt;{{ set.enName }}&gt;</span>
              </div>
            </td>
            <td @click="filterByPlace(set.place)" class="place-link">
              <span>{{ set.place.split(',')[0] }}</span>
              <br />
              <span class="en-name">{{ set.enplace.split(',')[0] }}</span>
            </td>
            <td @click="filterByType(set.type)" class="type-link">{{ getTypeText(set.type) }}</td>
            <td>
              <ul id="bonuses">
                <li v-for="(effect, key) in set.bonuses" :key="key" v-html="effect" @click = "handleClick"></li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>
    </transition>

    <!-- 无数据提示 -->
    <div v-if="filteredEquipment.length === 0 && !isLoading" class="no-data">没有找到符合条件的装备</div>

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)" class="page-btn">上一页</button>
      <span
        v-for="page in visiblePages"
        :key="page"
        @click="changePage(page)"
        :class="{ active: currentPage === page }"
        class="page-number"
      >
        {{ page }}
      </span>
      <span v-if="currentPage + 2 < totalPages" class="ellipsis">...</span>
      <span
        v-if="currentPage + 2 < totalPages"
        @click="changePage(totalPages)"
        :class="{ active: currentPage === totalPages }"
        class="page-number"
      >
        {{ totalPages }}
      </span>
      <input
        type="number"
        v-model="inputPage"
        @keyup.enter="jumpToPage"
        class="page-input"
        placeholder="跳转"
      />
      <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)" class="page-btn">下一页</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { loadEquipment } from '../utils/loadEquipment';
import { parseColorTags } from '@/utils/parseColorTags';
import { loadAllEquipment } from '../utils/loadEquipment'
import { RouterLink } from 'vue-router';
import BuffLink from "@/components/BuffLink.vue";

const equipment = ref<any[]>([]);
const router = useRouter();
const route = useRoute();
const currentPage = ref(1);
const itemsPerPage = 20;
const totalPages = ref(0); // 暂时手动设置，后续需后端支持
const isLoading = ref(true);
const searchQuery = ref('');
const showFilter = ref(false);
const activeTypeFilters = ref<string[]>([]);
// const activePartFilters = ref<string[]>([]); // 暂时禁用部件过滤

const typeOptions = ['制造', '试炼', '副本', '竞技场', 'PVP', '怪物', '区域', '神器', '职业'];
const partOptions = ['重甲', '中甲', '轻甲']; // 保留但未使用

const inputPage = ref('');

// 加载所有装备数据
const fetchAllEquipment = async () => {
  isLoading.value = true;
  try {
    const data = await loadAllEquipment(); // 一次性加载所有数据
    equipment.value = data;
    totalPages.value = Math.ceil(data.length / itemsPerPage); // 计算总页数
    console.log("data.length", data.length)
  } catch (error) {
    console.error('加载装备数据失败:', error);
  } finally {
    isLoading.value = false;
  }
};

// 获取当前页的装备数据
const paginatedEquipment = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredEquipment.value.slice(start, end); // 只返回当前页的数据
});

const handleClick = (event: Event) =>{
  const target = event.target as HTMLElement;
    if (target.classList.contains("link")) {
      const to = target.dataset.to;
      if (to) {
        router.push(to); // 使用 Vue Router 跳转
      }
    }
};

// 筛选逻辑
const filteredEquipment = computed(() => {
  let filtered = equipment.value;

  if (searchQuery.value) {
    filtered = filtered.filter(set =>
      set.name.includes(searchQuery.value) ||
      set.enName.includes(searchQuery.value) ||
      set.place.includes(searchQuery.value)
    );
  }

  if (activeTypeFilters.value.length > 0) {
    filtered = filtered.filter(set =>
      activeTypeFilters.value.includes(getTypeText(set.type))
    );
  }

  return filtered;
});


onMounted(() => {
  fetchAllEquipment();
  restorePageState();
  applyRouteFilters();
});

// 保存页面状态
const savePageState = () => {
  const state = {
    currentPage: currentPage.value,
    scrollPosition: window.scrollY,
    searchQuery: searchQuery.value,
    activeTypeFilters: activeTypeFilters.value,
    // activePartFilters: activePartFilters.value, // 禁用
  };
  localStorage.setItem('equipmentListState', JSON.stringify(state));
};

// 恢复页面状态
const restorePageState = () => {
  const savedState = localStorage.getItem('equipmentListState');
  if (savedState) {
    const state = JSON.parse(savedState);
    currentPage.value = state.currentPage || 1;
    searchQuery.value = state.searchQuery || '';
    activeTypeFilters.value = state.activeTypeFilters || [];
    // activePartFilters.value = state.activePartFilters || [];
  }
};

const visiblePages = computed(() => {
  const pages = [];
  const start = Math.max(1, currentPage.value - 2);
  const end = Math.min(totalPages.value, currentPage.value + 2);
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

const getTypeText = (type: number): string => {
  const typeMap: { [key: number]: string } = {
    1: '竞技场', 2: 'PVP', 3: '制造', 4: 'PVP', 5: 'PVP', 6: '副本', 7: 'PVP',
    8: '怪物', 9: '区域', 10: '新手', 11: '试炼', 12: '神器', 13: '怪物', 14: '怪物', 15: '职业',
  };
  return typeMap[type] || '未知';
};

const applyRouteFilters = () => {
  const { search, type, place } = route.query;
  if (search) searchQuery.value = String(search);
  if (place) searchQuery.value = String(place);
  if (type) {
    const typeText = String(type);
    if (!activeTypeFilters.value.includes(typeText)) {
      activeTypeFilters.value = [typeText];
      showFilter.value = true;
    }
  }
};

watch(() => route.path, (newPath) => {
  if (newPath === '/equipment') {
    restorePageState();
    applyRouteFilters();
  }
});

watch(
  [activeTypeFilters, searchQuery],
  () => {
    currentPage.value = 1;
    savePageState();
  },
  { deep: true }
);

const goToDetail = (enName: string) => {
  savePageState();
  const formattedName = enName.replace(/\s+/g, '_');
  router.push(`/equipment/${formattedName}`);
};

const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    savePageState();
  }
};

const jumpToPage = () => {
  const page = parseInt(inputPage.value);
  if (page >= 1 && page <= totalPages.value) {
    changePage(page);
  }
};

const clearSearch = () => {
  searchQuery.value = '';
};

const toggleFilter = () => {
  showFilter.value = !showFilter.value;
};

const toggleTypeFilter = (type: string) => {
  const index = activeTypeFilters.value.indexOf(type);
  if (index === -1) {
    activeTypeFilters.value.push(type);
  } else {
    activeTypeFilters.value.splice(index, 1);
  }
};

// const togglePartFilter = (part: string) => { /* 禁用 */ };

const filterByType = (type: number) => {
  const typeText = getTypeText(type);
  toggleTypeFilter(typeText);
  showFilter.value = true;
};

const filterByPlace = (place: string) => {
  searchQuery.value = place.split(',')[0];
};
</script>

<style scoped>
.equipment-list {
  max-width: 1200px;
  margin: 0 auto;
}

.search-filter {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  gap: 2rem;
}

.search-container {
  position: relative;
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #444;
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

.filter-btn {
  margin-left: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #262626;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.filter-area {
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: #1A1A1A;
  border-radius: 4px;
}

.filter-row {
  display: flex;
  gap: 2rem; /* 类型和部件之间的间距 */
}

.filter-column {
  
  flex: auto; 

}

.filter-column h4 {
  margin-bottom: 0.5rem; /* 缩小标题与选项列表的距离 */
  margin: 1rem 1rem
}

.filter-section {
  display: flex;
  align-items: center;
  gap: 1rem; /* 类型和部件之间的间距 */
  
  margin-bottom: 0.5rem; /* 缩小与上方的距离 */
  
}

.filter-section h4 {
  margin: 0; /* 去掉 h4 的默认 margin */
  
}


.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-options span {
  padding: 0.5rem;
  background-color: #262626;
  border-radius: 4px;
  cursor: pointer;
}

.filter-options span.active {
  background-color: #555555;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #101010;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

td {
  padding: 0.5rem;
  text-align: center;
  border-bottom: 1px solid #444;
  vertical-align: middle;
}

.icon-column {
  cursor: pointer;
  width: 10%;
  padding: 0 0.5rem 0 1rem;
}

.name-column {
  width: 22%;
  text-align: center; /* 改为居中，原为left */
  padding: 0 0.5rem; /* 调整padding以保持居中对齐 */
}

td:nth-child(3) {
  width: 10%;
  text-align: center;
}

td:nth-child(4) {
  width: 8%;
  text-align: center;
}

td:nth-child(5) {
  width: 53%;
  text-align: left;
}

.row-dark {
  background-color: #101010;
}

.row-light {
  background-color: #1A1A1A;
}

/* 套装名称悬停效果 */
.name-link {
  cursor: pointer;
  text-decoration: none; /* 默认无下划线 */
}

.name-link:hover {
  text-decoration: underline; /* 鼠标悬停时显示下划线 */
}

/* 类型悬停效果 */
.type-link {
  cursor: pointer;
  text-decoration: none; /* 默认无下划线 */
}

.type-link:hover {
  text-decoration: underline; /* 鼠标悬停时显示下划线 */
}

/* 出处悬停效果 */
.place-link {
  cursor: pointer;
  text-decoration: none; /* 默认无下划线 */
}

.place-link:hover {
  text-decoration: underline; /* 鼠标悬停时显示下划线 */
}

.no-data {
  text-align: center;
  font-size: 1.2rem;
  margin-top: 2rem;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  margin-top: 2rem;
  color: #C5C29E;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  gap: 1rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  background-color: #262626;
  color: #C5C29E;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  background-color: #262626;
}

.page-btn:disabled {
  background-color: #262626;
  cursor: not-allowed;
}

.page-number {
  padding: 0.5rem 1rem;
  background-color: #262626;
  color: #C5C29E;
  border-radius: 4px;
  cursor: pointer;
}

.page-number.active {
  background-color: #555555;
}

.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from, .slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

table {
  transition: margin-top 0.3s ease;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  gap: 0.5rem;
}

.page-input {
  padding: 0.5rem;
  width: 60px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #262626;
  color: #C5C29E;
  text-align: center;
  appearance: textfield; /* 隐藏增减按钮 */
}

.page-input::-webkit-inner-spin-button,
.page-input::-webkit-outer-spin-button {
  -webkit-appearance: none; /* 隐藏 WebKit 浏览器的增减按钮 */
  margin: 0;
}

.ellipsis {
  padding: 0.5rem;
  color: #C5C29E;
}

#bonuses {
  margin: 0;
  padding-left: 1.5rem; /* 保持缩进 */
  font-size: 0.85rem; /* 缩小文字大小，原默认可能是1rem */
  line-height: 1.2; /* 缩小行高，原默认可能是1.5或更高 */
  list-style-type: none; /* 移除圆点标记 */
}

#bonuses li {
  margin-bottom: 0.2rem; /* 减小列表项间距 */
}

/* 修改英文名称样式 */
.en-name {
  font-size: 0.80rem; /* 缩小字体，原默认可能是1rem */
}

</style>