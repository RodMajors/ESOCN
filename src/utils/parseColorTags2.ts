import buffs from '@/Data/buffs.json';
import { RouterLink } from 'vue-router';


export function parseColorTags2(text: string): string {
  // 忽略掉 \r \n
  text = text.replace(/\\r\\n/g, '<br>')

  // 先处理 |cFFFFFF25|r 形式的标记，还原为原始内容
  let formattedText = text.replace(/\|c([0-9a-fA-F]{6})(.*?)\|r/g, (_, __, content) => {
    return content; // 只保留内容，丢弃颜色标记
  });

  // 处理件套字段，将其颜色设置为 #ccc
  const setEffectRegex = /（(\d+)件(完美)?套）/g;
  formattedText = formattedText.replace(setEffectRegex, (match) => {
    return `<span style="color: #ccc;">${match}</span>`;
  });

  //替换BUFF和deBUFF
  let BUFFS = buffs.buffs;  
  for (var i = 0 ; i < BUFFS.length ; i ++){
    formattedText = formattedText.replace(BUFFS[i].name, `<span data-to="/buffs/${BUFFS[i].enName.replace(' ', '-')}" style = "color: #FDFF00" class = "link">${BUFFS[i].name}</span>`);
  }
  BUFFS = buffs.debuffs;  
  for (var i = 0 ; i < BUFFS.length ; i ++){
    formattedText = formattedText.replace(BUFFS[i].name, `<span data-to="/buffs/${BUFFS[i].enName.replace(' ', '-')}" style = "color: #FDFF00" class = "link">${BUFFS[i].name}</span>`);
  }

  // 定义关键字和样式
  let keywords = ['魔力恢复', '魔力回复', '魔力上限', '魔力'];
  let color = '#0077cc'; // 深蓝色

  // 遍历关键字并替换为带样式的 HTML 标签
  keywords.forEach((keyword) => {
    const regexWithNumber = new RegExp(`([-+]?\\d*\\.?\\d+)\\s*${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithNumber, `<span style="color: ${color};">$1 ${keyword}</span>`);
    const regexWithoutNumber = new RegExp(`(?<![-+]?\\d*\\.?\\d+\\s*)${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithoutNumber, `<span style="color: ${color};">${keyword}</span>`);
  });

  keywords = ['耐力恢复', '耐力回复', '耐力上限', '耐力'];
  color = '#009000'; // 深绿色

  keywords.forEach((keyword) => {
    const regexWithNumber = new RegExp(`([-+]?\\d*\\.?\\d+)\\s*${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithNumber, `<span style="color: ${color};">$1 ${keyword}</span>`);
    const regexWithoutNumber = new RegExp(`(?<![-+]?\\d*\\.?\\d+\\s*)${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithoutNumber, `<span style="color: ${color};">${keyword}</span>`);
  });

  keywords = ['生命恢复', '生命回复', '生命上限', '生命', '治疗'];
  color = '#FF6666'; // 红色

  keywords.forEach((keyword) => {
    const regexWithNumber = new RegExp(`([-+]?\\d*\\.?\\d+)\\s*${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithNumber, `<span style="color: ${color};">$1 ${keyword}</span>`);
    const regexWithoutNumber = new RegExp(`(?<![-+]?\\d*\\.?\\d+\\s*)${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithoutNumber, `<span style="color: ${color};">${keyword}</span>`);
  });

  // “武器伤害”规则，颜色 #CC6600（橙色）
  keywords = ['武器伤害'];
  color = '#AD4E0F';

  keywords.forEach((keyword) => {
    const regexWithNumber = new RegExp(`([-+]?\\d*\\.?\\d+)\\s*${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithNumber, `<span style="color: ${color};">$1 ${keyword}</span>`);
    const regexWithoutNumber = new RegExp(`(?<![-+]?\\d*\\.?\\d+\\s*)${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithoutNumber, `<span style="color: ${color};">${keyword}</span>`);
  });

  // “法术伤害”规则，颜色 #990099（紫色）
  keywords = ['法术伤害'];
  color = '#9856FF';

  keywords.forEach((keyword) => {
    const regexWithNumber = new RegExp(`([-+]?\\d*\\.?\\d+)\\s*${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithNumber, `<span style="color: ${color};">$1 ${keyword}</span>`);
    const regexWithoutNumber = new RegExp(`(?<![-+]?\\d*\\.?\\d+\\s*)${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithoutNumber, `<span style="color: ${color};">${keyword}</span>`);
  });

  // keywords = ['暴击率', '暴击伤害', '暴击抗性'];
  // color = '#B39611';

  // keywords.forEach((keyword) => {
  //   const regexWithNumber = new RegExp(`([-+]?\\d*\\.?\\d+)\\s*${keyword}`, 'g');
  //   formattedText = formattedText.replace(regexWithNumber, `<span style="color: ${color};">$1 ${keyword}</span>`);
  //   const regexWithoutNumber = new RegExp(`(?<![-+]?\\d*\\.?\\d+\\s*)${keyword}`, 'g');
  //   formattedText = formattedText.replace(regexWithoutNumber, `<span style="color: ${color};">${keyword}</span>`);
  // });

  keywords = ['护甲'];
  color = '#DDD';

  keywords.forEach((keyword) => {
    const regexWithNumber = new RegExp(`([-+]?\\d*\\.?\\d+)\\s*${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithNumber, `<span style="color: ${color};">$1 ${keyword}</span>`);
    const regexWithoutNumber = new RegExp(`(?<![-+]?\\d*\\.?\\d+\\s*)${keyword}`, 'g');
    formattedText = formattedText.replace(regexWithoutNumber, `<span style="color: ${color};">${keyword}</span>`);
  });
  return formattedText;
}
