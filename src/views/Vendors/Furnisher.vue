<template>
    <header
        class="vendor-header"
        :style="{ backgroundImage: `url(/background/vendor/Furnisher.jpg)` }"
    >
        <div class="title-overlay">
            <h1>豪华家具商</h1>
            <p class="en-title">LUXURY FURNISHER</p>
        </div>
    </header>
    <div class="body">
        <div class="content">
            <b>扎尼尔·瑟兰(Zanil Theran)</b
            >，又称<b>豪华家具商</b>，是一位出现在<b>冷港的空洞之城</b>、或<b>荒崖的贝尔卡斯</b>的特殊行商。
            <br /><br />
            豪华家具商会在GMT标准时间周五凌晨1点、<b>北京时间每周六上午9点</b>准时开放。
            并于GMT标准时间周一中午12点、<b>北京时间每周一下午8点</b>离开。
            <br /><br />
            他每周末都会出售同一主题的几件商品，以及每周添加一件该主题的新品。
            虽然商品会年度轮换，但是有些周会进行调整以便推出全新的商品。
        </div>
        <h2>家具列表（{{ time }}）</h2>

        <transition name="slide-down">
            <table>
                <tbody>
                    <tr
                        v-for="(furniture, index) in furnitures"
                        :key="furniture.enName"
                        :class="index % 2 === 0 ? 'row-dark' : 'row-light'"
                    >
                        <td class="icon-column">
                            <img
                                :src="furniture.icon"
                                class="set-icon"
                                alt="Set Icon"
                            />
                        </td>
                        <td class="name-column" :style="{ color: getQualityColor(furniture.quality) }">
                            <div class="name-link">
                                <span>{{ furniture.name }}</span>
                                <br />
                                <span class="en-name">{{
                                    furniture.enName.toUpperCase()
                                }}</span>
                            </div>
                        </td>
                        <td class="category-column">
                            <span class="category">{{ furniture.category }}</span>
                            <br />
                            <span class="subCategory">{{
                                furniture.subCategory
                            }}</span>
                        </td>
                        <td>{{ furniture.description }}</td>
                        <td>
                            <span v-if="furniture.cost" class="gold">
                                {{ furniture.cost.toLocaleString() }}
                                <img src="/public/icon/gold.png" class="goldicon" alt="Gold Icon" />
                            </span>
                            <span v-else>价格未知</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </transition>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import type { Furniture } from "@/types/furniture";

// 定义接口
interface LuxuryFurnisherItem {
    name: string;
    cost: number;
}

export default defineComponent({
    name: "Furnisher",
    setup() {
        const data = ref<LuxuryFurnisherItem[]>([]);
        const time = ref<string>("");
        const furnitures = ref<Furniture[]>([]);
        type Quality = '传说' | '优良' | '普通' | '上乘' | '史诗';
        // 品质颜色映射
        const qualityColors: Record<Quality, string> = {
            传说: '#DCC55F',
            优良: '#6BC34B',
            普通: '#6BC34B',
            上乘: '#6797EC',
            史诗: '#9B4AE5'
        };
        const getQualityColor = (quality: string) => {
            return qualityColors[quality as Quality] || '#C5C29E';
        };

        const getFurnitureByEnName = async (
            enName: string
        ): Promise<Furniture | null> => {
            try {
                const response = await fetch(
                    `http://localhost:3000/api/furniture/${encodeURIComponent(
                        enName
                    )}`
                );
                if (!response.ok) {
                    throw new Error(`网络请求失败: ${response.status}`);
                }
                const result = await response.json();
                return result as Furniture;
            } catch (error) {
                console.error(`获取家具 ${enName} 失败:`, error);
                return null;
            }
        };

        const fetchTime = async () => {
            try {
                const response = await fetch(
                    "http://localhost:3000/api/golden-vendor"
                );
                if (!response.ok) {
                    throw new Error(`网络请求失败: ${response.status}`);
                }
                const result = await response.json();
                time.value = result.time
            } catch (error) {
                console.error("获取时间失败:", error);
                time.value = new Date().toLocaleDateString("zh-CN", {
                    timeZone: "Asia/Shanghai",
                });
            }
        };

        const fetchFurnisher = async () => {
            try {
                const response = await fetch(
                    "http://localhost:3000/api/luxury-furnisher"
                );
                if (!response.ok) {
                    throw new Error(`网络请求失败: ${response.status}`);
                }
                const result = await response.json();
                data.value = result.data || [];
            } catch (error) {
                console.error("获取家具列表失败:", error);
                data.value = [];
            }

            furnitures.value = [];
            for (const item of data.value) {
                const furniture = await getFurnitureByEnName(item.name);
                if (furniture) {
                    const furnitureWithCost: Furniture = {
                        ...furniture,
                        cost: item.cost,
                    };
                    furnitures.value.push(furnitureWithCost);
                    console.log(
                        `添加家具: ${furnitureWithCost.name}, 价格: ${furnitureWithCost.cost}`
                    );
                } else {
                    console.warn(`未找到家具: ${item.name}`);
                }
            }
        };

        // 初始化
        fetchTime();
        fetchFurnisher();

        return {
            data,
            time,
            furnitures,
            getQualityColor
        };
    },
});
</script>

