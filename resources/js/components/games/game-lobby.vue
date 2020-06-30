<template>
    <div class="ct-container">
        <div class="col-lg-auto bt-table">
            <div class="col-lg-9 bt-col-mid">
                <div class="inner-cell">
                    <article class="heading-component">
                        <div class="heading-component-inner">
                            <h5 class="heading-component-title">Highlights
                            </h5>
                            <div>
                                <ul class="list-inline list-inline-xs">
                                    <li><span class="button button-xs button-red-outline"
                                              :class="{'active': is_today_game}" @click="toggleDay(0)">Today’s
                                        games</span></li>
                                    <li><span class="button button-xs button-red-outline"
                                              :class="{'active': !is_today_game}" @click="toggleDay(1)">Tomorrow’s
                                        games</span></li>
                                </ul>
                            </div>
                        </div>
                    </article>

                    <game-countdown></game-countdown>

                    <div class="selection-tip">
                        <div class="tip-heading">
                            <div class="blink"></div>
                            Tips
                        </div>
                        <div class="info-holder d-flex mb-2"
                             :class="{'flex-column': window.width > 992, 'flex-row': window.width < 992}">
                            <div class="">
                                <span class="tip-wager-button">1X2<span></span></span><span> = 3 Points</span>
                            </div>
                            <div :class="{'mt-2': window.width > 992, 'ml-3': window.width < 992}">
                                <span class="tip-wager-button point">Over/Under 2.5</span><span> = 1 Point</span>
                            </div>
                        </div>
                        <div class="info-holder">
                            <small><b>NOTE:</b> The match odds are irrelevant to the outcome. They only act as a guide to reflect the strength of each team.</small>
                        </div>
                    </div>

                    <div class="__sport_preloader" v-if="is_loading">
                        <div class="preloader-body">
                            <div class="preloader-item"></div>
                        </div>
                    </div>
                    <div class="__sport_issue" v-else-if="issues || gameData.length < 1">
                        <div>
                            <div class="__issue_helper">
                                Connection issue, kindly check your network connection.
                            </div>
                            <button type="button" class="btn __issue_btn"
                                    @click="loadPreRequisites((is_today_game)?0:1)">Reload
                            </button>
                        </div>
                    </div>
                    <div class="__sport-table position-relative" :class="{'in-active': is_active}" v-else>
                        <div class="mb-4">

                        </div>
                        <div v-if="is_active && !gameData[9].resulted" class="games-overlay">
                            <div class="overlay-content">Today's games already in session, please play <span
                                    @click="toggleDay(1)" style="color: #ff4f2e; cursor: pointer">tomorrow games</span>
                            </div>
                        </div>
                        <div v-else-if="gameData[9].resulted" class="games-overlay">
                            <div class="overlay-content">Today's games have been concluded, please play <span
                                    @click="toggleDay(1)" style="color: #ff4f2e; cursor: pointer">tomorrow games</span>
                            </div>
                        </div>
                        <div class="__table-tr" v-for="(match, match_index) in gameData" :id="'accordion'+match_index">
                            <div class="d-flex flex-row">
                                <span class="event-figure"><span>{{match_index+1}}</span></span>
                                <div v-if="matchActivityCheck(match)">
                                    <div class="event-schedule" :class="matchActivityClass(match)">
                                        {{matchActivityText(match)}}
                                    </div>
                                </div>
                            </div>
                            <div class="sport-event clearfix">
                                <div class="col-md-8">
                                    <span class="event-title">{{match.event.event_name}}</span>
