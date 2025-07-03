<template>
    <div class="build-editor">
        <!-- 导入代码 -->

        <!-- 步骤导航 -->
        <div class="steps-nav">
            <button
                v-for="(step, index) in steps"
                :key="step"
                class="step-btn"
                :class="{ active: currentStep === index }"
                @click="goToStep(index)"
            >
                {{ step }}
            </button>
        </div>

        <!-- 步骤内容 -->
        <div class="content-card">
            <!-- 基础信息 -->
            <div v-if="currentStep === 0" class="step-content">
                <div class="form-group">
                    <h2>基本信息</h2>
                    <div class="info-grid">
                        <input
                            v-model="buildData.basicInfo.buildName"
                            type="text"
                            class="input-text"
                            :class="{ 'input-error': errors.buildName }"
                            placeholder="构建名称 *"
                        />
                        <span v-if="errors.buildName" class="error-text">{{
                            errors.buildName
                        }}</span>
                        <input
                            v-model="buildData.basicInfo.subtitle"
                            type="text"
                            class="input-text"
                            placeholder="副标题"
                        />
                        <input
                            v-model="buildData.basicInfo.authorName"
                            type="text"
                            class="input-text"
                            placeholder="作者名称"
                        />
                    </div>
                </div>
                <div class="form-group">
                    <h2>职业 <span class="required">*</span></h2>
                    <div class="class-group">
                        <div
                            v-for="cls in classes"
                            :key="cls.id"
                            class="class-btn"
                            :class="{
                                active: buildData.basicInfo.classId === cls.id,
                            }"
                            @click="buildData.basicInfo.classId = cls.id"
                        >
                            <img
                                v-if="cls.enName"
                                :src="
                                    buildData.basicInfo.classId === cls.id
                                        ? `/icon/${cls.enName.toLowerCase()}-icon.webp`
                                        : `/icon/${cls.enName.toLowerCase()}-icon-full.png`
                                "
                                clss="class-icon"
                            />
                            <div class="class-name">
                                {{ cls.name }}
                            </div>
                        </div>
                    </div>
                    <span v-if="errors.classId" class="error-text">{{
                        errors.classId
                    }}</span>
                </div>
                <div class="form-group">
                    <h2>推荐种族 <span class="required">*</span></h2>
                    <div class="race-grid">
                        <div class="race-column">
                            <div
                                v-for="race in races.slice(0, 3)"
                                :key="race"
                                class="race-btn"
                                :class="{
                                    active: buildData.basicInfo.race === race,
                                }"
                                @click="buildData.basicInfo.race = race"
                            >
                                <img
                                    :src="`/icon/${race}.png`"
                                    alt=""
                                    class="race-icon"
                                />
                                <div class="race-name">
                                    {{ race }}
                                </div>
                            </div>
                        </div>
                        <div class="race-column">
                            <div
                                v-for="race in races.slice(3, 7)"
                                :key="race"
                                class="race-btn"
                                :class="{
                                    active: buildData.basicInfo.race === race,
                                }"
                                @click="buildData.basicInfo.race = race"
                            >
                                <img
                                    :src="`/icon/${race}.png`"
                                    alt=""
                                    class="race-icon"
                                />
                                <div class="race-name">
                                    {{ race }}
                                </div>
                            </div>
                        </div>
                        <div class="race-column">
                            <div
                                v-for="race in races.slice(7, 10)"
                                :key="race"
                                class="race-btn"
                                :class="{
                                    active: buildData.basicInfo.race === race,
                                }"
                                @click="buildData.basicInfo.race = race"
                            >
                                <img
                                    :src="`/icon/${race}.png`"
                                    alt=""
                                    class="race-icon"
                                />
                                <div class="race-name">
                                    {{ race }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <span v-if="errors.race" class="error-text">{{
                        errors.race
                    }}</span>
                </div>
                <div class="form-group">
                    <h2>属性点分配</h2>
                    <div class="attributes-grid">
                        <div class="attribute-item">
                            <svg class="progress-ring" width="100" height="100">
                                <circle
                                    class="progress-ring-bg"
                                    cx="50"
                                    cy="50"
                                    r="45"
                                />
                                <circle
                                    class="progress-ring-fill"
                                    cx="50"
                                    cy="50"
                                    r="45"
                                    :style="{
                                        strokeDasharray: magickaDasharray,
                                        stroke: '#3D82B9',
                                    }"
                                />
                                <text
                                    x="50"
                                    y="50"
                                    fill="#3D82B9"
                                    text-anchor="middle"
                                    dominant-baseline="middle"
                                    font-size="14"
                                    font-weight="bold"
                                >
                                    魔法
                                </text>
                            </svg>
                            <div class="attribute-control">
                                <div
                                    class="control-btn"
                                    @click="
                                        adjustAttribute('magicka', -1, $event)
                                    "
                                >
                                    <img
                                        src="/icon/removepoints.webp"
                                        alt=""
                                        class="control-btn-icon"
                                        v-if="attributeTotal > 0"
                                    />
                                </div>
                                <span class="attribute-value">{{
                                    buildData.basicInfo.attributes.magicka
                                }}</span>
                                <div
                                    class="control-btn"
                                    @click="
                                        adjustAttribute('magicka', 1, $event)
                                    "
                                >
                                    <img
                                        src="/icon/addpoints.webp"
                                        alt=""
                                        class="control-btn-icon"
                                        v-if="attributeTotal < 64"
                                    />
                                </div>
                            </div>
                        </div>
                        <div class="attribute-item">
                            <svg class="progress-ring" width="100" height="100">
                                <circle
                                    class="progress-ring-bg"
                                    cx="50"
                                    cy="50"
                                    r="45"
                                />
                                <circle
                                    class="progress-ring-fill"
                                    cx="50"
                                    cy="50"
                                    r="45"
                                    :style="{
                                        strokeDasharray: healthDasharray,
                                        stroke: '#E45342',
                                    }"
                                />
                                <text
                                    x="50"
                                    y="50"
                                    fill="#E45342"
                                    text-anchor="middle"
                                    dominant-baseline="middle"
                                    font-size="14"
                                    font-weight="bold"
                                >
                                    生命
                                </text>
                            </svg>
                            <div class="attribute-control">
                                <div
                                    class="control-btn"
                                    @click="
                                        adjustAttribute('health', -1, $event)
                                    "
                                >
                                    <img
                                        src="/icon/removepoints.webp"
                                        alt=""
                                        class="control-btn-icon"
                                        v-if="attributeTotal > 0"
                                    />
                                </div>
                                <span class="attribute-value">{{
                                    buildData.basicInfo.attributes.health
                                }}</span>
                                <div
                                    class="control-btn"
                                    @click="
                                        adjustAttribute('health', 1, $event)
                                    "
                                >
                                    <img
                                        src="/icon/addpoints.webp"
                                        alt=""
                                        class="control-btn-icon"
                                        v-if="attributeTotal < 64"
                                    />
                                </div>
                            </div>
                        </div>
                        <div class="attribute-item">
                            <svg class="progress-ring" width="100" height="100">
                                <circle
                                    class="progress-ring-bg"
                                    cx="50"
                                    cy="50"
                                    r="45"
                                />
                                <circle
                                    class="progress-ring-fill"
                                    cx="50"
                                    cy="50"
                                    r="45"
                                    :style="{
                                        strokeDasharray: staminaDasharray,
                                        stroke: '#287E19',
                                    }"
                                />
                                <text
                                    x="50"
                                    y="50"
                                    fill="#287E19"
                                    text-anchor="middle"
                                    dominant-baseline="middle"
                                    font-size="14"
                                    font-weight="bold"
                                >
                                    耐力
                                </text>
                            </svg>
                            <div class="attribute-control">
                                <div
                                    class="control-btn"
                                    @click="
                                        adjustAttribute('stamina', -1, $event)
                                    "
                                >
                                    <img
                                        src="/icon/removepoints.webp"
                                        alt=""
                                        class="control-btn-icon"
                                        v-if="attributeTotal > 0"
                                    />
                                </div>
                                <span class="attribute-value">{{
                                    buildData.basicInfo.attributes.stamina
                                }}</span>
                                <div
                                    class="control-btn"
                                    @click="
                                        adjustAttribute('stamina', 1, $event)
                                    "
                                >
                                    <img
                                        src="
                                        /icon/addpoints.webp"
                                        alt=""
                                        class="control-btn-icon"
                                        v-if="attributeTotal < 64"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                    <span v-if="errors.attributes" class="error-text">{{
                        errors.attributes
                    }}</span>
                </div>
                <div class="form-group">
                    <div class="mode-grid">
                        <div class="mode-column">
                            <h2>模式 <span class="required">*</span></h2>
                            <div class="option-group">
                                <button
                                    v-for="style in playstyles"
                                    :key="style"
                                    class="option-btn"
                                    :class="{
                                        active:
                                            buildData.basicInfo.playstyle ===
                                            style,
                                    }"
                                    @click="
                                        buildData.basicInfo.playstyle = style
                                    "
                                >
                                    {{ style }}
                                </button>
                            </div>
                            <span v-if="errors.playstyle" class="error-text">{{
                                errors.playstyle
                            }}</span>
                        </div>
                        <div class="mode-column">
                            <h2>定位 <span class="required">*</span></h2>
                            <div class="option-group">
                                <button
                                    v-for="role in roles"
                                    :key="role"
                                    class="option-btn"
                                    :class="{
                                        active:
                                            buildData.basicInfo.role === role,
                                    }"
                                    @click="buildData.basicInfo.role = role"
                                >
                                    {{ role }}
                                </button>
                            </div>
                            <span v-if="errors.role" class="error-text">{{
                                errors.role
                            }}</span>
                        </div>
                    </div>
                </div>

                <div class="disease-grid">
                    <div class="disease-column">
                        <h2>吸血病</h2>
                        <div class="disease-group">
                            <div
                                class="disease-item"
                                v-for="stage in 5"
                                :key="stage"
                                :class="{
                                    active:
                                        buildData.basicInfo.vampire === stage,
                                }"
                                @click="
                                    buildData.basicInfo.vampire =
                                        buildData.basicInfo.vampire === stage
                                            ? 0
                                            : stage
                                "
                            >
                                <img
                                    :src="`/esoui/art/icons/ability_u26_vampire_infection_stage${stage}.webp`"
                                    alt=""
                                    class="disease-icon"
                                />
                                <div class="disease-text">阶段{{ stage }}</div>
                            </div>
                        </div>
                    </div>

                    <div class="disease-column">
                        <h2>狼化病</h2>
                        <div class="disease-group">
                            <div
                                class="disease-item"
                                :class="{
                                    active: buildData.basicInfo.wolf === 1,
                                }"
                                @click="
                                    buildData.basicInfo.wolf =
                                        buildData.basicInfo.wolf === 1 ? 0 : 1
                                "
                            >
                                <img
                                    :src="`/esoui/art/icons/ability_werewolf_010.webp`"
                                    alt=""
                                    class="disease-icon"
                                />
                                <div class="disease-text">狼化</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- 装备选择 -->
            <div v-if="currentStep === 1" class="step-content">
                <h2>装备选择</h2>
                <div
                    v-for="slot in equipmentSlots"
                    :key="slot.key"
                    class="setslot-group"
                    :class="{ locked: isSlotLocked(slot.key) }"
                    @click="
                        !isSlotLocked(slot.key) && openEquipmentPopup(slot.key)
                    "
                >
                    <div class="icon-column">
                        <img
                            :src="
                                buildData.equipment[slot.key]?.icon
                                    ? buildData.equipment[slot.key]?.icon
                                    : slot.icon
                            "
                            class="setslot-icon"
                        />
                    </div>
                    <span class="setslot-label" :style="getLabelStyle(slot)">
                        {{ slot.label }}
                    </span>
                    <div
                        v-if="buildData.equipment[slot.key]"
                        class="setslot-info"
                    >
                        <span class="setslot-name">
                            {{ buildData.equipment[slot.key]?.name
                            }}<span
                                v-if="
                                    slot.key === 'mainHand' ||
                                    slot.key === 'offHand' ||
                                    slot.key === 'backbarMainHand' ||
                                    slot.key === 'backbarOffHand'
                                "
                            >
                                {{ buildData.equipment[slot.key]?.type }}
                            </span>
                            <span style="font-size: 14px">
                                &lt;{{
                                    buildData.equipment[slot.key]?.enName
                                }}&gt;</span
                            >
                        </span>
                    </div>
                    <div v-else>
                        <span class="setslot-name" style="color: #ada9ab">
                            N/A
                        </span>
                    </div>
                    <div class="setslot-bonuse" style="white-space: nowrap">
                        <span v-if="buildData.equipment[slot.key]?.trait">
                            <img
                                :src="
                                    buildData.equipment[slot.key]?.trait?.icon
                                "
                                :alt="
                                    buildData.equipment[slot.key]?.trait?.name
                                "
                                style="width: 14px; height: 14px"
                            />
                            {{ buildData.equipment[slot.key]?.trait?.name }}
                            &lt;{{
                                buildData.equipment[slot.key]?.trait?.enName
                            }}&gt;
                        </span>
                        <br />
                        <span
                            v-if="buildData.equipment[slot.key]?.enchantment"
                            style="color: #dec781"
                        >
                            <img
                                :src="
                                    buildData.equipment[slot.key]?.enchantment
                                        ?.icon
                                "
                                :alt="
                                    buildData.equipment[slot.key]?.enchantment
                                        ?.name
                                "
                                style="width: 14px; height: 14px"
                            />
                            {{
                                buildData.equipment[slot.key]?.enchantment?.name
                            }}
                        </span>
                    </div>
                </div>

                <!-- 装备选择浮窗 -->
                <div
                    v-if="showEquipmentPopup"
                    class="equipment-popup-backdrop"
                    @click="closePopup"
                >
                    <div class="equipment-popup" @click.stop>
                        <div class="popup-header">
                            <h3>
                                选择
                                {{
                                    equipmentSlots.find(
                                        (s) => s.key === selectedSlotKey
                                    )?.label
                                }}
                                装备
                            </h3>
                            <button class="close-btn" @click="closePopup">
                                ×
                            </button>
                        </div>
                        <div class="popup-content">
                            <div class="search-section">
                                <input
                                    v-model="equipmentSearch[selectedSlotKey]"
                                    type="text"
                                    class="set-input-text"
                                    placeholder="搜索装备名称、英文名或昵称"
                                    @input="filterEquipmentForTemplate()"
                                />
                                <ul class="equipment-list">
                                    <li
                                        v-for="item in filteredEquipment[
                                            selectedSlotKey
                                        ]"
                                        :key="item.enName || item.name"
                                        class="equipment-item"
                                        :class="{
                                            selected:
                                                selectedEquipment?.enName ===
                                                item.enName,
                                        }"
                                        @click="selectEquipment(item)"
                                    >
                                        <img
                                            v-if="item.icon"
                                            :src="item.icon"
                                            class="item-icon"
                                        />
                                        <span
                                            >{{ item.name }} &lt;{{
                                                item.enName || "N/A"
                                            }}&gt;</span
                                        >
                                    </li>
                                    <li
                                        v-if="
                                            filteredEquipment[selectedSlotKey]
                                                .length === 0
                                        "
                                        class="no-results"
                                    >
                                        {{
                                            equipmentSearch[selectedSlotKey]
                                                ? "无匹配装备，请检查输入或套装类型"
                                                : "请输入装备名称、英文名或昵称"
                                        }}
                                    </li>
                                </ul>
                            </div>
                            <div class="filter-section">
                                <div
                                    v-if="currentTypeOptions.length"
                                    class="type-options"
                                >
                                    <div
                                        v-for="type in currentTypeOptions"
                                        :key="type.value"
                                        class="type-option"
                                        :class="{
                                            selected:
                                                selectedType === type.label,
                                        }"
                                        @click="
                                            selectedType = type.label;
                                            filterEquipmentForTemplate();
                                        "
                                    >
                                        {{ type.label }}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="button-group">
                            <button
                                class="btn btn-secondary clear-btn"
                                @click="clearEquipment"
                            >
                                清除
                            </button>
                            <button
                                class="btn btn-primary confirm-btn"
                                :disabled="!selectedEquipment"
                                @click="confirmEquipment"
                            >
                                确认
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 特质选择浮窗 -->
                <div
                    v-if="showTraitPopup"
                    class="equipment-popup-backdrop"
                    @click="closePopup"
                >
                    <div class="trait-popup" @click.stop>
                        <div class="popup-header">
                            <h3>
                                选择
                                {{
                                    equipmentSlots.find(
                                        (s) => s.key === selectedSlotKey
                                    )?.label
                                }}
                                特质
                            </h3>
                            <button class="close-btn" @click="closePopup">
                                ×
                            </button>
                        </div>
                        <div class="trait-list">
                            <div
                                v-for="trait in traitOptions[
                                    selectedSlotKey === 'ring1' ||
                                    selectedSlotKey === 'ring2' ||
                                    selectedSlotKey === 'neck'
                                        ? 'jewelry'
                                        : [
                                              'mainHand',
                                              'offHand',
                                              'backbarMainHand',
                                              'backbarOffHand',
                                          ].includes(selectedSlotKey)
                                        ? 'weapon'
                                        : 'armor'
                                ]"
                                :key="trait.enName"
                                class="trait-item"
                                @click="selectTrait(trait)"
                            >
                                <img :src="trait.icon" class="item-icon" />
                                <div class="trait-info">
                                    <span class="trait-name"
                                        >{{ trait.name }} &lt;{{
                                            trait.enName
                                        }}&gt;</span
                                    >
                                    <span class="trait-bonuses">{{
                                        trait.bonuses
                                    }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 附魔选择浮窗 -->
                <div
                    v-if="showEnchantmentPopup"
                    class="equipment-popup-backdrop"
                    @click="closePopup"
                >
                    <div class="enchantment-popup" @click.stop>
                        <div class="popup-header">
                            <h3>
                                选择
                                {{
                                    equipmentSlots.find(
                                        (s) => s.key === selectedSlotKey
                                    )?.label
                                }}
                                附魔
                            </h3>
                            <button class="close-btn" @click="closePopup">
                                ×
                            </button>
                        </div>
                        <div class="enchantment-list">
                            <div
                                v-for="enchantment in enchantmentOptions[
                                    selectedSlotKey === 'ring1' ||
                                    selectedSlotKey === 'ring2' ||
                                    selectedSlotKey === 'neck'
                                        ? 'jewelry'
                                        : [
                                              'mainHand',
                                              'offHand',
                                              'backbarMainHand',
                                              'backbarOffHand',
                                          ].includes(selectedSlotKey)
                                        ? 'weapon'
                                        : 'armor'
                                ]"
                                :key="enchantment.enName"
                                class="enchantment-item"
                                @click="selectEnchantment(enchantment)"
                            >
                                <img
                                    :src="enchantment.icon"
                                    class="item-icon"
                                />
                                <div class="trait-info">
                                    <span class="enchantment-name"
                                        >{{ enchantment.name }} &lt;{{
                                            enchantment.enName.toUpperCase()
                                        }}&gt;</span
                                    >
                                    <span class="enchantment-effect">{{
                                        enchantment.effect
                                    }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 技能选择 -->
            <div v-if="currentStep === 2" class="step-content">
                <h2>已选技能</h2>
                <div style="text-align: center;">
                    <div class="selected-skills">

                        <div 
                            class="skill-frame"
                            v-for="skill in buildData.skills.mainBar"
                            :key="skill?.name"
                        >
                            <img
                                v-if="skill?.icon"
                                :src="skill.icon"
                                alt="skill icon"
                                class="skill-icon"
                            />
                            
                            <div class="skill-name">
                                {{ skill?.name }}
                            </div>
                        </div>
                    </div>
                    <div class="selected-skills" style="margin-top: 10px;">
                        <div 
                            class="skill-frame"
                            v-for="skill in buildData.skills.backBar"
                            :key="skill?.name"
                        >
                            <img
                                v-if="skill?.icon"
                                :src="skill.icon"
                                alt="skill icon"
                                class="skill-icon"
                            />
                            {{ skill?.name }}
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <label>搜索技能</label>
                    <input
                        v-model="skillSearch"
                        type="text"
                        class="input-text"
                        placeholder="输入技能名称或英文名"
                        @input="filterSkills"
                    />
                </div>
                <h5>主技能栏</h5>
                <div
                    v-for="(slot, index) in buildData.skills.mainBar"
                    :key="'main-' + index"
                    class="form-group"
                >
                    <label
                        >技能槽 {{ index + 1 }}
                        {{ index === 5 ? "(终极)" : "" }}</label
                    >
                    <select
                        v-model="buildData.skills.mainBar[index]"
                        class="input-select"
                    >
                        <option :value="null">无</option>
                        <option
                            v-for="skill in filteredSkills"
                            :key="'skill-' + skill.id"
                            :value="skill"
                        >
                            {{ skill.name }} ({{ skill.enName || "N/A" }})
                        </option>
                        <option
                            v-for="variant in filteredSkillVariants"
                            :key="'variant-' + variant.id"
                            :value="variant"
                        >
                            {{ variant.name }} ({{ variant.enName || "N/A" }})
                        </option>
                    </select>
                </div>
                <h5>备用技能栏</h5>
                <div
                    v-for="(slot, index) in buildData.skills.backBar"
                    :key="'back-' + index"
                    class="form-group"
                >
                    <label
                        >技能槽 {{ index + 1 }}
                        {{ index === 5 ? "(终极)" : "" }}</label
                    >
                    <select
                        v-model="buildData.skills.backBar[index]"
                        class="input-select"
                    >
                        <option :value="null">无</option>
                        <option
                            v-for="skill in filteredSkills"
                            :key="'skill-' + skill.id"
                            :value="skill"
                        >
                            {{ skill.name }} ({{ skill.enName || "N/A" }})
                        </option>
                        <option
                            v-for="variant in filteredSkillVariants"
                            :key="'variant-' + variant.id"
                            :value="variant"
                        >
                            {{ variant.name }} ({{ variant.enName || "N/A" }})
                        </option>
                    </select>
                </div>
            </div>

            <!-- CP选择 -->
            <div v-if="currentStep === 3" class="step-content">
                <div
                    v-for="category in cpCategories"
                    :key="category.id"
                    class="category-group"
                >
                    <h5>{{ category.name }}</h5>
                    <div
                        v-for="cp in cpSkills.filter(
                            (cp) =>
                                cp.category_id === category.id &&
                                cp.is_slottable
                        )"
                        :key="cp.id"
                        class="checkbox-group"
                    >
                        <input
                            type="checkbox"
                            :id="'cp-' + cp.id"
                            :value="cp"
                            v-model="buildData.cpSkills"
                        />
                        <label :for="'cp-' + cp.id"
                            >{{ cp.name }} ({{ cp.en_name || "N/A" }})</label
                        >
                    </div>
                </div>
            </div>

            <!-- 增益选择 -->
            <div v-if="currentStep === 4" class="step-content">
                <div class="form-group">
                    <label>食物</label>
                    <select v-model="buildData.buffs.food" class="input-select">
                        <option :value="null">无</option>
                        <option
                            v-for="food in foods"
                            :key="food.id"
                            :value="food"
                        >
                            {{ food.name }} ({{ food.enName }})
                        </option>
                    </select>
                </div>
                <div class="form-group">
                    <label>药水</label>
                    <select
                        v-model="buildData.buffs.potion"
                        class="input-select"
                    >
                        <option :value="null">无</option>
                        <option
                            v-for="potion in potions"
                            :key="potion.id"
                            :value="potion"
                        >
                            {{ potion.name }} ({{ potion.enName }})
                        </option>
                    </select>
                </div>
                <div class="form-group">
                    <label>梦达斯之石</label>
                    <select
                        v-model="buildData.buffs.mundusStone"
                        class="input-select"
                    >
                        <option :value="null">无</option>
                        <option
                            v-for="stone in mundusStones"
                            :key="stone.id"
                            :value="stone"
                        >
                            {{ stone.name }} ({{ stone.enName }})
                        </option>
                    </select>
                </div>
            </div>

            <!-- 构建结果 -->
            <div v-if="currentStep === 5" class="step-content">
                <div class="result-section">
                    <h5>基础信息</h5>
                    <p>
                        <strong>作者名称:</strong>
                        {{ buildData.basicInfo.authorName || "未填写" }}
                    </p>
                    <p>
                        <strong>构建名称:</strong>
                        {{ buildData.basicInfo.buildName || "未填写" }}
                    </p>
                    <p>
                        <strong>副标题:</strong>
                        {{ buildData.basicInfo || "未填写" }}
                    </p>
                    <p>
                        <strong>职业:</strong>
                        {{
                            classes.find(
                                (c) => c.id === buildData.basicInfo.classId
                            )?.name || "未选择"
                        }}
                    </p>
                    <p>
                        <strong>种族:</strong>
                        {{ buildData.basicInfo.race || "未选择" }}
                    </p>
                    <p>
                        <strong>属性点:</strong> 生命:
                        {{ buildData.basicInfo.attributes.health || 0 }}, 魔法:
                        {{ buildData.basicInfo.attributes.magicka || 0 }}, 耐力:
                        {{ buildData.basicInfo.attributes.stamina || 0 }}
                    </p>
                    <p>
                        <strong>玩法:</strong>
                        {{ buildData.basicInfo.playstyle || "未选择" }}
                    </p>
                    <p>
                        <strong>位置:</strong>
                        {{ buildData.basicInfo.role || "未选择" }}
                    </p>
                </div>
                <div class="result-section">
                    <h5>装备</h5>
                    <div
                        v-for="slot in equipmentSlots"
                        :key="slot.key"
                        class="result-item"
                    >
                        <strong>{{ slot.label }}:</strong>
                        <img
                            v-if="buildData.equipment[slot.key]?.icon"
                            :src="buildData.equipment[slot.key]?.icon"
                            alt="icon"
                            class="item-icon"
                        />
                        <span>{{
                            buildData.equipment[slot.key]?.name || "未选择"
                        }}</span>
                    </div>
                </div>
                <div class="result-section">
                    <h5>技能</h5>
                    <p><strong>主技能栏:</strong></p>
                    <ul>
                        <li
                            v-for="(skill, index) in buildData.skills.mainBar"
                            :key="'main-' + index"
                            class="result-item"
                        >
                            <img
                                v-if="skill?.icon"
                                :src="skill.icon"
                                alt="skill icon"
                                class="item-icon"
                            />
                            {{ skill?.name || "未选择" }}
                        </li>
                    </ul>
                    <p><strong>备用技能栏:</strong></p>
                    <ul>
                        <li
                            v-for="(skill, index) in buildData.skills.backBar"
                            :key="'back-' + index"
                            class="result-item"
                        >
                            <img
                                v-if="skill?.icon"
                                :src="skill.icon"
                                alt="skill icon"
                                class="item-icon"
                            />
                            {{ skill?.name || "未选择" }}
                        </li>
                    </ul>
                </div>
                <div class="result-section">
                    <h5>CP技能</h5>
                    <ul>
                        <li
                            v-for="cp in buildData.cpSkills"
                            :key="cp.id"
                            class="result-item"
                        >
                            {{ cp.name }} ({{ cp.category_name || "N/A" }})
                        </li>
                        <li v-if="buildData.cpSkills.length === 0">未选择</li>
                    </ul>
                </div>
                <div class="result-section">
                    <h5>增益效果</h5>
                    <p class="result-item">
                        <strong>食物:</strong>
                        <img
                            v-if="buildData.buffs.food?.icon"
                            :src="buildData.buffs.food.icon"
                            alt="food icon"
                            class="item-icon"
                        />
                        {{ buildData.buffs.food?.name || "未选择" }}
                    </p>
                    <p class="result-item">
                        <strong>药水:</strong>
                        <img
                            v-if="buildData.buffs.potion?.icon"
                            :src="buildData.buffs.potion.icon"
                            alt="potion icon"
                            class="item-icon"
                        />
                        {{ buildData.buffs.potion?.name || "未选择" }}
                    </p>
                    <p class="result-item">
                        <strong>梦达斯之石:</strong>
                        <img
                            v-if="buildData.buffs.mundusStone?.icon"
                            :src="buildData.buffs.mundusStone.icon"
                            alt="mundus icon"
                            class="item-icon"
                        />
                        {{ buildData.buffs.mundusStone?.name || "未选择" }}
                    </p>
                </div>
                <div class="share-section">
                    <button class="btn btn-primary" @click="generateShareCode">
                        生成分享代码
                    </button>
                    <div v-if="shareCode" class="share-code">
                        <span
                            >分享代码: <code>{{ shareCode }}</code></span
                        >
                        <button
                            class="btn btn-secondary"
                            @click="copyShareCode"
                        >
                            复制
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import * as LZString from "lz-string";
import { enchantmentOptions } from "@/Data/enchantment.ts";
import { traitOptions } from "@/Data/trait.ts";

