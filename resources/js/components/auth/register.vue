<template>
    <div class="row row-50 justify-content-center">
        <div class="col-md-10 col-lg-8 col-xl-5">
            <div class="card-login-register" v-if="current_view === 1">
                <div class="card-top-panel">
                    <div class="card-top-panel-left">
                        <h5 class="card-title card-title-login">Register</h5>
                    </div>
                </div>
                <div class="card-form card-form-login">
                    <form class="rd-form" @submit.prevent="register">
                        <div class="alert alert-warning" v-show="non_field_errors">
                            {{ non_field_errors }}
                        </div>
                        <div class="form-wrap">
<!--                            <select v-model="calling_code" class="form-input" style="padding: 10px 10px;">-->
<!--                                <option selected value="234">&plus;234</option>-->
<!--                            </select>-->
                            <input class="form-input" placeholder="Phone Number" type="tel" v-model="phone"
                                   name="form-input">
                        </div>
                        <div class="form-wrap form-input-group">
                            By clicking proceed, you confirm that you are over 18 years and agree to our terms and privacy policy.
                        </div>
                        <button class="button button-primary button-block d-flex justify-content-between" type="submit"
                                :disabled="is_loading">
                            <div class="__sport_preloader" v-if="is_loading">
                                <div class="preloader-body reduced">
                                    <div class="preloader-item"></div>
                                </div>
                            </div>
                            <span>Proceed</span>
                        </button>
                        <div class="d-flex justify-content-between mt-4">
                            <a href="/lost-password">Lost Password?</a>
                            <a href="/login">Login</a>
                        </div>
                    </form>
                </div>
            </div>
            <complete-profile-details v-else :user_data="userData"></complete-profile-details>
        </div>
    </div>
</template>

<script>
    import otp from './otp-view';
    import CompleteProfileDetails from './complete-register';
    export default {//
        props: [],
        data() {
            return {
                phone: '',
                // calling_code: '234',
                current_view: 1, // 1 for form view as it is needed before otp is requested, 2 for otp view
                non_field_errors: '',
                userData: [],
                is_loading: false
            }
        },
        components: {
            otp,
            CompleteProfileDetails
        },
        methods: {
            register: function () {
                this.is_loading = true
                let phone = this.phone
                let calling_code = this.calling_code

                axios.post('/users/request-otp', {phone: phone})
                    .then((resp) => {
                        this.userData = resp.data;
                        this.enableOTPVIew()})
                    .catch((err) => {
                        this.is_loading = false;
                        this.non_field_errors = err.response.data.non_field_errors instanceof Array ? err.response.data.non_field_errors[0] : err.response.data.non_field_errors
                    })
            },
            enableOTPVIew: function () {
                this.is_loading = false;
                this.current_view = 2
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