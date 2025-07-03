<template>
    <div class="container" @click="handleOutsideClick">
        <!-- 左侧筛选区域 -->
        <div class="sidebar">
            <div v-if="loading">加载中...</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <div
                v-else
                v-for="classItem in classes"
                :key="classItem.id"
                class="class-item"
            >
                <div class="class-name" @click="toggleClass(classItem.id)">
                    {{ classItem.name }}
                </div>
                <transition name="slide">
                    <div
                        v-show="expandedClass === classItem.id"
                        class="skill-tree-list"
                    >
                        <div
                            v-for="tree in skillTrees.filter(
                                (t) => t.class_id === classItem.id
                            )"
                            :key="tree.id"
                            :class="[
                                'skill-tree-item',
                                { selected: selectedSkillTree === tree.id },
                            ]"
                            @click="selectSkillTree(tree.id)"
                        >
                            {{ tree.name }}
                        </div>
                    </div>
                </transition>
            </div>
        </div>

        <!-- 中间技能栏区域 -->
        <div class="main-content">
            <!-- 搜索框 -->
            <div class="search-container" @click.stop>
                <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="请输入技能/技能树/职业中英文名"
                    class="search-input"
                    @input="handleSearch"
                    @focus="showSearchResults = true"
                />
                <button
                    v-if="searchQuery"
                    @click="clearSearch"
                    class="clear-search-btn"
                >
                    ×
                </button>
            </div>
            <!-- 搜索结果浮动窗口 -->
            <transition name="slide-down">
                <div
                    v-if="
                        showSearchResults &&
                        searchQuery &&
                        searchResults.length > 0
                    "
                    class="search-results"
                >
                    <div
                        v-for="result in searchResults"
                        :key="result.type + '-' + result.item.id"
                        class="search-result-item"
                        @click.stop="navigateToResult(result)"
                    >
                        <img
                            v-lazy="result.item.icon"
                            alt="icon"
                            class="skill-icon"
                        />
                        <div>
                            <h3>
                                {{ result.item.name }} ({{
                                    result.item.enName ?? "N/A"
                                }})
                            </h3>
                            <p
                                class="result-desc"
                                v-html="parseColorTags(result.item.description)"
                            ></p>
                            <p class="result-path">
                                {{
                                    classes.find((c) => c.id === result.classId)
                                        ?.name ?? "未知职业"
                                }}
                                >
                                {{
                                    skillTrees.find(
                                        (t) => t.id === result.treeId
                                    )?.name ?? "未知技能树"
                                }}
                            </p>
                        </div>
                    </div>
                </div>
            </transition>

            <div v-if="loading">加载中...</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <div v-else-if="selectedSkillTree" class="skills-list">
                <!-- 终极技能 -->
                <div
                    class="skill-section"
                    v-if="
                        skills.filter(
                            (s) =>
                                s.skill_tree_id === selectedSkillTree &&
                                s.ultimate === 1
                        ).length > 0
                    "
                >
                    <h2>终极技能</h2>
                    <div
                        v-for="skill in skills.filter(
                            (s) =>
                                s.skill_tree_id === selectedSkillTree &&
                                s.ultimate === 1
                        )"
                        :key="skill.id"
                        class="skill-item"
                    >
                        <div
                            class="skill-header"
                            @click="toggleSkill(skill.id)"
                        >
                            <img
                                v-lazy="skill.icon"
                                alt="skill icon"
                                class="skill-icon"
                            />
                            <div>
                                <h3>
                                    {{ skill.name }} ({{
                                        skill.enName ?? "N/A"
                                    }})
                                </h3>
                                <p
                                    class="skill_des"
                                    v-html="parseColorTags(skill.description)"
                                ></p>
                            </div>
                        </div>
                        <transition name="slide">
                            <div
                                v-show="expandedSkills.includes(skill.id)"
                                class="variants-list"
                            >
                                <div
                                    v-for="variant in skillVariants.filter(
                                        (v) => v.skill_id === skill.id
                                    )"
                                    :key="variant.id"
                                    class="variant-item"
                                    @click="selectSkillOrVariant(variant)"
                                >
                                    <img
                                        v-lazy="variant.icon"
                                        alt="variant icon"
                                        class="skill-icon"
                                    />
                                    <div>
                                        <h3>
                                            {{ variant.name }} ({{
                                                variant.enName ?? "N/A"
                                            }})
                                        </h3>
                                        <p
                                            class="variant-desc"
                                            v-html="
                                                parseColorTags(
                                                    variant.description
                                                )
                                            "
                                            @click="handleClick"
                                        ></p>
                                    </div>
                                </div>
                            </div>
                        </transition>
                    </div>
                </div>

                <!-- 主动技能 -->
                <div
                    class="skill-section"
                    v-if="
                        skills.filter(
                            (s) =>
                                s.skill_tree_id === selectedSkillTree &&
                                s.passive === 0 &&
                                s.ultimate !== 1
                        ).length > 0
                    "
                >
                    <h2>主动技能</h2>
                    <div
                        v-for="skill in skills.filter(
                            (s) =>
                                s.skill_tree_id === selectedSkillTree &&
                                s.passive === 0 &&
                                s.ultimate !== 1
                        )"
                        :key="skill.id"
                        class="skill-item"
                    >
                        <div
                            class="skill-header"
                            @click="toggleSkill(skill.id)"
                        >
                            <img
                                v-lazy="skill.icon"
                                alt="skill icon"
                                class="skill-icon"
                            />
                            <div>
                                <h3>
                                    {{ skill.name }} ({{
                                        skill.enName ?? "N/A"
                                    }})
                                </h3>
                                <p
                                    class="skill_des"
                                    v-html="parseColorTags(skill.description)"
                                    @click="handleClick"
                                ></p>
                            </div>
                        </div>
                        <transition name="slide">
                            <div
                                v-show="expandedSkills.includes(skill.id)"
                                class="variants-list"
                            >
                                <div
                                    v-for="variant in skillVariants.filter(
                                        (v) => v.skill_id === skill.id
                                    )"
                                    :key="variant.id"
                                    class="variant-item"
                                    @click="selectSkillOrVariant(variant)"
                                >
                                    <img
                                        v-lazy="variant.icon"
                                        alt="variant icon"
                                        class="skill-icon"
                                    />
                                    <div>
                                        <h3>
                                            {{ variant.name }} ({{
                                                variant.enName ?? "N/A"
                                            }})
                                        </h3>
                                        <p
                                            class="variant-desc"
                                            v-html="
                                                parseColorTags(
                                                    variant.description
                                                )
                                            "
                                            @click="handleClick"
                                        ></p>
                                    </div>
                                </div>
                            </div>
                        </transition>
                    </div>
                </div>

                <!-- 被动技能 -->
                <div
                    class="skill-section"
                    v-if="
                        skills.filter(
                            (s) =>
                                s.skill_tree_id === selectedSkillTree &&
                                s.passive === 1
                        ).length > 0
                    "
                >
                    <h2>被动技能</h2>
                    <div
                        v-for="skill in skills.filter(
                            (s) =>
                                s.skill_tree_id === selectedSkillTree &&
                                s.passive === 1
                        )"
                        :key="skill.id"
                        class="skill-item"
                    >
                        <div
                            class="skill-header"
                            @click="toggleSkill(skill.id)"
                        >
                            <img
                                v-lazy="skill.icon"
                                alt="skill icon"
                                class="skill-icon"
                            />
                            <div>
                                <h3>
                                    {{ skill.name }} ({{
                                        skill.enName ?? "N/A"
                                    }})
                                </h3>
                                <p
                                    class="skill_des"
                                    v-html="parseColorTags(skill.description)"
                                ></p>
                            </div>
                        </div>
                        <transition name="slide">
                            <div
                                v-show="expandedSkills.includes(skill.id)"
                                class="variants-list"
                            >
                                <div
                                    v-for="variant in skillVariants.filter(
                                        (v) => v.skill_id === skill.id
                                    )"
                                    :key="variant.id"
                                    class="variant-item"
                                    @click="selectSkillOrVariant(variant)"
                                >
                                    <img
                                        v-lazy="variant.icon"
                                        alt="variant icon"
                                        class="skill-icon"
                                    />
                                    <div>
                                        <h3>
                                            {{ variant.name }} ({{
                                                variant.enName ?? "N/A"
                                            }})
                                        </h3>
                                        <p
                                            class="variant-desc"
                                            v-html="
                                                parseColorTags(
                                                    variant.description
                                                )
                                            "
                                        ></p>
                                    </div>
                                </div>
                            </div>
                        </transition>
                    </div>
                </div>
            </div>
            <p v-else class="placeholder">请选择一个技能树</p>
        </div>

        <!-- 右侧技能详情区域 -->
        <div class="details-panel">
            <div v-if="loading">加载中...</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <SkillArea v-else-if="selectedDetail" :skill="selectedDetail" />
            <p v-else class="placeholder">请选择一个技能或变体</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { parseColorTags } from "@/utils/parseColorTags";
