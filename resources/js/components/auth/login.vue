<template>
    <div class="row row-50 justify-content-center">
        <div class="col-md-10 col-lg-8 col-xl-5">
            <div class="card-login-register" v-if="change_view === false">
                <div class="card-top-panel">
                    <div class="card-top-panel-left">
                        <h5 class="card-title card-title-login">Login</h5>
                    </div>
                </div>
                <div class="card-form card-form-login">
                    <form class="rd-form" @submit.prevent="login">
                        <div class="alert alert-warning" v-show="non_field_errors">
                            {{ non_field_errors }}
                        </div>
                        <div class="form-wrap">
                            <label>Phone number</label>
                            <input class="form-input" placeholder="Phone Number" type="tel" v-model="phone"
                                   name="form-input">
                        </div>
                        <label>Password</label>
                        <div class="form-wrap position-relative">
                            <input class="form-input" placeholder="Password" type="password" v-model="password"
                                   name="password" id="login-password">
                            <span @click="passwordVisibilityToggle" class="position-absolute password-eye">
                                <span class="fa fa-eye" v-if="password_stat"></span>
                                <span class="fa fa-eye-slash" v-else></span>
                            </span>
                        </div>
                        <button class="button button-primary button-block d-flex justify-content-between" type="submit"
                                :disabled="is_loading">
                            <div class="__sport_preloader" v-if="is_loading">
                                <div class="preloader-body reduced">
                                    <div class="preloader-item"></div>
                                </div>
                            </div>
                            <span>Sign in</span>
                        </button>
                        <div class="d-flex justify-content-between mt-4">
                            <a href="/lost-password">Lost Password?</a>
                            <a href="/register">Register</a>
                        </div>
                    </form>
                </div>
            </div>
            <complete-profile-details v-else :user_data="userData"></complete-profile-details>
        </div>
    </div>
</template>

<script>
    import CompleteProfileDetails from './complete-register'

    export default {
        props: [],
        data() {
            return {
                phone: '',
                password: '',
                non_field_errors: '',
                change_view: false,
                userData: [],
                is_loading: false,
                password_stat: true
            }
        },
        components: {
            CompleteProfileDetails
        },
        methods: {
            passwordVisibilityToggle(){
                this.password_stat = !this.password_stat;
                showPassword('login-password')
            },
            login: function () {
                this.is_loading = true
                axios.post('/users/session-login', {phone: this.phone, password: this.password})
                    .then((resp) => {
                        this.is_loading = false;
                        if (resp.status === 200) {
                            window.location = resp.data.is_staff ? '/admin' : '/'
                        } else if (resp.status === 203) {
                            this.userData = resp.data
                            this.enableVIew()
                        }
                    }).catch((err) => {
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
<style scope>
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

    .password-eye {
        top: 30%;
        right: 15px;
        font-size: 17px;
        color: #4A5B5E;
        font-weight: 900;
        cursor: pointer;
    }
</style>