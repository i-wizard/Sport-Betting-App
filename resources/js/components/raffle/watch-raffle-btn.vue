<template>
    <div>
        <button type="button" class="btn watch-raffle-btn flying-btn" v-if="raffleTime" @click="navigateWinners">View Weekend Giveaway Winners
        </button>
<!--        <div class="watch-raffle-dialog" v-if="show_raffle_tv">-->
<!--            <span class="cancel-modal" @click="closeModal">&times;</span>-->
<!--            <div class="__sport_preloader" v-if="is_loading">-->
<!--                <div class="preloader-body">-->
<!--                    <div class="preloader-item"></div>-->
<!--                </div>-->
<!--            </div>-->
<!--            <div class="__sport_issue" v-else-if="raffle_error">-->
<!--                <div>-->
<!--                    <div class="__issue_helper">-->
<!--                        {{raffle_error}}-->
<!--                    </div>-->
<!--                </div>-->
<!--            </div>-->

<!--            <div class="d-flex col-auto content-section" v-else>-->
<!--                <div class="col-md-4 sliding-tray d-flex flex-row justify-content-around" v-if="!done_checking">-->
<!--                    <transition-group tag="div" class="img-slider" name="slide">-->
<!--                        <div v-for="number in [currentRaffle]" v-bind:key="number">-->
<!--                            {{raffle_players[Math.abs(currentRaffle) % raffle_players.length].raffle_hash}}-->
<!--                        </div>-->
<!--                    </transition-group>-->
<!--                </div>-->
<!--                <div class="col-md-8 resulting-view">-->
<!--                    <h6>Weekend Draw Winners</h6><br>-->
<!--                    <div class="table-responsive result-table-view" v-if="winners.length">-->
<!--                        <table class="table table-striped table-hover">-->
<!--                            <thead>-->
<!--                            <tr>-->
<!--                                <th>S/N</th>-->
<!--                                &lt;!&ndash;                                <th>Profile Image</th>&ndash;&gt;-->
<!--                                <th>Username</th>-->
<!--                                <th>Amount</th>-->
<!--                                <th>Raffle ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->
<!--                                </th>-->
<!--                            </tr>-->
<!--                            </thead>-->
<!--                            <tbody>-->
<!--                            <tr v-for="(winner, ind) in winners">-->
<!--                                <td>{{ind+1}}</td>-->
<!--                                &lt;!&ndash;                                <td class="text-center">&ndash;&gt;-->
<!--                                &lt;!&ndash;                                    <img :src="winner.user.profile_image" class="img-circle" style="height:35px">&ndash;&gt;-->
<!--                                &lt;!&ndash;                                </td>&ndash;&gt;-->
<!--                                <td>{{winner.user.username}}</td>-->
<!--                                <td>NGN 5,000.00</td>-->
<!--                                <td>{{winner.raffle_hash}}</td>-->
<!--                            </tr>-->

<!--                            </tbody>-->
<!--                        </table>-->
<!--                    </div>-->
<!--                </div>-->
<!--            </div>-->
<!--        </div>-->
    </div>
</template>

