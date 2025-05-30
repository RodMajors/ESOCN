<template>
    <div class="pledges">
        <h2>周常试炼</h2>
        <div class="line1">
            <div class="line2 dungeon-wrapper">
                <DungeonImage
                    class="dungeon"
                    :en-name="weeklytrials.PCNA"
                    :is-dual="false"
                    :type="Type"
                />
                <div class="label">PC NA</div>
            </div>
            <div class="line2 dungeon-wrapper">
                <DungeonImage
                    class="dungeon"
                    :en-name="weeklytrials.PCEU"
                    :is-dual="false"
                    :type="Type"
                />
                <div class="label">PC EU</div>
            </div>
            
        </div>
    </div>
</template>

<script lang="ts">
import DungeonImage from "../components/DungeonImage.vue"; // 确保路径正确
const Type = "trial"
export default {
    name: "WeeklyTrials",
    components: {
        DungeonImage, // 显式注册组件
    },
    data() {
        return {
            weeklytrials: { PCNA: "", PCEU: "" },
            currentDate: "",
            Type
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
                this.weeklytrials.PCNA = result.status.PCNA.replace(/&#039;/g, "'");
                this.weeklytrials.PCEU = result.status.PCEU.replace(/&#039;/g, "'");
                this.currentDate = result.currentDate || "";
            } catch (error) {
                console.error("获取周常试炼失败:", error);
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
    max-height: 305px;
}
.dungeon {
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

/* 新增样式 */
.dungeon-wrapper {
    position: relative; /* 使子元素定位相对于此容器 */
    display: flex;
    align-items: center;
}

.label {
    position: absolute;
    top: 0; /* 左上角 */
    left: 0;
    background-color: #4caf50; /* 绿色不透明背景 */
    color: #ffffff; /* 白色文字 */
    font-size: 0.9rem; /* 文字大小，适合小标签 */
    font-weight: 600; /* 稍粗的字体 */
    padding: 4px 8px; /* 内边距，控制长方形大小 */
    text-shadow: 
        1px 1px 2px rgba(0, 0, 0, 0.5), 
        -1px -1px 2px rgba(0, 0, 0, 0.5); /* 文字阴影 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); /* 标签本身的阴影，提升立体感 */
    border-radius: 0 0 4px 0; /* 右下角圆角，增加设计感 */
    z-index: 10; /* 确保标签在图片之上 */
    pointer-events: none; /* 防止标签干扰点击事件 */
}
</style>