import type {
    SlotKey,
    BuildData,
    classes,
    skills,
    skill_trees,
    EquipmentSet,
    skill_variants,
    Food,
    Potion,
    MundusStone,
    ChampionSkill,
} from "@/types/build";

const router = useRouter();

// 配置步骤
const steps = [
    "基础信息",
    "装备选择",
    "技能选择",
    "CP技能选择",
    "增益选择",
    "构建结果",
];
const currentStep = ref(0);

// 数据状态
const classes = ref<classes[]>([
    { id: 7, name: "奥术师", enName: "Arcanist" },
    { id: 6, name: "死灵法师", enName: "Necromancer" },
    { id: 5, name: "守望者", enName: "Warden" },
    { id: 3, name: "龙骑士", enName: "Dragonknight" },
    { id: 2, name: "圣殿骑士", enName: "Templar" },
    { id: 1, name: "巫师", enName: "Sorcerer" },
    { id: 4, name: "夜刃", enName: "NightBlade" },
]);

const skillTrees = ref<skill_trees[]>([]);
const equipmentList = ref<EquipmentSet[]>([]);
const skills = ref<skills[]>([]);
const skillVariants = ref<skill_variants[]>([]);
const cpSkills = ref<ChampionSkill[]>([]);
const foods = ref<Food[]>([]);
const potions = ref<Potion[]>([]);
const mundusStones = ref<MundusStone[]>([]);

