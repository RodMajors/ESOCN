// utils/loadEquipment.ts
import equipmentData from '../data/equipment.json';

// 定义 Bonus 为索引签名类型
interface Bonus {
  [key: string]: string; // 改为索引签名
}

// 定义完整的 EquipmentSet 接口
interface EquipmentSet {
  name: string;
  enName: string;
  place: string;
  bonuses: Bonus; // 使用索引签名类型
  type: number;
  id?: string;
  itemIDs?: string[];
  styles?: any;
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