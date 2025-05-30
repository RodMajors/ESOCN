// src/directives/tooltip.ts
// src/directives/tooltip.ts
import type { Directive } from 'vue';

const tooltipDirective: Directive = {
  mounted(el: HTMLElement, binding) {
    // 创建 tooltip 元素
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.innerHTML = binding.value || ''; // 使用 innerHTML 支持 parseColorTags 渲染
    tooltip.style.position = 'absolute';
    tooltip.style.backgroundColor = '#000000';
    tooltip.style.color = '#c5c29e';
    tooltip.style.border = 'solid';
    tooltip.style.borderColor = '#444';
    tooltip.style.borderWidth = '1px';
    tooltip.style.padding = '0.5rem';
    tooltip.style.borderRadius = '4px';
    tooltip.style.zIndex = '1000';
    tooltip.style.display = 'none';
    document.body.appendChild(tooltip);

    // 鼠标进入时显示 tooltip
    el.addEventListener('mouseenter', (e: MouseEvent) => {
      tooltip.style.display = 'block';
      // 定位 tooltip 在鼠标附近
      tooltip.style.left = `${e.pageX + 10}px`;
      tooltip.style.top = `${e.pageY + 10}px`;
    });

    // 鼠标离开时隐藏 tooltip
    el.addEventListener('mouseleave', () => {
      tooltip.style.display = 'none';
    });

    // 存储 tooltip 元素以便销毁
    el.dataset.tooltip = tooltip.outerHTML;
  },
  unmounted(el: HTMLElement) {
    // 清理 tooltip 元素
    const tooltip = document.querySelector('.custom-tooltip');
    if (tooltip) {
      tooltip.remove();
    }
  },
};

export default tooltipDirective;