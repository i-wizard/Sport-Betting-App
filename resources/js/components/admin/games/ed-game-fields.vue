<template>
    <tr>
        <td>
            <select class="form-control" @change="changeEvent($event)" :required="true" name="event" id="event">
                <option v-for="event in events" :value="event.id" :selected="event.id === match.event">
                    {{event.event_name}}
                </option>
            </select>

            <!-- <input type="text" @change="changeEvent($event)" :required="true" list="events" class="form-control">
            <datalist id="events">
                <option v-for="event in events" :data-value='event.id'>{{event.event_name}}</option>
            </datalist> -->
        </td>
        <td>
            <select class="form-control" @change="changeHomeTeam($event)" name="home_team" id="home_team">
                <option v-for="team in teams" :value="team.name" :selected="team.name === match.home_team">{{team.name}}</option>
            </select>

            <!-- <input type="text" @change="changeHomeTeam($event)" :required="true" list="home_team" class="form-control">
            <datalist id="home_team">
                <option v-for="team in teams" :data-value='team.id'>{{team.name}}</option>
            </datalist> -->
        </td>
        <td>
            <select class="form-control" @change="changeAwayTeam($event)" name="away_team" id="away_team">
                <option v-for="team in teams" :value="team.name" :selected="team.name === match.away_team">{{team.name}}</option>
            </select>

            <!-- <input type="text" @change="changeAwayTeam($event)" :required="true" list="away_team" class="form-control">
            <datalist id="away_team">
                <option v-for="team in teams" :data-value='team.id'>{{team.name}}</option>
            </datalist> -->
        </td>
        <td>
            <datetime v-model="match.match_start_time" placeholder="Match Start Time"
                      :use12-hour="true" type="datetime" input-class="form-control"
                      value-zone="Africa/Lagos" zone="Africa/Lagos"></datetime>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="home_team_odd" id="home_team_odd"
                   v-model="match.home_team_odd" placeholder="Odd"></money>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="away_team_odd" id="away_team_odd"
                   v-model="match.away_team_odd" placeholder="Odd"></money>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="even_odd" id="even_odd"
                   v-model="match.even_odd" placeholder="Odd"></money>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="ov_twofive" id="ov_twofive"
                   v-model="match.over_two_five" placeholder="Odd"></money>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="un_twofive" id="un_twofive"
                   v-model="match.under_two_five" placeholder="Odd"></money>
        </td>
    </tr>
</template>

<script>
    import {Money} from 'v-money'
    export default {
        name: "ed-game-fields",
        props: ['match', 'events', 'teams'],
        components: {Money},
        data() {
            return {
                money: {
                    decimal: '.',
                    thousands: ',',
                    prefix: '',
                    suffix: '',
                    precision: 2,
                    masked: false
                },
            }
        },
        mounted() {
            this.match.event = this.match.event.id;
        },
        methods: {
            changeEvent(event){
                this.match.event = event.target.value
            },
            changeHomeTeam(event){
                this.match.home_team = event.target.value
            },
            changeAwayTeam(event){
                this.match.away_team = event.target.value
            }
        }
    }
</script>

<style scoped>

</style>