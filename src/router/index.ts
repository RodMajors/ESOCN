// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import Home from '../views/Home.vue';
import DungeonList from '../views/DungeonList.vue';
import DungeonDetail from '../views/DungeonDetail.vue';
import NewsList from '../views/NewsList.vue';
import NewsDetail from '../views/NewsDetail.vue';
import EquipmentList from '../views/EquipmentList.vue';
import EquipmentDetail from '../views/EquipmentDetail.vue';

const routes: RouteRecordRaw[] = [
  { path: '/', component: Home },
  { path: '/dungeons', component: DungeonList },
  { path: '/dungeons/:enName', component: DungeonDetail },
  { path: '/news', component: NewsList },
  { path: '/news/:id', component: NewsDetail },
  { path: '/equipment', component: EquipmentList },
  { path: '/equipment/:enName', component: EquipmentDetail },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;