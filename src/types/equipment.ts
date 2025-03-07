export interface EquipmentSet {
    name: string;
    enName: string;
    place: string;
    icon: string;
    bonuses: { 
      [key: string]: string 
    };
    type: number;
    styles?: Array<string> | { 
      武器?: { [key: string]: any }; 
      护甲?: { [key: string]: any } 
    };
    enplace?: string; // 可选属性，兼容 GearArea
    style?: any;      // 可选属性，兼容 GearArea
    armor?: any;      // 可选属性，兼容 GearArea
  }