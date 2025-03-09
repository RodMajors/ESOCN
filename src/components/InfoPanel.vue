<!-- src/components/InfoPanel.vue -->
<template>
    <div class="info-panel-wrapper">
      <table class="info-panel">
        <tr class="header-row">
          <td colspan="2">
            <div class="img-class">
                <img :src="icon" alt="Icon" class="panel-icon" />
                <span class="panel-class">{{ className }}</span>
            </div>
            <div class="name-wrapper">
              <div>{{ dungeon.name }}</div>
              <div>{{ dungeon.enName }}</div>
            </div>
          </td>
        </tr>
        <tr class="key-row">
          <td colspan="2">地区</td>
        </tr>
        <tr class="value-row">
          <td colspan="2">{{ dungeon.place.join('，') }}</td>
        </tr>
        <tr class="key-row">
          <td colspan="2">地点</td>
        </tr>
        <tr class="value-row">
          <td colspan="2">{{ dungeon.location }}</td>
        </tr>
        <tr>
          <td class="key-cell">DLC</td>
          <td class="value-cell">
            <img :src="dungeon.DLCicon" alt="DLC Icon" class="dlc-icon" />
            {{ dungeon.DLC }}
          </td>
        </tr>
        <tr>
          <td class="key-cell">所需等级</td>
          <td class="value-cell">{{ dungeon.mini_level }}</td>
        </tr>
        <tr>
          <td class="key-cell">最大人数</td>
          <td class="value-cell">{{ dungeon.Group_Size }}</td>
        </tr>
        <tr>
          <td class="key-cell">BOSS 数</td>
          <td class="value-cell">{{ dungeon.Bosses }}</td>
        </tr>
        <tr>
          <td class="key-cell">Mini BOSS 数</td>
          <td class="value-cell">{{ dungeon.mini_Bosses }}</td>
        </tr>
        <tr class="mystery-row">
          <td colspan="2">{{ dungeon.mystery }}</td>
        </tr>
      </table>
    </div>
  </template>
  
  <script setup lang="ts">
  import type { Dungeon } from '../types/dungeon';
  
  defineProps<{
    dungeon: Dungeon;
    icon: string;
    className: string;
  }>();
  </script>
  
  <style scoped>
  tr {
    border-bottom: 0.5px solid #444;
  }
  .info-panel-wrapper {
    width: 350px;
    background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
    border: 2px solid transparent;
    border-image: linear-gradient(to bottom right, #806F4d, #d4af37) 1;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    margin: 0;
    padding: 0;
  }
  
  .info-panel {
    width: 100%;
    border-collapse: collapse;
    font-size: 1rem;
  }
  
  .header-row td {
    background-color: #000000;
    padding: 1rem;
    text-align: center;
    position: relative;
  }
  
  .panel-icon {
    width: 24px;
    height: 24px;
    position: absolute;
    top: 0.5rem;
    left: 0.5rem;
  }
  
  .panel-class {
    position:absolute;
    top: 0.5rem;
    left: 3rem;
    font-size: 0.9rem;
    color: #ccc;
  }
  
  .name-wrapper {
    margin-top: 0.5rem;
    text-shadow: rgb(80, 80, 80) 1px 1px 3px, rgb(80, 80, 80) 1px 2px 3px, rgb(80, 80, 80) 1px 3px 3px;
  }
  
  .key-row td {
    background-color: #000000;
    padding: 0.5rem;
    text-align: center;
  }
  
  .value-row td {
    background-color: #101010;
    padding: 0.5rem;
    text-align: center;
  }
  
  .key-cell {
    background-color: #000000;
    padding: 0.5rem;
    text-align: center;
    width: 40%;
    border-right: 0.5px solid #444;
  }
  
  .value-cell {
    background-color: #101010;
    padding: 0.5rem;
    text-align: center;
  }
  
  .dlc-icon {
    width: 20px;
    height: 20px;
    vertical-align: middle;
    margin-right: 0.5rem;
  }
  
  .mystery-row td {
    background-color: #101010;
    padding: 1rem;
    font-size: .88rem;
    text-align: center;
  }
  .img-class{
    display: flex;
    justify-content: space-between;
  }
  </style>