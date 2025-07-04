import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './style.css';
import VueLazyload from 'vue-lazyload';
import tooltipDirective from './directives/tooltip';


const app = createApp(App);
app.directive('tooltip', tooltipDirective);
app.use(router);
app.use(VueLazyload, {
  preLoad: 1.3, // 预加载高度比例
  error: 'path/to/error.png', // 加载失败时的占位图
  loading: 'path/to/loading.gif', // 加载中的占位图
  attempt: 1, // 尝试加载次数
});

router.isReady().then(() => {
  app.mount('#app');
});