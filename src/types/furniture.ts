export interface Furniture {
    id: string;
    name: string;
    enName: string;
    icon: string;
    type: string;
    quality: string;
    ingredients: { [key: string]: number };
    skills: { [key: string]: number };
    category: string;
    subCategory: string;
    description: string;
    cost?: number; // 可选，因为不是所有家具都有 cost
}