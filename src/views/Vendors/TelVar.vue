<template>
    <header
        class="vendor-header"
        :style="{ backgroundImage: `url(/background/vendor/TelVar.jpg)` }"
    >
        <div class="title-overlay">
            <h1>泰尔瓦石商人</h1>
            <p class="en-title">TELVAR VENDOR</p>
        </div>
    </header>
    <div class="body">
        <div class="content">
            <b>泰尔瓦石商人</b
            >是出现在每个阵营帝都下水道的特殊行商，它们分别是图曼德（Tumande 先祖神州）、听石动（Hears-the-Stone 黑檀心）和卡佐尔加（Kharzolga 匕落）。
            <br /><br />
            泰尔瓦石商人所出售的商品需要使用<b>泰尔瓦石</b><img src="/icon/telvar.png" class="icon">来购买。
            <br /><br />
            泰尔瓦石商人的货物会在GMT标准时间周三凌晨0点、<b>北京时间每周三上午八点</b>准时刷新，持续一周。
            <br /><br />
            泰尔瓦石商人会出售包括篆刻脚本、技能样式碎片、书籍、PVP装备在内的特殊物品。
        </div>
        <h2>泰尔瓦商品列表（{{ time }}）</h2>

        <transition name="slide-down">
            <table>
                <tbody>
                    <tr
                        v-for="(item, index) in data"
                        :key="item.enName"
                        :class="index % 2 === 0 ? 'row-dark' : 'row-light'"
                    >
                        <td class="infinite-icon-column">
                            <img
                                :src="item.icon"
                                class="set-icon"
                                alt="Set Icon"
                            />
                        </td>
                        <td class="infinite-name-column" :style="{ color: item.color }">
                            <div class="name-link">
                                <span>{{ item.name }}</span>
                                <br />
                                <span class="en-name">{{
                                    item.enName.toUpperCase()
                                }}</span>
                            </div>
                        </td>
                        <td>
                            <span v-if="item.value" class="infinite-gold-column">
                                {{ item.value }} 档案塔财富
                                <img src="/icon/telvar.png" class="icon">
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
import type { InfiniteType } from "@/types/infinite";


export default defineComponent({
    name: "TelVar",
    setup() {
        const data = ref<InfiniteType[]>([]);
        const time = ref<string>("");

        const fetchInfinite = async () => {
            try {
                const response = await fetch(
                    "http://localhost:3000/api/tel-var-vendor"
                );
                if (!response.ok) {
                    throw new Error(`网络请求失败: ${response.status}`);
                }
                const result = await response.json();
                data.value = result.data || [];
                time.value = result.time || "";
            } catch (error) {
                console.error("获取档案塔商人列表失败:", error);
                data.value = [];
            }
        };
        // 初始化
        fetchInfinite();

        return {
            data,
            time,
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

.infinite-icon-column {
    cursor: pointer;
    width: 10%;
    padding: 0 0.5rem 0 1rem;
}

.infinite-name-column {
    width: 70%;
    text-align: center;
    padding: 0 0.5rem;
}


.infinite-gold-column {
    width: 20%;
    text-align: center;
    padding: 0 0.5rem;
    color: #c3c3c3;
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

.infinite-name-column .name-link {
    cursor: pointer;
    text-decoration: none;
    transition: color 0.3s ease;
    text-shadow: rgb(0, 0, 0) -1px 1px 4px, rgb(0, 0, 0) -2px 2px 4px,
        rgb(0, 0, 0) -3px 3px 4px;
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
    margin: 0.5rem 0 0;
    font-weight: 600;
    text-shadow: rgb(0, 0, 0) -1px 1px 4px, rgb(0, 0, 0) -2px 2px 4px,
        rgb(0, 0, 0) -3px 3px 4px;
}

.subCategory {
    font-size: 0.9rem;
}

.goldicon {
    width: 16px;
}
</style>
