<template>
    <header
        class="vendor-header"
        :style="{ backgroundImage: `url(/background/vendor/Goden_Vendor.jpg)` }"
    >
        <div class="title-overlay">
            <h1>黄金商人</h1>
            <p class="en-name">GOLDEN VENDOR</p>
        </div>
    </header>
    <body>
        <div class="content">
            <b>阿哈扎比·阿巴·达萝(Adhazabi Aba-daro)</b
            >，又称<b>“金光闪闪”</b>，旧称<b>“黄金商人”</b>，是一位出现在西罗帝尔每个联盟的边境要塞的特殊行商。
            <br /><br />
            黄金商人会在GMT标准时间周五夜晚抵达，并在GMT标准时间周一中午12点、<b>北京时间每周六下午8点</b>之前开放。
            <br /><br />
            她每周末都会提供六件PvE专用套装，其中两件是护甲，另外四件是珠宝。
            <br /><br />
            护甲全部来自怪物套装。每个周末，她会出售两件头部护甲或两件肩部护甲。每件护甲都有三种重量可选——轻型、中型和重型。
            <br /><br />
            花费<span class="ap">200,000</span
            ><img
                src="/icon/ap.png"
                class="icon"
            />购买的护甲具有<b>牢不可破</b>特性，而花费<span class="gold"
                >100,000</span
            > <img
                src="/icon/gold.png"
                class="icon"
            />购买的护甲具有<b>注魔</b>特性。 <br /><br />
            而首饰均为<span style="color: gold">金色</span
            >，CP160，其中两件来自<b>地区套装</b>，另外两件来自<b>副本套装</b>。
        </div>
        <h2>装备列表（{{ time }}）</h2>
        <div class="sets-list">
            <GearArea
                v-for="equip in equipment"
                :key="equip.enName"
                :set="equip"
            />
        </div>
    </body>
</template>

<script>
import { getEquipmentByEnName } from "@/utils/loadEquipment";
import GearArea from "@/components/GearArea.vue";
export default {
    components: {
        GearArea,
    },
    data() {
        return {
            sets: [],
            time: "",
            equipment: [],
        };
    },
    mounted() {
        this.fetchGolden();
    },
    methods: {
        async fetchGolden() {
            try {
                const response = await fetch(
                    "http://localhost:3000/api/golden-vendor"
                );
                if (!response.ok) {
                    throw new Error("网络请求失败");
                }
                const result = await response.json();
                this.sets = result.data;
                this.time = result.time;
            } catch (error) {
                console.error("获取黄金商人失败:", error);
            }
            for (let now of this.sets) {
                let equip = await getEquipmentByEnName(now.setName);
                equip.icon = now.icon;
                let newbonuses = {
                    effect1:
                        '<span class="ap">' +
                        now.ap +
                        ' </span><img src="/icon/ap.png" class="icon"> | <span class="gold">' +
                        now.gp +
                        ' </span><img src="/icon/gold.png" class="icon">',
                };
                newbonuses = Object.assign(newbonuses, equip.bonuses);
                console.log("NEWBONUSES:", newbonuses);
                equip.bonuses = newbonuses;
                this.equipment.push(equip);
                console.log(equip);
            }
        },
    },
};
</script>

<style>
.vendor-header {
    position: relative;
    height: 200px;
    background-size: cover;
    background-position: top;
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
</style>
