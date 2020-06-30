<template>
  <div>
    <form @submit.prevent="createMatch" method="POST">
      <div class="modal-body">
        <div class="alert alert-success" v-if="form_success">Match created successfully.</div>
        <div class="alert alert-danger" v-if="form_error">{{form_error}}</div>
        <div class="form-group">
          <label class="bmd-label-floating">Event</label>
          <!-- <select class="form-control" v-model="formData.event" name="event" id="event">
            <option value selected disabled>Select Event</option>
            <option v-for="event in events" :value="event.event_name">{{event.event_name}}</option>
          </select> -->

          <input
            type="text"
            v-model="formData.event"
            list="event"
            class="form-control"
          />
          <datalist id="event">
            <option v-for="event in events">{{event.event_name}}</option>
          </datalist>
        </div>
        <div class="form-group">
          <label class="bmd-label-floating">Team A</label>
          <!-- <select v-model="formData.team_a" name="team_a" class="form-control">
            <option value selected disabled>Select First Team</option>
            <option v-for="(team, index) in teams" :key="index" :value="team.name">{{ team.name }}</option>
          </select> -->

          <input
            type="text"
            v-model="formData.team_a"
            list="team_a"
            class="form-control"
          />
          <datalist id="team_a">
            <option v-for="(team, index) in teams">{{ team.name }}</option>
          </datalist>
        </div>
        <div class="form-group">
          <label class="bmd-label-floating">Team B</label>
          <!-- <select v-model="formData.team_b" name="team_b" class="form-control">
            <option value selected disabled>Select Second Team</option>
            <option v-for="(team, index) in teams" :key="index" :value="team.name">{{ team.name }}</option>
          </select> -->

          <input
            type="text"
            v-model="formData.team_b"
            list="team_b"
            class="form-control"
          />
          <datalist id="team_b">
            <option v-for="(team, index) in teams">{{ team.name }}</option>
          </datalist>
        </div>
        <div class="form-group">
          <label class="bmd-label-floating">Team A Logo</label>
          <input
            class="form-control"
            v-model="formData.team_a_logo"
            name="team_a_logo"
            id="team_a_logo"
          />
        </div>
        <div class="form-group">
          <label class="bmd-label-floating">Team B Logo</label>
          <input
            class="form-control"
            v-model="formData.team_b_logo"
            name="team_b_logo"
            id="team_b_logo"
          />
        </div>
        <div class="form-group">
          <label class="bmd-label-floating">Close Entry</label>
          <datetime
            v-model="formData.closed_at"
            :use12-hour="true"
            type="datetime"
            input-class="form-control"
            value-zone="Africa/Lagos"
            zone="Africa/Lagos"
          ></datetime>
        </div>
      </div>
      <div class="modal-footer">
        <button type="submit" class="btn btn-primary" :disabled="is_loading">Save Question</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  props: [],
  data() {
    return {
      events: [],
      is_loading: false,
      form_success: false,
      teams: [],
      formData: {
        event: "",
        team_a: "",
        team_b: "",
        team_a_logo: "",
        team_b_logo: "",
        closed_at: ""
      },
      form_error: ""
    };
  },
  computed: {},
  created() {
    axios.get("/betting/games/creation/data").then(resp => {
      this.events = resp.data.events;
      this.teams = resp.data.teams;
    });
  },
  methods: {
    createMatch: function() {
      this.form_error = "";
      this.is_loading = true;

      if (this.formData.event.length < 1) {
        this.form_error = "Please select event.";
        this.is_loading = false;
        return false;
      } else if (this.formData.team_a.length < 1) {
        this.form_error = "Please select team a.";
        this.is_loading = false;
        return false;
      } else if (this.formData.team_b.length < 1) {
        this.form_error = "Please select team b.";
        this.is_loading = false;
        return false;
      } else if (this.formData.team_a_logo.length < 1) {
        this.form_error = "Please enter team a logo.";
        this.is_loading = false;
        return false;
      } else if (this.formData.team_b_logo.length < 1) {
        this.form_error = "Please enter team b logo.";
        this.is_loading = false;
        return false;
      } else if (this.formData.closed_at.length < 1) {
        this.form_error = "Please enter time for closing entry.";
        this.is_loading = false;
        return false;
      }

      axios
        .post("/trivia/api/create-match", this.formData)
        .then(resp => {
          this.form_success = true;
          setTimeout(() => {
            window.location.reload();
          }, 4000);
        })
        .catch(err => {
          this.is_loading = false;
          this.form_error =
            err.response.data.non_field_errors instanceof Array
              ? err.response.data.non_field_errors[0]
              : err.response.data.non_field_errors;
        });
      //
    }
  }
};
</script>

<style scoped>
</style>