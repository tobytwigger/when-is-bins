<template>
    <LayoutsHome :home-id="homeId">
        <div class="grid grid-cols-4 divide-x" v-if="!isLoadingBins">
            <BinSetup :home-id="homeId" :position="1" :options="binOptions" :bin="(bins ?? []).find(b => b.position === 1) || null" @updated="loadBins">

            </BinSetup>

            <BinSetup :home-id="homeId" :position="2" :options="binOptions" :bin="(bins ?? []).find(b => b.position === 2) || null" @updated="loadBins">

            </BinSetup>

            <BinSetup :home-id="homeId" :position="3" :options="binOptions" :bin="(bins ?? []).find(b => b.position === 3) || null" @updated="loadBins">

            </BinSetup>

            <BinSetup :home-id="homeId" :position="4" :options="binOptions" :bin="(bins ?? []).find(b => b.position === 4) || null" @updated="loadBins">

            </BinSetup>
        </div>
    </LayoutsHome>
</template>

<script lang="ts" setup>
import type {Bin} from "~/server/utils/drizzle";

const route = useRoute();

const homeId = Number(route.params.id);

const isLoadingBins = ref<boolean>(true)

const bins = ref<Bin[]>([])

const loadBins = () => {
    isLoadingBins.value = true
    $fetch(`/api/home/${homeId}/bins`)
        .then((response) => {
            if(!Array.isArray(response.bins)) {
                bins.value = [response.bins]
            } else {
                bins.value = response.bins || [];
            }
        })
        .catch((error) => {
            console.error(error)
        })
        .finally(() => {
            isLoadingBins.value = false
        })
}

const isLoadingBinOptions = ref<boolean>(true)
const binOptions = ref<string[]>([])
const loadBinOptions = () => {
    isLoadingBinOptions.value = true
    $fetch(`/api/home/${homeId}/bins/options`)
        .then((response) => {
            binOptions.value = response.options || []
        })
        .catch((error) => {
            console.error(error)
        })
        .finally(() => {
            isLoadingBinOptions.value = false
        })
}

onMounted(() => {
    loadBins();
    loadBinOptions();
})

</script>