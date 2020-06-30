<template>
    <div class="container">
        <div class="">

        </div>
        <div class="row row-50">
            <div class="col-xl-12">
                <!-- Heading Component-->
                <article class="heading-component">
                    <div class="heading-component-inner">
                        <h5 class="heading-component-title">My Games
                        </h5>
                        <div class="heading-component-aside">
                            <ul class="list-inline list-inline-xs list-inline-middle">
                                <li>
                                    <span class="button button-xs button-red-outline"
                                          :class="{'active': filter_bet === 0}"
                                          @click="reloadSlipFilter(0)">Ongoing</span>
                                </li>
                                <li>
                                    <span class="button button-xs button-red-outline"
                                          :class="{'active': filter_bet > 0}"
                                          @click="reloadSlipFilter(2)">Concluded</span>
                                </li>
                                <li>
                                    <select class="select select-minimal" @change="reloadSlip($event)"
                                            data-dropdown-class="select-minimal-dropdown"
                                            style="min-width: 110px">
                                        <option selected>Filter by day</option>
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
                    <div class="__sport_issue" v-else-if="!is_loading && slips.length < 1">
                        <div>
                            <div class="__issue_helper">
                                There are no games at this time.
                            </div>
                        </div>
                    </div>
                    <div class="row" v-else>
                        <div class="col-12 col-sm-6 col-md-4 result-cont" v-for="slip in slips">
                            <article class="game-result game-result-classic container-cursor"
                                     :class="checkOutcome(slip)" @click="seeSlip(slip)">
                                <div class="__game-result-main">
                                    <div class="result-base-info">
                                        <div class="bet">
                                            Game ID: <span class="token outcome-wrapper">{{ slip.slip_token }}<span
                                                class="game-result-team-label game-result-team-label-top"
                                                :class="checkOutcome(slip)">{{checkOutcomeText(slip)}}</span>
                                    </span>
                                        </div>
                                        <div class="time">
                                            {{ formatDate(slip.played_at) }}
                                        </div>
                                    </div>
                                    <div class="result-content">
                                        <div class="col-4">
                                            <div class="content-cell">
                                                <div class="cell-heading">Point(s)</div>
                                                <div class="score round-badge-sm-score">
                                                    <span>{{slip.score}}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-4">
                                            <div class="content-cell">
                                                <div class="cell-heading">Stake</div>
                                                <div><span class="money">&#8358;</span>{{slip.stake| currency('')}}
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-4">
                                            <div class="content-cell">
                                                <div class="cell-heading">Return</div>
                                                <div><span class="money">&#8358;</span>{{slip.amount_won |
                                                    currency('')}}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="game-result-footer">
                                    <ul class="game-result-details">
                                        <li>
                                            {{formatDateTime(slip.played_at)}}
                                        </li>
                                    </ul>
                                </div>
                            </article>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {DateTime} from "luxon";

    export default {
        props: [],
        data() {
            return {
                days: [],
                slips: [],
                active_date: '',
                is_loading: true,
                filter_bet: 0,
            }
        },
        methods: {
            reloadSlipFilter(action) {
                this.filter_bet = action;
                this.getSlips();
            },
            formatDateTime(time) {
                return DateTime.fromISO(time).setZone("Africa/Lagos").toFormat("hh':'mm' 'a',' dd',' LLL yyyy");
            },
            formatDate(time) {
                const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

                let current_datetime = new Date(time);
                return current_datetime.getDate() + ", " + months[current_datetime.getMonth()] + " " + current_datetime.getFullYear()
            },
            seeSlip(slip) {
                window.location = '/slip/' + slip.slip_token
            },
            checkOutcome(slip) {
                if (slip.game_fate == 0) {
                    return "undefined";
                } else if (slip.game_fate == 1) {
                    return "win";
                } else {
                    return "lose";
                }
            },
            checkOutcomeText(slip) {
                if (slip.game_fate == 0) {
                    return "Ongoing";
                } else if (slip.game_fate == 1) {
                    return "Won";
                } else {
                    return "Lose";
                }
            },
            getSlips() {
                this.is_loading = true;
                axios.get(`betting/slips?q=${this.active_date}&filter=${this.filter_bet}`)
                    .then((resp) => {
                        this.slips = resp.data;
                        this.is_loading = false;
                    }).catch((err) => console.log(err))
            },
            getTodaySlip() {
                this.getSlips()
            },
            reloadSlip(event) {
                this.active_date = event.target.value;
                this.getSlips()
            }
        },
        created() {
            this.days = past7Days();
            this.getSlips()
        }
    }
</script>

<style scoped>

</style>