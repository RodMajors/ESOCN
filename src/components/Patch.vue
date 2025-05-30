<template>
    <div class="pledges">
        <h2>更新补丁</h2>
        <div class="line1">
            <div class="line2 dungeon-wrapper">
                <PatchImage
                    class="dungeon"
                    :enName="weeklytrials.PC.name"
                    :background="weeklytrials.PC.img"
                    :link="weeklytrials.PC.href"
                />
            </div>
            <div class="line2 dungeon-wrapper">
                <PatchImage
                    class="dungeon"
                    :enName="weeklytrials.PS.name"
                    :background="weeklytrials.PS.img"
                    :link="weeklytrials.PS.href"
                />
            </div>
            <div class="line2 dungeon-wrapper">
                <PatchImage
                    class="dungeon"
                    :enName="weeklytrials.XBOX .name"
                    :background="weeklytrials.XBOX.img"
                    :link="weeklytrials.XBOX.href"
                />
            </div>
            <div class="line2 dungeon-wrapper">
                <PatchImage
                    class="dungeon"
                    :enName="weeklytrials.PTS.name"
                    :background="weeklytrials.PTS.img"
                    :link="weeklytrials.PTS.href"
                />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import DungeonImage from "../components/DungeonImage.vue"; // 确保路径正确
import PatchImage from "../components/PatchImage.vue";
const Type = "trial"
export default {
    name: "WeeklyTrials",
    components: {
        PatchImage
    },
    data() {
        return {
            weeklytrials: {
                PC: {
                    name: "PC",
                    href: "",
                    img: ""
                }, 
                PS: {
                    name: "PS",
                    href: "",
                    img: ""
                },
                XBOX: {
                    name: "XBOX",
                    href: "",
                    img: ""
                },
                PTS: {
                    name: "PTS",
                    href: "",
                    img: ""
                } 
            },
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
                    "http://localhost:3000/api/patch-notes"
                );
                if (!response.ok) {
                    throw new Error("网络请求失败");
                }
                const result = await response.json();
                this.weeklytrials.PC = result.data.PC;
                this.weeklytrials.PC.name = "PC"
                this.weeklytrials.PS = result.data.PS;
                this.weeklytrials.PS.name = "PS"
                this.weeklytrials.XBOX = result.data.XBOX;
                this.weeklytrials.XBOX.name = "XBOX"
                this.weeklytrials.PTS = result.data.PTS;
                this.weeklytrials.PTS.name = "PTS"
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
</style>