interface Trait {
    icon: string;
    name: string;
    enName: string;
    bonuses: string;
}

interface Enchantment {
    name: string;
    enName: string;
    effect: string;
}

// 构建数据
const buildData = reactive<BuildData>({
    basicInfo: {
        authorName: "",
        buildName: "",
        subtitle: "",
        classId: null,
        race: "",
        attributes: { health: 0, magicka: 0, stamina: 0 },
        playstyle: "",
        role: "",
        vampire: 0,
        wolf: 0,
    },
    equipment: {
        head: null,
        shoulders: null,
        chest: null,
        hands: null,
        waist: null,
        legs: null,
        feet: null,
        ring1: null,
        ring2: null,
        neck: null,
        mainHand: null,
        offHand: null,
        backbarMainHand: null,
        backbarOffHand: null,
    },
    skills: {
        mainBar: Array(6).fill(null),
        backBar: Array(6).fill(null),
    },
    cpSkills: [],
    buffs: {
        food: null,
        potion: null,
        mundusStone: null,
    },
});

// 固定选项
const races = [
    "布莱顿人",
    "兽人",
    "红卫人",
    "高精灵",
    "木精灵",
    "虎人",
    "帝国人",
    "亚龙人",
    "暗精灵",
    "诺德人",
];

const playstyles = ["PvP", "PvE", "SOLO"] as const;
const roles = ["输出", "治疗", "坦克"] as const;

