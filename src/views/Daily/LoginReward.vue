<template>
    <header
        class="vendor-header"
        :style="{ backgroundImage: `url(/background/daily/login.jpg)` }"
    >
        <div class="title-overlay">
            <h1>登录奖励</h1>
            <p class="en-title">LOGIN REWARD</p>
        </div>
    </header>
    <div class="body">
        <div class="content">
            <b>登录奖励</b
            >是每天可以领取一次的每日登录奖励，您需要每天登录才能领取本月的所有奖励。
            <br /><br />
            您可以在角色登录之后立即领取奖励，即使您错过，也可以通过前往皇冠商店（默认快捷键"，"）的每日奖励选项卡获取奖励
            <br /><br />
            登陆奖励会在每个月一号的<b>北京时间下午六点</b>重置。
        </div>
        <h2>当月登录奖励（{{ time }}）</h2>
        <div
            class="content reward-container"
            style="
                border-radius: 0px;
                margin-top: -20px;
                padding: 2rem 1rem 4rem 1rem;
            "
        >
            <div v-for="(item, index) in data" :key="index" class="rewardblock">
                <picture>
                    <img
                        :src="item.icon"
                        class="reward-icon"
                        alt="Reward Icon"
                    />
                </picture>
                <div class="day">
                    {{ item.day }}
                </div>
                <div class="rewardName">
                    {{ item.name }}
                </div>
                <div class="amount">
                    {{ item.amount }}
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import type { InfiniteType } from "@/types/infinite";
import type { LoginReward } from "@/types/loginReward";

export default defineComponent({
    name: "TelVar",
    setup() {
        const data = ref<LoginReward[]>([]);
        const time = ref<string>("");

        const fetchInfinite = async () => {
            try {
                const response = await fetch(
                    "http://localhost:3000/api/daily-login-rewards"
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
            for (const item of data.value) {
                item.icon = `/esoui/art/icons/${item.icon}.webp`;
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

.en-title {
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
.reward-container {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    box-sizing: border-box;
    row-gap: 8px;
    column-gap: 8px;
    text-shadow: -1px 1px 4px #000, -2px 2px 4px #000, -3px 3px 4px #000;
}

.rewardblock {
    color: white;
    padding: 24px;
    background-color: oklab(0 0 0 / 0.6);
    border-right: 1.5px solid #242424;
    border-bottom: 1.5px solid #242424;
    justify-content: center;
    align-items: center;
    display: flex;
    position: relative;
    transition: border-right 0.6s ease, border-bottom 0.6s ease;
}

.reward-icon {
    width: 64px;
    height: 64px;
    object-fit: cover;
    display: block;
    transition: transform 0.6s ease;
}

.rewardblock:hover .reward-icon {
    transform: scale(1.3);
}

.rewardblock:hover {
    border-right: 2px solid #707070;
    border-bottom: 2px solid #707070;
}

.rewardblock .day {
    left: 8px;
    top: 8px;
    position: absolute;
    font-size: 12px;
    font-weight: bold;
}

.rewardblock .amount {
    bottom: 32px;
    right: 28px;
    position: absolute;
    font-size: 16px;
    font-weight: bold;
    display: block;
}

.rewardblock .rewardName {
    bottom: 4px;
    position: absolute;
    font-size: 10px;
    font-weight: bold;
    text-align: center;
    align-items: center;
}

h2 {
    color: #e5e2b9;
    padding: 4px;
    text-shadow: rgb(80, 80, 80) 1px 1px 4px, rgb(80, 80, 80) 1px 1px 4px,
        rgb(80, 80, 80) 1px 1px 4px;
    border-radius: 10px;
    font-size: 24px;
    font-weight: bold;
}
</style>
