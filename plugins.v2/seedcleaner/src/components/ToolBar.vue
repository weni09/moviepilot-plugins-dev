<template>
  <div class="toolbar-container" :class="{ 'collapsed': isCollapsed }">
         <div class="pa-2 toolbar-content">
          <!-- 第一行：缺失选项、有无辅种、删除选项 -->
          <v-row class="mb-0">
           <v-col :cols="smAndDown ? 12 : 12" :md="smAndDown ? 6 : 4">
            <div class="option-group" :class="smAndDown ? 'option-group-mobile' : 'option-group-fixed'">
              <div class="option-label mb-1">
                <v-icon icon="mdi-alert-circle" size="small" class="mr-2" color="warning"/>
                <span class="font-weight-medium">缺失选项</span>
              </div>
                           <div class="d-flex flex-wrap gap-4">
                 <v-checkbox 
                   v-model="state.missingOptions.file" 
                   label="缺文件的种子" 
                   hide-details
                   density="compact"
                   class="ma-0"
                 />
                 <v-checkbox 
                   v-model="state.missingOptions.seed" 
                   label="缺种的源文件" 
                   hide-details
                   density="compact"
                   class="ma-0"
                 />
               </div>
            </div>
          </v-col>
          
                    <v-col :cols="smAndDown ? 12 : 12" :md="smAndDown ? 6 : 4">
             <div class="option-group" :class="smAndDown ? 'option-group-mobile' : 'option-group-fixed'">
                               <div class="option-label mb-2">
                  <v-icon icon="mdi-seed" size="small" class="mr-2" color="success"/>
                  <span class="font-weight-medium">有无辅种</span>
                </div>
              <v-radio-group v-model="state.auxOption" inline hide-details class="ma-0">
                <div class="d-flex gap-4">
                  <v-radio label="全部" value="all" density="compact"/>
                  <v-radio label="无辅种" value="no_aux" density="compact"/>
                  <v-radio label="有辅种" value="has_aux" density="compact"/>
                </div>
              </v-radio-group>
            </div>
          </v-col>
          
                    <v-col :cols="smAndDown ? 12 : 12" :md="smAndDown ? 12 : 4">
             <div class="option-group" :class="smAndDown ? 'option-group-mobile' : 'option-group-fixed'">
               <div class="option-label mb-2">
                 <v-icon icon="mdi-delete" size="small" class="mr-2" color="error"/>
                 <span class="font-weight-medium">删除选项</span>
               </div>
               <v-radio-group v-model="state.removeOption" inline hide-details class="ma-0">
                 <div class="d-flex gap-4">
                   <v-radio label="全部" value="all" density="compact"/>
                   <v-radio label="仅删除种子" value="only_torrent" density="compact"/>
                 </div>
               </v-radio-group>
             </div>
           </v-col>
        </v-row>

            <!-- 第二行：存量数据、Tracker、名称查询 -->
            <v-row class="mb-0" :class="smAndDown ? 'mt-2' : 'mt-n3'">
           <v-col :cols="smAndDown ? 12 : 12" :md="smAndDown ? 6 : 4">
            <div class="option-group" :class="smAndDown ? 'option-group-mobile' : 'option-group-fixed'">
              <div class="option-label mb-2">
                <v-icon icon="mdi-database" size="small" class="mr-2" color="info"/>
                <span class="font-weight-medium">存量数据</span>
                <v-tooltip location="right" offset="8">
                  <template v-slot:activator="{ props }">
                    <v-icon 
                      v-bind="props"
                      icon="mdi-help-circle" 
                      size="small" 
                      class="ml-1 help-icon" 
                      color="grey-lighten-1" 
                      style="cursor: pointer;"
                    />
                  </template>
                  <span>使用缓存在MoviePilot插件的数据文件进行扫描</span>
                </v-tooltip>
              </div>
             <v-radio-group v-model="state.existingSeedData" inline hide-details class="ma-0">
               <div class="d-flex gap-4">
                 <v-radio label="否" :value="false" density="compact"/>
                 <v-radio label="是" :value="true" density="compact"/>
               </div>
             </v-radio-group>
           </div>
         </v-col>
              <v-col :cols="smAndDown ? 12 : 12" :md="smAndDown ? 6 : 4">
             <div class="option-group" :class="smAndDown ? 'option-group-mobile' : 'option-group-fixed'">
               <div class="option-label mb-2">
                 <v-icon icon="mdi-link" size="small" class="mr-2" color="success"/>
                 <span class="font-weight-medium">Tracker</span>
               </div>
              <v-text-field
                v-model="state.trackerInput"
                label="多个用分号分隔"
                placeholder="tracker1.com;tracker2.com"
                variant="outlined"
                density="compact"
                size="small"
                hide-details
                class="ma-0"
              />
            </div>
          </v-col>
            <v-col :cols="smAndDown ? 12 : 12" :md="smAndDown ? 12 : 4">
              <div class="option-group" :class="smAndDown ? 'option-group-mobile' : 'option-group-fixed'">
                <div class="option-label mb-2">
                   <v-icon icon="mdi-magnify" size="small" class="mr-2" color="info"/>
                   <span class="font-weight-medium">名称查询</span>
                 </div>
               <v-text-field
                 v-model="state.name"
                 label="支持正则表达式(Python)"
                 placeholder="多啦A梦"
                 variant="outlined"
                 density="compact"
                 size="small"
                 hide-details
                 class="ma-0"
               />
             </div>
           </v-col>
                 </v-row>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useDisplay } from 'vuetify';

