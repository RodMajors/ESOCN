export type SlotKey =
    | "head"
    | "shoulders"
    | "chest"
    | "hands"
    | "waist"
    | "legs"
    | "feet"
    | "ring1"
    | "ring2"
    | "neck"
    | "mainHand"
    | "offHand"
    | "backbarMainHand"
    | "backbarOffHand";

// src/types/skills.ts
export interface skills {
    id: number;
    skill_tree_id?: number | null; // 对于变体技能有值，对于主技能可能是 null
    name: string;
    description?: string | null;
    newEffect?: string | null;
    cost?: string | null;
    duration?: number | null;
    castTime?: number | null;
    maxRange?: number | null;
    minRange?: number | null;
    radius?: number | null;
    target?: string | null;
    icon?: string;
    enName?: string | null;
    passive?: number | null; // 使用字符串，因为数据库中是 varchar(255)
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
    cost?: string | null;
    duration?: number | null;
    castTime?: number | null;
    maxRange?: number | null;
    minRange?: number | null;
    radius?: number | null;
    target?: string | null;
    icon?: string;
    enName?: string | null;
    passive?: number | null; // 使用字符串，因为数据库中是 varchar(255)
    ultimate?: number | null; // 0 或 1
    isChanneled?: number | null; // 0 或 1
    magickaCost?: string;
    staminaCost?: string;
    healthCost?: string;
}

export interface skill_trees {
    id: number;
    class_id: number;
    name: string;
    enName: string | null;
}

export interface classes {
    id: number;
    name: string;
    enName: string | null;
}

export interface selectedSkill {
    skill_id?: number | null; // 对于变体技能有值，对于主技能可能是 null
    name: string;
    description?: string | null;
    newEffect?: string | null;
    cost?: string | null;
    duration?: number | null;
    castTime?: number | null;
    maxRange?: number | null;
    minRange?: number | null;
    radius?: number | null;
    target?: string | null;
    icon?: string;
    enName?: string | null;
    passive?: number | null; // 使用字符串，因为数据库中是 varchar(255)
    ultimate?: number | null; // 0 或 1
    isChanneled?: number | null; // 0 或 1
    magickaCost?: string;
    staminaCost?: string;
    healthCost?: string;
}

export interface Food {
    id: number;
    name: string;
    enName: string;
    ingredients: Record<string, number>;
    icon: string;
    itemTypeText: string;
    quality: string;
    description: string;
    canBeCrafted: number;
    specializedItemTypeText: string;
}
export interface Potion {
    id: number;
    name: string;
    enName: string;
    icon: string;
    description: string;
}

export interface MundusStone {
    id: number;
    name: string;
    enName: string;
    icon: string;
    description: string;
}

export interface ChampionSkill {
    id: number;
    name: string;
    en_name?: string;
    category_id: number;
    category_name?: string;
    is_slottable: boolean;
}

export interface Trait {
    icon: string;
    name: string;
    enName: string;
    bonuses: string;
}

export interface Enchantment {
    name: string;
    icon?: string;
    enName: string;
    effect: string;
}

export interface EquipmentSet {
    id?: number;
    name: string;
    enName?: string;
    place?: string;
    enPlace?: string;
    icon?: string;
    armor?: "轻甲" | "中甲" | "重甲" | "随机护甲类型" | "自选护甲类型" | null;
    weaponType?:
        | "Axe"
        | "Mace"
        | "Sword"
        | "BattleAxe"
        | "Maul"
        | "GreatSword"
        | "Dagger"
        | "Bow"
        | "InfernoStaff"
        | "IceStaff"
        | "LightningStaff"
        | "RestorationStaff"
        | null;
    styles?: {
        护甲?: any;
        武器?: any;
    };
    trait?: Trait | null;
    enchantment?: Enchantment | null;
    type?: string;
}

export interface selectedSet {
    id?: number;
    name: string;
    enName?: string;
    trait?: Trait | null;
    enchantment?: Enchantment | null;
    armor?: string;
}

export interface BuildData {
    basicInfo: {
        authorName: string;
        buildName: string;
        subtitle: string;
        classId: number | null;
        race: string;
        attributes: { health: number; magicka: number; stamina: number };
        playstyle: string;
        role: string;
        vampire: number;
        wolf: number;
    };
    equipment: {
        head: EquipmentSet | null;
        shoulders: EquipmentSet | null;
        chest: EquipmentSet | null;
        hands: EquipmentSet | null;
        waist: EquipmentSet | null;
        legs: EquipmentSet | null;
        feet: EquipmentSet | null;
        ring1: EquipmentSet | null;
        ring2: EquipmentSet | null;
        neck: EquipmentSet | null;
        mainHand: EquipmentSet | null;
        offHand: EquipmentSet | null;
        backbarMainHand: EquipmentSet | null;
        backbarOffHand: EquipmentSet | null;
        [key: string]: EquipmentSet | null; // <-- Add this index signature
    };
    skills: {
        mainBar: (selectedSkill)[];
        backBar: (selectedSkill)[];
    };
    cpSkills: ChampionSkill[];
    buffs: {
        food: Food | null;
        potion: Potion | null;
        mundusStone: MundusStone | null;
    };
}
