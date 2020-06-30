<template>
    <div class="container">
        <div class="row row-50">
            <div class="col-xl-12">
                <!-- Heading Component-->
                <article class="heading-component">
                    <div class="heading-component-inner">
                        <h5 class="heading-component-title">Giveaway Winners
                        </h5>
                        <div class="heading-component-aside">

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
                                There are no winners for the past week.
                            </div>
                        </div>
                    </div>
                    <div class="table-custom-responsive" v-else>
                        <table class="table-custom table-roster team2-blue">
                            <thead>
                            <tr>
                                <th colspan="5">{{week_date}} Winners</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td>Profile Image</td>
                                <td>Username</td>
                                <td>Prize</td>
                                <td>Raffle ID</td>
                            </tr>
                            <tr v-for="winner in winners" :class="{'table-success':user_id == winner.user.user.id}">
                                <td class="text-center"><img :src="winner.user.user.profile_image" class="img-circle" style="height:35px"></td>
                                <td>{{winner.user.user.username}}</td>
                                <td>{{1000| currency('&#8358;')}}</td>
                                <td><a>{{winner.user.raffle_hash}}</a></td>
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
        data() {
            return {
                winners: [],
                is_loading: true,
                week_date: ''
            }
        },
        methods: {
            getWinners(){
                this.is_loading = true;
                axios.get(`/betting/raffle-winners`)
                    .then((resp) => {
                        this.winners = resp.data;
                        this.is_loading = false;
                        this.week_date = DateTime.fromISO(this.winners[0].created_at).setZone("Africa/Lagos").toFormat("yyyy'-'LL'-'dd");
                    }).catch((err) => console.log(err))
            }
        },
        mounted(){
            this.getWinners()
        }
    }
</script>

<style scoped>

</style>