<template>
    <div class="pledges">
        <h2>每周商人</h2>
        <div class="line1">
            <div class="line2">
                <DungeonImage
                    class="vendor"
                    :name="golden.name"
                    :enName="golden.enName"
                    :background="golden.background"
                    :link="golden.link"
                    :is-dual="false"
                    :type="Type"
                />
            </div>
            <div class="line2">
                <DungeonImage
                    class="vendor"
                    :name="archieve.name"
                    :enName="archieve.enName"
                    :background="archieve.background"
                    :link="archieve.link"
                    :is-dual="false"
                    :type="Type"
                />
            </div>
            <div class="line2">
                <DungeonImage
                    class="vendor"
                    :name="telvar.name"
                    :enName="telvar.enName"
                    :background="telvar.background"
                    :link="telvar.link"
                    :is-dual="false"
                    :type="Type"
                />
            </div>
            <div class="line2">
                <DungeonImage
                    class="vendor"
                    :name="furnisher.name"
                    :enName="furnisher.enName"
                    :background="furnisher.background"
                    :link="furnisher.link"
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
            golden: {
                name: "黄金商人",
                enName: "Golden Vendor", 
                background: "/background/vendor/Goden_Vendor.jpg", 
                link: "/golden-vendor"
            },
            archieve: {
                name: "档案塔商人",
                enName: "Infinite Archieve Vendor", 
                background: "/background/vendor/Infinite_Archive.png", 
                link: "/infinite-archieve-vendor"
            },
            telvar: {
                name: "泰尔瓦石商人",
                enName: "TelVar Vendor", 
                background: "/background/vendor/TelVar.jpg", 
                link: "/telvar-vendor"
            },
            furnisher: {
                name: "豪华家具商",
                enName: "Luxury Funisher", 
                background: "/background/vendor/Furnisher.jpg", 
                link: "/luxury-furnisher"
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
    background-color: #101010;
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
