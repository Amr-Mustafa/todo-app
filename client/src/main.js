import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';
import Vue from 'vue';
import store from './store'
import App from './App.vue';
import router from './router';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.css';

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons)
Vue.config.productionTip = false;

axios.defaults.baseURL = 'http://localhost:8000/api/'//'http://doit.com/api/';

new Vue({
  router,
  render: (h) => h(App),
  store
}).$mount('#app');
