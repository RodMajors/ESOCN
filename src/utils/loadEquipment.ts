// utils/loadEquipment.ts
import equipmentData from '../data/equipment.json';

// 定义 Bonus 为索引签名类型
interface Bonus {
  [key: string]: string;
}

// 定义 Styles 的具体结构
interface Styles {
  武器?: { [key: string]: any };
  护甲?: { [key: string]: any };
}

// 定义完整的 EquipmentSet 接口
interface EquipmentSet {
  name: string;
  enName: string;
  place: string;
  bonuses: Bonus;
  type: number;
  id?: string;
  itemIDs?: string[];
  styles?: Styles; // 使用具体类型替代 any
}

// 定义 JSON 文件的结构
interface EquipmentData {
  timestamp: number;
  sets: EquipmentSet[];
}

// 显式类型断言，确保 equipmentData 符合预期结构
const typedEquipmentData = equipmentData as EquipmentData;

export function loadEquipment(): EquipmentSet[] {
  return typedEquipmentData.sets;
}