<template>
    <div class="row row-50 justify-content-center">
        <div class="col-md-10 col-lg-8 col-xl-5">
            <div class="card-login-register">
                <div class="card-top-panel">
                    <div class="card-top-panel-left">
                        <h5 class="card-title card-title-login">Contact Support</h5>
                    </div>
                </div>
                <div class="card-form card-form-login">
                    <form class="rd-form" @submit.prevent="submitComplain">
                        <div class="alert alert-warning" v-show="non_field_errors">
                            {{ non_field_errors }}
                        </div>
                        <div class="form-wrap">
                            <input class="form-input" placeholder="Phone Number" type="tel" v-model="phone"
                                   name="form-input">
                        </div>
                        <div class="form-wrap">
                            <input class="form-input" placeholder="Password" type="password" v-model="password"
                                   name="password">
                        </div>
                        <button class="button button-primary button-block d-flex justify-content-between" type="submit" :disabled="is_loading">
                            <div class="__sport_preloader" v-if="is_loading">
                                <div class="preloader-body reduced">
                                    <div class="preloader-item"></div>
                                </div>
                            </div>
                            <span>Sign in</span>
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: [],
        data() {
            return {
                phone: '',
                password: '',
                non_field_errors: '',
                change_view: false,
                userData: [],
                is_loading: false
            }
        },
        methods: {
            submitComplain: function () {
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
</style>