<!--                                    <a class="example-image-link cursor sport-table-icon"-->
<!--                                       :href="match.clubs_history"-->
<!--                                       data-lightbox="example-1">-->
<!--                                        <span class="fa fa-bar-chart"></span>-->
<!--                                    </a>-->
                                </div>
                                <div class="col-md-4" style="text-align: right">
                                    <span class="sport-event-time">
                                        <span class="fa fa-clock-o"></span>&nbsp; {{eventTime(match.match_start_time)}}
                                    </span>
                                </div>
                            </div>
                            <div class="__games-table">
                                <div class="col-6 col-sm-5 col-md-5 col-lg-5">
                                    <div class="match-details">
                                        <div class="detail-item detail-item-left">
                                            <span class="match-detail-team">{{match.home_team}}</span><span
                                                class="match-detail-team">{{match.away_team}}</span></div>
                                        <div class="detail-item detail-item-right"
                                             v-if="is_active && matchActivityCheck(match) && match.resulted">
                                            <span class="match-detail-team-score"><span>{{match.home_team_score}}</span></span>
                                            <span class="match-detail-team-score"><span>{{match.away_team_score}}</span></span>
                                        </div>
                                    </div>
                                </div>

                                <div class="col-6 col-sm-7 col-md-5 col-lg-5 wins">
                                    <div class="bt-table">
                                        <div class="col-4 col-sm-4 col-md-4 match-module">
                                            <div class="module-bet-wager">
                                                <button type="button" class="wager-button"
                                                        @click="addToSlip(match, 'home')"
                                                        :class="{'active': match.home_team_selected}">
                                                    <span class="wager-button-count">1</span>
                                                </button>
                                            </div>
                                            <div class="module-title">
                                                {{match.home_team_odd}}
                                            </div>
                                        </div>
                                        <div class="col-4 col-sm-4 col-md-4 match-module">
                                            <div class="module-bet-wager">
                                                <button type="button" class="wager-button"
                                                        @click="addToSlip(match, 'even')"
                                                        :class="{'active': match.even_selected}">
                                                    <span class="wager-button-count">X</span>
                                                </button>
                                            </div>
                                            <div class="module-title">
                                                {{match.even_odd}}
                                            </div>
                                        </div>
                                        <div class="col-4 col-sm-4 col-md-4 match-module">
                                            <div class="module-bet-wager">
                                                <button type="button" class="wager-button"
                                                        @click="addToSlip(match, 'away')"
                                                        :class="{'active': match.away_team_selected}">
                                                    <span class="wager-button-count">2</span>
                                                </button>
                                            </div>
                                            <div class="module-title">
                                                {{match.away_team_odd}}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-lg-2" :class="{'pointFiveContainer': window.width < 992}">
                                    <div :class="{'bt-table': window.width < 992}">
                                        <div class="col-4 col-sm-5 col-md-5 col-lg-5" v-if="window.width < 992">
                                            <span style="color: #64DD57;font-weight: bold;">Total Goals</span>
                                        </div>
                                        <div :class="{'col-8 col-sm-7 col-md-5 col-lg-5 ': window.width < 992}"
                                             class="bt-table">


                                            <div class="col-6 col-sm-6 col-md-6 match-module">
                                                <div class="module-bet-wager">
                                                    <button type="button" class="wager-button point"
                                                            @click="addToSlip(match, 'over_two')"
                                                            :class="{'active': match.over_two_five_selected}">
                                                        <span class="wager-button-count"><span class="md-query-pc">OV. 2.5</span>
                                                    <span class="md-query-mobile">Over 2.5</span></span>
                                                    </button>
                                                </div>
                                                <div class="module-title">
                                                    {{match.over_two_five}}
                                                </div>
                                            </div>
                                            <div class="col-6 col-sm-6 col-md-6 match-module">
                                                <div class="module-bet-wager">
                                                    <button type="button" class="wager-button point"
                                                            @click="addToSlip(match, 'under_two')"
                                                            :class="{'active': match.under_two_five_selected}">
                                                        <span class="wager-button-count"><span class="md-query-pc">UN. 2.5</span>
                                                    <span class="md-query-mobile">Under 2.5</span></span>
                                                    </button>
                                                </div>
                                                <div class="module-title">
                                                    {{match.under_two_five}}

                                                </div>
                                            </div>

                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
            <div class="col-lg-3 bt-col-right" :class="modalClass">
                <div class="selection-slip">
                    <span class="cancel-modal md-query-mobile" @click="closeModal">
                        &times;
                    </span>
                    <div class="slip-header">
                        <div>Betslip</div>
                    </div>
                    <div class="slip-body">
                        <div class="__sport_preloader" v-if="is_loading || issues || gameData.length < 1">
                            <div class="preloader-body">
                                <div class="preloader-item"></div>
                            </div>
                        </div>

                        <div v-else>
                            <div class="alert alert-success" v-if="success_msg">
                                <p>{{success_msg}}</p>
                            </div>

                            <div class="stake" v-if="!is_active">
                                &nbsp;{{games_amount | currency('&#8358;')}}
                            </div>
                            <div class="helper" v-if="!is_active">
                                <div class="helper-text">Use from bonus account</div>
                                <input name="input-checkbox-1" v-model="use_bonus" @change="bonusUsage" true-value="1"
                                       false-value="0" type="checkbox" class="checkbox-custom">
                                <!--<input type="checkbox" v-model="use_bonus" @change="bonusUsage" true-value="1"-->
                                <!--false-value="0">-->
                            </div>
                            <div class="slip-action" v-if="!is_active && !betIssues">
                                <button type="button" class="btn bet-btn"
                                        :disabled="submitting"
                                        @click="placeBet">
                                    Play Game
                                </button>
                            </div>

                            <div class="slip-issues" v-if="is_active || betIssues || submissionError">
                                <div v-if="is_active">Game in sessions</div>
                                <div v-else-if="betIssues">{{betIssues}}</div>
                                <div v-else-if="submissionError">{{submissionError}}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <span class="floating-button" @click="toggleModal" v-if="!issues && gameData.length > 1 && modal_state === 0">
            <span class="dot" v-if="slip.selections.length > 0"><span>{{slip.selections.length}}</span></span>
            <span class="content-group">
                <span class="content-self">Play</span>
                <span class="content-self">{{games_amount | currency('&#8358;')}}</span>
            </span>
        </span>
    </div>
