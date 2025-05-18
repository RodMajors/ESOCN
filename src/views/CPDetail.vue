```vue
<template>
      <header 
        class="champion-header"  
        :style="{ backgroundImage: `url(${background})`}"  
        @click="navigateToConstellation"
      >
      <div class="title-overlay">
        <h1>{{ skill?.category_name }}</h1>
        <p class="en-name">{{ enName?.toUpperCase() }}</p>
      </div>
    </header>


  <div class="champion-detail">
    <ChampionArea v-if="skill" :skill="skill" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { loadSkillByEnName } from '@/utils/loadChampion';
import type { ChampionSkill } from '@/utils/loadChampion';
import ChampionArea from '@/components/ChampionArea.vue';

export default defineComponent({
  name: 'ChampionDetail',
  components: { ChampionArea },
  setup() {
    const route = useRoute();
    const router = useRouter(); // 添加 useRouter
    const skill = ref<ChampionSkill | null>(null);

    // 类别到星图的映射
    const categorySvgMap: Record<number, { category: string; svg: string; history: string[] }> = {
      1: { category: 'mage', svg: '/background/cp/warfare.svg', history: ['/background/cp/warfare.svg'] },
      2: { category: 'warrior', svg: '/background/cp/warrior.svg', history: ['/background/cp/warrior.svg'] },
      3: { category: 'thief', svg: '/background/cp/craft.svg', history: ['/background/cp/craft.svg'] }
    };

    // 子星图技能映射（需替换为真实数据）
    const subSvgSkillsMap: Record<string, string[]> = {
      '/background/cp/subcon_mage1.svg': ['Blessed', 'Another_Skill'],
      '/background/cp/subcon_mage2.svg': ['Skill3', 'Skill4'],
      '/background/cp/subcon_mage3.svg': ['Skill5', 'Skill6'],
      '/background/cp/subcon_warrior1.svg': ['Wind_Chaser_Skill', 'Skill7'],
      '/background/cp/subcon_warrior2.svg': ['Walking_Fortress_Skill', 'Skill8'],
      '/background/cp/subcon_warrior3.svg': ['Survivors_Spite_Skill', 'Skill9']
    };

    const background = computed(() => {
      switch (skill.value?.category_id) {
        case 1:
          return '/background/cp/ON-champion-mageHeader.png';
        case 2:
          return '/background/cp/ON-champion-warriorHeader.png';
        case 3:
          return '/background/cp/ON-champion-thiefHeader.png';
        default:
          return '/background/cp/ON-champion-mageHeader.png'; // 默认值
      }
    });

    const enName = computed(() => {
      switch (skill.value?.category_id) {
        case 1:
          return 'Warfare';
        case 2:
          return 'fitness';
        case 3:
          return 'craft';
      }
    })

    // 跳转到单栏星座页面
    const navigateToConstellation = () => {
      if (!skill.value?.category_id) {
        console.warn('No category_id available for navigation');
        return;
      }

      const category = categorySvgMap[skill.value.category_id]?.category;
      if (!category) {
        console.warn(`No category found for category_id: ${skill.value.category_id}`);
        return;
      }

      let svg = categorySvgMap[skill.value.category_id].svg;
      let history = categorySvgMap[skill.value.category_id].history;

      if (skill.value.en_name) {
        for (const [subSvg, skills] of Object.entries(subSvgSkillsMap)) {
          if (skills.includes(skill.value.en_name)) {
            svg = subSvg;
            history = [categorySvgMap[skill.value.category_id].svg, subSvg];
            break;
          }
        }
      }

      router.push({
        path: '/champions',
        state: {
          activeColumn: category,
          currentSvg: svg,
          svgHistory: history,
          fromChampionDetail: true
        }
      });
    };

    const fetchSkill = async () => {
      const enName = route.params.enName as string;
      try {
        skill.value = await loadSkillByEnName(enName);
        if (!skill.value) {
          console.warn(`Skill not found: ${enName}`);
          return;
        }

        // 初始化 history.state
        let state = categorySvgMap[skill.value.category_id] || categorySvgMap[1];
        if (skill.value.en_name) {
          for (const [svg, skills] of Object.entries(subSvgSkillsMap)) {
            if (skills.includes(skill.value.en_name)) {
              state = {
                category: categorySvgMap[skill.value.category_id].category,
                svg,
                history: [categorySvgMap[skill.value.category_id].svg, svg]
              };
              break;
            }
          }
        }
        window.history.replaceState(
          { activeColumn: state.category, currentSvg: state.svg, svgHistory: state.history, fromChampionDetail: true },
          ''
        );
        console.log('CPDetail state initialized:', {
          activeColumn: state.category,
          currentSvg: state.svg,
          svgHistory: state.history
        });
      } catch (error: unknown) {
        console.error('Failed to load skill in CPDetail:', {
          enName,
          error: error instanceof Error ? error.message : String(error)
        });
      }
    };

    onMounted(fetchSkill);

    return { skill, background, navigateToConstellation, enName };
  }
});
</script>

<style scoped>
.champion-header {
  position: relative;
  height: 150px;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  margin-bottom: 0.5rem;
  cursor: pointer;
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

.champion-detail {
  min-height: 100vh;
  background: #000;
  padding: 20px;
  position: relative;
}

.skill-details {
  color: #e5e2b9;
  margin-top: 20px;
}

.skill-details p {
  margin: 5px 0;
  font-size: 1em;
}

@media (max-width: 768px) {
  .champion-detail {
    padding: 10px;
  }

  .skill-details {
    margin-top: 10px;
  }

  .skill-details p {
    font-size: 0.9em;
  }
}
</style>
```