const equipmentSlots = [
    {
        key: "head",
        label: "头部",
        icon: "/icon/gearslot_head.webp",
    },
    {
        key: "shoulders",
        label: "肩部",
        icon: "/icon/gearslot_shoulders.webp",
    },
    {
        key: "chest",
        label: "胸部",
        icon: "/icon/gearslot_chest.webp",
    },
    {
        key: "hands",
        label: "手部",
        icon: "/icon/gearslot_hands.webp",
    },
    {
        key: "waist",
        label: "腰部",
        icon: "/icon/gearslot_belt.webp",
    },
    {
        key: "legs",
        label: "腿部",
        icon: "/icon/gearslot_legs.webp",
    },
    {
        key: "feet",
        label: "足部",
        icon: "/icon/gearslot_feet.webp",
    },
    {
        key: "ring1",
        label: "戒指1",
        icon: "/icon/gearslot_ring.webp",
    },
    {
        key: "ring2",
        label: "戒指2",
        icon: "/icon/gearslot_ring.webp",
    },
    {
        key: "neck",
        label: "项链",
        icon: "/icon/gearslot_neck.webp",
    },
    {
        key: "mainHand",
        label: "主手武器",
        icon: "/icon/gearslot_mainhand.webp",
    },
    {
        key: "offHand",
        label: "副手武器",
        icon: "/icon/gearslot_offhand.webp",
    },
    {
        key: "backbarMainHand",
        label: "后排主手武器",
        icon: "/icon/gearslot_mainhand.webp",
    },
    {
        key: "backbarOffHand",
        label: "后排副手武器",
        icon: "/icon/gearslot_offhand.webp",
    },
];

// 颜色映射
const armorColorMap: Record<string, string> = {
    轻甲: "#3694F9", // 蓝色
    中甲: "#3ACC1F", // 绿色
    重甲: "#CF2C26", // 红色
};

// 获取 setslot-label 的样式
const getLabelStyle = (slot: { key: string; label: string; icon: string }) => {
    const armorSlots = [
        "head",
        "shoulders",
        "chest",
        "hands",
        "waist",
        "legs",
        "feet",
    ];
    if (!armorSlots.includes(slot.key)) {
        return {};
    }
    const type = buildData.equipment[slot.key]?.type;
    if (type && armorColorMap[type]) {
        return { color: armorColorMap[type] };
    }
    return {};
};

// CP 类别（模拟）
const cpCategories = ref([
    { id: 1, name: "Warfare" },
    { id: 2, name: "Fitness" },
    { id: 3, name: "Craft" },
]);

// 搜索状态
const equipmentSearch = reactive<Record<string, string>>({
    head: "",
    shoulders: "",
    chest: "",
    hands: "",
    waist: "",
    legs: "",
    feet: "",
    ring1: "",
    ring2: "",
    neck: "",
    mainHand: "",
    offHand: "",
    backbarMainHand: "",
    backbarOffHand: "",
});

const filteredEquipment = reactive<Record<string, EquipmentSet[]>>({
    head: [],
    shoulders: [],
    chest: [],
    hands: [],
    waist: [],
    legs: [],
    feet: [],
    ring1: [],
    ring2: [],
    neck: [],
    mainHand: [],
    offHand: [],
    backbarMainHand: [],
    backbarOffHand: [],
});

const skillSearch = ref("");
const filteredSkills = ref<skills[]>([]);
const filteredSkillVariants = ref<skill_variants[]>([]);

// 验证错误
const errors = reactive({
    buildName: "",
    classId: "",
    race: "",
    attributes: "",
    playstyle: "",
    role: "",
});

// 属性点总计
const attributeTotal = computed(() => {
    return (
        buildData.basicInfo.attributes.health +
        buildData.basicInfo.attributes.magicka +
        buildData.basicInfo.attributes.stamina
    );
});

// 圆环填充（0-100%）
const magickaDasharray = computed(() => {
    const progress = buildData.basicInfo.attributes.magicka / 64;
    const circumference = 2 * Math.PI * 45;
    return `${progress * circumference} ${circumference}`;
});

const healthDasharray = computed(() => {
    const progress = buildData.basicInfo.attributes.health / 64;
    const circumference = 2 * Math.PI * 45;
    return `${progress * circumference} ${circumference}`;
});

const staminaDasharray = computed(() => {
    const progress = buildData.basicInfo.attributes.stamina / 64;
    const circumference = 2 * Math.PI * 45;
    return `${progress * circumference} ${circumference}`;
});

// 分享代码
const shareCode = ref("");
const importCode = ref("");

const nicknameMap = ref<{
    [key: string]: string[];
}>({
    spc: ["Spell Power Cure"],
    pp: ["Pillager's Profit", "Perfected Pillager's Profit"],
    pa: ["Powerful Assault"],
    pw: ["Pearlescent Ward", "Perfected Pearlescent Ward"],
    le: ["Lucent Echoes", "Perfected Lucent Echoes"],
    ro: ["Roaring Opportunist", "Perfected Roaring Opportunist"],
    jo: ["Jorvuld's Guidance"],
    rojo: [
        "Jorvuld's Guidance",
        "Roaring Opportunist",
        "Perfected Roaring Opportunist",
    ],
    DR: ["Drake's Rush"],
    zen: ["Z'en's Redress"],
    mk: ["Way of Martial Knowledge"],
    ec: ["Elemental Catalyst"],
    tt: ["Turning Tide"],
    yol: ["Claw of Yolnahkriin"],
    co: ["Crimson Oath's Rive"],
    sax: ["Saxhleel Champion", "Perfected Saxhleel Champion"],
    wm: ["War Machine"],
    ma: ["Master Architect"],
    大鳄鱼: ["Maw of the Infernal"],
    小鳄鱼: ["Slimecraw"],
    鳄鱼: ["Maw of the Infernal", "Slimecraw"],
    泽恩: ["Z'en's Redress"],
    火伤: ["Encratis's Behemoth"],
    压耐: ["Coral Riptide", "Perfected Coral Riptide"],
    压蓝: ["Bahsei's Mania", "Perfected Bahsei's Mania"],
});

const armorTypeOptions = [
    { label: "轻甲", value: "Light" },
    { label: "中甲", value: "Medium" },
    { label: "重甲", value: "Heavy" },
];

// 武器类型选项
const weaponTypeOptions = [
    { label: "斧头", value: "Axe" },
    { label: "钉锤", value: "Mace" },
    { label: "剑", value: "Sword" },
    { label: "战斧", value: "BattleAxe" },
    { label: "重锤", value: "Maul" },
    { label: "巨剑", value: "GreatSword" },
    { label: "匕首", value: "Dagger" },
    { label: "弓", value: "Bow" },
    { label: "炼狱法杖", value: "InfernoStaff" },
    { label: "寒冰法杖", value: "IceStaff" },
    { label: "闪电法杖", value: "LightningStaff" },
    { label: "恢复法杖", value: "RestorationStaff" },
    { label: "盾牌", value: "shield" },
];

// 单手武器类型
const singleHandWeaponTypes = [
    "Axe",
    "Mace",
    "Sword",
    "Dagger",
    "Shield",
    "斧头",
    "钉锤",
    "剑",
    "匕首",
    "盾牌",
];

// 双手武器类型
const twoHandWeaponTypes = [
    "BattleAxe",
    "Maul",
    "GreatSword",
    "Bow",
    "InfernoStaff",
    "IceStaff",
    "LightningStaff",
    "RestorationStaff",
    "巨剑",
    "战斧",
    "重锤",
    "炼狱法杖",
    "寒冰法杖",
    "闪电法杖",
    "治疗法杖",
    "弓",
];

// 状态管理
const showEquipmentPopup = ref(false);
const showTraitPopup = ref(false);
const showEnchantmentPopup = ref(false);
const selectedSlotKey = ref<string>("");
const selectedType = ref<string>("Light"); // 默认轻甲
const selectedEquipment = ref<EquipmentSet | null>(null);
const selectedTrait = ref<Trait | null>(null);

