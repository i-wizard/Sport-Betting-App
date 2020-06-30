<template>
    <div class="card-login-register">
        <div class="card-top-panel">
            <div class="card-top-panel-left">
                <h5 class="card-title card-title-login">Complete Profile Details</h5>
            </div>
        </div>
        <div class="card-form card-form-login">
            <form class="rd-form" @submit.prevent="submitDetails">
                <div class="alert alert-warning" v-show="non_field_errors">
                    {{ non_field_errors }}
                </div>
                <div class="form-wrap" :class="{'has-error':formErrors.username}">
                    <input class="form-input" placeholder="Username" type="text" v-model="formData.username"
                           name="form-input">
                    <div class="form-output error" v-if="formErrors.username">
                        {{formErrors.username[0]}}
                    </div>
                </div>
                <div class="form-wrap position-relative">
                    <input class="form-input" placeholder="Enter Password" type="password" v-model="formData.password" id="reg-password">
                    <span @click="passwordVisibilityToggle" class="position-absolute password-eye">
                                <span class="fa fa-eye" v-if="password_stat"></span>
                                <span class="fa fa-eye-slash" v-else></span>
                            </span>
                </div>
                <div class="form-wrap position-relative">
                    <input class="form-input" placeholder="Retype Password" type="password" v-model="formData.retype_password" id="reg-retype-password">
                    <span @click="retypePasswordVisibilityToggle" class="position-absolute password-eye">
                                <span class="fa fa-eye" v-if="retype_password_stat"></span>
                                <span class="fa fa-eye-slash" v-else></span>
                            </span>
                </div>
                <div class="form-wrap position-relative" :class="{'has-error':formErrors.email}">
                    <input class="form-input" placeholder="Enter Valid Email Address" type="email" v-model="formData.email">
                    <div class="form-output error" v-if="formErrors.email">
                        {{formErrors.email[0]}}
                    </div>
                </div>
                <div class="form-wrap">
                    <input class="form-input" placeholder="Referral Code (optional)" type="text" v-model="formData.referral_code">
                </div>
                <button class="button button-primary button-block d-flex justify-content-between" type="submit" :disabled="is_loading">
                    <div class="__sport_preloader" v-if="is_loading">
                        <div class="preloader-body reduced">
                            <div class="preloader-item"></div>
                        </div>
                    </div>
                    <span>Save Details</span>
                </button>
            </form>
        </div>
    </div>
</template>

<script>

    export default {
        props: ['user_data'],
        data() {
            return {
                non_field_errors: '',
                formErrors: [],
                formData: {
                    username: '',
                    password: '',
                    retype_password: '',
                    email: '',
                    phone: this.user_data.phone,
                    referral_code: ''
                },
                is_loading: false,
                password_stat: true,
                retype_password_stat: true
            }
        },
        methods: {
            passwordVisibilityToggle(){
                this.password_stat = !this.password_stat;
                showPassword('reg-password')
            },
            retypePasswordVisibilityToggle(){
                this.retype_password_stat = !this.retype_password_stat;
                showPassword('reg-retype-password')
            },
            submitDetails: function () {
                this.is_loading = true;
                axios.post('/users/profile-completion', this.formData)
                    .then((resp) => {
                        this.is_loading = false;
                        window.location = this.user_data.is_staff ? '/admin' : '/'
                    })
                    .catch((err) => {
                        this.is_loading = false;
                        if(err.response.data.non_field_errors){
                            this.non_field_errors = err.response.data.non_field_errors instanceof Array ? err.response.data.non_field_errors[0] : err.response.data.non_field_errors
                        }else{
                            this.formErrors = err.response.data?err.response.data:[]
                        }
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

    .password-eye {
        top: 30%;
        right: 15px;
        font-size: 17px;
        color: #4A5B5E;
        font-weight: 900;
        cursor: pointer;
    }
</style>