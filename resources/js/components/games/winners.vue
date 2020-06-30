<template>
    <div class="container">
        <div class="row row-50">
            <div class="col-xl-12">
                <!-- Heading Component-->
                <article class="heading-component">
                    <div class="heading-component-inner">
                        <h5 class="heading-component-title">Winners
                        </h5>
                        <div class="heading-component-aside">
                            <ul class="list-inline list-inline-xs list-inline-middle">
                                <li>
                                    <span class="button button-xs button-red-outline"
                                          :class="{'active': active_date===''}" @click="getTodayWinners">Recent
                                    winners</span>
                                </li>
                                <li>
                                    <select class="select select-minimal" @change="reloadWinners($event)"
                                            data-dropdown-class="select-minimal-dropdown"
                                            style="min-width: 110px">
                                        <option value="" selected>Filter by day</option>
                                        <option v-for="day in days" :value="day.date">{{day.day}}</option>
                                    </select>
                                </li>
                            </ul>
                        </div>
                    </div>
                </article>
                <div class="">
                    <div class="__sport_preloader" v-if="is_loading">
                        <div class="preloader-body">
                            <div class="preloader-item"></div>
                        </div>
                    </div>
                    <div class="__sport_issue" v-else-if="!is_loading && winners.length < 1">
                        <div>
                            <div class="__issue_helper">
                                There are no winners at this time.
                            </div>
                        </div>
                    </div>
                    <div class="table-custom-responsive" v-else>
                        <table class="table-custom table-roster team2-blue">
                            <thead>
                            <tr>
                                <th colspan="5">{{winners_date}} <span class="text-center">Top 20 Players</span></th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td>Profile Image</td>
                                <td>Username</td>
                                <td>Score</td>
                                <td>Amount</td>
                                <td>Game ID</td>
                                <td>Phone Number</td>
                            </tr>
                            <tr v-for="winner in winners" :class="{'table-success':user_id == winner.user.id}">
                                <td class="text-center"><img :src="winner.user.profile_image" class="img-circle"
                                                             style="height:35px"></td>
                                <td>{{winner.user.username}}</td>
                                <td><span class="round-badge-sm-score"><span>{{winner.score}}</span></span></td>
                                <td>{{winner.amount_won| currency('&#8358;')}}</td>
                                <td><a :href="'/slip/'+winner.slip_token">{{winner.slip_token}}</a></td>
                                <td>{{winnersPhone(winner.user.phone)}}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {DateTime} from "luxon";
    export default {
        props: ['user_id'],
        data() {
            return {
                days: [],
                winners: [],
                active_date: '',
                today_date: '',
                is_loading: true,
                winners_date: ''
            }
        },
        methods: {
            winnersPhone(phone) {
                if (phone.length > 7) {
                    return `${phone.substr(0, 7)}XXXX`
                }

                return phone;
            },
            seeSlip(slip) {
                window.location = '/slip/' + slip.slip_token
            },
            getTodayWinners() {
                this.active_date = '';
                this.getWinners()
            },
            reloadWinners(event) {
                this.active_date = event.target.value;
                this.getWinners()
            },
            getWinners() {
                this.is_loading = true;
                axios.get(`/betting/winners?q=${this.active_date}`)
                    .then((resp) => {
                        this.winners = resp.data;
                        this.winners_date = (this.winners.length)?DateTime.fromISO(this.winners[0].played_at).setZone("Africa/Lagos").toFormat("yyyy'-'LL'-'dd"):'';
                        this.is_loading = false;
                    }).catch((err) => console.log(err))
            }
        },
        created() {
            this.days = past7Days();
            let d = new Date();

            this.active_date = '';
            this.today_date = d.getFullYear() + '-' + ("0" + (d.getMonth() + 1)).slice(-2) + '-' + ("0" + d.getDate()).slice(-2);
            this.getWinners()
        }
    }
</script>

<style scoped>

</style>