const armorTypeMap: Record<string, string> = {
    轻甲: "轻型",
    中甲: "中型",
    重甲: "重型",
    随机护甲类型: "随机护甲类型",
    自选护甲类型: "自选护甲类型",
};

const weaponTypeMap: Record<string, string> = {
    斧头: "斧头",
    钉锤: "钉锤",
    剑: "剑",
    战斧: "战斧",
    重锤: "重锤",
    巨剑: "巨剑",
    匕首: "匕首",
    弓: "弓",
    炼狱法杖: "炼狱法杖",
    寒冰法杖: "寒冰法杖",
    闪电法杖: "闪电法杖",
    治疗法杖: "治疗法杖",
    盾牌: "盾牌",
};

// 判断槽位是否被锁定
const isSlotLocked = (slotKey: string): boolean => {
    if (slotKey === "offHand" && buildData.equipment.mainHand?.type) {
        return twoHandWeaponTypes.includes(buildData.equipment.mainHand.type);
    }
    if (
        slotKey === "backbarOffHand" &&
        buildData.equipment.backbarMainHand?.type
    ) {
        return twoHandWeaponTypes.includes(
            buildData.equipment.backbarMainHand.type
        );
    }
    return false;
};

// 获取当前槽位类型选项
const currentTypeOptions = computed(() => {
    if (["ring1", "ring2", "neck"].includes(selectedSlotKey.value)) {
        return [];
    } else if (["offHand", "backbarOffHand"].includes(selectedSlotKey.value)) {
        return weaponTypeOptions.filter((type) =>
            singleHandWeaponTypes.includes(type.value)
        );
    } else if (
        ["mainHand", "backbarMainHand"].includes(selectedSlotKey.value)
    ) {
        return weaponTypeOptions;
    } else {
        return armorTypeOptions;
    }
});

// 打开装备浮窗
const openEquipmentPopup = (slotKey: string) => {
    selectedSlotKey.value = slotKey;
    equipmentSearch[slotKey] = "";
    selectedType.value = ["ring1", "ring2", "neck"].includes(slotKey)
        ? ""
        : ["mainHand", "offHand", "backbarMainHand", "backbarOffHand"].includes(
              slotKey
          )
        ? "Dagger"
        : "轻甲";
    selectedEquipment.value = null;
    selectedTrait.value = null;
    filterEquipment(slotKey as SlotKey);
    showEquipmentPopup.value = true;
    console.log(
        `Opened popup for ${slotKey}, default type: ${selectedType.value}`
    );
};

// 确认特质选择
const selectTrait = (trait: Trait) => {
    selectedTrait.value = trait;
    showTraitPopup.value = false;
    showEnchantmentPopup.value = true;
};

// 确认附魔选择
const selectEnchantment = (enchantment: Enchantment) => {
    if (selectedEquipment.value && selectedTrait.value) {
        const mappedArmor = selectedEquipment.value.armor
            ? armorTypeMap[selectedEquipment.value.armor] || null
            : null;
        const equipment: EquipmentSet = {
            ...selectedEquipment.value,
            trait: selectedTrait.value,
            enchantment,
            styles: selectedEquipment.value.styles,
            type: selectedType.value,
            icon:
                getEquipmentIcon(
                    selectedSlotKey.value as SlotKey,
                    selectedType.value,
                    selectedEquipment.value.styles
                ) || selectedEquipment.value.icon, // 回退到默认 icon
        };
        buildData.equipment[selectedSlotKey.value] = equipment;
        selectedEquipmentMap[selectedSlotKey.value as SlotKey] = equipment;
        saveToStorage();
        showEnchantmentPopup.value = false;
        selectedSlotKey.value = "";
        selectedEquipment.value = null;
        selectedTrait.value = null;
        console.log(
            `Selected enchantment for ${selectedSlotKey.value}:`,
            equipment
        );
    }
};

// 关闭浮窗
const closePopup = () => {
    showEquipmentPopup.value = false;
    showTraitPopup.value = false;
    showEnchantmentPopup.value = false;
    selectedSlotKey.value = "";
    equipmentSearch[selectedSlotKey.value] = "";
    selectedEquipment.value = null;
    selectedTrait.value = null;
};

// 新增：记录已选套装
const selectedEquipmentMap = reactive<Record<SlotKey, EquipmentSet | null>>({
    head: null,
    shoulders: null,
    chest: null,
    hands: null,
    waist: null,
    legs: null,
    feet: null,
    ring1: null,
    ring2: null,
    neck: null,
    mainHand: null,
    offHand: null,
    backbarMainHand: null,
    backbarOffHand: null,
});

const slotStyleMap: Record<SlotKey, string[]> = {
    head: ["头部"],
    shoulders: ["肩部"],
    chest: ["胸甲"],
    hands: ["手部"],
    waist: ["腰部"],
    legs: ["腿部"],
    feet: ["足部"],
    neck: ["颈部装备"],
    ring1: ["戒指"],
    ring2: ["戒指"],
    mainHand: ["单手武器", "双手武器", "副武器"],
    offHand: ["单手武器", "双手武器", "副武器"],
    backbarMainHand: ["单手武器", "双手武器", "副武器"],
    backbarOffHand: ["单手武器", "双手武器", "副武器"],
};

// 根据槽位、类型和 styles 获取正确的 icon
const getEquipmentIcon = (
    slotKey: SlotKey,
    type: string,
    styles: EquipmentSet["styles"]
): string | undefined => {
    if (!styles) return undefined;

    const slotStyle = slotStyleMap[slotKey][0];

    // 饰品槽位（ring1, ring2, neck）
    if (["ring1", "ring2", "neck"].includes(slotKey)) {
        return styles.护甲?.[slotStyle]?.["无"]?.icon;
    }

    // 武器槽位
    if (
        ["mainHand", "offHand", "backbarMainHand", "backbarOffHand"].includes(
            slotKey
        )
    ) {
        const apiWeaponType = type;
        // 遍历武器类别（单手武器、双手武器、副武器）
        for (const weaponCategory in styles.武器) {
            if (styles.武器[weaponCategory]?.[apiWeaponType]?.icon) {
                return styles.武器[weaponCategory][apiWeaponType].icon;
            }
        }
        return undefined;
    }

    // 护甲槽位
    const apiArmorType = armorTypeMap[type] || type;
    return styles.护甲?.[slotStyle]?.[apiArmorType]?.icon;
};

const filterEquipmentForTemplate = () => {
    filterEquipment(selectedSlotKey.value as SlotKey);
};

const filterEquipment = (slotKey: SlotKey) => {
    const query = equipmentSearch[slotKey].toLowerCase().trim();
    console.log(
        `Filtering for slot: ${slotKey}, query: ${query}, selectedType: ${selectedType.value}`
    );

    // 获取所有已选套装（仅用于去重逻辑）
    const selectedSets = Object.entries(selectedEquipmentMap)
        .filter(([key, item]) => item !== null)
        .map(([key, item]) => item!)
        .filter(
            (item, index, self) =>
                self.findIndex((i) => i.enName === item.enName) === index
        );
    console.log(
        "已经选择过的套装：",
        selectedSets.map((s) => ({
            name: s.name,
            enName: s.enName,
            armor: s.armor,
            styles: s.styles,
        }))
    );

    filteredEquipment[slotKey] = [];

    // 类型映射

    // 步骤 1：筛选符合条件的装备（仅当 query 不为空时）
    let matchedEquipment: EquipmentSet[] = [];
    if (query) {
        matchedEquipment = equipmentList.value
            .map((item) => ({ ...item })) // 浅拷贝以避免修改原始数据
            .filter((item) => {
                // 搜索匹配
                const matchesStandardFields =
                    (item.name && item.name.toLowerCase().includes(query)) ||
                    (item.enName && item.enName.toLowerCase().includes(query));

                const matchesNickname = Object.keys(nicknameMap.value).some(
                    (nickname) =>
                        nickname.toLowerCase().includes(query) &&
                        nicknameMap.value[nickname].includes(item.enName || "")
                );

                const matchesSearch = matchesStandardFields || matchesNickname;

                // 部件和类型匹配
                let matchesStyleAndType = false;
                const slotStyle = slotStyleMap[slotKey][0]; // 例如 "头部", "颈部装备"
                if (["ring1", "ring2", "neck"].includes(slotKey)) {
                    matchesStyleAndType =
                        item.styles?.护甲?.[slotStyle]?.["无"] !== undefined;
                } else if (
                    [
                        "mainHand",
                        "offHand",
                        "backbarMainHand",
                        "backbarOffHand",
                    ].includes(slotKey)
                ) {
                    const apiWeaponType =
                        weaponTypeMap[selectedType.value] || "";
                    matchesStyleAndType = Object.keys(
                        item.styles?.武器 || {}
                    ).some(
                        (weaponCategory) =>
                            item.styles?.武器?.[weaponCategory]?.[
                                apiWeaponType
                            ] !== undefined
                    );
                } else {
                    const apiArmorType = armorTypeMap[selectedType.value] || "";
                    matchesStyleAndType =
                        item.styles?.护甲?.[slotStyle]?.[apiArmorType] !==
                        undefined;
                }

                return matchesSearch && matchesStyleAndType;
            });
    }

    // 步骤 2：添加已选套装
    const includeSelectedSets = selectedSets
        .map((selectedItem) => {
            // 从 equipmentList 中找到原始数据以保留默认 icon
            const originalItem = equipmentList.value.find(
                (item) => item.enName === selectedItem.enName
            );
            return originalItem ? { ...originalItem } : null;
        })
        .filter((item): item is EquipmentSet => item !== null)
        .filter((item) => {
            let matchesStyleAndType = false;
            const slotStyle = slotStyleMap[slotKey][0];
            if (["ring1", "ring2", "neck"].includes(slotKey)) {
                matchesStyleAndType =
                    item.styles?.护甲?.[slotStyle]?.["无"] !== undefined;
            } else if (
                [
                    "mainHand",
                    "offHand",
                    "backbarMainHand",
                    "backbarOffHand",
                ].includes(slotKey)
            ) {
                const apiWeaponType = weaponTypeMap[selectedType.value] || "";
                matchesStyleAndType = Object.keys(item.styles?.武器 || {}).some(
                    (weaponCategory) =>
                        item.styles?.武器?.[weaponCategory]?.[apiWeaponType] !==
                        undefined
                );
            } else {
                const apiArmorType = armorTypeMap[selectedType.value] || "";
                matchesStyleAndType =
                    item.styles?.护甲?.[slotStyle]?.[apiArmorType] !==
                    undefined;
            }
            return matchesStyleAndType;
        });

    // 合并结果，去重并按名称排序
    filteredEquipment[slotKey] = [
        ...includeSelectedSets,
        ...matchedEquipment.filter(
            (item) => !includeSelectedSets.some((s) => s.enName === item.enName)
        ),
    ].sort((a, b) => (a.name || "").localeCompare(b.name || ""));

    console.log(`Filtered results for ${slotKey}:`, filteredEquipment[slotKey]);
};
// 清除当前槽位的装备
const clearEquipment = () => {
    if (selectedSlotKey.value) {
        // 清除当前槽位的装备
        buildData.equipment[selectedSlotKey.value as SlotKey] = null;
        selectedEquipmentMap[selectedSlotKey.value as SlotKey] = null;
        // 清空搜索和选择状态
        equipmentSearch[selectedSlotKey.value] = "";
        selectedEquipment.value = null;
        selectedTrait.value = null;
        // 关闭浮窗
        showEquipmentPopup.value = false;
        // 保存到本地存储
        saveToStorage();
        console.log(`Cleared equipment for ${selectedSlotKey.value}`);
    }
};

