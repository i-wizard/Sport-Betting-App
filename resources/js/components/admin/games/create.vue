<template>
    <div class="card-body">
        <div class="row">
            <div class="col-md-12">
                <div class="alert alert-success" v-if="form_success">
                    Game and all its matches created successfully.
                </div>
                <div class="alert alert-danger" v-if="form_error">
                    {{form_error}}
                </div>
                <div class="form-group" v-if="!form_success">
                    <label class="bmd-label-floating">Games Schedule Date</label>
                    <datetime :use12-hour="true" type="date" value-zone="Africa/Lagos"
                              zone="Africa/Lagos" input-class="form-control"
                              v-model="match_schedule_start_time"></datetime>
                </div>
            </div>
        </div>

        <div class="table-responsive" v-if="!form_success">
            <table class="table">
                <thead class=" text-primary">
                <th>
                    Event&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
                <th>
                    Home Team&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
                <th>
                    Away Team&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
                <th>
                    Start Time&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
                <th>
                    Home Team Odd&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
                <th>
                    Away Team Odd&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
                <th>
                    Draw Odd&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
                <th>
                    Over 2.5 Odd&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
                <th>
                    Under 2.5 Odd&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </th>
<!--                <th>-->
<!--                    Match Statistic&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->
<!--                </th>-->
                </thead>
                <tbody>

                <game-fields v-for="(limit, index) in match_limit" v-on:add_match="populateMatch" :index="index"
                             :added_matches="added_matches" :key="limit"
                             :matches="matches" :events="events"
                             :teams="teams"></game-fields>
                </tbody>
            </table>
        </div>
        <!--<button type="submit" class="btn btn-primary mt-5" @click="createGame" v-if="matchesCheck && !form_success">-->
        <!--Save Game-->
        <!--</button>-->
        <button type="submit" class="btn btn-primary mt-5" @click="createGame" v-if="matchesCheck && !form_success">
            Save Game
        </button>
    </div>
</template>

<script>
    import GameFields from './cp-game-fields'

    export default {
        props: [],
        data() {
            return {
                match_schedule_start_time: '',
                events: [],
                form_success: false,
                teams: [],
                matches: [],
                match_limit: 10,
                added_matches: 0,
                form_error: ''
            }
        },
        components: {
            GameFields
        },
        computed: {
            matchesCheck() {
                if (this.match_schedule_start_time && this.matches.length === 10) {
                    for (let i = 0; i <= this.matches.length - 1; i++) {
                        if ((!this.matches[i].event || this.matches[i].event == '') || (!this.matches[i].home_team || this.matches[i].home_team == '') || (!this.matches[i].away_team || this.matches[i].away_team == '') || (!this.matches[i].match_start_time || this.matches[i].match_start_time == '')) {
                            return false
                        }
                    }
                    return true
                }
                return false
            }
        },
        created() {
            axios.get('/betting/games/creation/data')
                .then((resp) => {
                    this.events = resp.data.events
                    this.teams = resp.data.teams
                })
        },
        methods: {
            populateMatch: function (data) {
                this.added_matches += data.count
                let new_data = data.data
                new_data['role'] = this.added_matches

                this.matches.push(new_data)

//                console.log(this.matches)
            },
            createGame: function () {
                this.form_error = '';

                let formData = {
                    'matches': this.matches,
                    'match_schedule_start_time': this.match_schedule_start_time
                }

                if (this.matches.length < 10) {
                    this.form_error = 'Please fill in all fields.';
                    return false
                }

                axios.post('/betting/create-game', formData, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then((resp) => {
                    this.form_success = true
                }).catch((err) => {
                    this.form_error = err.response.data.non_field_errors instanceof Array ? err.response.data.non_field_errors[0] : err.response.data.non_field_errors
                })
//
            }
        }
    }
</script>

<style scoped>

</style>