<script>
    import {DateTime} from "luxon";
    import {EventBus} from "../event-bus";

    export default {
        name: "watch-raffle-btn",
        data() {
            return {
                // raffle_players: [],
                // raffle_winners: [],
                // winners: [],
                // show_raffle_tv: false,
                // is_loading: true,
                // raffle_error: null,
                // show: true,
                // currentRaffle: 0,
                // done_checking: false
            }
        },
        mounted() {
            // setInterval(() => {
            //     this.currentRaffle = this.currentRaffle + 1;
            // }, 1000);
            //
            // let that = this;
            // EventBus.$on('raffleData', function () {
            //     setInterval(() => {
            //         if (that.raffle_winners.length && !that.done_checking) {
            //             // console.log("LENGTH OF WINNERS: ", that.raffle_winners)
            //             // console.log("LENGTH OF WINNERS LIST: ", that.winners)
            //             // console.log("LENGTH OF WINNERS LIST 2: ", that.winners[0])
            //
            //             let winner = that.raffle_winners.pop();
            //             that.raffle_players.forEach((player, inx) => {
            //                 console.log("PLAYER: ", player)
            //                 if (JSON.stringify(player) === JSON.stringify(winner.user)) {
            //                     // let winner_index = that.raffle_players.indexOf(winner.user)
            //                     // if (winner_index > -1) {
            //                     console.log("WINNER BEFORE: ", winner.user)
            //                     that.winners.push(winner.user)
            //                     that.raffle_players.splice(inx, 1)
            //
            //                     if (that.raffle_winners.length < 1) {
            //                         that.done_checking = true
            //                         return true
            //                     }
            //                     // }
            //                 }
            //             });
            //         }
            //     }, 10000);
            //
            //     // if(that.done_checking){
            //     //     clearInterval(timer)
            //     // }
            // });
        },
        computed: {
            raffleTime() {
                let date = DateTime.local().setZone("Africa/Lagos");
                let week_day = date.weekday;
                let current_hour = date.hour;
                let current_minute = date.minute;

                if (week_day === 7) {
                    if (current_hour === 20 && current_minute < 11) {
                        return true
                    }
                }
                return false;
            }
        },
        methods: {
            navigateWinners(){
                window.location = '/jackpot/winners';
            }
            // getRaffleDetails() {
            //     axios.get(`/betting/get-raffle-winners`).then((resp) => {
            //         this.raffle_winners = resp.data
            //         if (this.raffle_winners.length < 1) {
            //             this.raffle_error = 'No winners for this week. please try next week.'
            //             return
            //         }
            //         axios.get(`/betting/get-raffle-players`).then((resp) => {
            //             this.raffle_players = resp.data
            //             if (this.raffle_players < 1) {
            //                 this.raffle_error = 'Request not validated. Please reload and try again.'
            //                 return
            //             }
            //
            //             this.is_loading = false;
            //             EventBus.$emit('raffleData')
            //         }).catch((err) => console.log(err))
            //     }).catch((err) => console.log(err))
            // },
            // showTv() {
            //     this.getRaffleDetails();
            //     this.show_raffle_tv = true
            // },
            // closeModal() {
            //     this.show_raffle_tv = false
            // }
        }
    }
</script>

<style scoped>
    .sliding-tray {
        margin-top: 55px;
        position: relative;
        background: transparent;
    }

    .watch-raffle-btn {
        padding: 9px 15px;
        background: #ff4f2e;
        border-color: #FF4120;
        color: #fff;
        box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5)
    }

    .flying-btn {
        position: fixed;
        top: 265px;
        right: 45px;
        z-index: 10
    }

    .watch-raffle-dialog {
        background: rgba(255, 255, 255, .96);
        padding: 25px;
        z-index: 1200;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh
    }

    .content-section {
        position: relative;
        flex-direction: column;
        margin-top: 65px;
    }

    .content-section .sliding-tray {
        text-align: center;
    }

    .watch-raffle-dialog .cancel-modal {
        position: absolute;
        top: 10px;
        left: 8px;
        font-size: 30px;
        font-weight: 600;
        color: #7b7b7b;
        cursor: pointer;
        padding: 5px;
        z-index: 100;
    }


    #demo {
        overflow: hidden;
    }

    .slide-leave-active,
    .slide-enter-active {
        transition: .1s;
    }

    .slide-enter {
        transform: translate(0, 50%);
    }

    .slide-leave-to {
        transform: translate(0, -30%);
    }

    .img-slider {
        overflow: hidden;
        position: relative;
        height: 45px;
    }

    .img-slider div {
        font-size: 24px;
        font-weight: 900;
    }

    .result-table-view {
        max-height: 100vh;
        overflow-y: auto;
        padding-bottom: 30px;
    }

    @media (max-width: 769px) {
        .result-table-view {
            max-height: 75vh;
        }
    }

    @media (min-width: 770px) {
        .content-section {
            flex-direction: row;
            justify-content: space-between;
        }
    }

</style>