//更新已选装备
const confirmEquipment = () => {
    console.log("当前选择装备：", selectedEquipment.value);
    console.log("当前选择槽位：", selectedSlotKey.value);
    console.log("当前选择类型：", selectedType.value);
    if (selectedEquipment.value && selectedSlotKey.value) {
        const mappedArmor = selectedEquipment.value.armor || null;
        const equipment: EquipmentSet = {
            ...selectedEquipment.value,
            armor: mappedArmor,
            trait: null,
            enchantment: null,
            styles: selectedEquipment.value.styles,
            type: selectedType.value,
            icon:
                getEquipmentIcon(
                    selectedSlotKey.value as SlotKey,
                    selectedType.value,
                    selectedEquipment.value.styles
                ) || selectedEquipment.value.icon,
        };
        selectedEquipmentMap[selectedSlotKey.value as SlotKey] = equipment;
        buildData.equipment[selectedSlotKey.value as SlotKey] = equipment;
        // 如果选择的是主手武器或备用主手武器，并且是双手武器，则清除对应的副手武器
        if (
            selectedSlotKey.value === "mainHand" &&
            twoHandWeaponTypes.includes(selectedType.value)
        ) {
            buildData.equipment.offHand = null;
            selectedEquipmentMap.offHand = null;
        }
        if (
            selectedSlotKey.value === "backbarMainHand" &&
            twoHandWeaponTypes.includes(selectedType.value)
        ) {
            buildData.equipment.backbarOffHand = null;
            selectedEquipmentMap.backbarOffHand = null;
        }
        saveToStorage();
        showEquipmentPopup.value = false;
        showTraitPopup.value = true;
        console.log(
            `Confirmed equipment for ${selectedSlotKey.value}:`,
            equipment
        );
        console.log("已经选择的装备：", buildData.equipment);
    }
};

// 选择装备
const selectEquipment = (item: EquipmentSet) => {
    selectedEquipment.value = item;
};

// 调整属性点
const adjustAttribute = (
    attr: "health" | "magicka" | "stamina",
    delta: number,
    event: MouseEvent
) => {
    const isShift = event?.shiftKey;
    const amount = isShift ? 10 : 1;
    const current = buildData.basicInfo.attributes[attr];
    const total = attributeTotal.value;
    const maxPoints = 64;

    if (delta > 0) {
        // 加点
        const available = maxPoints - total;
        const add = Math.min(amount * delta, available, maxPoints - current);
        if (add > 0) {
            buildData.basicInfo.attributes[attr] += add;
        }
    } else if (delta < 0) {
        // 减点
        const subtract = Math.min(amount * -delta, current);
        if (subtract > 0) {
            buildData.basicInfo.attributes[attr] -= subtract;
        }
    }
};

// 加载数据
const fetchData = async () => {
    try {
        // 加载技能（保持不变）
        const skillsResponse = await fetch("http://localhost:3000/api/skills");
        if (!skillsResponse.ok) throw new Error("Failed to fetch skills");
        const skillsData = await skillsResponse.json();
        skillTrees.value = skillsData.skill_trees;
        skills.value = skillsData.skills;
        skillVariants.value = skillsData.skill_variants;

        // 加载装备
        const equipmentResponse = await fetch(
            "http://localhost:3000/api/equipment/all"
        );
        if (!equipmentResponse.ok) throw new Error("Failed to fetch equipment");
        const equipmentData = await equipmentResponse.json();
        equipmentList.value = equipmentData
            .filter((item: any) => item && typeof item.name === "string")
            .map((item: any) => {
                // 复制 styles 并处理“巨剑”
                const styles = { ...item.styles };
                // 处理“剑”到“巨剑”
                if (styles?.武器?.双手武器?.剑) {
                    styles.武器.双手武器.巨剑 = { ...styles.武器.双手武器.剑 };
                    delete styles.武器.双手武器.剑;
                }
                // 处理“斧头”到“战斧”
                if (styles?.武器?.双手武器?.斧头) {
                    styles.武器.双手武器.战斧 = {
                        ...styles.武器.双手武器.斧头,
                    };
                    delete styles.武器.双手武器.斧头;
                }
                // 处理“钉锤”到“重锤”
                if (styles?.武器?.双手武器?.钉锤) {
                    styles.武器.双手武器.重锤 = {
                        ...styles.武器.双手武器.钉锤,
                    };
                    delete styles.武器.双手武器.钉锤;
                }

                return {
                    id: item.id as number,
                    name: item.name as string,
                    enName: item.enName as string | undefined,
                    place: item.place as string | undefined,
                    enPlace: item.enplace as string | undefined,
                    icon: item.icon as string | undefined,
                    armor: item.armor || null,
                    styles,
                    type: item.armor || null, // 初始化 type
                };
            }) as EquipmentSet[];
        console.log("Loaded equipmentList:", equipmentList.value.slice(0, 3));

        // 加载 CP 技能、食物、药水、梦达斯之石（保持不变）
        const cpPromises = cpCategories.value.map((category) =>
            fetch(`http://localhost:3000/api/cp/${category.id}`).then((res) =>
                res.json()
            )
        );
        const cpData = await Promise.all(cpPromises);
        cpSkills.value = cpData.flat();

        const foodResponse = await fetch("http://localhost:3000/api/foods");
        if (!foodResponse.ok) throw new Error("Failed to fetch foods");
        const foodData = await foodResponse.json();
        foods.value = foodData
            .filter((item: any) => item && typeof item.name === "string")
            .map((item: any) => ({
                id: item.id as number,
                name: item.name as string,
                enName: item.enName as string,
                ingredients: item.ingredients as Record<string, number>,
                icon: item.icon as string,
                itemTypeText: item.itemTypeText as string,
                quality: item.quality as string,
                description: item.description as string,
                canBeCrafted: item.canBeCrafted as number,
                specializedItemTypeText: item.specializedItemTypeText as string,
            })) as Food[];
        console.log("Loaded foods:", foods.value.slice(0, 3));

        potions.value = [
            {
                id: 1,
                name: "Essence of Health",
                enName: "Essence of Health",
                icon: "/icons/potion1.png",
                description: "Restore Health",
            },
            {
                id: 2,
                name: "Essence of Magicka",
                enName: "Essence of Magicka",
                icon: "/icons/potion2.png",
                description: "Restore Magicka",
            },
        ];

        mundusStones.value = [
            {
                id: 1,
                name: "The Thief",
                enName: "The Thief",
                icon: "/icons/mundus1.png",
                description: "Increase Critical Chance",
            },
            {
                id: 2,
                name: "The Warrior",
                enName: "The Warrior",
                icon: "/icons/mundus2.png",
                description: "Increase Weapon Damage",
            },
        ];

        // 初始化过滤
        equipmentSlots.forEach((slot) => filterEquipment(slot.key as SlotKey));
        filterSkills();

        // 加载本地数据
        loadFromStorage();
    } catch (err) {
        console.error("Fetch error:", err);
    }
};

// 筛选技能
const filterSkills = () => {
    const query = skillSearch.value.toLowerCase();
    filteredSkills.value = skills.value.filter(
        (skill) =>
            skill.name.toLowerCase().includes(query) ||
            (skill.enName?.toLowerCase().includes(query) ?? false)
    );
    filteredSkillVariants.value = skillVariants.value.filter(
        (variant) =>
            variant.name.toLowerCase().includes(query) ||
            (variant.enName?.toLowerCase().includes(query) ?? false)
    );
};

// 保存到本地
const saveToStorage = () => {
    localStorage.setItem("buildData", JSON.stringify(buildData));
};