import { useRouter, useRoute } from "vue-router";
import SkillArea from "@/components/SkillArea.vue";
import type {
    classes,
    skill_trees,
    skills,
    skill_variants,
} from "@/types/skills";

// 数据状态
const classes = ref<classes[]>([]);
const skillTrees = ref<skill_trees[]>([]);
const skills = ref<skills[]>([]);
const skillVariants = ref<skill_variants[]>([]);
const router = useRouter();
const route = useRoute();

// 交互状态
const expandedClass = ref<number | null>(null);
const selectedSkillTree = ref<number | null>(null);
const expandedSkills = ref<number[]>([]);
const selectedDetail = ref<skills | skill_variants | null>(null);

// 加载和错误状态
const loading = ref<boolean>(false);
const error = ref<string | null>(null);

// 搜索状态
const searchQuery = ref<string>("");
const showSearchResults = ref<boolean>(false);

// 搜索结果
interface SearchResult {
    type: "skill" | "variant";
    item: skills | skill_variants;
    classId: number;
    treeId: number;
}

const searchResults = computed(() => {
    if (!searchQuery.value) return [];
    const query = searchQuery.value.toLowerCase();
    const results: SearchResult[] = [];

    // 搜索技能
    skills.value.forEach((skill) => {
        const skillTree = skillTrees.value.find(
            (tree) => tree.id === skill.skill_tree_id
        );
        const classItem = skillTree
            ? classes.value.find((cls) => cls.id === skillTree.class_id)
            : null;
        if (
            skill.name.toLowerCase().includes(query) ||
            (skill.enName?.toLowerCase().includes(query) ?? false) ||
            (skillTree?.name.toLowerCase().includes(query) ?? false) ||
            (classItem?.name.toLowerCase().includes(query) ?? false)
        ) {
            results.push({
                type: "skill",
                item: skill,
                classId: skillTree?.class_id ?? 0,
                treeId: skill.skill_tree_id ?? 0,
            });
        }
    });

    // 搜索变体
    skillVariants.value.forEach((variant) => {
        const skill = skills.value.find((s) => s.id === variant.skill_id);
        const skillTree = skill
            ? skillTrees.value.find((tree) => tree.id === skill.skill_tree_id)
            : null;
        const classItem = skillTree
            ? classes.value.find((cls) => cls.id === skillTree.class_id)
            : null;
        if (
            variant.name.toLowerCase().includes(query) ||
            (variant.enName?.toLowerCase().includes(query) ?? false) ||
            (skillTree?.name.toLowerCase().includes(query) ?? false) ||
            (classItem?.name.toLowerCase().includes(query) ?? false)
        ) {
            results.push({
                type: "variant",
                item: variant,
                classId: skillTree?.class_id ?? 0,
                treeId: skill?.skill_tree_id ?? 0,
            });
        }
    });

    return results;
});

