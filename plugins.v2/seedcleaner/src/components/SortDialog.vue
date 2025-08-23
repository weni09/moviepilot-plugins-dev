<template>
<div>
    <!-- 筛选对话框 -->
    <v-dialog v-model="props.dialogShow" max-width="600px">
      <v-card flat class="rounded border filter-card">
        <v-card-title class="text-subtitle-1 d-flex align-center px-3 py-2 bg-primary-lighten-5">
          <v-icon icon="mdi-sort" class="mr-2" color="primary" size="small" />
          <span>排序规则</span>
          <v-spacer></v-spacer>
          <v-btn
            color="grey"
            @click="closeDialog"
            variant="text"
            size="small"
            density="compact"
            icon="mdi-close"
          />
        </v-card-title>
        <v-card-text class="px-3 py-2">
         <!-- 第一行：缺失选项、有无辅种、删除选项 -->
          <v-row class="mb-0 d-flex align-center" gutters="2">
            <v-col :cols="smAndDown ? 12 : 6"  v-for="(item, index) in sortItems" :key="item.key">
             <div class="option-group" :class="smAndDown ? 'option-group-mobile' : 'option-group-fixed'">
                <div class="option-label">
                  <v-icon :icon="item.icon" size="small" class="mr-2" :color="item.color"/>
                  <span class="font-weight-medium">{{ item.title }}</span>
                  <v-spacer></v-spacer>
                  <div class="move-buttons">
                    <v-btn 
                      icon="mdi-arrow-collapse-up"
                      variant="text"
                      size="small"
                      density="comfortable"
                      :disabled="index === 0"
                      @click="moveItemToFirst(index)"
                      class="move-btn"
                      title="移至最前"
                    ></v-btn>
                     <v-btn 
                      icon="mdi-arrow-collapse-down"
                      variant="text"
                      size="small"
                      density="comfortable"
                      :disabled="index === sortItems.length - 1"
                      @click="moveItemToLast(index)"
                      class="move-btn"
                      title="移至最后"
                    ></v-btn>
                    <v-btn 
                      icon="mdi-arrow-up"
                      variant="text"
                      size="small"
                      density="comfortable"
                      :disabled="index === 0"
                      @click="moveItem(index, -1)"
                      class="move-btn"
                      title="移至前一个"
                    ></v-btn>
                    <v-btn 
                      icon="mdi-arrow-down"
                      variant="text"
                      size="small"
                      density="comfortable"
                      :disabled="index === sortItems.length - 1"
                      @click="moveItem(index, 1)"
                      class="move-btn"
                      title="移至后一个"
                    ></v-btn>
                  </div>
                </div>
              <v-radio-group v-model="state.sortOptions[item.key]" inline hide-details class="ma-0 radio-group-styled">
                <div class="d-flex radio-styled">
                  <v-radio label="不排序" :value="null" density="compact"/>
                  <v-radio label="升序" value="asc" density="compact"/>
                  <v-radio label="降序" value="desc" density="compact"/>
                </div>
              </v-radio-group>
            </div>
          </v-col>
        </v-row>
        </v-card-text>
        <div class="px-3 py-2 text--secondary">
          <div class="text-caption d-flex align-center justify-end px-3" style="color:#E91E63">
            <v-icon icon="mdi-information-outline" size="small" class="mr-2"></v-icon>
            <span>注意：前面的排序规则优先级将更高</span>
          </div>
        </div>
        <v-card-actions class="px-3 py-2 d-flex justify-end">
          <v-btn 
            @click="closeDialog"
            variant="outlined"
            size="small"
            class="mr-2"
          >
            <v-icon icon="mdi-close" size="small" class="mr-1"></v-icon>
            取消
          </v-btn>
          <v-btn 
            @click="resetSort"
            variant="outlined"
            size="small"
            class="mr-2"
          >
         <v-icon icon="mdi-refresh" size="small" class="mr-1"></v-icon>
            重置
          </v-btn>
          <v-btn 
            color="primary"
            @click="applySort"
            variant="tonal"
            size="small"
          >
            <v-icon icon="mdi-check" size="small" class="mr-1"></v-icon>
            应用排序
          </v-btn>
        </v-card-actions>
    </v-card>
    </v-dialog>
</div>
</template>

<script setup lang="ts">
import { color } from 'echarts';
import {reactive, ref} from 'vue';
import { SortItem } from './definedFunctions';
// 响应式断点：小屏幕（含）仅显示图标
import { useDisplay } from 'vuetify';
const { smAndDown } = useDisplay();

interface StateModel{
  sortOptions: Record<string, 'asc' | 'desc' | null>;
  sortOptionList: SortItem[];
}

const props = defineProps({
    dialogShow: {
      type: Boolean,
      default: false,
    },
});

const emit = defineEmits(['update:dialogShow','applySort']);

