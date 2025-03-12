<template>
    <div class="container">
      <!-- 左侧筛选区域 -->
      <div class="sidebar">
        <div v-if="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else v-for="classItem in classes" :key="classItem.id" class="class-item">
          <div class="class-name" @click="toggleClass(classItem.id)">
            {{ classItem.name }}
          </div>
          <transition name="slide">
            <div v-show="expandedClass === classItem.id" class="skill-tree-list">
              <div
                v-for="tree in skillTrees.filter((t) => t.class_id === classItem.id)"
                :key="tree.id"
                :class="['skill-tree-item', { selected: selectedSkillTree === tree.id }]"
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
        <div v-if="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="selectedSkillTree" class="skills-list">
          <!-- 终极技能 -->
          <div class="skill-section" v-if="skills.filter((s) => s.skill_tree_id === selectedSkillTree && s.ultimate === 1).length > 0">
            <h2>终极技能</h2>
            <div
              v-for="skill in skills.filter((s) => s.skill_tree_id === selectedSkillTree && s.ultimate === 1)"
              :key="skill.id"
              class="skill-item"
            >
              <div class="skill-header" @click="toggleSkill(skill.id)">
                <img v-lazy="skill.icon" alt="skill icon" class="skill-icon" />
                <div>
                  <h3>{{ skill.name }} &lt;{{ skill.enName }}&gt;</h3>
                  <p class="skill_des" v-html="parseColorTags(skill.description)"></p>
                </div>
              </div>
              <transition name="slide">
                <div v-show="expandedSkills.includes(skill.id)" class="variants-list">
                  <div
                    v-for="variant in skillVariants.filter((v) => v.skill_id === skill.id)"
                    :key="variant.id"
                    class="variant-item"
                    @click="selectSkillOrVariant(variant)"
                  >
                    <img v-lazy="variant.icon" alt="skill icon" class="skill-icon" />
                    <div>
                      <h3>{{ variant.name }} &lt;{{ variant.enName }}&gt;</h3>
                      <p class="variant-desc" v-html="parseColorTags(variant.description)" @click="handleClick"></p>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <!-- 主动技能 -->
          <div class="skill-section" v-if="skills.filter((s) => s.skill_tree_id === selectedSkillTree && s.passive === '0' && s.ultimate !== 1).length > 0">
            <h2>主动技能</h2>
            <div
              v-for="skill in skills.filter((s) => s.skill_tree_id === selectedSkillTree && s.passive === '0' && s.ultimate !== 1)"
              :key="skill.id"
              class="skill-item"
            >
              <div class="skill-header" @click="toggleSkill(skill.id)">
                <img v-lazy="skill.icon" alt="skill icon" class="skill-icon" />
                <div>
                  <h3>{{ skill.name }} &lt;{{ skill.enName }}&gt;</h3>
                  <p class="skill_des" v-html="parseColorTags(skill.description)" @click="handleClick"></p>
                </div>
              </div>
              <transition name="slide">
                <div v-show="expandedSkills.includes(skill.id)" class="variants-list">
                  <div
                    v-for="variant in skillVariants.filter((v) => v.skill_id === skill.id)"
                    :key="variant.id"
                    class="variant-item"
                    @click="selectSkillOrVariant(variant)"
                  >
                    <img v-lazy="variant.icon" alt="skill icon" class="skill-icon" />
                    <div>
                      <h3>{{ variant.name }} &lt;{{ variant.enName }}&gt;</h3>
                      <p class="variant-desc" v-html="parseColorTags(variant.description)" @click="handleClick"></p>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <!-- 被动技能 -->
          <div class="skill-section" v-if="skills.filter((s) => s.skill_tree_id === selectedSkillTree && s.passive === '1').length > 0">
            <h2>被动技能</h2>
            <div
              v-for="skill in skills.filter((s) => s.skill_tree_id === selectedSkillTree && s.passive === '1')"
              :key="skill.id"
              class="skill-item"
            >
              <div class="skill-header" @click="toggleSkill(skill.id)">
                <img v-lazy="skill.icon" alt="skill icon" class="skill-icon" />
                <div>
                  <h3>{{ skill.name }} &lt;{{ skill.enName }}&gt;</h3>
                  <p class="skill_des" v-html="parseColorTags(skill.description)"></p>
                </div>
              </div>
              <transition name="slide">
                <div v-show="expandedSkills.includes(skill.id)" class="variants-list">
                  <div
                    v-for="variant in skillVariants.filter((v) => v.skill_id === skill.id)"
                    :key="variant.id"
                    class="variant-item"
                    @click="selectSkillOrVariant(variant)"
                  >
                    <img v-lazy="variant.icon" alt="skill icon" class="skill-icon" />
                    <div>
                      <h3>{{ variant.name }} &lt;{{ variant.enName }}&gt;</h3>
                      <p class="variant-desc" v-html="parseColorTags(variant.description)"></p>
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
import { ref, onMounted } from 'vue';
import { parseColorTags } from '@/utils/parseColorTags';
import { useRouter, useRoute } from 'vue-router';
import SkillArea from '@/components/SkillArea.vue';
import type { classes, skill_trees, skills, skill_variants } from '@/types/skills';


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

