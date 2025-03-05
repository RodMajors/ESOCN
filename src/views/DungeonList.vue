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

    <!-- 副本列表 -->
    <transition name="slide-down">
      <table v-if="filteredDungeons.length > 0 && !isLoading">
        <tbody>
          <tr v-for="(dungeon, index) in paginatedDungeons" :key="dungeon.enName">
            <!-- 奇数行（index为偶数）：图片-神话 -->
            <template v-if="index % 2 === 0">
              <td @click="goToDetail(dungeon.enName)" class="icon-column">
                <div class="image-container">
                  <img :src="dungeon.background" class="dungeon-icon" alt="Dungeon Background" />
                  <div class="overlay">
                    <div class="name-text">
                      <span>{{ dungeon.name }}</span>
                      <br />
                      <span class="en-name">&lt;{{ dungeon.enName }}&gt;</span>
                    </div>
                  </div>
                </div>
              </td>
              <td class="mystery-column">{{ dungeon.mystery }}</td>
            </template>
            <!-- 偶数行（index为奇数）：神话-图片 -->
            <template v-else>
              <td class="mystery-column">{{ dungeon.mystery }}</td>
              <td @click="goToDetail(dungeon.enName)" class="icon-column">
                <div class="image-container">
                  <img :src="dungeon.background" class="dungeon-icon" alt="Dungeon Background" />
                  <div class="overlay">
                    <div class="name-text">
                      <span>{{ dungeon.name }}</span>
                      <br />
                      <span class="en-name">&lt;{{ dungeon.enName }}&gt;</span>
                    </div>
                  </div>
                </div>
              </td>
            </template>
          </tr>
        </tbody>
      </table>
    </transition>

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
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import dungeonsData from '../data/dungeons.json';

const dungeons = ref(dungeonsData);
const router = useRouter();
const currentPage = ref(1);
const itemsPerPage = 20;
const isLoading = ref(true);
const searchQuery = ref('');
const inputPage = ref('');

// 筛选副本
const filteredDungeons = computed(() => {
  let filtered = dungeons.value;
  if (searchQuery.value) {
    filtered = filtered.filter(dungeon =>
      dungeon.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      dungeon.enName.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }
  return filtered;
});

// 分页副本
const paginatedDungeons = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredDungeons.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(filteredDungeons.value.length / itemsPerPage);
});

const visiblePages = computed(() => {
  const pages = [];
  const start = Math.max(1, currentPage.value - 2);
  const end = Math.min(totalPages.value, currentPage.value + 2);
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

// 跳转到详情页
const goToDetail = (enName: string) => {
  const formattedName = enName.toLowerCase().replace(/\s+/g, '-');
  router.push(`/dungeon/${formattedName}`);
};

const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
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

onMounted(() => {
  isLoading.value = false;
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
  margin-bottom: 1rem;
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

table {
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
  text-align: left;
}

tr {
}

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
  transform: scale(1.2); /* 鼠标悬停时放大1.2倍 */
}

.overlay {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 50%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  transform: translateY(-50%);
  transition: background-color 0.6s ease; /* 不透明度动画 */
}

.image-container:hover .overlay {
  background-color: rgba(0, 0, 0, 0.9); /* 悬停时不透明度增加 */
}

.name-text {
  text-align: center;
}

.name-text:hover {
  text-decoration: underline;
}

.en-name {
  font-size: 0.85rem;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  margin-top: 2rem;
  color: #C5C29E;
}

.no-data {
  text-align: center;
  font-size: 1.2rem;
  margin-top: 2rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  gap: 0.5rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  background-color: #292929;
  color: #C5C29E;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  background-color: #555555;
}

.page-btn:disabled {
  background-color: #292929;
  cursor: not-allowed;
}

.page-number {
  padding: 0.5rem 1rem;
  background-color: #292929;
  color: #C5C29E;
  border-radius: 4px;
  cursor: pointer;
}

.page-number.active {
  background-color: #555555;
}

.page-input {
  padding: 0.5rem;
  width: 60px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #2c2c2c;
  color: #fff;
  text-align: center;
  appearance: textfield;
}

.page-input::-webkit-inner-spin-button,
.page-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.ellipsis {
  padding: 0.5rem;
  color: #C5C29E;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.name-text {
  transition: transform 0.6s ease;
}
.image-container:hover .name-text {
  transform: scale(1.1); /* 文字放大1.1倍 */
}
</style>