const { smAndDown } = useDisplay();
const isCollapsed = ref(false);

const state = reactive({
   missingOptions:{
        seed: false,
        file: false
    },
    auxOption:"all",
    removeOption:"all",
    trackerInput:"",
    existingSeedData: false,
    name:""
});

const initParams = () =>{
  // console.log("initParams called",state);
  state.missingOptions.seed = false;
  state.missingOptions.file = false;
  state.auxOption = 'all';
  state.removeOption = 'all';
  state.trackerInput = '';
  state.existingSeedData = false;
  state.name = '';
  // console.log("state after initParams", state.value); 
}

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};

defineExpose({
  state,
  initParams,
  isCollapsed,  // 暴露折叠状态给父组件
  toggleCollapse  // 暴露切换方法给父组件
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
  height: 75px;
  min-height: 75px;
}

.option-group-compact {
  min-height: 85px;
  height: 85px;
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
}

.gap-4 {
  gap: 16px;
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
}

// 移除默认边距
.ma-0 {
  margin: 0 !important;
}

// 缩小选项文字
:deep(.v-checkbox .v-label),
:deep(.v-radio .v-label) {
  font-size: 0.75rem !important;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

// 缩小输入框标签
:deep(.v-text-field .v-field__label) {
  font-size: 0.75rem !important;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

// 缩小输入框占位符
:deep(.v-text-field input::placeholder) {
  font-size: 0.75rem !important;
  color: rgba(var(--v-theme-on-surface), 0.5);
}

// 进一步缩小输入框高度
:deep(.v-text-field .v-field) {
  min-height: 32px !important;
  height: 32px !important;
}

:deep(.v-text-field .v-field__input) {
  min-height: 32px !important;
  height: 32px !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

// 过渡动画相关样式
.transition-button {
  transition: transform 0.3s ease;
}

.rotate-180 {
  transform: rotate(180deg);
}

// 自定义折叠动画容器
.toolbar-container {
  overflow: hidden;
  transition: max-height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 500px; // 设置一个足够大的最大高度
  will-change: max-height;
  transform: translateZ(0); // 启用硬件加速
}

.toolbar-container.collapsed {
  max-height: 0;
}

// 优化折叠动画性能
.toolbar-content {
  will-change: transform;
  transform: translateZ(0); // 启用硬件加速
  backface-visibility: hidden; // 防止闪烁
}

// 优化选项组动画性能
.option-group {
  will-change: transform;
  transform: translateZ(0);
}

// 帮助图标提示框样式 - 基本样式
:deep(.v-tooltip__content) {
  text-align: left !important;
  max-width: 300px !important;
}

// 移动端特殊优化
@media (max-width: 960px) {
  .toolbar-container {
    max-height: 800px; // 移动端增加最大高度
  }
  
  .toolbar-content {
    padding: 4px !important; // 减少移动端容器内边距
  }
  
  // 使用:deep()覆盖Vuetify的.v-col组件padding
  :deep(.v-col-12) {
    padding: 4px 0px !important; // 上下4px
    margin: 0 !important; // 统一设置margin为0
  }
  
  // 移动端卡片间距优化
  .option-group {
    margin-bottom: 6px; // 减少移动端卡片间距
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  // 确保行间距一致
  .v-row {
    margin: 0 !important; // 统一设置行margin为0
  }
  
  // 移动端标签文字大小调整
  .option-label {
    font-size: 0.85rem !important;
    margin-bottom: 8px !important; // 减少移动端标签下边距
  }
  
  // 移动端复选框和单选框标签调整
  :deep(.v-checkbox .v-label),
  :deep(.v-radio .v-label) {
    font-size: 0.8rem !important;
  }
  
  // 移动端输入框标签调整
  :deep(.v-text-field .v-field__label) {
    font-size: 0.8rem !important;
  }
}
</style>