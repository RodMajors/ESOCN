<template>
  <div class="gear-area">
    <!-- 左上角：套装类型和护甲类型 -->
    <div class="type-place">
      <div>
        <span class="type">{{ typeText }}</span>
        <br v-if="set.armor.length > 0" />
        <span v-if="set.armor.length > 0" class="armor-type">{{ set.armor }}</span>
      </div>
      <span class="place">{{ set.place.split(',')[0] }}</span>
    </div>

    <!-- 居中内容 -->
    <div class="center-content">
      <!-- 套装图标 -->
      <img :src="set.icon" class="set-icon" alt="Set Icon" />

      <!-- 套装名称和英文名 -->
      <div @click="goToDetail(set.enName)" class="name-container">
        <span class="name">{{ set.name }}</span>
        <br />
        <span class="en-name">{{ set.enName.toUpperCase() }}</span>
      </div>

      <!-- 分割线 -->
      <div class="divider"></div>

      <!-- 套装效果 -->
      <ul class="bonuses">
        <li v-for="(effect, key) in Object.values(set.bonuses).filter(e => e)" :key="key" 
          v-html="parseColorTags(effect)" @click = "handleClick"></li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import { parseColorTags } from '../utils/parseColorTags';
import type { EquipmentSet } from '../types/equipment'; // 导入公共类型

const router = useRouter() ;

export default defineComponent({
  name: 'GearArea',
  props: {
    set: {
      type: Object as () => EquipmentSet,
      required: true,
    },
  },
  
  setup(props) {
    
    const router = useRouter();

    // 获取套装类型对应的文本
    const typeMap: { [key: number]: string } = {
      1: '竞技场', 2: 'PVP', 3: '制造', 4: 'PVP', 5: 'PVP', 6: '副本', 7: 'PVP',
      8: '怪物', 9: '区域', 10: '新手', 11: '试炼', 12: '神器', 13: '怪物', 14: '怪物', 15: '职业',
    };

    const typeText = computed(() => {
      return typeMap[props.set.type] || '未知';
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

    // 获取图标路径

    // 跳转到套装详情页
    const goToDetail = (enName: string) => {
      const formattedName = enName.replace(/\s+/g, '_');
      router.push(`/equipment/${formattedName}`);
    };

    return {
      typeText,
      goToDetail,
      parseColorTags,
      handleClick
    };
  },
});
</script>

<style scoped>
.gear-area {
  width: 300px;
  padding: 1rem;
  background-color: #000000;
  border: 1px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  margin: 0.5rem;
}

.type-place {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.type-place .type,
.type-place .place,
.type-place .armor-type {
  font-size: 0.9rem;
  color: #C5C29E;
}

.center-content {
  text-align: center;
}

.set-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 1rem;
}

.name-container {
  cursor: pointer;
  margin-bottom: 1rem;
}

.name-container .name {
  font-size: 1.2rem;
  color: #F6E43A;
}

.name-container .en-name {
  font-size: 0.9rem;
  color: #F6E43A;
}

.name-container:hover .name,
.name-container:hover .en-name {
  text-decoration: underline;
}

.divider {
  width: 100%;
  height: 1px;
  background: linear-gradient(to right, transparent, #fff, transparent);
  margin: 1rem auto;
}

.bonuses {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: center;
}

.bonuses li {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}
</style>