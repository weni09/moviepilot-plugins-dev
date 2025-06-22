<template>
  <v-card flat class="tool-bar px-2 py-1">
     <v-card-title class="text-subtitle-2 d-flex align-center px-3 py-2 bg-primary-lighten-5">
        <v-icon icon="mdi-magnify" class="mr-2" color="primary" size="small"/>
        <span>扫描选项</span>
      </v-card-title>
    <v-card-text>
      <!-- 缺失选项 -->
      <v-row align="center" no-gutters class="d-flex">
         <v-col cols="2">
          <span class="label-text font-weight-bold">缺失选项：</span>
        </v-col>
        <v-col cols="3">
          <v-checkbox v-model="state.missingOptions.file" label="缺失源文件的种子" hide-details size="small"/>
        </v-col>
        <v-col cols="3">
          <v-checkbox v-model="state.missingOptions.seed" label="缺失种子的源文件" hide-details size="small"/>
        </v-col>
      </v-row>
      <!-- 有无辅种选项 -->
      <v-row align="center" no-gutters class="d-flex">
        <v-col cols="2">
          <span class="label-text font-weight-bold">有无辅种：</span>
        </v-col>
        <v-col cols="10">
          <v-radio-group v-model="state.auxOption" inline hide-details size="small">
            <div class="div-radio-group">
            <v-radio label="全部" value="all"/>
            <v-radio label="无辅种" value="no_aux"/>
            <v-radio label="有辅种" value="has_aux"/>
            </div>
          </v-radio-group>
        </v-col>
      </v-row>

      <!-- 删除选项 -->
      <v-row align="center" no-gutters class="d-flex">
        <v-col cols="2">
          <span class="label-text font-weight-bold">删除选项：</span>
        </v-col>
       <v-col cols="10">
          <v-radio-group v-model="state.removeOption" inline hide-details size="small">
            <div class="div-radio-group">
            <v-radio label="全部" value="all"/>
            <v-radio label="仅删除种子" value="only_torrent"/>
            <!--删除此项-->
            <!-- <v-radio label="仅删除源文件" value="only_data"/> -->
            </div>
          </v-radio-group>
        </v-col>
      </v-row>
      <!-- Tracker 输入框 -->
      <v-row class="mt-2 d-flex" align="center" no-gutters>
        <v-col cols="2">
          <span class="label-text font-weight-bold">Tracker：</span>
        </v-col>
        <v-col cols="10">
          <v-text-field
              v-model="state.trackerInput"
              label="Tracker (多个用分号分隔)"
              placeholder="tracker1.com;tracker2.com"
              variant="outlined"
              density="compact"
              size="small"
          />
        </v-col>
      </v-row>
         <!-- 是否使用存量种子数据 -->
      <v-row class="d-flex" align="center" no-gutters>
        <v-col cols="2">
          <span class="label-text font-weight-bold">是否使用存量种子数据：</span>
        </v-col>
        <v-col cols="10">
           <v-radio-group v-model="state.existingSeedData" inline hide-details size="small">
            <div class="div-radio-group">
            <v-radio label="否" :value="false"/>
            <v-radio label="是" :value="true"/>
            </div>
          </v-radio-group>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
import {reactive} from 'vue';

const state = reactive({
   missingOptions:{
        seed: false,
        file: false
    },
    auxOption:"all",
    removeOption:"all",
    trackerInput:"",
    existingSeedData: false
});

const initParams = ()=>{
  // console.log("initParams called",state);
  state.missingOptions.seed = false;
  state.missingOptions.file = false;
  state.auxOption = 'all';
  state.removeOption = 'all';
  state.trackerInput = '';
  state.existingSeedData = false;
  console.log("state after initParams", state.value); 
}
defineExpose({
  state,
  initParams,
})
</script>
<style lang="scss" scoped>
.label-text {
  font-size: 0.9rem !important;
  line-height: 1.667;
  letter-spacing: 0.0333333333em !important;
  font-family: "Roboto", sans-serif;
  text-transform: none !important;
}
.div-radio-group{
  display: flex;
}
.bg-primary-lighten-5 {
  background-color: rgba(var(--v-theme-primary), 0.07);
}

.border {
  border: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
}
.text-subtitle-2 {
  font-size: 0.9rem !important;
  font-weight: 500;
  margin-bottom: 2px;
}

</style>