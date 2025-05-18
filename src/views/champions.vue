```vue
<template>
  <div class="column-container" :class="{ 'single-column': activeColumn }">
    <!-- 盗贼列 -->
    <div class="columns" v-if="!activeColumn || activeColumn === 'thief'" :class="{ active: activeColumn === 'thief' }">
      <div v-if="activeColumn === 'thief'" class="svg-container">
        <svg
          :width="svgWidth"
          :height="svgHeight"
          class="constellation-svg"
          ref="svgContainer"
          @mouseover="handleMouseOver"
          @mouseout="hideTooltip"
        >
          <g v-html="svgContent"></g>
        </svg>
        <ChampionArea
          v-if="tooltip.skill"
          class="tooltip-champion-area"
          :style="{ top: tooltip.y + 'px', left: tooltip.x + 'px' }"
          :skill="tooltip.skill"
        />
        <button v-if="activeColumn && svgContent" class="back-button" @click="goBack">返回</button>
      </div>
      <img
        v-else
        class="background"
        src="/background/cp/ON-champion-thief.png"
        alt="盗贼"
        @click="setActiveColumn('thief')"
      >
      <table class="skill-list">
        <tr
          v-for="skill in thiefSkills"
          :key="skill.id"
          @click="skill.en_name && navigateToSkill(skill.en_name)"
          class="skill-row"
        >
          <td class="icon-column">
            <img class="icon" src="/background/cp/ON-icon-Champion_Stamina.png" alt="技能图标">
          </td>
          <td class="name-column">
            <span class="cp-name">{{ skill.name }}</span>
          </td>
          <td class="enName-column cp-name">&lt;{{ skill.en_name ?? 'Unknown' }}&gt;</td>
          <td v-if="activeColumn === 'thief'" class="description-column">
            <p v-html="parseColorTags(skill.description)"></p>
          </td>
        </tr>
      </table>
    </div>

    <!-- 法师列 -->
    <div class="columns" v-if="!activeColumn || activeColumn === 'mage'" :class="{ active: activeColumn === 'mage' }">
      <div v-if="activeColumn === 'mage'" class="svg-container">
        <svg
          :width="svgWidth"
          :height="svgHeight"
          class="constellation-svg"
          ref="svgContainer"
          @mouseover="handleMouseOver"
          @mouseout="hideTooltip"
        >
          <g v-html="svgContent"></g>
        </svg>
        <ChampionArea
          v-if="tooltip.skill"
          class="tooltip-champion-area"
          :style="{ top: tooltip.y + 'px', left: tooltip.x + 'px' }"
          :skill="tooltip.skill"
        />
        <button v-if="activeColumn && svgContent" class="back-button" @click="goBack">返回</button>
      </div>
      <img
        v-else
        class="background"
        src="/background/cp/ON-champion-mage.png"
        alt="法师"
        @click="setActiveColumn('mage')"
      >
      <table class="skill-list">
        <tr
          v-for="skill in filteredMageSkills"
          :key="skill.id"
          @click="skill.en_name && navigateToSkill(skill.en_name)"
          class="skill-row"
        >
          <td class="icon-column">
            <img class="icon" src="/background/cp/ON-icon-Champion_Magicka.png" alt="技能图标">
          </td>
          <td class="name-column">
            <span class="cp-name">{{ skill.name }}</span>
          </td>
          <td class="enName-column cp-name">&lt;{{ skill.en_name ?? 'Unknown' }}&gt;</td>
          <td v-if="activeColumn === 'mage'" class="description-column">
            <p v-html="parseColorTags(skill.description)"></p>
          </td>
        </tr>
      </table>
    </div>

    <!-- 战士列 -->
    <div class="columns" v-if="!activeColumn || activeColumn === 'warrior'" :class="{ active: activeColumn === 'warrior' }">
      <div v-if="activeColumn === 'warrior'" class="svg-container">
        <svg
          :width="svgWidth"
          :height="svgHeight"
          class="constellation-svg"
          ref="svgContainer"
          @mouseover="handleMouseOver"
          @mouseout="hideTooltip"
        >
          <g v-html="svgContent"></g>
        </svg>
        <ChampionArea
          v-if="tooltip.skill"
          class="tooltip-champion-area"
          :style="{ top: tooltip.y + 'px', left: tooltip.x + 'px' }"
          :skill="tooltip.skill"
        />
        <button v-if="activeColumn && svgContent" class="back-button" @click="goBack">返回</button>
      </div>
      <img
        v-else
        class="background"
        src="/background/cp/ON-champion-warrior.png"
        alt="战士"
        @click="setActiveColumn('warrior')"
      >
      <table class="skill-list">
        <tr
          v-for="skill in filteredWarriorSkills"
          :key="skill.id"
          @click="skill.en_name && navigateToSkill(skill.en_name)"
          class="skill-row"
        >
          <td class="icon-column">
            <img class="icon" src="/background/cp/ON-icon-Champion_Health.png" alt="技能图标">
          </td>
          <td class="name-column">
            <span class="cp-name">{{ skill.name }}</span>
          </td>
          <td class="enName-column cp-name">&lt;{{ skill.en_name ?? 'Unknown' }}&gt;</td>
          <td v-if="activeColumn === 'warrior'" class="description-column">
            <p v-html="parseColorTags(skill.description)"></p>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted, watch, onUnmounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { loadChampion } from '@/utils/loadChampion';
import type { ChampionSkill } from '@/utils/loadChampion';
import { parseColorTags } from '@/utils/parseColorTags';
import ChampionArea from '@/components/ChampionArea.vue';

interface Tooltip {
  visible: boolean;
  x: number;
  y: number;
  name: string;
  englishName: string;
  skill: ChampionSkill | null;
}

export default defineComponent({
  name: 'ChampionsPage',
  components: { ChampionArea },
  setup() {
    const thiefSkills = ref<ChampionSkill[]>([]);
    const mageSkills = ref<ChampionSkill[]>([]);
    const warriorSkills = ref<ChampionSkill[]>([]);
    const activeColumn = ref<string | null>(null);
    const svgContent = ref<string>('');
    const svgContainer = ref<SVGSVGElement | null>(null);
    const svgWidth = ref(800);
    const svgHeight = ref(450);
    const currentSvg = ref<string>(''); // 当前星图路径
    const svgHistory = ref<string[]>([]); // 星图历史栈
    const subSvgSkills = ref<Record<string, string[]>>({}); // 子星图技能列表
    const router = useRouter();
    const route = useRoute();

    const tooltip = reactive<Tooltip>({
      visible: false,
      x: 0,
      y: 0,
      name: '',
      englishName: '',
      skill: null
    });

    // 簇技能到子星图的映射
    const subSvgMap: Record<string, string> = {
      Extended_Might: '/background/cp/subcon_mage1.svg',
      Staving_Death: '/background/cp/subcon_mage3.svg',
      Mastered_Curation: '/background/cp/subcon_mage2.svg',
      Wind_Chaser: '/background/cp/subcon_warrior1.svg',
      Walking_Fortress: '/background/cp/subcon_warrior2.svg',
      "Survivor_s_Spite": '/background/cp/subcon_warrior3.svg'
    };

    // 类别到星图的映射
    const categorySvgMap: Record<string, { category: string; svg: string; history: string[] }> = {
      mage: { category: 'mage', svg: '/background/cp/warfare.svg', history: ['/background/cp/warfare.svg'] },
      warrior: { category: 'warrior', svg: '/background/cp/warrior.svg', history: ['/background/cp/warrior.svg'] },
      thief: { category: 'thief', svg: '/background/cp/craft.svg', history: ['/background/cp/craft.svg'] }
    };

    // 过滤法师技能
    const filteredMageSkills = computed(() => {
      if (activeColumn.value !== 'mage' || !currentSvg.value.includes('subcon_mage')) {
        return mageSkills.value;
      }
      const skills = subSvgSkills.value[currentSvg.value] || [];
      return mageSkills.value.filter(skill => skill.en_name && skills.includes(skill.en_name));
    });

    // 过滤战士技能
    const filteredWarriorSkills = computed(() => {
      if (activeColumn.value !== 'warrior' || !currentSvg.value.includes('subcon_warrior')) {
        return warriorSkills.value;
      }
      const skills = subSvgSkills.value[currentSvg.value] || [];
      return warriorSkills.value.filter(skill => skill.en_name && skills.includes(skill.en_name));
    });

    // 加载技能数据
    const fetchSkills = async () => {
      mageSkills.value = await loadChampion(1);
      warriorSkills.value = await loadChampion(2);
      thiefSkills.value = await loadChampion(3);
    };

    // 解码HTML实体
    const decodeHtmlEntities = (str: string): string => {
      const textarea = document.createElement('textarea');
      textarea.innerHTML = str;
      return textarea.value;
    };

    // 加载SVG文件并解析技能
    const loadSvg = async (svgPath: string) => {
      console.log('Loading SVG:', svgPath);
      try {
        const response = await fetch(svgPath);
        const text = await response.text();
        svgContent.value = text.replace(/<\?xml[^>]*>/, '').replace(/<!DOCTYPE[^>]*>/, '');

        // 解析子星图的技能（法师和战士）
        if ((svgPath.includes('subcon_mage') || svgPath.includes('subcon_warrior')) && !subSvgSkills.value[svgPath]) {
          const parser = new DOMParser();
          const doc = parser.parseFromString(text, 'image/svg+xml');
          const useElements = doc.querySelectorAll('use[id]:not([id="image"])');
          const skills: string[] = [];
          useElements.forEach((useEl) => {
            const id = useEl.getAttribute('id') || '';
            const dataName = (useEl.getAttribute('data-name') || id.replace(/_/g, ' ')).replace(/'/g, "'").replace(/_/g, ' ');
            if (dataName) {
              skills.push(dataName);
            }
          });
          subSvgSkills.value[svgPath] = skills;
          console.log('Sub SVG skills:', { svgPath, skills });
        }

        if (svgContainer.value) {
          const viewBox = svgContainer.value.getAttribute('viewBox')?.split(' ').map(Number);
          if (viewBox) {
            const scaleX = svgWidth.value / viewBox[2];
            const scaleY = svgHeight.value / viewBox[3];
            svgContainer.value.querySelectorAll('use, path').forEach(el => {
              if (el.tagName === 'use' && el.getAttribute('id') !== 'image') {
                const transform = el.getAttribute('transform') || '';
                const match = transform.match(/translate\(([\d.-]+)\s+([\d.-]+)\)/);
                if (match) {
                  const x = parseFloat(match[1]) * scaleX;
                  const y = parseFloat(match[2]) * scaleY;
                  el.setAttribute('transform', `translate(${x} ${y})`);
                  const width = 101 * scaleX;
                  const height = 101 * scaleY;
                  el.setAttribute('width', width.toString());
                  el.setAttribute('height', height.toString());
                }
              } else if (el.tagName === 'path') {
                const d = el.getAttribute('d') || '';
                const match = d.match(/M\s*([\d.-]+),([\d.-]+)\s*[cL][^M]*?([\d.-]+),([\d.-]+)/);
                if (match) {
                  const x1 = parseFloat(match[1]) * scaleX;
                  const y1 = parseFloat(match[2]) * scaleY;
                  const x2 = parseFloat(match[3]) * scaleX;
                  const y2 = parseFloat(match[4]) * scaleY;
                  el.setAttribute('d', `M${x1},${y1} L${x2},${y2}`);
                }
              }
            });
          }
        }
        currentSvg.value = svgPath;
        window.history.replaceState({ activeColumn: activeColumn.value, currentSvg: svgPath, svgHistory: [...svgHistory.value] }, '');
      } catch (error) {
        console.error(`Failed to load SVG: ${svgPath}`, error);
      }
    };

    watch(activeColumn, (newValue) => {
      if (newValue) {
        const svgPath = categorySvgMap[newValue]?.svg || '/background/cp/warfare.svg';
        svgHistory.value = [svgPath];
        loadSvg(svgPath);
      } else {
        currentSvg.value = '';
        svgContent.value = '';
        svgHistory.value = [];
        console.log('Returning to three-column view:', { activeColumn: activeColumn.value, currentSvg: currentSvg.value });
      }
    });

    const setActiveColumn = (column: string) => {
      activeColumn.value = column;
    };

    const goBack = () => {
      if (svgHistory.value.length > 1) {
        svgHistory.value.pop();
        const prevSvg = svgHistory.value[svgHistory.value.length - 1];
        loadSvg(prevSvg);
      } else {
        activeColumn.value = null;
        currentSvg.value = '';
        svgContent.value = '';
        svgHistory.value = [];
        window.history.replaceState({ activeColumn: null, currentSvg: '', svgHistory: [] }, '');
        console.log('Returning to three-column view:', { activeColumn: activeColumn.value, currentSvg: currentSvg.value });
      }
    };

    const handleMouseOver = (event: MouseEvent) => {
      const target = event.target as SVGElement;
      if (target.tagName === 'use' && target.getAttribute('id') !== 'image') {
        const id = target.getAttribute('id') || '';
        const dataName = (target.getAttribute('data-name') || id.replace(/_/g, ' ')).replace(/&apos;/g, "'").replace(/_/g, ' ');
        if (id in subSvgMap) {
          tooltip.visible = false;
          tooltip.skill = null;
          target.onclick = () => {
            const subSvgPath = subSvgMap[id];
            console.log('Cluster skill clicked:', id, 'Sub SVG:', subSvgPath);
            svgHistory.value.push(subSvgPath);
            loadSvg(subSvgPath);
          };
          return;
        }
        let skills: ChampionSkill[] = [];
        if (activeColumn.value === 'thief') skills = thiefSkills.value;
        else if (activeColumn.value === 'mage') skills = mageSkills.value;
        else if (activeColumn.value === 'warrior') skills = warriorSkills.value;
        const skill = skills.find(s => s.en_name === dataName);
        if (skill && skill.en_name) {
          tooltip.skill = skill;
          tooltip.name = decodeHtmlEntities(dataName);
          tooltip.englishName = id;
          tooltip.visible = true;
          tooltip.x = event.clientX + 10;
          tooltip.y = event.clientY + 10;
          target.onclick = () => {
            console.log('Navigating to skill:', dataName);
            navigateToSkill(dataName);
          };
        } else {
          console.warn(`Skill not found for id: ${dataName} in ${activeColumn.value}`);
        }
      }
    };

    const hideTooltip = () => {
      tooltip.visible = false;
      tooltip.name = '';
      tooltip.englishName = '';
      tooltip.skill = null;
    };

    const navigateToSkill = (enName: string | null) => {
      if (!enName) {
        console.warn('Cannot navigate: en_name is null');
        return;
      }
      const formattedName = enName.replace(/\s+/g, '_');
      window.history.replaceState(
        { activeColumn: activeColumn.value, currentSvg: currentSvg.value, svgHistory: [...svgHistory.value], fromChampionDetail: false },
        ''
      );
      router.push(`/champions/${formattedName}`).catch(err => {
        console.log("Navigation error:", err);
      });
    };

    const handlePopState = (event: PopStateEvent) => {
      const state = event.state;
      console.log('Popstate restored:', { activeColumn: state?.activeColumn, currentSvg: state?.currentSvg, svgHistory: state?.svgHistory });
      if (state && state.activeColumn) {
        activeColumn.value = state.activeColumn;
        currentSvg.value = state.currentSvg || '';
        svgHistory.value = state.svgHistory || (
          state.currentSvg.includes('subcon_')
            ? [categorySvgMap[state.activeColumn]?.svg || '/background/cp/warfare.svg', state.currentSvg]
            : [state.currentSvg]
        );
        if (currentSvg.value) {
          loadSvg(currentSvg.value);
        } else {
          svgContent.value = '';
        }
      } else {
        activeColumn.value = null;
        svgContent.value = '';
        currentSvg.value = '';
        svgHistory.value = [];
      }
    };

    onMounted(() => {
      fetchSkills();
      const initialState = window.history.state;

      if (initialState?.activeColumn && initialState?.currentSvg) {
        activeColumn.value = initialState.activeColumn;
        currentSvg.value = initialState.currentSvg;
        svgHistory.value = initialState.svgHistory || (
          initialState.currentSvg.includes('subcon_')
            ? [categorySvgMap[initialState.activeColumn]?.svg || '/background/cp/warfare.svg', initialState.currentSvg]
            : [initialState.currentSvg]
        );
        loadSvg(initialState.currentSvg);
      }
      window.addEventListener('popstate', handlePopState);
    });

    onUnmounted(() => {
      window.removeEventListener('popstate', handlePopState);
    });

    return {
      thiefSkills,
      mageSkills,
      warriorSkills,
      filteredMageSkills,
      filteredWarriorSkills,
      parseColorTags,
      activeColumn,
      setActiveColumn,
      goBack,
      svgContent,
      svgContainer,
      svgWidth,
      svgHeight,
      tooltip,
      handleMouseOver,
      hideTooltip,
      navigateToSkill
    };
  }
});
</script>

<style scoped>
.column-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}

.column-container.single-column {
  padding: 0;
  display: block;
}

.columns {
  flex: 1;
  margin: 0 10px;
  padding: 20px;
  border-radius: 8px;
}

.columns.active {
  margin: 0 100px;
  padding: 20px 0;
  max-width: 100%;
}

.background {
  width: 100%;
  height: 300px;
  max-width: 800px;
  object-fit: cover;
  border-radius: 4px;
  margin: 0 auto 20px;
  display: block;
  cursor: pointer;
  transition: transform 0.6s ease;
}

.columns:hover .background {
  transform: scale(1.1);
}

.svg-container {
  width: 100%;
  display: block;
  position: relative;
}

.constellation-svg {
  width: 100%;
  height: auto;
  max-height: 600px;
  border-radius: 4px;
  background: #000;
}

:deep(.constellation-svg use) {
  cursor: pointer;
}

.constellation-svg path {
  stroke: #ffffff;
  stroke-width: 1;
  fill: none;
}

.columns.active .svg-container {
  max-height: 600px;
}

.back-button {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1100;
  padding: 8px 16px;
  color: #C5C29E;
  background-color: #1A1A1A;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.back-button:hover {
  background-color: #212121;
}

.skill-list {
  width: 100%;
  border-collapse: collapse;
  padding: 0;
  margin: 0 auto;
}

.columns.active .skill-list {
  width: calc(100% - 40px);
  margin: 0;
  box-sizing: border-box;
}

.skill-list tr {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.skill-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.skill-row:hover {
  background-color: #1A1A1A;
}

.icon-column {
  width: 40px;
  padding: 0 4px;
  text-align: center;
  vertical-align: middle;
}

.icon {
  width: 100%;
  max-width: 64px;
  height: auto;
  display: block;
  margin: 0 auto;
}

.name-column {
  width: 20%;
  padding: 0 8px;
  text-align: center;
  vertical-align: middle;
}

.enName-column {
  flex: 20%;
  text-align: center;
  padding: 0;
  vertical-align: middle;
}

.description-column {
  flex: 50%;
  padding: 0 0 0 100px;
  vertical-align: middle;
}

.description-column p {
  margin: 0;
  font-size: 0.9em;
}

.cp-name {
  color: #e5e2b9;
  padding: 4px;
  text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px;
  border-radius: 10px;
  font-size: 16px;
}

.tooltip-champion-area {
  position: fixed;
  z-index: 1000;
  pointer-events: none;
  max-width: 300px;
  transform: translate(10px, 10px);
}

@media (max-width: 768px) {
  .column-container {
    flex-direction: column;
    padding: 10px;
  }

  .column-container.single-column {
    padding: 0;
  }

  .columns {
    margin: 10px 0;
    padding: 10px;
  }

  .columns.active {
    padding: 10px 0;
    width: 100%;
    max-width: none;
  }

  .background,
  .svg-container {
    height: 200px;
    max-width: 100%;
  }

  .columns.active .background,
  .columns.active .svg-container {
    max-height: 400px;
  }

  .columns.active .skill-list {
    margin: 0 10px;
    max-width: none;
  }

  .skill-list tr {
    flex-direction: column;
    align-items: flex-start;
  }

  .icon-column,
  .name-column,
  .enName-column,
  .description-column {
    width: 100%;
    text-align: left;
    padding: 5px 8px;
  }

  .icon {
    max-width: 24px;
  }

  .tooltip-champion-area {
    max-width: 90%;
    transform: translate(5px, 5px);
  }

  .back-button {
    top: 5px;
    left: 5px;
    padding: 6px 12px;
    font-size: 0.9em;
  }
}
</style>
```