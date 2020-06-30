<template>
    <tr v-if="matches[index]">
        <td>
            <select class="form-control" v-model="matches[index].event" name="event" id="event">
                <option value="" selected>Select Event</option>
                <option v-for="event in events" :value="event.id">{{event.event_name}}</option>
            </select>

            <!-- <input type="text" v-model="matches[index].event" list="events" class="form-control">
            <datalist id="events">
                <option v-for="event in events" :data-value='event.id'>{{event.event_name}}</option>
            </datalist> -->
        </td>
        <td>
            <select class="form-control" v-model="matches[index].home_team" name="home_team" id="home_team">
                <option value="" selected>Team Name</option>
                <option v-for="team in teams" :value="team.id">{{team.name}}</option>
            </select>

            <!-- <input type="text" v-model="matches[index].home_team" list="home_team" class="form-control">
            <datalist id="home_team">
                <option v-for="team in teams" :data-value='team.id'>{{team.name}}</option>
            </datalist> -->
        </td>
        <td>
            <select class="form-control" v-model="matches[index].away_team" name="away_team" id="away_team">
                <option value="" selected>Team Name</option>
                <option v-for="team in teams" :value="team.id">{{team.name}}</option>
            </select>

            <!-- <input type="text" v-model="matches[index].away_team" list="away_team" class="form-control">
            <datalist id="away_team">
                <option v-for="team in teams" :data-value='team.id'>{{team.name}}</option>
            </datalist> -->
        </td>
        <td>
            <datetime v-model="matches[index].match_start_time" placeholder="Match Start Time"
                      :use12-hour="true" type="datetime" input-class="form-control"
                      value-zone="Africa/Lagos" zone="Africa/Lagos"></datetime>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="home_team_odd" id="home_team_odd"
                   v-model="matches[index].home_team_odd" placeholder="Odd"></money>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="away_team_odd" id="away_team_odd"
                   v-model="matches[index].away_team_odd" placeholder="Odd"></money>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="even_odd" id="even_odd"
                   v-model="matches[index].even_odd" placeholder="Odd"></money>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="ov_twofive" id="ov_twofive"
                   v-model="matches[index].ov_twofive" placeholder="Odd"></money>
        </td>
        <td>
            <money v-bind="money" class="form-control" name="un_twofive" id="un_twofive"
                   v-model="matches[index].un_twofive" placeholder="Odd"></money>
        </td>
<!--        <td>-->
<!--            <input type="text" v-model="matches[index].stat" placeholder="Image URL" class="form-control">-->
<!--        </td>-->
    </tr>
</template>

<script>
    import {Money} from 'v-money'
    export default {
        props: ['matches', 'teams', 'events', 'added_matches', 'index'],
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
        mounted(){
//            console.log("KEY CHECK: ", this.index)
            let data = {
                data: {
                    event: '',
                    home_team: '',
                    away_team: '',
                    match_start_time: '',
                    teams_history: '',
                    home_team_odd: 0.00,
                    away_team_odd: 0.00,
                    even_odd: 0.00,
                    ov_twofive: 0.00,
                    un_twofive: 0.00,
                    // stat: ''
                },
                count: 1
            }

            this.$emit('add_match', data)
        },
        methods: {

        },
        computed: {

        }
    }
</script>

<style scoped>

</style>