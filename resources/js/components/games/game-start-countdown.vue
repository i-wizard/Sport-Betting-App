<template>
    <div class="countdown-container">
        <div class="countdown-content" v-if="is_resulted">Today's games have been concluded, please play tomorrow
            games.
        </div>
        <div class="countdown-content" v-else>
            <div v-if="other_msg">{{other_msg}}</div>
            <div v-else>Today's games starts in: <span>{{countDown}}</span></div>
        </div>
    </div>
</template>

<script>
    import {EventBus} from '../event-bus';

    export default {
        name: "game-start-countdown",
        data() {
            return {
                start_time: null,
                end_time: null,
                timeinterval: null,
                daysSpan: null,
                hoursSpan: null,
                minutesSpan: null,
                secondsSpan: null,
                is_resulted: false,
                other_msg: ''
            }
        },
        computed: {
            countDown() {
                if (this.start_time) {
                    if (new Date(this.start_time) > new Date()) {
                        return `${this.daysSpan}:${this.hoursSpan}:${this.minutesSpan}:${this.secondsSpan}`
                    }
                    this.other_msg = 'Today’s Games already in session please play tomorrow’s games';
                    return true;
                }
            }
        },
        mounted() {
            let that = this;
            EventBus.$on('getGames', function (details) {
                that.other_msg = '';
                that.start_time = details[0].match_start_time;
                that.is_resulted = details[1];

                that.deadline = new Date(Date.parse(new Date(that.start_time)));
                that.initializeClock();
            });

        },
        methods: {
            getTimeRemaining(endtime) {
                var t = Date.parse(endtime) - Date.parse(new Date());
                var seconds = Math.floor((t / 1000) % 60);
                var minutes = Math.floor((t / 1000 / 60) % 60);
                var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
                var days = Math.floor(t / (1000 * 60 * 60 * 24));
                return {
                    'total': t,
                    'days': days,
                    'hours': hours,
                    'minutes': minutes,
                    'seconds': seconds
                };
            },
            initializeClock() {
                this.updateClock();
                this.timeinterval = setInterval(this.updateClock, 1000);
            },
            updateClock() {
                var t = this.getTimeRemaining(this.deadline);
                this.daysSpan = t.days;
                this.hoursSpan = ('0' + t.hours).slice(-2);
                this.minutesSpan = ('0' + t.minutes).slice(-2);
                this.secondsSpan = ('0' + t.seconds).slice(-2);


                if (t.total <= 0) {
                    clearInterval(this.timeinterval);
                }
            }
        }
    }
</script>

<style scoped>
    .countdown-container {
        padding: 8px 15px;
        margin-bottom: 15px;
    }

    .countdown-content {
        color: #2D4239;
        font-size: 15px;
    }

    .countdown-content span {
        color: #E10000;
        font-size: 18px;
        font-weight: 800;
        margin-left: 2px;
    }
</style>