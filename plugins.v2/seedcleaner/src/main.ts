import { createApp } from 'vue'
import App from './App.vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles' // 引入Vuetify样式
import defaults from './vuetify/defaults'
import theme from './vuetify/theme'
import '@mdi/font/css/materialdesignicons.css' // 引入Material Design Icons
// 创建Vuetify实例
const vuetify = createVuetify({
  components,
  directives,
  theme,
  defaults
})

// 创建应用
const app = createApp(App)

// 使用插件
app.use(vuetify)

// 挂载应用
app.mount('#app')