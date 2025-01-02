import { createApp } from 'vue'
import App from './App.vue'

import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

import ArcoVue from '@arco-design/web-vue';
import '@arco-design/web-vue/dist/arco.css';

import router from './router'

const app = createApp(App)
app.use(ElementPlus) // 添加这一行
app.use(router)
app.use(ArcoVue);
app.mount('#app') 