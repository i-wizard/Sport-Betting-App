<template>
    <div class="card custom-card mt-3">
        <div class="card-header d-flex justify-content-between" data-toggle="collapse"
             data-target="#collapseWithdrawal" aria-expanded="true"
             aria-controls="collapseWithdrawal">
            <div class="card-title">Withdrawals</div>
            <span style="color: #fff"><i class="fa fa-chevron-down"></i></span>
        </div>
        <div class="card-body collapse" id="collapseWithdrawal" data-parent="#accountAccordion">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                    <tr>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Reference ID</th>
                        <th>Receiving Bank name</th>
                        <th>Account Name</th>
                        <th>Account Number</th>
                        <th>Date/Time</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-if="withdrawals.length" v-for="withdrawal in withdrawals">
                        <td>{{withdrawal.amount | currency('&#8358;')}}</td>
                        <td>{{withdrawal.transaction_status == 1? withdrawal.is_confirmed ?'Success':'Canceled':'Pending'}}</td>
                        <td>{{withdrawal.transaction_uid}}</td>
                        <td>{{withdrawal.bank_name}}</td>
                        <td>{{withdrawal.bank_account_name}}</td>
                        <td>{{withdrawal.bank_account_number}}</td>
                        <td>{{formatDateTime(withdrawal.request_at)}}</td>
                    </tr>
                    <tr v-else>
                        <td colspan="100%" class="text-center">No withdrawal history.
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <ul class="pagination">
                <li v-if="pagination.current_page > 1" class="page-item previous">
                    <a href="#" aria-label="Previous" class="page-link"
                       @click.prevent="changePage(pagination.current_page - 1)">
                        <span aria-hidden="true">Prev</span>
                    </a>
                </li>
                <li v-for="page in pagesNumber" class="page-item"
                    v-bind:class="[ page == isActived ? 'active' : '']">
                    <a href="#" class="page-link"
                       @click.prevent="changePage(page)">{{ page }}</a>
                </li>
                <li v-if="pagination.current_page < pagination.last_page" class="page-item next">
                    <a href="#" aria-label="Next" class="page-link"
                       @click.prevent="changePage(pagination.current_page + 1)">
                        <span aria-hidden="true">Next</span>
                    </a>
                </li>
            </ul>
        </div>

    </div>
</template>

<script>
    import {DateTime} from "luxon";
    export default {
        name: "withdrawals",
        props: ['wallet_id'],
        data() {
            return {
                withdrawals: [],
                is_loading: true,
                pagination: {
                    total: 0,
                    per_page: 12,
                    from: 1,
                    to: 0,
                    current_page: 1
                },
                offset: 4,
            }
        },
        created() {
            this.getWithdrawals(this.pagination.current_page);
        },
        methods: {
            formatDateTime(time) {
                return DateTime.fromISO(time).setZone("Africa/Lagos").toFormat("hh':'mm ' 'a',' dd',' LLL yyyy");
            },
            changePage: function (page) {
                this.getWithdrawals(page);
            },
            getWithdrawals(page) {
                this.is_loading = false

                axios.get('/account/api/withdrawals?page=' + page)
                    .then((resp) => {
                        this.withdrawals = resp.data.results
                        this.pagination.total = resp.data.count;
                        this.$set(this, 'pagination', resp.data.pagination);
                    }).catch((err) => console.log(err))
            }
        },
        computed: {
            isActived: function () {
                return this.pagination.current_page;
            },
            pagesNumber: function () {
                if (!this.pagination.to) {
                    return [];
                }
                var from = this.pagination.current_page - this.offset;
                if (from < 1) {
                    from = 1;
                }
                var to = from + (this.offset * 2);
                if (to >= this.pagination.last_page) {
                    to = this.pagination.last_page;
                }
                var pagesArray = [];
                while (from <= to) {
                    pagesArray.push(from);
                    from++;
                }
                return pagesArray;
            }
//
        }
    }
</script>

<style scoped>

</style>