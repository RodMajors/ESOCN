<template>
    <div class="pledges">
        <h2>每日任务</h2>
        <div class="line1">
            <div class="line2">
                <DungeonImage
                    class="vendor"
                    :name="endeavor.name"
                    :enName="endeavor.enName"
                    :background="endeavor.background"
                    :link="endeavor.link"
                    :is-dual="false"
                    :type="Type"
                />
            </div>
            <div class="line2">
                <DungeonImage
                    class="vendor"
                    :name="login.name"
                    :enName="login.enName"
                    :background="login.background"
                    :link="login.link"
                    :is-dual="false"
                    :type="Type"
                />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { computed } from "vue";
import DungeonImage from "../components/DungeonImage.vue"; // 确保路径正确
const Type = "default"
export default {
    name: "DailyPledges",
    components: {
        DungeonImage, // 显式注册组件
    },
    data() {
        return {
            currentDate: "",
            Type,
            endeavor: {
                name: "勉励任务",
                enName: "Endeavors", 
                background: "/background/daily/Endeavors.jpg", 
                link: "/endeavor"
            },
            login: {
                name: "登录奖励",
                enName: "Login Reward", 
                background: "/background/daily/login.jpg", 
                link: "/login-reward"
            }
        };
    },
    mounted() {
        this.fetchDailyPledges();
    },
    methods: {
        async fetchDailyPledges() {
            try {
                const response = await fetch(
                    "http://localhost:3000/api/week-trial"
                );
                if (!response.ok) {
                    throw new Error("网络请求失败");
                }
                const result = await response.json();
                this.currentDate = result.currentDate || "";
            } catch (error) {
                console.error("获取每日誓约失败:", error);
            }
        },
    },
};
</script>

<style scoped>
.pledges {
    background-color: #121113;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}
.vendor {
    max-height: 80px;
    cursor: pointer;
}
h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    padding: 0 0 0 1rem;
}
.line1 {
    list-style: none;
    padding: 0;
}
.line2 {
    margin-top: 0.15rem;
}
</style>