// 从本地加载
const loadFromStorage = () => {
    const saved = localStorage.getItem("buildData");
    if (saved) {
        const parsed = JSON.parse(saved);
        // 定义类型映射
        const armorTypeMap: Record<string, EquipmentSet["armor"]> = {
            轻甲: "轻甲",
            中甲: "中甲",
            重甲: "重甲",
            随机护甲类型: "随机护甲类型",
            自选护甲类型: "自选护甲类型",
        };
        // 同步 basicInfo
        Object.assign(buildData.basicInfo, parsed.basicInfo || {});
        // 同步 equipment 并更新 selectedEquipmentMap
        Object.entries(parsed.equipment || {}).forEach(([key, item]) => {
            if (
                item &&
                typeof item === "object" &&
                "name" in item &&
                typeof item.name === "string"
            ) {
                const equipment: EquipmentSet = {
                    id: (item as any).id as number | undefined,
                    name: item.name as string,
                    enName: (item as any).enName as string | undefined,
                    icon: (item as any).icon as string | undefined,
                    place: (item as any).place as string | undefined,
                    enPlace: (item as any).enPlace as string | undefined,
                    armor: (item as any).armor || null,
                    styles: (item as any).styles as
                        | EquipmentSet["styles"]
                        | undefined,
                    trait: (item as any).trait as Trait | null | undefined,
                    enchantment: (item as any).enchantment as
                        | Enchantment
                        | null
                        | undefined,
                    type: (item as any).type as string | undefined, // 加载 type 字段
                };
                buildData.equipment[key as SlotKey] = equipment;
                selectedEquipmentMap[key as SlotKey] = equipment;
            }
        });
        // 同步 skills
        Object.assign(buildData.skills, parsed.skills || {});
        // 同步 buffs
        Object.assign(buildData.buffs, parsed.buffs || {});
        // 同步 cpSkills
        buildData.cpSkills = (parsed.cpSkills || []) as ChampionSkill[];
        // 同步 foods（仅同步 buildData.buffs.food）
        if (parsed.buffs?.food && typeof parsed.buffs.food.name === "string") {
            buildData.buffs.food = {
                id: parsed.buffs.food.id as number,
                name: parsed.buffs.food.name as string,
                enName: parsed.buffs.food.enName as string,
                ingredients: parsed.buffs.food.ingredients as Record<
                    string,
                    number
                >,
                icon: parsed.buffs.food.icon as string,
                itemTypeText: parsed.buffs.food.itemTypeText as string,
                quality: parsed.buffs.food.quality as string,
                description: parsed.buffs.food.description as string,
                canBeCrafted: parsed.buffs.food.canBeCrafted as number,
                specializedItemTypeText: parsed.buffs.food
                    .specializedItemTypeText as string,
            };
        }
        // 不覆盖 equipmentList，依赖 fetchData 加载
        console.log("Loaded from storage:", {
            foods: buildData.buffs.food ? [buildData.buffs.food] : [],
            equipmentList: equipmentList.value.slice(0, 3),
            selectedEquipmentMap,
            equipment: buildData.equipment,
        });
    }
};

// 验证基础信息
const validateBasicInfo = () => {
    let valid = true;
    errors.buildName = buildData.basicInfo.buildName ? "" : "构建名称为必填项";
    errors.classId = buildData.basicInfo.classId !== null ? "" : "请选择职业";
    errors.race = buildData.basicInfo.race ? "" : "请选择种族";
    errors.playstyle = buildData.basicInfo.playstyle ? "" : "请选择玩法";
    errors.role = buildData.basicInfo.role ? "" : "请选择位置";
    errors.attributes =
        attributeTotal.value === 64 ? "" : "属性点总和必须为 64";

    if (
        errors.buildName ||
        errors.classId ||
        errors.race ||
        errors.playstyle ||
        errors.role ||
        errors.attributes
    ) {
        valid = false;
    }
    return valid;
};

// 步骤导航
const nextStep = () => {
    if (currentStep.value === 0 && !validateBasicInfo()) return;
    if (currentStep.value < steps.length - 1) {
        currentStep.value++;
        saveToStorage();
    }
};

const previousStep = () => {
    if (currentStep.value > 0) {
        currentStep.value--;
        saveToStorage();
    }
};

const goToStep = (index: number) => {
    if (index === 0 || validateBasicInfo()) {
        currentStep.value = index;
        saveToStorage();
    }
};

// 生成分享代码
const generateShareCode = () => {
    try {
        const data = JSON.stringify(buildData);
        shareCode.value = LZString.compressToBase64(data);
        saveToStorage();
    } catch (error) {
        console.error("Error generating share code:", error);
    }
};

// 复制分享代码
const copyShareCode = async () => {
    try {
        await navigator.clipboard.writeText(shareCode.value);
        alert("分享代码已复制到剪贴板！");
    } catch (err) {
        console.error("Copy failed:", err);
    }
};

// 导入构建
const importBuild = async () => {
    try {
        const decompressed = LZString.decompressFromBase64(importCode.value);
        if (!decompressed) throw new Error("无效的分享代码");
        const parsed = JSON.parse(decompressed);
        Object.assign(buildData.basicInfo, parsed.basicInfo);
        Object.assign(buildData.equipment, parsed.equipment);
        Object.assign(buildData.skills, parsed.skills);
        Object.assign(buildData.buffs, parsed.buffs);
        buildData.cpSkills = parsed.cpSkills || [];
        saveToStorage();
        importCode.value = "";
        alert("构建导入成功！");
    } catch (err) {
        console.error("Import failed:", err);
        alert("导入构建失败，请检查代码");
    }
};

// 初始化
onMounted(() => {
    fetchData().then(() => {
        // 初始化 selectedEquipmentMap
        Object.entries(buildData.equipment).forEach(([key, item]) => {
            if (item) {
                selectedEquipmentMap[key as SlotKey] = item;
            }
        });
        console.log("Initialized selectedEquipmentMap:", selectedEquipmentMap);
    });
});
</script>

<style scoped>
.build-editor {
    max-width: 800px;
    margin: 0 auto;
    background-color: #121113;
    color: #e5e2b9;
    font-family: Arial, sans-serif;
    border: 1px solid #948159;
    border-collapse: collapse;
    font-family: "Mythica Medium", "HYWenHei";
}
.build-editor h2 {
    font-size: 1.4rem;
    margin-bottom: 1rem;
    margin-top: 1rem;
    padding: 1rem 0 1rem 0;
}

.import-section {
    margin-bottom: 20px;
    max-width: 800px;
}

.input-group {
    display: flex;
    gap: 10px;
}

.input-text {
    flex: 1;
    padding: 6px;
    border: 1px solid #444;
    border-radius: 4px;
    background-color: #121113;
    font-family: Microsoft YaHei, Arial, sans-serif;
    color: #e5e2b9;
    font-size: 16px;
    height: 40px;
}

.input-text:focus {
    outline: none;
    border-color: #ffffff;
    box-shadow: 5 5 10px #ffffff;
}

.input-select {
    width: 100%;
    padding: 8px;
    border: 1px solid #444;
    border-radius: 4px;
    background-color: #2a2a2a;
    color: #e5e2b9;
    font-size: 14px;
}

.input-select:focus {
    outline: none;
    border-color: #6b7280;
}

.input-error {
    border-color: #ff5555;
}

.error-text {
    color: #ff5555;
    font-size: 12px;
    margin-top: 4px;
    display: block;
}

.form-text {
    color: #888;
    font-size: 12px;
    margin-top: 4px;
    display: block;
}

.steps-nav {
    display: flex;
    overflow-x: auto;
    padding-bottom: 5px;
    height: 50px;
}

.step-btn {
    padding: 8px 16px;
    border-left: 0px;
    border-right: 1px solid #948159;
    border-bottom: 1px solid #948159;
    border-top: 0px;
    background-color: #000000;
    border-collapse: collapse;
    color: #e5e2b9;
    cursor: pointer;
    font-size: 16px;
    transition: color 0.3s ease;
    flex: auto;
    text-shadow: rgb(25, 25, 25) 0px 0px 1px, rgb(25, 25, 25) 0px 1px 1px,
        rgb(25, 25, 25) 0px 1px 10px;
}

.step-btn:hover {
    color: #ffffff;
}

.step-btn.active {
    border-bottom: 0px;
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    background-color: #121113;
    text-shadow: rgb(0, 0, 0) 0px 0px 1px, rgb(0, 0, 0) 0px 1px 1px,
        rgb(0, 0, 0) 0px 1px 10px;
}

.content-card {
    padding: 0px 20px 20px 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    min-height: 400px;
}

