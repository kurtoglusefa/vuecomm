import { createApp } from 'vue'
import App from './App.vue'


import { BootstrapVueNext } from 'bootstrap-vue-next'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'


import { library } from '@fortawesome/fontawesome-svg-core'
import { faCopy, faSpinner, faPaperPlane, faQuestionCircle, faPencilSquare } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faCopy, faSpinner, faPaperPlane, faQuestionCircle, faPencilSquare)

const app = createApp(App)
app.use(BootstrapVueNext)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
