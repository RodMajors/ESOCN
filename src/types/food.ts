export interface food {
    id: number;
    name: string;
    enName: string;
    place: string;
    icon: string;
    itemTypeText: number;
    ingredients: { [key: string]: number };
    quality: string;
    description: string;
    canBeCrafted: number;
    specializedItemTypeText: string;
}