// 获取数据并初始化默认选中
const fetchData = async () => {
    loading.value = true;
    error.value = null;
    try {
        const response = await fetch("http://localhost:3000/api/skills");
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        classes.value = data.classes;
        skillTrees.value = data.skill_trees;
        skills.value = data.skills;
        skillVariants.value = data.skill_variants;

        // 处理路由参数
        const { classId, treeId, skillId, variantId } = route.query;
        if (classId && treeId) {
            expandedClass.value = Number(classId);
            selectedSkillTree.value = Number(treeId);
            if (skillId) {
                expandedSkills.value = [Number(skillId)];
                selectedDetail.value =
                    skills.value.find((s) => s.id === Number(skillId)) || null;
            } else if (variantId) {
                const variant = skillVariants.value.find(
                    (v) => v.id === Number(variantId)
                );
                if (variant) {
                    const skill = skills.value.find(
                        (s) => s.id === variant.skill_id
                    );
                    if (skill) {
                        expandedSkills.value = [skill.id];
                        selectedDetail.value = variant;
                    }
                }
            }
        } else if (classes.value.length > 0) {
            const firstClass = classes.value[0].id;
            expandedClass.value = firstClass;
            const firstTree = skillTrees.value.find(
                (t) => t.class_id === firstClass
            );
            if (firstTree) {
                selectedSkillTree.value = firstTree.id;
                const firstSkill = skills.value.find(
                    (s) => s.skill_tree_id === firstTree.id
                );
                if (firstSkill) {
                    expandedSkills.value.push(firstSkill.id);
                    selectedDetail.value = firstSkill;
                }
            }
        }
    } catch (err: unknown) {
        error.value = `获取数据失败: ${(err as Error).message}`;
        console.error("Fetch error:", err);
    } finally {
        loading.value = false;
    }
};

