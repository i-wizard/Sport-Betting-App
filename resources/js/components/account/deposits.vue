<template>
    <div class="card custom-card">
        <div class="card-header d-flex justify-content-between" data-toggle="collapse"
             data-target="#collapseDeposit" aria-expanded="true"
             aria-controls="collapseDeposit">
            <div class="card-title">Deposits</div>
            <span style="color: #fff"><i class="fa fa-chevron-down"></i></span>
        </div>
        <div class="card-body collapse show" id="collapseDeposit" data-parent="#accountAccordion">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                    <tr>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Reference ID</th>
                        <th>Date/Time</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-if="deposits.length" v-for="deposit in deposits">
                        <td>{{deposit.amount | currency('&#8358;')}}</td>
                        <td>{{deposit.is_confirmed ?'Success':'Canceled'}}</td>
                        <td>{{deposit.transaction_uid}}</td>
                        <td>{{formatDateTime(deposit.request_at)}}</td>
                    </tr>
                    <tr v-else>
                        <td colspan="100%" class="text-center">No deposit history.
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
        name: "deposits",
        props: ['wallet_id'],
        data() {
            return {
                deposits: [],
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
            this.getDeposits(this.pagination.current_page);
        },
        methods: {
            formatDateTime(time) {
                return DateTime.fromISO(time).setZone("Africa/Lagos").toFormat("hh':'mm ' 'a',' dd',' LLL yyyy");
            },
            changePage: function (page) {
                this.getDeposits(page);
            },
            getDeposits(page) {
                this.is_loading = false

                axios.get('/account/api/deposits?page=' + page)
                    .then((resp) => {
                        this.deposits = resp.data.results
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

        },
    }
</script>

<style scoped>

</style>