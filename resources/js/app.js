require('./bootstrap');

import Vue from 'vue';
import Datetime from 'vue-datetime'
import Vue2Filters from 'vue2-filters'
import 'vue-datetime/dist/vue-datetime.css'

Vue.use(Datetime);
Vue.use(Vue2Filters);

// Vue.component('example-component', require('./components/ExampleComponent.vue').default);
Vue.component('login-v', require('./components/auth/login.vue').default);
Vue.component('register', require('./components/auth/register.vue').default);
Vue.component('support', require('./components/support.vue').default);

Vue.component('create-game', require('./components/admin/games/create.vue').default);
Vue.component('edit-game', require('./components/admin/games/edit-game.vue').default);
Vue.component('match-details', require('./components/admin/games/match-details.vue').default);
Vue.component('game-listing', require('./components/games/game-lobby.vue').default);
Vue.component('bets', require('./components/games/bets.vue').default);
Vue.component('winners', require('./components/games/winners.vue').default);

Vue.component('gravatar-selection', require('./components/profile/gravatar-upload.vue').default);

Vue.component('account-details', require('./components/account/index.vue').default);
Vue.component('make-withdrawals', require('./components/account/make-withdrawals.vue').default);

Vue.component('watch-raffle-btn', require('./components/raffle/watch-raffle-btn.vue').default);
Vue.component('raffle-winners', require('./components/raffle/raffle-winners.vue').default);

Vue.component('create-trivia-match', require('./components/trivia/create_match').default);
Vue.component('new-trivia', require('./components/onetime-trivia').default);

const app = new Vue({
    el: '#app'
});