// 切换职业展开状态并默认选中第一个 skill_tree
const toggleClass = (classId: number) => {
    if (expandedClass.value === classId) {
        expandedClass.value = null;
        selectedSkillTree.value = null;
        expandedSkills.value = [];
        selectedDetail.value = null;
    } else {
        expandedClass.value = classId;
        const firstTree = skillTrees.value.find((t) => t.class_id === classId);
        if (firstTree) {
            selectedSkillTree.value = firstTree.id;
        }
    }
    updateRoute();
};

// 选择技能树
const selectSkillTree = (treeId: number) => {
    selectedSkillTree.value = treeId;
    expandedSkills.value = [];
    selectedDetail.value = null;
    updateRoute();
};

// 切换技能展开状态
const toggleSkill = (skillId: number) => {
    const index = expandedSkills.value.indexOf(skillId);
    if (index !== -1) {
        expandedSkills.value.splice(index, 1);
    } else {
        expandedSkills.value.push(skillId);
        selectedDetail.value =
            skills.value.find((s) => s.id === skillId) || null;
    }
    updateRoute();
};

// 选择技能或变体显示详情
const selectSkillOrVariant = (item: skills | skill_variants) => {
    selectedDetail.value = item;
    if ("skill_id" in item) {
        const skill = skills.value.find((s) => s.id === item.skill_id);
        if (skill && !expandedSkills.value.includes(skill.id)) {
            expandedSkills.value.push(skill.id);
        }
    }
    updateRoute();
};

// 清除搜索
const clearSearch = () => {
    searchQuery.value = "";
    showSearchResults.value = false;
};

// 处理搜索输入
const handleSearch = () => {
    showSearchResults.value = !!searchQuery.value;
};

// 处理点击外部区域
const handleOutsideClick = (event: MouseEvent) => {
    const target = event.target as HTMLElement;
    if (
        !target.closest(".search-container") &&
        !target.closest(".search-results")
    ) {
        showSearchResults.value = false;
    }
};

// 导航到搜索结果
const navigateToResult = (result: SearchResult) => {
    expandedClass.value = result.classId;
    selectedSkillTree.value = result.treeId;
    expandedSkills.value = [];
    selectedDetail.value = result.item;

    if (result.type === "variant") {
        const variant = result.item as skill_variants;
        const skill = skills.value.find((s) => s.id === variant.skill_id);
        if (skill && !expandedSkills.value.includes(skill.id)) {
            expandedSkills.value.push(skill.id);
        }
    } else {
        const skill = result.item as skills;
        if (!expandedSkills.value.includes(skill.id)) {
            expandedSkills.value.push(skill.id);
        }
    }

    searchQuery.value = "";
    showSearchResults.value = false;
    updateRoute();
};

// 更新路由
const updateRoute = () => {
    const query: { [key: string]: string } = {};
    if (expandedClass.value) query.classId = expandedClass.value.toString();
    if (selectedSkillTree.value)
        query.treeId = selectedSkillTree.value.toString();
    if (selectedDetail.value) {
        if ("skill_id" in selectedDetail.value) {
            query.variantId = selectedDetail.value.id.toString();
            const skillId = (selectedDetail.value as skill_variants)?.skill_id;
            if (skillId !== undefined && skillId !== null) {
                query.skillId = skillId.toString();
            }
        } else {
            query.skillId = selectedDetail.value.id.toString();
        }
    }
    router.push({ path: route.path, query });
};

// 初始化加载数据
onMounted(() => {
    fetchData();
});

const handleClick = (event: Event) => {
    const target = event.target as HTMLElement;
    console.log("点击目标:", target);
    if (target.classList.contains("link")) {
        const to = target.dataset.to;
        console.log("跳转目标:", to);
        if (to) {
            router.push(to);
        }
    }
};
</script>

<style>
.container {
    display: flex;
    width: 100%;
    background-color: #000000;
}

