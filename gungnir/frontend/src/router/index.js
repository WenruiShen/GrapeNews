import Vue from 'vue'
import Router from 'vue-router'
import AboutUs from '@/components/AboutUs'
import Home from '@/components/Home'
import Search from '@/components/Search'
import Settings from '@/components/Settings'
import Signin from '@/components/Signin'
import Signup from '@/components/Signup'
import Timeline from '@/components/Timeline'
import TopicList from '@/components/TopicList'
import Test from '@/components/test'

Vue.use(Router)

export default new Router({
  routes: [
    {path: '/about', name: 'AboutUs', component: AboutUs},
    {path: '/', name: 'Home', component: Home},
    {path: '/search', name: 'Search', component: Search},
    {path: '/settings/:user', name: 'User', component: Settings},
    {path: '/login', name: 'login', component: Signin},
    {path: '/signup', name: 'Signup', component: Signup},
    {path: '/topic/:topicId/timeline', name: 'Timeline', component: Timeline},
    {path: '/topic/list', name: 'TopicList', component: TopicList},
    {path: '/test', name: 'test', component: Test}
  ]
})