.step-content {
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.form-group {
    margin-bottom: 20px;
    display: block;
    margin-bottom: 8px;
    font-size: 16px;
    font-weight: bold;
}

.required {
    color: #ff5555;
}

.info-grid {
    display: flex;
    gap: 10px;
}

.info-grid > div {
    flex: 1;
}

.option-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.option-btn {
    padding: 8px 16px;
    border: 1px solid #444;
    border-radius: 4px;
    background-color: #121113;
    color: #e5e2b9;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s;
}

.option-btn.active {
    border: 1px solid #6b7280;
    background-color: #3a3a3a;
    color: #ffffff;
    text-shadow: rgb(0, 0, 0) 0px 0px 1px, rgb(0, 0, 0) 0px 1px 1px,
        rgb(0, 0, 0) 0px 1px 10px;
}

.class-group {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
}

.class-btn {
    flex: 1;
    cursor: pointer;
    display: block;
    text-align: center;
}

.class-btn.active {
    color: #ffffff;
    text-shadow: rgb(80, 80, 80) 1px 1px 3px, rgb(80, 80, 80) 1px 2px 3px,
        rgb(80, 80, 80) 1px 3px 3px;
}

.class-btn.active .class-icon {
    filter: brightness(200%);
}

.class-icon {
    display: block;
}

.class-name {
    display: block;
}

.race-grid {
    display: grid;
    max-width: 800px;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 10px;
}

.race-column {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.race-btn {
    cursor: pointer;
    display: block;
    text-align: center;
    align-items: center;
    justify-content: center;
}

.race-btn.active {
    color: #ffffff;
    text-shadow: rgb(80, 80, 80) 1px 1px 3px, rgb(80, 80, 80) 1px 2px 3px,
        rgb(80, 80, 80) 1px 3px 3px;
}

.race-btn.active .race-icon {
    filter: brightness(250%);
}

.race-icon {
    filter: brightness(80%);
    width: 80px;
    height: 80px;
    display: block;
    margin: 0 auto;
}

.race-name {
    display: block;
    margin: 0 auto;
}

.attributes-grid {
    display: flex;
    justify-content: space-between;
    gap: 20px;
}

.attribute-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
}

.progress-ring-bg {
    fill: none;
    stroke: #292929;
    stroke-width: 5;
}

.progress-ring-fill {
    fill: none;
    stroke-width: 5;
    stroke-linecap: round;
    transform: rotate(-90deg);
    transform-origin: center;
    transition: stroke-dasharray 0.3s ease;
}

.attribute-control {
    display: flex;
    align-items: center;
    gap: 0px;
    margin-top: 8px;
}

.control-btn {
    width: 30px;
    height: 30px;
    cursor: pointer;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    user-select: none;
}

.control-btn-icon {
    width: 32px;
    height: 32px;
    user-select: none;
}

.control-btn:hover {
    filter: brightness(200%);
}

.attribute-value {
    width: 40px;
    text-align: center;
    font-size: 16px;
}

.mode-grid {
    display: flex;
}

.mode-column {
    flex: 1;
}

.disease-grid {
    display: flex;
}

.disease-column {
    flex: 1;
}

.disease-group {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    max-width: 320px;
}

.disease-item {
    flex: 1;
    cursor: pointer;
    display: block;
    text-align: center;
}

.disease-item.active {
    color: #ffffff;
    text-shadow: rgb(80, 80, 80) 1px 1px 3px, rgb(80, 80, 80) 1px 2px 3px,
        rgb(80, 80, 80) 1px 3px 3px;
}

.disease-item.active .disease-icon {
    filter: brightness(250%);
}

.disease-icon {
    filter: brightness(80%);
    width: 48px;
    height: 48px;
    display: block;
    margin: 0 auto;
}

.disease-text {
    display: block;
    margin: 0 auto;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}

.btn-primary {
    background-color: #4a4a4a;
    color: #e5e2b9;
}

.btn-primary:hover {
    background-color: #5a5a5a;
}

.btn-secondary {
    background-color: #3a3a3a;
    color: #e5e2b9;
}

.btn-secondary:hover {
    background-color: #4a4a4a;
}

.btn:disabled {
    background-color: #2a2a2a;
    color: #888;
    cursor: not-allowed;
}

.setslot-group {
    border-bottom: 1px solid #3a3a3a;
    font-size: 16px;
    cursor: pointer;
    background-color: #121113;
    height: 60px;
    display: flex;
    align-items: center;
    font-family: "Mythica Medium", "HYWenHei";
}

.setslot-group:hover {
    background-color: #050505;
}

.setslot-group.locked {
    cursor: not-allowed;
    opacity: 0.6;
}

.setslot-group.locked:hover {
    background-color: inherit; /* 移除悬停效果 */
}

.setslot-group:first-child {
    margin-top: 20px;
}

.setslot-group:last-child {
    border-bottom: none;
}

.icon-column {
    width: 5%;
    padding: 10px 0.5rem 10px 1rem;
    vertical-align: middle;
}

.setslot-icon {
    width: 40px;
    height: 40px;
}

.setslot-label {
    width: 18%;
    font-size: 16px;
    color: #e5e2b9;
    font-weight: 700;
    text-align: center;
}

.setslot-info {
    width: 54%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.setslot-bonuse {
    width: 23%;
    font-size: 14px;
    align-items: left;
    text-align: left;
    font-family: "Mythica Medium", "HYWenHei";
}

.setslot-name {
    color: #f5e842;
    font-family: "Mythica Medium", "HYWenHei";
}

.equipment-popup-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
}

.equipment-popup {
    background-color: #121113;
    border: 1px solid #948159;
    border-radius: 8px;
    width: 600px;
    max-height: 90vh;
    padding: 20px;
    animation: slideIn 0.3s ease-in;
    position: relative; /* 确保 armor-popup 相对于 equipment-popup 定位 */
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.popup-header h3 {
    font-size: 20px;
    color: #ffffff;
}

.close-btn {
    background: none;
    border: none;
    color: #e5e2b9;
    font-size: 24px;
    cursor: pointer;
}

.close-btn:hover {
    color: #ff5555;
}

.popup-content {
    display: flex;
    gap: 40px;
}

.search-section {
    flex: 2;
}

.set-input-text {
    padding: 6px;
    border: 1px solid #444;
    border-radius: 4px;
    background-color: #121113;
    font-family: Microsoft YaHei, Arial, sans-serif;
    color: #e5e2b9;
    font-size: 16px;
    height: 30px;
    width: 100%;
}

.equipment-list {
    list-style: none;
    padding: 0;
    margin-top: 10px;
    max-height: 300px;
    overflow-y: auto;
}
.equipment-list::-webkit-scrollbar {
    display: none;
}

.equipment-item {
    display: flex;
    align-items: center;
    padding: 8px;
    border-bottom: 1px solid #191616;
    cursor: pointer;
}

.equipment-item:hover {
    background-color: #1a1a1a;
}

.no-results {
    padding: 8px;
    color: #777777;
}

.filter-section {
    position: relative; /* 保留，为可能的其他子元素提供定位 */
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

@media (max-width: 768px) {
    .equipment-popup {
        width: 90vw;
        padding: 15px;
    }

    .popup-content {
        flex-direction: column;
    }

    .search-section,
    .filter-section {
        flex: auto;
    }
}

.type-options {
    display: grid;
    gap: 10px;
}

.type-option {
    padding: 4px 6px;
    border: 1px solid #948159;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
    text-align: center;
}

.type-option.selected {
    border: 1px solid #6b7280;
    background-color: #3a3a3a;
    color: #ffffff;
    text-shadow: rgb(0, 0, 0) 0px 0px 1px, rgb(0, 0, 0) 0px 1px 1px,
        rgb(0, 0, 0) 0px 1px 10px;
}

.button-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}

.clear-btn {
    background-color: #2a2a2a; /* 深灰色，区别于 confirm-btn 的 #4a4a4a */
    color: #ad0000;
    border: 1px solid #444; /* 添加边框以增强区分 */
    transition: color 0.3s, background-color 0.3s;
}

.clear-btn:hover {
    background-color: #3a3a3a;
    color: red;
}

.confirm-btn {
    align-self: flex-end;
    margin-top: 10px;
    border: 1px solid #444; /* 添加边框以增强区分 */
}

.equipment-item.selected {
    background-color: #3a3a3a;
}

/* 确保弹出框整体样式 */
.enchantment-popup,
.trait-popup {
    background-color: #121113;
    border: 1px solid #948159;
    border-radius: 8px;
    width: 600px;
    max-height: 80vh; /* 限制弹出框高度 */
    padding: 20px;
    animation: slideIn 0.3s ease-in;
    position: relative;
    overflow: hidden; /* 防止内容溢出 */
}

.trait-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.enchantment-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-height: 300px; /* 限制最大高度，约可显示10-12个雕文 */
    overflow-y: auto; /* 启用垂直滚动 */
    padding-right: 8px; /* 为滚动条预留空间 */
}

/* 隐藏默认滚动条（可选，跨浏览器兼容） */
.enchantment-list::-webkit-scrollbar,
.trait-list::-webkit-scrollbar {
    width: 6px; /* 滚动条宽度 */
}

.enchantment-list::-webkit-scrollbar-track,
.trait-list::-webkit-scrollbar-track {
    background: #121113; /* 轨道背景与弹出框一致 */
}

.enchantment-list::-webkit-scrollbar-thumb,
.trait-list::-webkit-scrollbar-thumb {
    background: #3a3a3a; /* 滚动条滑块颜色 */
    border-radius: 3px;
}

.enchantment-list::-webkit-scrollbar-thumb:hover,
.trait-list::-webkit-scrollbar-thumb:hover {
    background: #4a4a4a; /* 悬停时颜色 */
}

.trait-item,
.enchantment-item {
    display: flex;
    align-items: center;
    padding: 8px;
    border-bottom: 1px solid #191616;
    cursor: pointer;
}

.trait-item:hover,
.enchantment-item:hover {
    background-color: #1a1a1a;
}

.trait-info {
    display: flex;
    flex-direction: column;
    margin-left: 8px;
}

.trait-name {
    font-size: 14px;
    color: #e5e2b9;
}

.enchantment-name {
    font-size: 14px;
    color: #eeca2a;
}

.trait-bonuses,
.enchantment-effect {
    font-size: 12px;
    color: #777777;
}

@media (max-width: 768px) {
    .trait-popup,
    .enchantment-popup {
        width: 90vw;
        padding: 15px;
    }

    .type-options {
        flex-direction: row;
        flex-wrap: wrap;
    }
}

.selected-skills {
    display: inline-block;
    gap: 1rem;
    width: auto;
    white-space: nowrap;
}

.skill-frame {
    text-align: center;
    display: inline-block;
    margin: 0px 5px 10px 5px;
    width: 52px;
    height: 52px;
    cursor: pointer;
    border: #444 solid 2px;
}
.skill-icon {
    width: 52px;
    height: 52px;
}

.nav-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}

.result-section {
    margin-bottom: 20px;
}

.result-section h5 {
    font-size: 16px;
    margin-bottom: 10px;
    color: #ffffff;
}

.result-item {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
    font-size: 14px;
}

.result-item strong {
    min-width: 120px;
}

.item-icon {
    width: 32px;
    height: 32px;
    margin-right: 8px;
}

.share-section {
    margin-top: 20px;
}

.share-code {
    margin-top: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.share-code code {
    background-color: #3a3a3a;
    padding: 4px 8px;
    border-radius: 4px;
}

h3 {
    font-size: 20px;
    margin-bottom: 16px;
    color: #ffffff;
}

h5 {
    font-size: 16px;
    margin-bottom: 10px;
}

p,
ul {
    font-size: 14px;
}

ul {
    padding-left: 20px;
}

@media (max-width: 768px) {
    .build-editor {
        padding: 10px;
    }

    .info-grid {
        flex-direction: column;
    }

    .race-grid {
        grid-template-columns: 1fr;
    }

    .attributes-grid {
        flex-direction: column;
        align-items: center;
    }

    .steps-nav {
        flex-wrap: nowrap;
    }

    .step-btn {
        flex: 0 0 auto;
        font-size: 12px;
        padding: 6px 12px;
    }

    .input-group {
        flex-direction: column;
    }

    .input-text {
        width: 100%;
    }
}
</style>