.sidebar {
    width: 10%;
    background-color: #000000;
    padding: 10px;
    border-right: solid rgb(98, 98, 98) 1px;
}

.class-name {
    color: #e5e2b9;
    padding: 4px;
    background-color: #000000;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px,
        rgb(80, 80, 80) 1px 1px 4px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 18px;
}

.class-name:hover {
    background-color: #1b1b1b;
}

.skill-tree-list {
    margin-left: 20px;
    margin-top: 5px;
}

.skill-tree-item {
    color: #e5e2b9;
    padding: 4px;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px,
        rgb(80, 80, 80) 1px 1px 4px;
    background-color: #000000;
    border-radius: 3px;
    cursor: pointer;
    font-size: 18px;
}

.skill-tree-item:hover,
.skill-tree-item.selected {
    background-color: #1b1b1b;
}

.main-content {
    width: 65%;
    padding: 10px;
    background-color: #000000;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.skills-list {
    width: 100%;
    position: relative;
    z-index: 1;
}

.skill-section {
    margin-bottom: 20px;
}

.skill-section h2 {
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 2px 4px,
        rgb(80, 80, 80) 1px 3px 4px;
    margin-bottom: 10px;
}

.skill-item {
    padding: 10px;
    margin-bottom: 5px;
    border-radius: 3px;
    cursor: pointer;
}

.skill-header {
    display: flex;
    align-items: center;
}

.skill-icon {
    border-radius: 5px;
    width: 52px;
    height: 52px;
    margin-right: 10px;
}

.skill-item h3 {
    font-size: 16px;
    font-weight: bold;
    margin: 0;
    color: #e5e2b9;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px,
        rgb(80, 80, 80) 1px 1px 4px;
}

.skill-item p {
    font-size: 0.85rem;
    margin: 0;
}

.variants-list {
    margin-top: 15px;
    margin-left: 40px;
}

.variant-item {
    display: flex;
    align-items: center;
    padding: 8px;
    background-color: #000000;
    border-radius: 3px;
    margin-bottom: 3px;
    cursor: pointer;
}

.variant-item h3 {
    font-size: 16px;
    font-weight: bold;
    margin: 0;
    color: #e5e2b9;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px,
        rgb(80, 80, 80) 1px 1px 4px;
}

.variant-desc {
    font-size: 0.8rem;
}

.details-panel {
    overflow: hidden;
    width: 25%;
    background-color: #000000;
    padding: 10px;
}

.placeholder {
    color: #888888;
    font-style: italic;
}

.error {
    color: #ff5555;
    font-weight: bold;
}

.search-container {
    position: relative;
    z-index: 1001;
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
    font-size: 1.3rem;
    position: absolute;
    right: -1rem;
    top: 50%;
    transform: translateY(-50%);
    background-color: transparent;
    color: #eeeeee;
    border: none;
    cursor: pointer;
}

.main-content .search-results {
    position: absolute;
    top: 2.5rem;
    width: calc(100% - 18px);
    left: 9px;
    overflow-y: scroll;
    max-height: 500px;
    background-color: #1a1a1a;
    border: 1px solid #444;
    border-radius: 4px;
    z-index: 1000;
    padding: 10px 0.5rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.main-content .search-results::-webkit-scrollbar {
    width: 4px;
}
.main-content .search-results:-webkit-scrollbar-thumb {
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.2);
}
.main-content .search-results::-webkit-scrollbar-track {
    border-radius: 0;
    background: rgba(0, 0, 0, 0.1);
}

.main-content .search-result-item {
    display: flex;
    align-items: center;
    padding: 8px;
    background-color: #1b1b1b;
    border-radius: 3px;
    margin-bottom: 5px;
    cursor: pointer;
}

.main-content .search-result-item:hover {
    background-color: #000000;
}

.main-content .search-result-item h3 {
    font-size: 16px;
    font-weight: bold;
    margin: 0;
    color: #e5e2b9;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px,
        rgb(80, 80, 80) 1px 1px 4px;
}

.main-content .result-desc {
    font-size: 0.8rem;
    margin: 5px 0;
}

.main-content .result-path {
    font-size: 0.75rem;
    color: #888888;
    margin: 0;
}

/* 动画样式 */
.slide-enter-active,
.slide-leave-active {
    transition: all 0.6s ease;
}

.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    max-height: 0;
}

.slide-enter-to,
.slide-leave-from {
    opacity: 1;
    max-height: 500px;
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
</style>
