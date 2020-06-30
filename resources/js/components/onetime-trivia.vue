<template>
    <span class="new-content text-light" v-if="showFlag">New</span>
</template>

<script>
    export default {
        props: [],
        data() {
            return {
                show_flag: false
            }
        },
        mounted() {
            if(!localStorage.seen_flag){
                localStorage.seen_flag = true;
            }
        },
        computed: {
            showFlag(){
                console.log(localStorage.seen_flag ? false : true)
                console.log("STORAGE VALUE: ", localStorage.seen_flag)
                return localStorage.seen_flag ? false : true
            }
        }
    }
</script>
<style scoped>
    .new-content {
        position: absolute;
        background: red;
        border-radius: 10px;
        padding: 4px 6px;
        top: -15px;
        right: 84px;
        font-size: 13px;
    }

    @media(max-width: 1199px) {
        .new-content {
            right: -32px;
        }
    }

</style>