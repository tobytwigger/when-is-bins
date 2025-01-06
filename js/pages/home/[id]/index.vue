<template>
    <LayoutsHome :home-id="homeId">

        <div class="flex flex-row justify-end">
            <UButton @click="test" :loading="isTesting">Test</UButton>
        </div>

        <div class="flex flex-col" v-if="selectedCouncil">
            <div class="flex flex-row space-x-4">
                <span class="font-bold">Home Name</span>
                <span>{{home?.name}}</span>
            </div>

            <div class="flex flex-row space-x-4">
                <span class="font-bold">Council</span>
                <span>{{selectedCouncil?.name}}</span>
            </div>

            <div class="flex flex-col ml-4">
                <div class="flex flex-row space-x-4" v-for="key in Object.keys(home?.council_data ?? {})">
                    <span class="font-bold">{{ key }}</span>
                    <span>{{home?.council_data[key]}}</span>
                </div>
            </div>


        </div>
    </LayoutsHome>
</template>

<script lang="ts" setup>
import {Council} from "~/composables/useCouncils";

const route = useRoute();

const toast = useToast();

const {councils, councilSelectSchema, councilKeys} = useCouncils();

const selectedCouncil = computed<Council | null>(() => {
    return councils.find(council => council.key === home.value?.council) || null
})

const homeId = Number(route.params.id);

const home = ref<Home | null>(null)

onMounted(() => {
    loadHome();
})

const isLoadingHome = ref<boolean>(true)

const loadHome = () => {
    isLoadingHome.value = true
    $fetch(`/api/home/${homeId}`)
        .then((response) => {
            home.value = response.home || null
        })
        .catch((error) => {
            console.error(error)
        })
        .finally(() => {
            isLoadingHome.value = false
        })
}

const isTesting = ref<boolean>(false)

const test = () => {
    isTesting.value = true
    $fetch(`/api/home/${homeId}/test`)
        .then((response) => {
            if(response.valid) {
                toast.add({
                    title: 'Success',
                    description: 'Your connection is set up',
                })
            } else {
                toast.add({
                    title: 'Error',
                    description: 'There was an error setting up your connection',
                    color: 'red'
                })
            }
        })
        .catch((error) => {
            toast.add({
                title: 'Error',
                description: 'There was an error setting up your connection',
                color: 'red'
            })
        })
        .finally(() => {
            isTesting.value = false
        })
}

</script>