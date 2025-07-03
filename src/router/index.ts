import SideBar from "@/components/SideBar.vue";
import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
    { 
      path: "/", 
      component: () => import("../views/Home.vue") 
    },
    { 
      path: "/dungeons", 
      component: () => import("../views/DungeonList.vue") 
    },
    {
        path: "/dungeons/:enName",
        component: () => import("../views/DungeonDetail.vue"),
    },
    {
        path: "/trials",
        component: () => import("../views/TrialsList.vue"),
    },
    {
        path: "/trials/:enName",
        component: () => import("../views/TrialDetail.vue"),
    },
    {
        path: "/news",
        component: () => import("../views/NewsList.vue"),
    },
    {
        path: "/news/:id",
        component: () => import("../views/NewsDetail.vue"),
    },
    {
        path: "/equipment",
        component: () => import("../views/EquipmentList.vue"),
    },
    {
        path: "/equipment/:enName",
        component: () => import("../views/EquipmentDetail.vue"),
    },
    { 
        path: "/buffs", 
        component: () => import("../views/BuffsList.vue") 
    },
    {
        path: "/buffs/:enName",
        component: () => import("../views/BuffsDetail.vue"),
        
    },
    { 
        path: "/foods", 
        component: () => import("../views/Foods.vue") 
    },
    { 
        path: "/foods/:enName", 
        component: () => import("../views/FoodsDetail.vue") 
    },
    {
        path: "/skills",
        component: () => import("../views/Skills.vue"),
        meta: { 
            hideSidebar: true 
        },
    },
    {
        path: "/champions",
        component: () => import("../views/champions.vue"),
        meta: { 
            hideSidebar: true
        }
    },
    {
        path: "/champions/:enName",
        component: () => import("../views/CPDetail.vue"),
        meta: { 
            hideSidebar: false
        }
    },
    {
        path: "/golden-vendor",
        component: () => import("../views/Vendors/GoldenVendor.vue"),
        meta: { 
            hideSidebar: false
        }
    },
    {
        path: "/infinite-archieve-vendor",
        component: () => import("../views/Vendors/Archieve.vue"),
        meta: { 
            hideSidebar: false
        }
    },
    {
        path: "/telvar-vendor",
        component: () => import("../views/Vendors/TelVar.vue"),
        meta: { 
            hideSidebar: false
        }
    },
    {
        path: "/luxury-furnisher",
        component: () => import("../views/Vendors/Furnisher.vue"),
        meta: { 
            hideSidebar: false
        }
    },
    {
        path: "/endeavors",
        component: () => import("../views/Daily/Endeavor.vue"),
        meta: { 
            hideSidebar: false
        }
    },
    {
        path: "/login-reward",
        component: () => import("../views/Daily/LoginReward.vue"),
        meta: { 
            hideSidebar: false
        }
    },
    {
        path: "/build-editor",
        component: () => import("../views/BuildEditor.vue"),
        meta: { 
            hideSidebar: false
        }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
