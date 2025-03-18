<template>
  <div class="server-status">
    <h2>服务器状态</h2>
    <table>
      <thead>
        <tr>
          <th>平台</th>
          <th>服务器</th>
          <th>状态</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="server in servers" :key="server.platform + server.region">
          <td>{{ server.platform }}</td>
          <td>{{ server.region }}</td>
          <td :class="server.status === 'Online' ? 'status-online' : 'status-offline'">
            {{ server.status }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

interface Server {
  platform: string;
  region: string;
  status: string;
}

// 默认显示绿色 "Online"
const servers = ref<Server[]>([
  { platform: 'PC', region: '欧服', status: 'Online' },
  { platform: 'PC', region: '美服', status: 'Online' },
  { platform: 'PC', region: 'PTS', status: 'Online' },
  { platform: 'Xbox', region: '欧服', status: 'Online' },
  { platform: 'Xbox', region: '美服', status: 'Online' },
  { platform: 'PS', region: '欧服', status: 'Online' },
  { platform: 'PS', region: '美服', status: 'Online' },
]);

// 从 API 获取服务器状态并覆盖默认值
const fetchServerStatus = async () => {
  try {
    const response = await fetch('http://localhost:3000/api/server-status');
    if (!response.ok) {
      throw new Error('网络请求失败');
    }
    const data = await response.json();
    const status = data.status;

    // 映射后端返回的字典到前端数组
    servers.value = [
      { platform: 'PC', region: '欧服', status: status.PCEU },
      { platform: 'PC', region: '美服', status: status.PCNA },
      { platform: 'PC', region: 'PTS', status: status.PCPTS },
      { platform: 'Xbox', region: '欧服', status: status.XBOXEU },
      { platform: 'Xbox', region: '美服', status: status.XBOXNA },
      { platform: 'PS', region: '欧服', status: status.PSEU },
      { platform: 'PS', region: '美服', status: status.PSNA },
    ];
  } catch (error) {
    console.error('获取服务器状态失败:', error);
    // 如果失败，保持默认的 "Online" 不变
  }
};

// 组件挂载时获取数据
onMounted(fetchServerStatus);
</script>

<style scoped>
.server-status {
  color: #C5C29E;
  background-color: #101010;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

h2 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 0.5rem;
  text-align: left;
}

th {
  background-color: #3a3a3a;
}

td {
  border-bottom: 1px solid #444;
}

th:nth-child(1),
td:nth-child(1) {
  width: 25%;
}

th:nth-child(2),
td:nth-child(2) {
  width: 35%;
}

th:nth-child(3),
td:nth-child(3) {
  width: 40%;
}

.status-online {
  color: #00cc00; /* 绿色 */
}

.status-offline {
  color: #ff0000; /* 红色 */
}
</style>