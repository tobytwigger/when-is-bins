<script setup lang="ts">
const props = withDefaults(defineProps<{
    value: {
        uprn: null|string
    }
}>(), {
    value: {
        uprn: null
    }
});

const emit = defineEmits<{
    (event: 'update:value', value: object): void
}>();

const dynamicModel = computed<object>({
    get() {
        return props.value;
    },
    set(value: object) {
        emit('update:value', value);
    }
});

</script>

<template>
    <UFormGroup label="UPRN" hint="Find your house UPRN at https://www.findmyaddress.co.uk/search">
        <UInput v-model="dynamicModel.uprn" />
    </UFormGroup>
</template>

<style scoped>

</style>