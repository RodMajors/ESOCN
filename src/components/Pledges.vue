<template>
  <div class="pledges">
    <h2>无畏者日常</h2>
    <ul v-if="dailyPledges.length > 0">
      <li v-for="(pledge, index) in dailyPledges" :key="index">
        <DungeonImage class="dungeon" :en-name="pledge" :is-dual="false" />
      </li>
    </ul>
    <p v-else>加载中...</p>
  </div>
</template>

<script lang="ts">
import DungeonImage from '../components/DungeonImage.vue'; // 确保路径正确

export default {
  name: 'DailyPledges',
  components: {
    DungeonImage // 显式注册组件
  },
  data() {
    return {
      dailyPledges: [],
      currentDate: ''
    };
  },
  mounted() {
    this.fetchDailyPledges();
  },
  methods: {
    async fetchDailyPledges() {
      try {
        const response = await fetch('http://localhost:3000/api/daily-pledges');
        if (!response.ok) {
          throw new Error('网络请求失败');
        }
        const result = await response.json();
        this.dailyPledges = result.dailyPledges || [];
        this.currentDate = result.currentDate || '';
      } catch (error) {
        console.error('获取每日誓约失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.pledges {
  background-color: #101010;
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
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-top: 0.15rem;
}
</style>