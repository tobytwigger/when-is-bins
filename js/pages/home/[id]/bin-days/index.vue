<template>
    <LayoutsHome :home-id="homeId">

        Bin Days
    </LayoutsHome>
</template>

<script lang="ts" setup>
const route = useRoute();

const homeId = Number(route.params.id);

</script>