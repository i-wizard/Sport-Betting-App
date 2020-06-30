<template>
    <div class="col-xl-12">
        <!-- Heading Component-->
        <article class="heading-component">
            <div class="heading-component-inner">
                <h5 class="heading-component-title">
                </h5>
                <div class="heading-component-aside">
                    <ul class="list-inline list-inline-xs list-inline-middle">
                        <li>
                            <button type="button" data-toggle="modal" data-target="#depositDialogOld"
                                    class="button button-xs button-default-outline">Deposit (old details)
                            </button>
                        </li>
                        <li>
                            <button type="button" data-toggle="modal" data-target="#depositDialog"
                                    class="button button-xs button-primary-outline">Deposit (new details)
                            </button>
                        </li>
                        <li>
                            <a href="/account/withdrawal"
                               class="button button-xs button-secondary-outline">Withdrawal</a>
                        </li>
                    </ul>
                </div>
            </div>
        </article>

        <div class="row">
            <div class="col-md-12">
                <div class="alert alert-success" v-if="success_message">
                    {{success_message}}
                </div>
                <div class="alert alert-warning" v-if="warning_message">
                    {{warning_message}}
                </div>
                <div class="alert alert-danger" v-if="error_message">
                    {{error_message}}
                </div>
            </div>
        </div>

        <div class="accordion" id="accountAccordion">
            <deposits :wallet_id="wallet_id"></deposits>
            <withdrawals :wallet_id="wallet_id"></withdrawals>
        </div>

        <div id="depositDialogOld" class="modal fade" role="dialog">
            <div class="modal-dialog">

                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title">Deposit from previously used cards</h4>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-info" v-if="chargeIssue">{{chargeIssue}}</div>
                        <div class="row">
                            <div class="col-md-12">
                                <div class="alert alert-success" v-if="formMsg.success_message">
                                    {{formMsg.success_message}}
                                </div>
                                <div class="alert alert-warning" v-if="formMsg.warning_message">
                                    {{formMsg.warning_message}}
                                </div>
                                <div class="alert alert-danger" v-if="formMsg.error_message">
                                    {{formMsg.error_message}}
                                </div>
                            </div>
                        </div>

                        <div class="table-responsive">
                            <table class="table table-striped table-hover">
                                <thead>
                                <tr>
                                    <th></th>
                                    <th>Bank</th>
                                    <th>Credit Card</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-if="authorizations.length" v-for="authorization in authorizations">
                                    <td><input type="radio" id="authorization_code"
                                               v-model="detailsForm.authorization_code"
                                               :value="authorization.authorization_code"></td>
                                    <td for="authorization_code">{{authorization.bank}}</td>
                                    <td>Ending in {{authorization.last4}}</td>
                                </tr>
                                <tr v-else>
                                    <td colspan="100%" class="text-center">No saved credit card.
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="form-wrap">
                            <label>Enter Amount</label>
                            <input type="tel" class="form-input" placeholder="Enter Amount"
                                   v-model="detailsForm.amount" :disabled="is_loading"/>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-dismiss="modal" :disabled="is_loading">Close
                        </button>
                        <button type="button" class="btn btn-success" :disabled="is_loading" @click="makePayment">Make
                            Payment
                        </button>
                    </div>
                </div>

            </div>
        </div>

        <div id="depositDialog" class="modal fade" role="dialog">
            <div class="modal-dialog">

                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title">Make Deposit</h4>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-info" v-if="depositIssue">{{depositIssue}}</div>
                        <div class="form-wrap">
                            <input type="tel" class="form-input" placeholder="Enter Amount"
                                   v-model="deposit_amount"/>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
                        <paystack class="btn btn-success" data-dismiss="modal" :amount="deposit_amount"
                                  :email="email"
                                  :paystackkey="paystackkey"
                                  :callback="callback"
                                  :close="close"
                                  :embed="false" v-if="!depositIssue">Make Payment
                        </paystack>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import deposits from './deposits'
    import withdrawals from "./withdrawals";
    import {Money} from 'v-money'
    import paystack from './paystack'

    export default {
        name: "index",
        props: ['wallet_id', 'balance', 'bonus', 'user_email'],
        data() {
            return {
                deposit_amount: 0,
                paystackkey: "pk_live_5be431bc3e2d4d710306c7b7e3c5b2fba69d1304",
                email: this.user_email,
                money: {
                    decimal: '.',
                    thousands: ',',
                    prefix: '₦',
                    suffix: '',
                    precision: 2,
                    masked: false
                },
                success_message: '',
                error_message: '',
                warning_message: '',
                authorizations: [],
                is_loading: false,
                formMsg: {
                    success_message: '',
                    error_message: '',
                    warning_message: '',
                },
                detailsForm: {
                    amount: '',
                    authorization_code: ''
                }
            }
        },
        components: {
            deposits,
            withdrawals,
            Money,
            paystack
        },
        created() {
            this.getAuthorizations();
        },
        computed: {
            amountInKobo() {
                return this.detailsForm.amount * 100
            },
            depositIssue() {
                if (this.deposit_amount < 100) {
                    return 'Minimum deposit is NGN 100'
                }
                return null;
            },
            chargeIssue() {
                if (this.detailsForm.amount < 100) {
                    return 'Minimum deposit is NGN 100'
                }
                return null;
            }
        },
        methods: {
            makePayment() {
                if (!this.detailsForm.authorization_code) return false;
                this.is_loading = true;

                axios.post('/account/api/charge', {...this.detailsForm}).then((resp) => {
                    this.formMsg.success_message = 'Despot made successfully';
                    window.location.reload();
                }).catch(err => {
                    this.is_loading = false;
                    this.formMsg.error_message = err.response.data.non_field_errors
                })
            },
            getAuthorizations: function () {
                axios.get('/account/api/authorizations').then((resp) => this.authorizations = resp.data)
                    .catch(err => console.log(err));
            },
            callback: function (response) {
                this.deposit_amount = 0
                axios.post('/account/payment/verify', {ref_id: response.trxref}).then((resp) => {
                    if (resp.data.status === 'success') {
                        this.success_message = 'Despot made successfully'
                        window.location.reload()
                    } else {
                        this.warning_message = `Transaction failed! If you think this is an issue then contact support with this reference id: ${resp.data.reference_id}`
                    }
                }).catch((err) => {
                    this.error_message = err.response.data.non_field_errors
                })
            },
            close: function () {
                this.deposit_amount = 0
                console.log("Payment closed")
            }

        }
    }
</script>

<style scoped>

</style>