// 默认的排序项配置
const defaultSortItems = [
  { key:"name",
    title:"名称",
    icon:"mdi-alpha-n-circle-outline",
    color:"primary"
 },{ key:"path",
    title:"路径",
    icon:"mdi-folder-outline",
    color:"info"
  },{ key:"size",
    title:"大小",
    icon:"mdi-database-outline",
    color:"success"
  },{ key:"seeds",
    title:"做种数",
    icon:"mdi-seed-outline",
    color:"warning"
  }
];

// 使用ref使sortItems响应式，支持重新排序
const sortItems = ref([...defaultSortItems]);

const defaultSortOptions: Record<string, 'asc' | 'desc' | null> = {
  name: 'asc',
  path: null,
  size: null,
  seeds: null,
};

const state = reactive<StateModel>({
  sortOptions: {...defaultSortOptions},
  sortOptionList: [],
});

const closeDialog = () => {
  emit('update:dialogShow',false);
};

//应用排序
const applySort = () => {
  // 构建排序选项列表
  const sortOptionList: SortItem[] = [];
  sortItems.value.forEach(item => {
    const order = state.sortOptions[item.key];
    if (order !== null) {
      sortOptionList.push({
        key: item.key,
        order: order
      });
    }
  });
  
  state.sortOptionList = sortOptionList;
  closeDialog();
  emit('applySort', sortOptionList);
};

// 移动排序项
const moveItem = (index: number, direction: number) => {
  const newIndex = index + direction;
  
  // 检查边界
  if (newIndex < 0 || newIndex >= sortItems.value.length) {
    return;
  }
  
  // 交换元素
  const items = [...sortItems.value];
  [items[index], items[newIndex]] = [items[newIndex], items[index]];
  sortItems.value = items;
};

// 移动排序项到第一个位置
const moveItemToFirst = (index: number) => {
  if (index === 0) return;
  
  const items = [...sortItems.value];
  const [item] = items.splice(index, 1);
  items.unshift(item);
  sortItems.value = items;
};

// 移动排序项到最后一个位置
const moveItemToLast = (index: number) => {
  if (index === sortItems.value.length - 1) return;
  
  const items = [...sortItems.value];
  const [item] = items.splice(index, 1);
  items.push(item);
  sortItems.value = items;
};

// 重置排序
const resetSort = () => {
  // 重置排序项顺序
  sortItems.value = [...defaultSortItems];
  
  // 重置排序选项
  state.sortOptions = {...defaultSortOptions};
  
  // 重置排序选项列表
  state.sortOptionList = [];
};

// 获取排序选项
const getSortOptions = () => {
  return state.sortOptionList;
};

defineExpose({
  getSortOptions
});
</script>
<style lang="scss" scoped> 
.option-group {
  padding: 8px;
  border-radius: 8px;
  background-color: rgba(var(--v-theme-surface), 0.5);
  border: 1px solid rgba(var(--v-border-color), 0.1);
  transition: all 0.2s ease;
  min-height: 95px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  
  &:hover {
    background-color: rgba(var(--v-theme-surface), 0.8);
    border-color: rgba(var(--v-border-color), 0.2);
  }
}

.option-group-fixed {
  min-height: 75px;
}

.option-group-compact {
  min-height: 85px;
}

.option-group-mobile {
  min-height: 90px; // 减少移动端最小高度
  height: auto;
  padding: 8px; // 减少移动端内边距
  
  // 移动端优化间距
  .option-label {
    margin-bottom: 8px !important; // 减少移动端标签下边距
  }
  
  // 移动端优化输入框
  :deep(.v-text-field .v-field) {
    min-height: 32px !important; // 减少移动端输入框高度
    height: 32px !important;
  }
  
  :deep(.v-text-field .v-field__input) {
    min-height: 32px !important; // 减少移动端输入框高度
    height: 32px !important;
  }
}

.option-label {
  display: flex;
  align-items: center;
  color: rgba(var(--v-theme-on-surface), 0.87);
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.move-buttons {
  display: flex;
  gap: 2px;
}

.move-btn {
  opacity: 0.7;
  transition: all 0.2s ease;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  
  &:hover {
    opacity: 1;
    background-color: rgba(var(--v-theme-surface), 0.5);
  }
  
  &:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }
}

.gap-4 {
  gap: 16px;
}

.radio-group-styled {
  :deep(.v-radio) {
    .v-selection-control {
      min-height: 24px;
    }
    
    .v-label {
      font-size: 0.8rem;
      padding-left: 4px;
    }
  }
  
  :deep(.v-selection-control__wrapper) {
    width: 16px;
    height: 16px;
  }
}

.radio-styled{
  width: 100%;
  justify-content: space-between;
  margin-right: 3.5rem;
}
// 移动端响应式间距调整
@media (max-width: 960px) {
  .gap-4 {
    gap: 8px; // 减少移动端选项之间的间距
  }
  
  .option-group {
    margin-bottom: 4px; // 减少移动端卡片之间的间距
  }
  
  // 移动端行间距调整
  .v-row {
    margin-bottom: 4px !important; // 减少移动端行间距
  }
  
  .move-btn {
    width: 26px;
    height: 26px;
  }
}

// 移除默认边距
.ma-0 {
  margin: 0 !important;
}
</style>