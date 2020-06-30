<template>
    <div class="">
        <button type="button" class="btn btn-success" data-toggle="modal" data-target="#grvatarDialog">Choose Gravatar
        </button>

        <div id="grvatarDialog" class="modal fade" role="dialog">
            <div class="modal-dialog">

                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title">Select Gravatar</h4>
                    </div>
                    <div class="modal-body">
                        <div class="__sport_preloader" v-if="is_loading">
                            <div class="preloader-body">
                                <div class="preloader-item"></div>
                            </div>
                        </div>
                        <div class="grid-container" v-else>
                            <div class="grid-item" v-if="images.length" v-for="image in images"
                                 @click="submitImage(image)">
                                <img :src="image"/>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
                    </div>
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
                is_loading: true,
                images: []
            }
        },
        created(){
            this.getGravatars();
        },
        methods: {
            getGravatars(){
                let numImages = 19;
                for (let i = 1; i <= numImages; i++) {
                    let url = window.location.href;
                    let domain = hostName(url);
                    let image = `${domain}/static/images/logos/teams/team-${i}.png`;
                    this.images.push(image)
                }

                this.is_loading = false
            },
            submitImage(image_url){
                this.is_loading = true
                axios.post('/users/upload-image-url', {img_url: image_url})
                    .then((resp) => {
                        location.reload()
                    }).catch((err) => console.log(err))
            }
        }
    }
</script>

<style scoped>
    * {
        box-sizing: border-box;
    }

    .grid-container {
        max-width: 90%;
        width: 90%;
        margin: 10px auto;
        display: grid;
        grid-auto-rows: 100px;
        grid-template-columns: repeat(auto-fill, minmax(120px, 100px));
        grid-gap: 1em;
    }

    .grid-item {
        cursor: pointer;
        border-radius: 4px;
        border: solid 1px #e1e1e1;
    }

    .grid-item img {
        width: 100%;
        height: 100%;
    }

    @media (max-width: 540px) {
        .grid-container {
            grid-template-columns: repeat(auto-fill, minmax(70px, 100px));
        }
    }

    .__sport_preloader {
        display: flex;
        justify-content: center;
        flex-direction: row;
        text-align: center;

    }

    .preloader-body {
        height: 30px;
        width: 30px;
    }

</style>