</template>

<script>
    import {DateTime} from "luxon";
    import GameCountdown from './game-start-countdown'
    import {EventBus} from '../event-bus';

    export default {
        props: ['logged_in'],
        data() {
            return {
                submitting: false,
                window: {
                    width: 0,
                    height: 0
                },
                is_today_game: true,
                use_bonus: 0,
                balances: {
                    bonus: null,
                    main: null,
                    amount: null
                },
                slip: {
                    selections: [],
                },
                modal_state: 0,
                gameData: [],
                games_amount: 100,
                issues: false,
                is_loading: true,
                is_active: false,
                submissionError: '',
                success_msg: '',
                error_msg: '',
            }
        },
        components: {
            GameCountdown
        },
        computed: {
            selectionCount: function () {
                return 0
            },
            modalClass() {
                if (this.window.width < 992) {
                    if (this.modal_state === 1) {
                        return 'show-dialog';
                    } else {
                        return 'hide-dialog'
                    }
                } else {
                    return 'show-dialog'
                }
            },
            betIssues() {
                if (this.slip.selections.length === 10) {
                    if (this.logged_in) {
                        //console.log("HEY", this.balances)
                        if (this.balances.main < this.games_amount) {
                            return "Your balance is not enough for your selection. Please modify your selection or deposit to your account.";
                        }
                    } else {
                        return "You must be logged in to place a bet.";
                    }
                }
            },
        },
        created() {
            window.addEventListener('resize', this.handleResize)
            this.handleResize();

            this.loadPreRequisites((this.is_today_game) ? 0 : 1);
        },
        destroyed() {
            window.removeEventListener('resize', this.handleResize)
        },
        methods: {
            eventTime(time) {
                time = DateTime.fromISO(time).setZone("Africa/Lagos").toFormat("hh ' : ' mm ' 'a'");
                return time;
            },
            matchActivityClass(match) {
                if (this.matchActivityText(match) === 'live') {
                    return 'status-active';
                } else if (this.matchActivityText(match) === 'concluded') {
                    return 'status-done';
                }
            },
            matchActivityText(match) {
                let start_time = new Date(match.match_start_time);
                let current_time = new Date();

                if (this.matchActivityCheck(match)) {
                    if (start_time < current_time && !match.resulted) {
                        return 'live';
                    } else if (start_time < current_time && match.resulted) {
                        return 'concluded'
                    }
                }
            },
            matchActivityCheck(match) {
                let start_time = new Date(match.match_start_time);
                let current_time = new Date()

                return current_time >= start_time
            },
            toggleDay(day) {
                this.is_today_game = day === 0;
                this.loadPreRequisites((this.is_today_game) ? 0 : 1)
            },
            placeBet() {
                this.submissionError = ''
                if (this.slip.selections.length < 10) {
                    this.submissionError = 'please complete your selection';
                    return false
                }
                this.submitting = true;
                if (!this.logged_in) {
                    window.location = '/login'
                }

                axios.post('/betting/play-game', {
                    games: this.slip.selections,
                    games_amount: this.games_amount,
                    use_bonus: this.use_bonus
                })
                    .then((resp) => {
                        this.success_msg = 'Slip created successfully'
                        setTimeout(() => {
                            window.location.reload()
                        }, 800)
                    }).catch((err) => {
                    this.loadPreRequisites((this.is_today_game) ? 0 : 1);
                    this.games_amount = 100
                })
            },
            bonusUsage() {
                if (this.logged_in) {
                    if (this.use_bonus == 1) {
                        this.balances.amount = this.balances.main + this.balances.bonus;
                        this.balances.bonus -= this.balances.amount
                        this.balances.main += this.balances.amount
                    } else {
                        this.balances.bonus += this.balances.amount
                        this.balances.main -= this.balances.amount
                    }
                }
            },
            closeModal() {
                this.modal_state = 0
            },
            toggleModal() {
                if (this.modal_state === 1) {
                    this.modal_state = 0
                } else {
                    this.modal_state = 1
                }
            },
            handleResize() {
                this.window.width = window.innerWidth;
                this.window.height = window.innerHeight;
            },
            getWalletDetails: function () {
                return axios.get('/account/wallet')
            },
            getGames(date) {
                return axios.get(`/betting/games/${date}`)
            },
            loadPreRequisites(date = 0) {
                this.is_loading = true;
                this.issues = false;
                this.balances.bonus = null;
                this.balances.main = null;
                this.balances.amount = null;
                this.use_bonus = 0;
                this.slip.selections = [];
                this.submissionError = '';
                this.success_msg = '';

                this.getWalletDetails().then((wallet) => {
                    this.balances.bonus = wallet.data.bonus_balance;
                    this.balances.main = wallet.data.balance;
                }).catch((err) => console.log(err));

                this.getGames(date).then((game_resp) => {
                    this.is_loading = false;
                    this.is_active = game_resp.data.is_active;
                    this.gameData = game_resp.data.matches
                    EventBus.$emit('getGames', [this.gameData[0], this.gameData[9].resulted]);

                }).catch((err) => {
//                    console.log(err);
                    this.is_loading = false;
                    this.issues = true;
                })
            },
            alterSelection(match, action, selection, state) {
                if (action === 'add') {
                    let old_rec = match
                    if (selection === 'over_two_five_selected' || selection === 'under_two_five_selected') {
                        if (match.over_two_five_selected || match.under_two_five_selected) return;

                        match[selection] = !state
                    }


                    if (match.home_team_selected || match.away_team_selected || match.even_selected) {
                        if (selection !== 'over_two_five_selected' && selection !== 'under_two_five_selected') {
                            this.games_amount += 50
                        }
                    }

                    if (selection !== 'over_two_five_selected' && selection !== 'under_two_five_selected') {
                        match[selection] = !state
                    }

                    if (this.slip.selections.includes(old_rec)) {
                        let selectionIndex = this.slip.selections.indexOf(old_rec)
                        this.slip.selections[selectionIndex] = match
                    } else {
                        if (!match.over_two_five_selected && !match.under_two_five_selected) return;
                        if (!match.home_team_selected && !match.away_team_selected && !match.even_selected) return;
                        this.slip.selections.push(match)
                    }

                } else {
                    match[selection] = !state

                    if ((!match.home_team_selected && !match.away_team_selected && !match.even_selected)) {
                        if (this.slip.selections.includes(match)) {
                            let selectionIndex = this.slip.selections.indexOf(match)

                            this.slip.selections.splice(selectionIndex, 1)
                        }
                    } else if (!match.over_two_five_selected && !match.under_two_five_selected) {
                        if (this.slip.selections.includes(match)) {
                            let selectionIndex = this.slip.selections.indexOf(match)

                            this.slip.selections.splice(selectionIndex, 1)
                        }
                    }

                    if (selection === 'over_two_five_selected' || selection === 'under_two_five_selected') {
                        return;
                    }
                    if (match.home_team_selected || match.away_team_selected || match.even_selected) {
                        this.games_amount -= 50
                    }
                }
            },
            addToSlip: function (match, selected) {
                this.submissionError = ''
                let action = '';
                let current_state = null;
                let selection = '';
                if (selected === 'home') {
                    if (match.away_team_selected && match.even_selected) return;
                    current_state = match.home_team_selected
                    selection = 'home_team_selected';
                } else if (selected === 'even') {
                    if (match.away_team_selected && match.home_team_selected) return;
                    current_state = match.even_selected
                    selection = 'even_selected';
                } else if (selected === 'away') {
                    if (match.home_team_selected && match.even_selected) return;
                    current_state = match.away_team_selected
                    selection = 'away_team_selected';
                } else if (selected === 'over_two') {
                    current_state = match.over_two_five_selected
                    selection = 'over_two_five_selected';
                } else if (selected === 'under_two') {
                    current_state = match.under_two_five_selected
                    selection = 'under_two_five_selected';
                }

                if (current_state) {
                    action = 'remove'
                } else {
                    action = 'add'
                }

                this.alterSelection(match, action, selection, current_state)
            }
        }
    }
</script>

<style scoped>

</style>