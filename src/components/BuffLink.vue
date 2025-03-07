<!-- BuffLink.vue -->
<template>
    <template v-for="(segment, index) in segments" :key="index">
      <RouterLink
        v-if="segment.isBuff"
        :to="segment.to"
        style="color: #FDFF00"
        class="buff-link"
      >
        {{ segment.text }}
      </RouterLink>
      <span v-else>{{ segment.text }}</span>
    </template>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  interface Buff {
    name: string;
    enName: string;
  }
  
  export default defineComponent({
    props: {
      text: { type: String, required: true },
      buffs: { type: Array as () => Buff[], required: true },
    },
    computed: {
      segments(): { text: string; isBuff: boolean; to?: string }[] {
        let remainingText = this.text;
        const segments: { text: string; isBuff: boolean; to?: string }[] = [];
        const buffMap = new Map(this.buffs.map(buff => [buff.name, buff.enName]));
  
        while (remainingText.length > 0) {
          let matched = false;
          for (const [name, enName] of buffMap) {
            if (remainingText.startsWith(name)) {
              segments.push({
                text: name,
                isBuff: true,
                to: `/buffs/${enName.replace(" ", "-")}`,
              });
              remainingText = remainingText.slice(name.length);
              matched = true;
              break;
            }
          }
          if (!matched) {
            const nextMatch = [...buffMap.keys()].reduce((earliest, name) => {
              const index = remainingText.indexOf(name);
              if (index !== -1 && (earliest.index === -1 || index < earliest.index)) {
                return { index, name };
              }
              return earliest;
            }, { index: -1, name: "" });
  
            if (nextMatch.index === -1) {
              segments.push({ text: remainingText, isBuff: false });
              remainingText = "";
            } else {
              segments.push({
                text: remainingText.slice(0, nextMatch.index),
                isBuff: false,
              });
              remainingText = remainingText.slice(nextMatch.index);
            }
          }
        }
        return segments;
      },
    },
  });
  </script>
  
  <style>
  .buff-link {
    text-decoration: underline; /* 可选：增加链接感 */
  }
  .buff-link:hover {
    color: #ffeb3b; /* 可选：hover 效果 */
  }
  </style>