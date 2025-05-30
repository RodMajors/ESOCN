```vue
<template>
    <div class="food-list">
        <!-- 搜索框 -->
        <div class="search-filter">
            <div class="search-container">
                <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="请输入食物中/英文名或特殊类型"
                    class="search-input"
                />
                <button
                    v-if="searchQuery"
                    @click="clearSearch"
                    class="clear-search-btn"
                >
                    ×
                </button>
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
                            <div class="filter-group">
                                <span
                                    v-for="type in ['肉类餐食', '水果餐食', '蔬菜餐食']"
                                    :key="type"
                                    v-tooltip="getTooltip(type)"
                                    @click="toggleTypeFilter(type)"
                                    :class="{ active: activeTypeFilters.includes(type) }"
                                    style="color: #6BC34B;"
                                >
                                    {{ type }}
                                </span>
                                <span
                                    v-for="type in ['小吃餐食', '蔬菜炖肉餐食', '甜点餐食']"
                                    :key="type"
                                    v-tooltip="getTooltip(type)"
                                    @click="toggleTypeFilter(type)"
                                    :class="{ active: activeTypeFilters.includes(type) }"
                                    style="color: #6797EC;"
                                >
                                    {{ type }}
                                </span>
                            </div>
                            <div class="filter-group">
                                <span
                                    v-for="type in ['酒精饮料', '茶饮料', '补品饮料']"
                                    :key="type"
                                    v-tooltip="getTooltip(type)"
                                    @click="toggleTypeFilter(type)"
                                    :class="{ active: activeTypeFilters.includes(type) }"
                                    style="color: #6BC34B;"
                                >
                                    {{ type }}
                                </span>
                                <span
                                    v-for="type in ['利口酒饮料', '酊剂饮料', '甜果汁茶饮料']"
                                    :key="type"
                                    v-tooltip="getTooltip(type)"
                                    @click="toggleTypeFilter(type)"
                                    :class="{ active: activeTypeFilters.includes(type) }"
                                    style="color: #6797EC;"
                                >
                                    {{ type }}
                                </span>
                            </div>
                            <div class="filter-group">
                                <span
                                    v-for="type in ['精致餐食', '蒸馏物饮料']"
                                    :key="type"
                                    v-tooltip="getTooltip(type)"
                                    @click="toggleTypeFilter(type)"
                                    :class="{ active: activeTypeFilters.includes(type) }"
                                    style="color: #9B4AE5;"
                                >
                                    {{ type }}
                                </span>
                                <span
                                    v-for="type in ['饮品', '独特餐食']"
                                    :key="type"
                                    v-tooltip="getTooltip(type)"
                                    @click="toggleTypeFilter(type)"
                                    :class="{ active: activeTypeFilters.includes(type) }"
                                    style="color: #DCC55F;"
                                >
                                    {{ type }}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="filter-column">
                        <h4>品质</h4>
                        <div class="filter-options" style="flex-direction: row;">
                            <span
                                v-for="quality in qualityOptions"
                                :key="quality"
                                @click="toggleQualityFilter(quality)"
                                :class="{
                                    active: activeQualityFilters.includes(
                                        quality
                                    ),
                                }"
                                :style="{ color: getQualityColor(quality) }"
                                
                            >
                                {{ quality }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <!-- 加载状态 -->
        <div v-if="isLoading" class="loading">“正在加载烹饪食谱数据... 请稍候”</div>

        <!-- 食物列表 -->
        <transition name="slide-down">
            <table
                v-if="paginatedFoods.length > 0 && !isLoading"
                :style="{ marginTop: showFilter ? '1rem' : '0' }"
            >
                <tbody>
                    <tr
                        v-for="(food, index) in paginatedFoods"
                        :key="food.id"
                        :class="index % 2 === 0 ? 'row-dark' : 'row-light'"
                    >
                        <td class="icon-column" @click="goToDetail(food.enName)">
                            <img
                                :src="food.icon"
                                class="food-icon"
                                alt="食物图标"
                            />
                        </td>
                        <td class="name-column" @click="goToDetail(food.enName)">
                            <div 
                                class="name-link" 
                                :style="{ 
                                    color: getQualityColor(food.quality), 
                                    '--underline-color': getQualityColor(food.quality) 
                                }"
                            >
                                <span>{{ food.name }}</span>
                                <br />
                                <span class="en-name">&lt;{{ food.enName }}&gt;</span>
                            </div>
                        </td>
                        <td class="type-link">
                            {{ food.specializedItemTypeText }}
                        </td>
                        <td class="ingredients-column">
                            <ul >
                                <li
                                    v-for="(
                                        quantity, ingredient
                                    ) in food.ingredients"
                                    :key="ingredient"
                                >
                                    {{ ingredient }}: {{ quantity }}
                                </li>
                            </ul>
                        </td>
                        <td class = "description-column">
                            <span
                                id="description"
                                v-html="parseDescription(food.description)"
                                @click="handleClick"
                            ></span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </transition>

        <!-- 无数据提示 -->
        <div v-if="filteredFoods.length === 0 && !isLoading" class="no-data">
            没有找到符合条件的食物
        </div>

        <!-- 分页 -->
        <div class="pagination" v-if="totalPages > 1">
            <button
                :disabled="currentPage === 1"
                @click="changePage(currentPage - 1)"
                class="page-btn"
            >
                上一页
            </button>
            <span
                v-for="page in visiblePages"
                :key="page"
                @click="changePage(page)"
                :class="{ active: currentPage === page }"
                class="page-number"
            >
                {{ page }}
            </span>
            <span v-if="currentPage + 2 < totalPages" class="ellipsis"
                >...</span
            >
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
            <button
                :disabled="currentPage === totalPages"
                @click="changePage(currentPage + 1)"
                class="page-btn"
            >
                下一页
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { parseColorTags } from "@/utils/parseColorTags";
import type { food } from "@/types/food.ts";

const foods = ref<food[]>([]);
const router = useRouter();
const route = useRoute();
const currentPage = ref(1);
const itemsPerPage = 20;
const totalPages = ref(0);
const isLoading = ref(true);
const searchQuery = ref("");
const showFilter = ref(false);
const activeTypeFilters = ref<string[]>([]);
const activeQualityFilters = ref<string[]>([]);

const typeOptions = [
    "肉类餐食", 
    "水果餐食", 
    "蔬菜餐食",
    "小吃餐食",
    "蔬菜炖肉餐食",
    "甜点餐食",
    "精致餐食",
    "酒精饮料",
    "茶饮料",
    "补品饮料",
    "利口酒饮料",
    "酊剂饮料",
    "甜果汁茶饮料",
    "蒸馏物饮料",
    "饮品",
    "独特餐食"
];
const qualityOptions = ["普通", "优良", "上乘", "史诗", "传说"];
type Quality = '传说' | '优良' | '普通' | '上乘' | '史诗';
// 品质颜色映射
const qualityColors: Record<Quality, string> = {
    传说: '#DCC55F',
    优良: '#6BC34B',
    普通: '#6BC34B',
    上乘: '#6797EC',
    史诗: '#9B4AE5'
};

// 类型描述映射
const typeTooltips: Record<string, string> = {
    "肉类餐食": "生命上限",
    "水果餐食": "魔力上限",
    "蔬菜餐食": "耐力上限",
    "小吃餐食": "生命上限+魔力上限",
    "蔬菜炖肉餐食": "生命上限+耐力上限",
    "甜点餐食": "魔力上限+耐力上限",
    "精致餐食": "生命+魔力+耐力上限",
    "酒精饮料": "生命回复",
    "茶饮料": "魔力回复",
    "补品饮料": "耐力回复",
    "利口酒饮料": "生命回复+魔力回复",
    "酊剂饮料": "生命回复+耐力回复",
    "甜果汁茶饮料": "魔力回复+耐力回复",
    "蒸馏物饮料": "生命+魔力+耐力回复",
    "饮品": "杂项",
    "独特餐食": "杂项"
};

// 获取 tooltip 内容并通过 parseColorTags 渲染
const getTooltip = (type: string) => {
    const tooltip = typeTooltips[type] || '';
    return parseColorTags(tooltip);
};

// 加载所有食物数据
const fetchAllFoods = async () => {
    isLoading.value = true;
    try {
        const response = await fetch("http://localhost:3000/api/foods");
        const data = await response.json();
        foods.value = data;
        totalPages.value = Math.ceil(data.length / itemsPerPage);
    } catch (error) {
        console.error("加载食物数据失败:", error);
    } finally {
        isLoading.value = false;
    }
};

// 处理描述文本
const parseDescription = (description: string) => {
    return parseColorTags(description);
};

// 处理点击事件（用于buff跳转）
const handleClick = (event: Event) => {
    const target = event.target as HTMLElement;
    if (target.classList.contains("link")) {
        const to = target.dataset.to;
        if (to) {
            router.push(to);
        }
    }
};

// 筛选逻辑
const filteredFoods = computed(() => {
    let filtered = foods.value;

    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        filtered = filtered.filter(
            (food) =>
                food.name.toLowerCase().includes(query) ||
                food.enName.toLowerCase().includes(query) ||
                food.specializedItemTypeText.toLowerCase().includes(query)
        );
    }

    if (activeTypeFilters.value.length > 0) {
        filtered = filtered.filter((food) =>
            activeTypeFilters.value.includes(food.specializedItemTypeText)
        );
    }

    if (activeQualityFilters.value.length > 0) {
        filtered = filtered.filter((food) =>
            activeQualityFilters.value.includes(food.quality)
        );
    }

    return filtered;
});

// 获取当前页的食物数据
const paginatedFoods = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return filteredFoods.value.slice(start, end);
});

onMounted(() => {
    fetchAllFoods();
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
        activeQualityFilters: activeQualityFilters.value,
    };
    localStorage.setItem("foodListState", JSON.stringify(state));
};

// 恢复页面状态
const restorePageState = () => {
    const savedState = localStorage.getItem("foodListState");
    if (savedState) {
        const state = JSON.parse(savedState);
        currentPage.value = state.currentPage || 1;
        searchQuery.value = state.searchQuery || "";
        activeTypeFilters.value = state.activeTypeFilters || [];
        activeQualityFilters.value = state.activeQualityFilters || [];
        window.scrollTo(0, state.scrollPosition || 0);
    }
};

// 应用路由参数
const applyRouteFilters = () => {
    const { search, type, quality } = route.query;
    if (search) searchQuery.value = String(search);
    if (type) {
        const typeText = String(type);
        if (!activeTypeFilters.value.includes(typeText)) {
            activeTypeFilters.value = [typeText];
            showFilter.value = true;
        }
    }
    if (quality) {
        const qualityText = String(quality);
        if (!activeQualityFilters.value.includes(qualityText)) {
            activeQualityFilters.value = [qualityText];
            showFilter.value = true;
        }
    }
};

// 监听路由变化
watch(
    () => route.path,
    (newPath) => {
        if (newPath === "/foods") {
            restorePageState();
            applyRouteFilters();
        }
    }
);

// 监听筛选条件变化
watch(
    [activeTypeFilters, activeQualityFilters, searchQuery],
    () => {
        currentPage.value = 1;
        savePageState();
    },
    { deep: true }
);

const goToDetail = (enName: string) => {
  savePageState();
  const formattedName = enName.replace(/\s+/g, '_');
  router.push(`/foods/${formattedName}`);
};

// 分页相关
const visiblePages = computed(() => {
    const pages = [];
    const start = Math.max(1, currentPage.value - 2);
    const end = Math.min(totalPages.value, currentPage.value + 2);
    for (let i = start; i <= end; i++) {
        pages.push(i);
    }
    return pages;
});

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
    searchQuery.value = "";
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

const toggleQualityFilter = (quality: string) => {
    const index = activeQualityFilters.value.indexOf(quality);
    if (index === -1) {
        activeQualityFilters.value.push(quality);
    } else {
        activeQualityFilters.value.splice(index, 1);
    }
};

const getQualityColor = (quality: string) => {
    return qualityColors[quality as Quality] || '#C5C29E';
};

const inputPage = ref("");
</script>

<style scoped>
.food-list {
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
    color: #eeeeee;
    border: none;
    cursor: pointer;
}

.filter-btn {
    margin-left: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: #262626;
    color: #C5C29E;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.filter-area {
    margin-bottom: 1rem;
    padding: 1rem;
    background-color: #101010;
    border: 1px solid #444;
    border-radius: 4px;
}

.filter-row {
    display: flex;
    gap: 2rem;
}

.filter-column {
    flex: auto;
}

.filter-column h4 {
    margin: 0rem 1rem 1rem 1rem;
}

.filter-options {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.filter-options-quality {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
}

.filter-options-quality span {
    padding: 0.5rem;
    background-color: #1A1A1A;
    border-radius: 4px;
    cursor: pointer;
}

.filter-group {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.filter-options span {
    padding: 0.5rem;
    background-color: #1A1A1A;
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
    width: 10%;
    padding: 0 0.5rem 0 1rem;
    cursor: pointer;
}

.name-column {
    width: 22%;
    text-align: center;
    padding: 0 0.5rem;
    cursor: pointer;
}

.type-link {
    width: 10%;
    text-align: center;
}

.quality-link {
    width: 10%;
    text-align: center;
}

.ingredients-column {
    width: 20%;
    text-align: left;
}

.description-column {
    width: 38%;
    text-align: left;
}

.row-dark {
    background-color: #101010;
}

.row-light {
    background-color: #1a1a1a;
}

.name-link {
    text-decoration: none;
}
.name-link:hover {
    text-decoration-line: underline;
    text-decoration-color: var(--underline-color);
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
    color: #c5c29e;
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
    background-color: #262626;
    color: #c5c29e;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.page-btn:hover:not(:disabled) {
    background-color: #555555;
}

.page-btn:disabled {
    background-color: #262626;
    cursor: not-allowed;
}

.page-number {
    padding: 0.5rem 1rem;
    background-color: #262626;
    color: #c5c29e;
    border-radius: 4px;
    cursor: pointer;
}

.page-number.active {
    background-color: #555555;
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

table {
    transition: margin-top 0.3s ease;
}

.page-input {
    padding: 0.5rem;
    width: 60px;
    border: 1px solid #444;
    border-radius: 4px;
    background-color: #262626;
    color: #c5c29e;
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
    color: #c5c29e;
}

#description {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.2;
  list-style-type: none;
}

#ingredients {
    margin: 0;
    padding-left: 1.5rem;
    font-size: 0.85rem;
    line-height: 1.2;
    list-style-type: none;
}

#ingredients li {
    margin-bottom: 0.2rem;
}

.en-name {
    font-size: 0.8rem;
}

.food-icon {
    width: 60px;
    height: 60px;
}
</style>
```