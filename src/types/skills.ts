// src/types/skills.ts
export interface skills {
    id: number;
    skill_tree_id?: number | null; // 对于变体技能有值，对于主技能可能是 null
    name: string;
    description?: string | null;
    newEffect?: string | null;
    cost?: number | null;
    duration?: number | null;
    castTime?: number | null;
    maxRange?: number | null;
    minRange?: number | null;
    radius?: number | null;
    target?: string | null;
    icon?: string;
    enName?: string | null;
    passive?: string | null; // 使用字符串，因为数据库中是 varchar(255)
    ultimate?: number | null; // 0 或 1
    isChanneled?: number | null; // 0 或 1
    magickaCost?: string;
    staminaCost?: string;
    healthCost?: string;
}

// src/types/skills.ts
export interface skill_variants {
  id: number;
  skill_id?: number | null; // 对于变体技能有值，对于主技能可能是 null
  name: string;
  description?: string | null;
  newEffect?: string | null;
  cost?: number | null;
  duration?: number | null;
  castTime?: number | null;
  maxRange?: number | null;
  minRange?: number | null;
  radius?: number | null;
  target?: string | null;
  icon?: string;
  enName?: string | null;
  passive?: string | null; // 使用字符串，因为数据库中是 varchar(255)
  ultimate?: number | null; // 0 或 1
  isChanneled?: number | null; // 0 或 1
  magickaCost?: string;
  staminaCost?: string;
  healthCost?: string;
}

export interface skill_trees{
  id: number;
  class_id: number;
  name: string ;
  enName: string | null ;
}

export interface classes{
  id: number;
  name: string ;
  enName: string | null ;
}