<style>
.vendor-header {
    position: relative;
    height: 150px;
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    margin-bottom: 1rem;
}

.title-overlay {
    text-align: center;
    color: #fff;
    text-shadow: 0 0 5px rgba(0, 0, 0, 0.8);
}

.title-overlay h1 {
    font-size: 2.2rem;
    text-shadow: rgb(0, 0, 0) -1px 1px 4px, rgb(0, 0, 0) -2px 2px 4px,
        rgb(0, 0, 0) -3px 3px 4px;
    margin: 0;
}

.en-name {
    font-size: 1.4rem;
    margin: 0.5rem 0 0;
    font-weight: 600;
    text-shadow: rgb(0, 0, 0) -1px 1px 4px, rgb(0, 0, 0) -2px 2px 4px,
        rgb(0, 0, 0) -3px 3px 4px;
}

.body {
    display: flex;
    flex-direction: column;
    gap: 1rem; /* 仅保留间距，不添加背景或边框 */
}

.sets-list {
    display: flex;
    max-width: 100%;
    flex-wrap: wrap;
    justify-content: space-between;
}

.ap {
    color: rgb(45, 197, 14);
}

.gold {
    color: #e0c850;
}

.icon {
    width: 16px;
}
h2 {
    color: #e5e2b9;
    padding: 4px;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px,
        rgb(80, 80, 80) 1px 1px 4px;
    border-radius: 10px;
    font-size: 24px;
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
    width: 100%;
    border-collapse: collapse;
    background-color: #101010;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    border: 1px solid #948159;
}

td {
    padding: 1rem;
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
    width: 30%;
    text-align: center;
    padding: 0 0.5rem;
}

.category-column {
    width: 15%;
    text-decoration: none;
}

.description-column {
    width: 20%;
    text-align: center;
    padding: 0 0.5rem;
}

.gold-column {
    width: 20%;
    text-align: center;
    padding: 0 0.5rem;
    color: #e0c850;
}

.row-dark {
    background-color: #101010;
}

.row-light {
    background-color: #1a1a1a;
}

.furniture-icon {
    width: 52px;
    height: 52px;
}

.name-link {
    cursor: pointer;
    text-decoration: none;
    transition: color 0.3s ease;
}

.name-link:hover {
    color: #ffffff;
}

.type-link {
    cursor: pointer;
    text-decoration: none;
}

.type-link:hover {
    text-decoration: underline;
}

.en-name {
    font-size: 0.9rem;
}

.subCategory {
    font-size: 0.9rem;
}

.goldicon {
    width: 16px;
}
</style>
