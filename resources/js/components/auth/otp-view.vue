<template>
    <div>
        <div class="card-login-register" v-if="change_view === false">
            <div class="card-top-panel">
                <div class="card-top-panel-left">
                    <h5 class="card-title card-title-login">Verify OTP</h5>
                </div>
            </div>
            <div class="card-form card-form-login">
                <form class="rd-form" @submit.prevent="saveOtp">
                    <div class="alert alert-warning" v-show="non_field_errors">
                        {{ non_field_errors }}
                    </div>
                    <div class="form-wrap">
                        <input class="form-input" placeholder="Enter OTP" type="tel" v-model="token"
                               name="form-input">
                    </div>
                    <button class="button button-primary button-block d-flex justify-content-between" type="submit"
                            :disabled="is_loading">
                        <div class="__sport_preloader" v-if="is_loading">
                            <div class="preloader-body reduced">
                                <div class="preloader-item"></div>
                            </div>
                        </div>
                        <span>Verify OTP</span>
                    </button>
                </form>
            </div>
        </div>
        <complete-profile-details v-else :user_data="userData"></complete-profile-details>
    </div>
</template>

<script>
    import CompleteProfileDetails from './complete-register'
    export default {
        props: ['phone', 'calling_code'],
        data() {
            return {
                token: '',
                non_field_errors: '',
                change_view: false,
                userData: [],
                is_loading: false
            }
        },
        components: {
            CompleteProfileDetails
        },
        methods: {
            saveOtp: function () {
                let phone = this.phone;
                let calling_code = this.calling_code;
                let token = this.token;
                this.is_loading = true;

                axios.post('/users/verify-otp', {phone: phone, calling_code: calling_code, token: token})
                    .then((resp) => {
                        this.userData = resp.data
                        this.is_loading = false

                        this.enableVIew()
                    })
                    .catch((err) => {
                        this.is_loading = false
                        this.non_field_errors = err.response.data.non_field_errors instanceof Array ? err.response.data.non_field_errors[0] : err.response.data.non_field_errors
                    })
            },
            enableVIew: function () {
                this.change_view = true
            }
        }
    }
</script>

<style scoped>
    .__sport_preloader {
        display: flex;
        justify-content: center;
        flex-direction: row;
        text-align: center;
    }

    .preloader-body.reduced {
        height: 25px;
        width: 25px;
    }
</style>