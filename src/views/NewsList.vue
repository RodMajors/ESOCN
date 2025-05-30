<template>
  <div class="news-page">
    <!-- 顶部最新新闻 -->
    <div v-if="latestNews" class="hero-section">
      <img
        :src="latestNews.cover"
        alt="Latest News Cover"
        class="hero-image"
        @error="handleImageError"
      />
      <h1 class="hero-title">{{ latestNews.name }}</h1>
      <p class="hero-description">{{ latestNews.des }}</p>
    </div>

    <!-- 新闻列表 -->
    <div class="news-list">
      <div v-for="news in displayedNews" :key="news.id" class="news-item">
        <router-link :to="`/news/${news.id}`" class="news-image">
          <img
            :src="news.cover"
            :alt="news.name"
            loading="lazy"
            @error="handleImageError"
          />
        </router-link>
        <div class="news-content">
          <router-link :to="`/news/${news.id}`" class="news-title">
            <h3>{{ news.name }}</h3>
          </router-link>
          <p class="news-description">{{ news.des }}</p>
          <p class="news-date">{{ news.date }}</p>
        </div>
      </div>
    </div>

    <!-- 查看更多按钮 -->
    <div v-if="hasMoreNews" class="more-button">
      <button @click="loadMore">查看更多</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { NewsItem } from '@/types/news';

const newsList = ref<NewsItem[]>([]);
const latestNews = ref<NewsItem | null>(null);
const itemsPerPage = 10;
const currentPage = ref(1);

// 计算显示的新闻列表（分页）
const displayedNews = computed(() => {
  return newsList.value.slice(0, currentPage.value * itemsPerPage);
});

// 是否有更多新闻可加载
const hasMoreNews = computed(() => {
  return currentPage.value * itemsPerPage < newsList.value.length;
});

// 加载更多新闻
const loadMore = () => {
  currentPage.value += 1;
};

// 处理图片加载失败
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement;
  img.src = 'https://via.placeholder.com/200x150'; // 备用图片
};

onMounted(async () => {
  try {
    const cached = localStorage.getItem('newsList');
    if (cached) {
      newsList.value = JSON.parse(cached);
      latestNews.value = newsList.value[0] || null;
    }
    const response = await fetch('/api/news');
    if (!response.ok) throw new Error('Failed to fetch news');
    const data = await response.json();
    newsList.value = data;
    latestNews.value = data[0] || null;
    localStorage.setItem('newsList', JSON.stringify(data));
  } catch (error) {
    console.error('Error fetching news:', error);
  }
});
</script>

<style scoped>
.news-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 顶部最新新闻 */
.hero-section {
  margin-bottom: 40px;
  margin: 0 auto;
  max-width: 800px;
  text-align: center;
  margin-bottom: 5rem;
}

.hero-image {
  width: 100%;
  max-width: 800px;
  border: 2px solid #444;
  transition: border-color 0.5s ease;
  cursor: pointer;
  text-align: center;
}

.hero-image:hover {
  border-color: #ffffff;
}

.hero-title {
  font-size: 60px;
  font-weight: bold;
  color: #ccb475;
  margin: 20px 0 10px;
  text-shadow: rgb(0, 0, 0) 0px 0px 1px, rgb(0, 0, 0) 0px 1px 1px, rgb(0, 0, 0) 0px 1px 10p;
}

.hero-title:hover {
  color: #F1C33C;
  cursor: pointer;
}
.hero-description {
  font-size: 20px;
  color: #c9c8c4;
  margin: 0;
}

/* 新闻列表 */
.news-list {
  display: grid;
  gap: 20px;
}

.news-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  transition: color 0.3s ease;
}

.news-item:hover .news-title h3,
.news-item:hover .news-description,
.news-item:hover .news-date {
  color: #ffffff;
}

.news-image {
  flex: 0 0 400px; /* 图片占更多空间 */
  text-decoration: none;
}

.news-image img {
  width: 100%;
  height: auto; /* 仅缩放，不裁剪 */
  border: 2px solid #444;
  transition: border-color 0.5s ease;
  cursor: pointer;
}

.news-image img:hover {
  border-color: #ffffff;
}

.news-content {
  flex: 1;
}

.news-title {
  text-decoration: none;
}

.news-title h3 {
  font-size: 28px;
  font-weight: bold;
  color: #ccb475;
  margin: 0 0 10px;
}

.news-description {
  font-size: 16px;
  color: #c9c8c4;
  margin: 0 0 5px;
}

.news-date {
  font-size: 12px;
  color: #c9c8c4;
  margin: 0;
}

/* 查看更多按钮 */
.more-button {
  text-align: center;
  margin-top: 20px;
}

.more-button button {
  width: 150px;
  padding: 10px 20px 10px 20px;
  font-size: 20px;
  background-color: #121113;
  color: #948159; 
  border: #948159 solid 2px;
  cursor: pointer;
  transition: color 0.2s ease;
  transition: border 0.2s ease;
}

.more-button button:hover {
  background-color: #000000;
  color: #ffffff;
  border: #ffffff solid 2px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-image {
    height: 300px;
  }

  .hero-title {
    font-size: 40px;
  }

  .hero-description {
    font-size: 16px;
  }

  .news-item {
    flex-direction: column;
  }

  .news-image {
    flex: 0 0 auto;
  }

  .news-image img {
    max-height: 200px;
  }
}
</style>