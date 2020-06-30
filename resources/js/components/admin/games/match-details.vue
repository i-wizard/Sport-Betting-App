<template>
    <div class="table-responsive">
        <table class="table">
            <thead class=" text-primary">
            <th>
                Event
            </th>

            <th>
                Home Team
            </th>
            <th>
                Away Team
            </th>
            <th>
                Home Team Score
            </th>
            <th>
                Away Team Score
            </th>
            <th>
                Actions
            </th>
            </thead>
            <tbody>
            <tr v-if="table_loading">
                <td colspan="100%" class="text-center text-primary">Fetching data...
                </td>
            </tr>
            <tr v-else-if="!table_loading && matches.length > 0" v-for="match in matches">
                <td>{{ match.event.event_name }}</td>
                <td>
                    {{ match.home_team }}
                </td>
                <td>
                    {{ match.away_team }}
                </td>
                <td v-if="match.resulted">{{ match.home_team_score }}</td>
                <td v-if="match.resulted">{{ match.away_team_score }}</td>
                <td v-if="!match.resulted"><input type="tel" class="form-control"
                                                  v-model="match.home_team_score" :readonly="is_loading"/></td>
                <td v-if="!match.resulted"><input type="tel" class="form-control"
                                                  v-model="match.away_team_score" :readonly="is_loading"/></td>
                <td v-if="!match.resulted">
                    <button type="button" class="btn btn-primary" @click="saveScore(match)"
                            v-if="!is_success" :id="'update-'+match.id">
                        Update Score
                    </button>
                </td>
                <td v-else></td>
            </tr>
            <tr v-else>
                <td colspan="100%" class="text-center text-primary">Request could not be
                    validated. Please contact developers for support.
                </td>
            </tr>
            </tbody>
        </table>
    </div>

</template>

<script>

    export default {
        props: ['game_id', 'game_over', 'game_active'],
        data() {
            return {
                is_loading: false,
                is_success: false,
                table_loading: true,
                matches: []
            }
        },
        created() {
            this.getMatches()
        },
        methods: {
            saveScore: function (match) {
                let result = confirm('Are you sure you want to result this game?');
                if (result) {
                    let button = `update-${match.id}`;

                let bt = document.getElementById(button);
                bt.disabled = true;

                let matchIndex = this.matches.indexOf(match)

                let match_record = this.matches[matchIndex]

                axios.post(`/betting/game/${this.game_id}/matches`, {
                    id: match.id,
                    home_team_score: match_record.home_team_score,
                    away_team_score: match_record.away_team_score
                })
                    .then((resp) => {
                        window.location = `/admin/games/matches/update/success/${this.game_id}`
                    }).catch((err) => {
                    if (err.response) {
                        bt.disabled = false;
                        alert(err.response.data.response)
                    }
                })
                }
            },
            getMatches() {
                axios.get(`/betting/game/${this.game_id}/matches`)
                    .then((resp) => {
                        this.matches = resp.data
                        this.table_loading = false
                    }).catch((err) => console.log(err))
            }
        }
    }
</script>

<style scoped>

</style>