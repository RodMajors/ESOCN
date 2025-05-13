export interface ChampionSkill {
    id: number;
    category_id: number;
    category_name: string;
    skill_index: number;
    name: string;
    en_name: string | null; // en_name 可能为 NULL
    description: string;
    is_slottable: boolean;
    cluster_name: string;
    bonus_text: Record<string, any>;
    is_in_cluster: boolean;
    type: number;
    max_points: number | null; // 新增，对应 max_points
    jump_points: string | null; // 新增，对应 jump_points
    num_jump_points: number | null; // 新增，对应 num_jump_points
    jump_point_delta: number | null; // 新增，对应 jump_point_delta
  }