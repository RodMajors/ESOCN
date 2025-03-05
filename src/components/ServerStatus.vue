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
          <td class="status-online">{{ server.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Server {
  platform: string;
  region: string;
  status: string;
}

const servers = ref<Server[]>([
  { platform: 'PC', region: '美服', status: '在线' },
  { platform: 'PC', region: '欧服', status: '在线' },
  { platform: 'PC', region: 'PTS', status: '在线' },
  { platform: 'PS', region: '美服', status: '在线' },
  { platform: 'PS', region: '欧服', status: '在线' },
  { platform: 'Xbox', region: '美服', status: '在线' },
  { platform: 'Xbox', region: '欧服', status: '在线' },
]);
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

/* 调整列宽以保持对齐和美观 */
th:nth-child(1),
td:nth-child(1) {
  width: 25%; /* 平台列 */
}

th:nth-child(2),
td:nth-child(2) {
  width: 35%; /* 服务器列 */
}

th:nth-child(3),
td:nth-child(3) {
  width: 40%; /* 状态列 */
}

.status-online {
  color: #00cc00;
}
</style>