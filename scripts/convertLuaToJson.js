import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import luaparse from 'luaparse';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function convertLuaToJson() {
  const cnLuaFilePath = path.join(__dirname, '../public/data/DataExtractor-Items-cn.lua');
  const enLuaFilePath = path.join(__dirname, '../public/data/DataExtractor-Items-en.lua');
  const jsonFilePath = path.join(__dirname, '../src/data/equipment.json');

  try {
    if (!fs.existsSync(cnLuaFilePath) || !fs.existsSync(enLuaFilePath)) {
      throw new Error('One or both Lua files not found');
    }

    const cnLuaStats = fs.statSync(cnLuaFilePath);
    const enLuaStats = fs.statSync(enLuaFilePath);
    const latestModifiedTime = Math.max(cnLuaStats.mtime.getTime(), enLuaStats.mtime.getTime());

    console.log('CN Lua file modified time:', new Date(cnLuaStats.mtime));
    console.log('EN Lua file modified time:', new Date(enLuaStats.mtime));

    let shouldGenerate = true;
    try {
      const existingJson = JSON.parse(fs.readFileSync(jsonFilePath, 'utf8'));
      if (existingJson.timestamp === latestModifiedTime) {
        shouldGenerate = false;
        console.log('Timestamps match, skipping JSON generation');
      }
    } catch (err) {
      console.log('No existing JSON or invalid, will generate new one');
    }

    if (!shouldGenerate) return;

    const cnLuaCode = fs.readFileSync(cnLuaFilePath, 'utf8');
    const enLuaCode = fs.readFileSync(enLuaFilePath, 'utf8');
    const cnAst = luaparse.parse(cnLuaCode);
    const enAst = luaparse.parse(enLuaCode);

    console.log('CN AST body length:', cnAst.body.length);
    console.log('EN AST body length:', enAst.body.length);

    const cnSets = extractSetsFromAst(cnAst, 'cn');
    const enSets = extractSetsFromAst(enAst, 'en');

    const equipment = mergeSets(cnSets, enSets);

    const output = {
      timestamp: latestModifiedTime,
      sets: equipment,
    };

    fs.writeFileSync(jsonFilePath, JSON.stringify(output, null, 2));
    console.log('JSON file generated successfully with', equipment.length, 'sets');
  } catch (error) {
    console.error('Error converting Lua to JSON:', error);
  }

  try{
    const rawData = fs.readFileSync(jsonFilePath)
    const data = JSON.parse(rawData)

    const setMap = new Map();
    data.sets.forEach(set => {
      setMap.set(set.enName, set);
    });

    data.sets = data.sets.filter(set => {
      if (set.place === "") {
          if (set.type === 2) {
              set.place = "竞技场"; // type为2时修改place
              return true; // 保留该套装
          } else {
              return false; // type不为2时删除该套装
          }
      }
      return true; // place不为空时保留
    });

    data.sets.forEach(setA => {
      // 1. 检查enName是否以"Perfected"开头且bonuses有4项
      if (setA.enName.startsWith('Perfected ')) {
          
          // 2. 获取非Perfected版本的enName
          const baseName = setA.enName.replace('Perfected ', '');
          const setB = setMap.get(baseName);

          // 3. 如果找到对应的B套装，复制effect5到A的effect6
          if (setB && setB.bonuses.effect5) {
              setA.bonuses.effect6 = setB.bonuses.effect5;
          }
      }
    });
    // 将修改后的数据写回文件
    data.sets = data.sets.reverse();
    fs.writeFileSync(jsonFilePath, JSON.stringify(data, null, 2));
    console.log('JSON文件处理完成！');
  }catch (error) {
    console.error('处理JSON文件时出错:', error);
  }
}

