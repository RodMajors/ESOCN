<template>
  <div class="gear-area">
    <!-- 左上角：套装类型和护甲类型 -->
    <div class="type-place">
      <div>
        <span class="type">{{ typeText }}</span>
        <br v-if="armorTypes.length > 0" />
        <span v-if="armorTypes.length > 0" class="armor-type">{{ armorTypes.join(' / ') }}</span>
      </div>
      <span class="place">{{ set.place }}</span>
    </div>

    <!-- 居中内容 -->
    <div class="center-content">
      <!-- 套装图标 -->
      <img :src="getIconPath(set)" class="set-icon" alt="Set Icon" />

      <!-- 套装名称和英文名 -->
      <div @click="goToDetail(set.enName)" class="name-container">
        <span class="name">{{ set.name }}</span>
        <br />
        <span class="en-name">&lt;{{ set.enName }}&gt;</span>
      </div>

      <!-- 分割线 -->
      <div class="divider"></div>

      <!-- 套装效果 -->
      <ul class="bonuses">
        <li v-for="(effect, key) in Object.values(set.bonuses).filter(e => e)" :key="key" v-html="parseColorTags(effect)"></li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import { parseColorTags } from '../utils/parseColorTags';

interface EquipmentSet {
  name: string;
  enName: string;
  place: string;
  bonuses: { [key: string]: string };
  type: number;
  styles?: {
    武器?: { [key: string]: any };
    护甲?: { [key: string]: any };
  };
}

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

    // 获取护甲类型
    const armorTypes = computed(() => {
      const armorStyles = props.set.styles?.护甲;
      if (!armorStyles) return [];

      const partMap = {
        '重型': '重甲',
        '中型': '中甲',
        '轻型': '轻甲'
      } as const;

      const armorParts = Object.values(armorStyles) as Array<{ [key: string]: any }>;
      const typesSet = new Set<string>();

      armorParts.forEach(part => {
        const partTypes = Object.keys(part);
        partTypes.forEach(type => {
          if (type in partMap) {
            typesSet.add(partMap[type as keyof typeof partMap]);
          }
        });
      });

      return Array.from(typesSet);
    });

    // 获取图标路径
    const getIconPath = (set: EquipmentSet): string => {
      let iconPath = '';
      if (set.styles?.护甲?.头部) {
        const headType = Object.values(set.styles.护甲.头部)[0] as any;
        iconPath = headType?.icon || '';
      } else {
        const getFirstIcon = (obj: any): string => {
          if (!obj) return '';
          if (obj.icon) return obj.icon;
          const firstValue = Object.values(obj)[0];
          return getFirstIcon(firstValue);
        };
        iconPath = getFirstIcon(set.styles);
      }
      const cleanPath = iconPath.replace(/^\/esoui\//, '').replace('.dds', '.webp');
      return cleanPath ? `/esoui/${cleanPath}` : 'https://via.placeholder.com/24';
    };

    // 跳转到套装详情页
    const goToDetail = (enName: string) => {
      const formattedName = enName.replace(/\s+/g, '-');
      router.push(`/equipment/${formattedName}`);
    };

    return {
      typeText,
      armorTypes,
      getIconPath,
      goToDetail,
      parseColorTags,
    };
  },
});
</script>

<style scoped>
.gear-area {
  width: 300px; /* 固定宽度 */
  padding: 1rem;
  background-color: #000000;
  border: 1px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  margin: 1rem;
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