// src/types/dungeon.ts
export interface Dungeon {
  name: string;
  enName: string;
  place: string[]; // 中文地点
  enplace: string[]; // 英文地点
  DLC: string; // DLC 名称
  DLCicon: string; // DLC 图标 URL
  location: string; // 具体位置
  mini_level?: string; // 最低等级
  Group_Size: string; // 组队人数
  Bosses: string; // BOSS 数量
  mini_Bosses: string; // 小型 BOSS 数量
  background: string; // 背景图片 URL
  picture: string; // 地点图片 URL
  mystery: string; // 神秘描述
  des: string; // 详细描述
  BOSS: Boss[]; // BOSS 列表
  equipment: string[]; // 装备套装
  achievement: Achievement[]; // 成就列表
  drop: string[]; // 掉落（当前为空）
  mech: string[]; // 机制（当前为空）
}

export interface Boss {
  name: string | null;
  enName: string;
  species: string; // 物种
  place: string; // 地点
  'n-Health': string; // 普通模式生命值
  'v-Health': string; // 老兵模式生命值
  hmHealth: string; // 困难模式生命值
  des: string; // 描述
  picture: string; // 图片 URL
  skills: Skill[]; // 技能列表
}

export interface Skill {
  name: string | null;
  enName: string;
  icon: string; // 技能图标 URL
  des: string; // 技能描述
}

export interface Achievement {
  name: string;
  enName: string;
  icon: string; // 成就图标 URL
  des: string; // 成就描述
  score: string; // 成就分数
}

// 双重地下城的分支结构（保持不变）
export interface DualDungeon {
  name: string;
  enName: string;
  originalEnName: string;
}

// 处理后的地下城结构（保持不变）
export interface ProcessedDungeon extends Omit<Dungeon, 'DLC' | 'DLCicon'> {
  isDual: boolean;
  dualDungeons: DualDungeon[];
  DLC: string;
  DLCicon: string;
}

// DLC 分组结构（保持不变）
export interface DlcGroup {
  icon: string; // DLCicon
  dungeons: ProcessedDungeon[];
}