function extractTable(value) {
  if (value.type === 'TableConstructorExpression') {
    const result = {};
    for (const f of value.fields) {
      if (f.type === 'TableKey') {
        const key =
          f.key.type === 'StringLiteral'
            ? f.key.raw.slice(1, -1)
            : f.key.type === 'NumericLiteral'
            ? f.key.value.toString() // 确保 key 是字符串
            : '';
        result[key] =
          f.value.type === 'StringLiteral'
            ? f.value.raw.slice(1, -1)
            : f.value.type === 'TableConstructorExpression'
            ? extractTable(f.value)
            : f.value.type === 'NumericLiteral'
            ? f.value.value
            : extractTable(f.value);
      }
    }
    return result;
  }
  return value.type === 'StringLiteral' ? value.raw.slice(1, -1) : value.value;
}

function extractSetsFromAst(ast, lang) {
  const equipment = [];
  const body = ast.body.find(
    (node) => node.type === 'AssignmentStatement' && node.variables[0].name === 'DataExtractorSavedVariables'
  );

  if (!body) {
    console.log(`${lang} - No AssignmentStatement for DataExtractorSavedVariables found`);
    return equipment;
  }

  console.log(`${lang} - Found DataExtractorSavedVariables`);

  const pathKeys = ['Default', '@Chicor', '$AccountWide', 'dataItems', 'Sets'];
  let currentTable = body.init[0];
  for (const key of pathKeys) {
    console.log(`${lang} - Searching for key: "${key}"`);
    const field = currentTable.fields?.find(
      (f) => f.type === 'TableKey' && f.key.raw === `"${key}"`
    );
    if (!field) {
      console.log(`${lang} - Key "${key}" not found. Available keys:`, 
        currentTable.fields?.map(f => f.key.raw) || 'No fields');
      return equipment;
    }
    currentTable = field.value;
  }

  console.log(`${lang} - Found Sets table`);

  for (const field of currentTable.fields) {
    if (field.type === 'TableKey') {
      const setData = extractTable(field.value);
      console.log(`${lang} - setData for key ${field.key.raw}:`, setData);

      const setEntry = {};
      if (lang === 'cn') {
        setEntry.name = setData.name || '';
        setEntry.place = setData.place || '';
        setEntry.bonuses = setData.bonuses
          ? {
              effect2: setData.bonuses['2'] || '',
              effect3: setData.bonuses['3'] || '',
              effect4: setData.bonuses['4'] || '',
              effect5: setData.bonuses['5'] || '',
              effect6: setData.bonuses['6'] || '',
              effect7: setData.bonuses['7'] || '',
              effect8: setData.bonuses['8'] || '',
              effect9: setData.bonuses['9'] || '',
              effect10: setData.bonuses['10'] || '',
              effect11: setData.bonuses['11'] || '',
              effect12: setData.bonuses['12'] || '',
              effect13: setData.bonuses['13'] || '',
            }
          : {};
        setEntry.id = setData.id || '';
        setEntry.type = setData.type || '';
        setEntry.itemIDs = setData.itemIDs || [];
        setEntry.styles = setData.styles || [];
      } else if (lang === 'en') {
        setEntry.enName = setData.name || '';
      }
      // 使用 field.key.value 转换为字符串，确保匹配一致
      setEntry.key = field.key.type === 'NumericLiteral' 
        ? field.key.value.toString() 
        : field.key.raw.slice(1, -1);
      equipment.push(setEntry);
    }
  }

  return equipment;
}

function mergeSets(cnSets, enSets) {
  const merged = [];

  for (const cnSet of cnSets) {
    const enSet = enSets.find((en) => en.key === cnSet.key);
    if (enSet && enSet.enName) {
      merged.push({
        name: cnSet.name,
        enName: enSet.enName,
        place: cnSet.place,
        bonuses: cnSet.bonuses,
        id: cnSet.id,
        type: cnSet.type,
        itemIDs: cnSet.itemIDs,
        styles: cnSet.styles,
      });
    } else {
      console.warn(`No English match found for set with key: ${cnSet.key}`);
      merged.push({
        ...cnSet,
        enName: cnSet.name, // Fallback to Chinese name
      });
    }
  }

  console.log('Merged sets sample:', merged.slice(0, 3));
  return merged;
}

convertLuaToJson();