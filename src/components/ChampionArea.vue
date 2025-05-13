    <template>
        <div class="champion-area">
        <div class="header">
            <span class="category">{{ skill.category_name }}</span>
            <span class="cluster">{{ skill.cluster_name }}</span>
        </div>
        <h2 class="name">{{ skill.name }}</h2>
        <p class="en-name">{{ skill.en_name.toUpperCase() }}</p>
        <div class="divider"></div>
        <div class="description" v-html="parseColorTags(skill.description)"></div>
        <div class="progressbar">
            <span style = "font-size: 0.9rem; color: #ffffff;">0</span>
            <span><img class = "bar" src="/background/cp/progressbar.png" alt=""></span>
            <span style = "font-size: 0.9rem; color: #ffffff;">{{ skill.max_points }}</span>
        </div>
        <div class="cost">
            <div style="color: #28D321;">花费</div>
            <div style="color: #ffffff;">{{skill.jump_point_delta}}</div>
            <img
                class="category-icon"
                :src="categoryIcon"
                alt="类别图标"
            />
            <div style="color: #28D321;">解锁</div>
        </div>
        <div class="slottable" style = "" v-if="skill.is_slottable === 1">
            添加至勇士栏激活
        </div>
        </div>
    </template>
    <script lang="ts">
    import { defineComponent, computed } from 'vue';
    import type { PropType } from 'vue';
    import { parseColorTags } from '@/utils/parseColorTags';
    import type { ChampionSkill } from '@/utils/loadChampion';
    
    export default defineComponent({
        name: 'ChampionArea',
        props: {
        skill: {
            type: Object as PropType<ChampionSkill>,
            required: true
        }
        },
        setup(props) {
        // 计算图标路径
        const categoryIcon = computed(() => {
            switch (props.skill.category_id) {
            case 1:
                return '/background/cp/ON-icon-Champion_Magicka.png'; // 法师
            case 2:
                return '/background/cp/ON-icon-Champion_Health.png'; // 战士
            case 3:
                return '/background/cp/ON-icon-Champion_Stamina.png'; // 盗贼
            default:
                return ''; // 默认无图标
            }
        });
        console.log(props.skill.is_slottable)
        console.log(props.skill)
        return { parseColorTags, categoryIcon };
        }
    });
    </script>
    <style scoped>
    /* 现有样式保持不变 */
    .champion-area {
        width: 300px;
        padding: 1rem;
        background-color: #000000;
        border: 1px solid #444;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        margin: 0.5rem;
    }
    
    .header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    
    .category {
        font-size: 0.9rem;
    }
    .cluster{
        font-size: 0.9rem;
    }
    
    .slottable {
        font-size: 0.9rem;
        color: #666666;
        text-align: center;
        margin-top: 20px;
    }
    
    .name {
        text-align: center;
        font-size: 1.2rem;
        margin: 0;
        color: #F6E43A;
        font-weight: 550;
    }
    
    .en-name {
        text-align: center;
        font-size: 0.9rem;
        color: #F6E43A;
        font-weight: 550;
    }
    
    .category-icon {
        display: block;
        width: 24px;
        height: 24px;
    }
    
    /* 其他样式（divider, description等）不变 */
    .divider {
        width: 100%;
        height: 1px;
        background: linear-gradient(to right, transparent, #fff, transparent);
        margin: 1rem auto;
    }
    
    .description {
        font-size: 0.9em;
        line-height: 1.5;
        text-align: center;
    }
    .progressbar{
        display: flex;
        padding: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
        gap: 5px;
        text-align: center;
    }
    .bar{
        max-width: 100%;
        height: auto;
        display: block;
    }
    .cost{
        display: flex;
        justify-content: center; /* 水平居中 */
        align-items: center; /* 垂直居中 */
    }
    
    /* 响应式 */
    @media (max-width: 768px) {
        .champion-area {
        padding: 15px;
        max-width: 90%;
        }
    
        .name {
        font-size: 1.5em;
        }
    
        .en-name {
        font-size: 1em;
        }
    
        .category-icon {
        width: 48px;
        height: 48px;
        }
    }
    </style>