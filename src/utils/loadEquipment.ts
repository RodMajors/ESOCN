// utils/loadEquipment.ts
import { parseColorTags } from './parseColorTags';
import { parseColorTags2 } from './parseColorTags2';

export async function loadEquipmentDetail(id: number): Promise<any> {
  const response = await fetch(`/api/equipment/${id}`);
  if (!response.ok) throw new Error('Failed to fetch equipment detail');
  const data = await response.json();
  return {
    ...data,
    bonuses: parseBonuses(data.bonuses), // 解析 bonuses
  };
}

//根据英文名找套装
export async function getEquipmentByEnName(enName: string): Promise<any> {
  enName = decodeURIComponent(enName).replace(/\s+/g, '%20');
  const response = await fetch(`/api/equipment/${enName}`);
  if (!response.ok) throw new Error('Failed to fetch equipment detail');
  const data = await response.json();
  return {
    ...data,
    bonuses: parseBonuses2(data.bonuses), // 解析 bonuses
  };
}

export async function getEquipmentByEnName0(enName: string): Promise<any> {
  enName = decodeURIComponent(enName).replace(/\s+/g, '%20');
  const response = await fetch(`/api/equipment/${enName}`);
  if (!response.ok) throw new Error('Failed to fetch equipment detail');
  const data = await response.json();
  return {
    ...data,
    bonuses: parseBonuses(data.bonuses), // 解析 bonuses
  };
}

// 解析 bonuses
const parseBonuses = (bonuses: { [key: string]: string }): { [key: string]: string } => {
  const parsedBonuses: { [key: string]: string } = {};
  for (const [key, value] of Object.entries(bonuses)) {
    parsedBonuses[key] = parseColorTags(value); // 使用 parseColorTags 解析颜色
  }
  return parsedBonuses;
};

const parseBonuses2 = (bonuses: { [key: string]: string }): { [key: string]: string } => {
  const parsedBonuses: { [key: string]: string } = {};
  for (const [key, value] of Object.entries(bonuses)) {
    parsedBonuses[key] = parseColorTags2(value); // 使用 parseColorTags 解析颜色
  }
  return parsedBonuses;
};

export async function loadAllEquipment(): Promise<any[]> {
  try {
    console.log(`Fetching /api/equipment/all`);
    const response = await fetch('/api/equipment/all');
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API response:', data);

    // 为每个装备加载 bonuses
    const equipmentWithBonuses = await Promise.all(
      data.map(async (set: any) => {
        const details = await getEquipmentByEnName0(set.enName);
        return {
          ...set,
          bonuses: details.bonuses, // 合并 bonuses
        };
      })
    );

    return equipmentWithBonuses;
  } catch (error) {
    console.error('Error loading equipment:', error);
    return [];
  }
}

// loadEquipment.ts
// utils/loadEquipment.ts
export async function loadRelatedEquipment(place: string): Promise<any[]> {
  try {
    const response = await fetch(`/api/equipment/related/${encodeURIComponent(place)}`);
    if (!response.ok) throw new Error('Failed to fetch related equipment');
    const data = await response.json();
    return Promise.all(
      data.map(async (set: any) => {
        const details = await getEquipmentByEnName(set.enName);
        return { ...set, bonuses: details.bonuses }; // 合并 bonuses（如果需要额外处理）
      })
    );
  } catch (error) {
    console.error('Error loading related equipment:', error);
    return [];
  }
}

export async function loadEquipment(page = 1, limit = 20): Promise<any[]> {
  try {
    console.log(`Fetching /api/equipment?page=${page}&limit=${limit}`);
    const response = await fetch(`/api/equipment?page=${page}&limit=${limit}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API response:', data);

    // 为每个装备加载 bonuses
    const equipmentWithBonuses = await Promise.all(
      data.map(async (set: any) => {
        const details = await getEquipmentByEnName0(set.enName);
        return {
          ...set,
          bonuses: details.bonuses, // 合并 bonuses
        };
      })
    );

    return equipmentWithBonuses;
  } catch (error) {
    console.error('Error loading equipment:', error);
    return [];
  }
}
