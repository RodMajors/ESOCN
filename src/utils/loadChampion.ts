import axios from 'axios';

export interface ChampionSkill {
  id: number;
  category_id: number;
  category_name: string;
  skill_index: number;
  name: string;
  en_name: string; // en_name 可能为 NULL
  description: string;
  is_slottable: number;
  cluster_name: string;
  bonus_text: Record<string, any>;
  is_in_cluster: boolean;
  type: number;
  max_points: number | null; // 新增，对应 max_points
  jump_points: string | null; // 新增，对应 jump_points
  num_jump_points: number | null; // 新增，对应 num_jump_points
  jump_point_delta: number | null; // 新增，对应 jump_point_delta
}

export async function loadChampion(categoryId: number): Promise<ChampionSkill[]> {
  try {
    const response = await axios.get(`http://localhost:3000/api/cp/${categoryId}`);
    return response.data as ChampionSkill[];
  } catch (error) {
    console.error(`无法获取分类 ${categoryId} 的技能数据:`, error);
    return [];
  }
}

export async function loadSkillByEnName(enName: string): Promise<ChampionSkill | null> {
  try {
    const response = await axios.get(`http://localhost:3000/api/cp/${encodeURIComponent(enName)}`);
    return response.data as ChampionSkill;
  } catch (error) {
    console.error(`无法获取技能 ${enName} 的数据:`, error);
    return null;
  }
}