import Vue from 'vue'
import Router from 'vue-router'
import VueMaterial from 'vue-material'
import Home from './views/Home.vue'
import Api from './views/Api.vue'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import TextareaAutosize from 'vue-textarea-autosize'

Vue.use(Router)
Vue.use(VueMaterial)
Vue.use(TextareaAutosize)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/api',
      name: 'api',
      component: Api
    }
  ]
})
