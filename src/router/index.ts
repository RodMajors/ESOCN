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
        component: () => import("../views/trialsList.vue"),
    },
    {
        path: "/trials/:enName",
        component: () => import("../views/trialDetail.vue"),
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
    { path: "/buffs", component: () => import("../views/BuffsList.vue") },
    {
        path: "/buffs/:enName",
        component: () => import("../views/BuffsDetail.vue"),
    },
    {
        path: "/skills",
        component: () => import("../views/Skills.vue"),
        meta: { hideSidebar: true }, // 在此页面隐藏侧边栏
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