// 获取数据并初始化默认选中
const fetchData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch('http://localhost:4000/api/skills');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    classes.value = data.classes;
    skillTrees.value = data.skill_trees;
    skills.value = data.skills;
    skillVariants.value = data.skill_variants;

    // 初始化默认选中
    if (classes.value.length > 0) {
      const firstClass = classes.value[0].id;
      expandedClass.value = firstClass;

      const firstTree = skillTrees.value.find((t) => t.class_id === firstClass);
      if (firstTree) {
        selectedSkillTree.value = firstTree.id;

        const firstSkill = skills.value.find((s) => s.skill_tree_id === firstTree.id);
        if (firstSkill) {
          expandedSkills.value.push(firstSkill.id);
          selectedDetail.value = firstSkill;
        }
      }
    }
  } catch (err: unknown) {
    error.value = `获取数据失败: ${(err as Error).message}`;
    console.error('Fetch error:', err);
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
};

// 选择技能树
const selectSkillTree = (treeId: number) => {
  selectedSkillTree.value = treeId;
  expandedSkills.value = [];
  selectedDetail.value = null;
};

// 切换技能展开状态
const toggleSkill = (skillId: number) => {
  const index = expandedSkills.value.indexOf(skillId);
  if (index !== -1) {
    expandedSkills.value.splice(index, 1); // 收起
  } else {
    expandedSkills.value.push(skillId); // 展开
    selectedDetail.value = skills.value.find((s) => s.id === skillId) || null;
  }
};

// 选择技能或变体显示详情
const selectSkillOrVariant = (item: skills | skill_variants) => {
  selectedDetail.value = item;
};

// 初始化加载数据
onMounted(() => {
  fetchData();
});

const handleClick = (event: Event) => {
  const target = event.target as HTMLElement;
  console.log('点击目标:', target); // 添加日志以调试
  if (target.classList.contains("link")) {
    const to = target.dataset.to;
    console.log('跳转目标:', to); // 添加日志以调试
    if (to) {
      router.push(to); // 使用 Vue Router 跳转
    }
  }
};
</script>
  
  <style scoped>
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
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px;
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
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px;
    background-color: #000000;
    border-radius: 3px;
    cursor: pointer ;
    font-size: 18px ;
  }
  
  .skill-tree-item:hover,
  .skill-tree-item.selected {
    background-color: #1b1b1b;
  }
  
  .main-content {
    width: 65%;
    padding: 10px;
    border-radius: 0;
    background-color: #000000;
  }
  
  .skills-list {
    width: 100%;
  }
  
  .skill-section {
    margin-bottom: 20px;
  }
  
  .skill-section h2 {
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 2px 4px, rgb(80, 80, 80) 1px 3px 4px;
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
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px;
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
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px;
  }
  
  .variant-desc {
    font-size: 0.8rem;
  }
  
  .details-panel {
    overflow:hidden;
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
  </style>