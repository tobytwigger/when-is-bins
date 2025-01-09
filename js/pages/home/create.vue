<template>
    <LayoutsDefault>

        Create a home

        <UForm :schema="schema" :state="state" class="space-y-4" @submit="onSubmit">
            <UFormGroup label="Name" name="name">
                <UInput v-model="state.name"/>
            </UFormGroup>

            <UFormGroup label="Council" name="council">
                <USelectMenu
                    v-model="state.council"
                    :options="councilSelectSchema"
                    class="w-full lg:w-48"
                    option-attribute="label"
                    placeholder="Select a council"
                    searchable
                    searchable-placeholder="Search councils..."
                    value-attribute="value"
                />
            </UFormGroup>

            <div v-if="selectedCouncil">
                <component :is="selectedCouncil.component"
                           :value="state.councilData"
                           :key="selectedCouncil.key ?? 'unselected'"
                           :properties="selectedCouncil.properties"
                           @update:value="state.councilData = $event">

                </component>
            </div>


            <UButton type="submit" :loading="isSubmitting">
                Submit
            </UButton>
        </UForm>
    </LayoutsDefault>

</template>

<script lang="ts" setup>
import {object, string, type InferType} from 'yup'
import type {FormSubmitEvent} from '#ui/types'
import {Council} from "~/composables/useCouncils";

definePageMeta({
    layout: 'home'
})

const {councils, councilSelectSchema, councilKeys} = useCouncils();

const selectedCouncil = computed<Council | null>(() => {
    return councils.find(council => council.key === state.council) || null
})

const schema = object({
    name: string().required('Required'),
    council: string().required('Required')
        .oneOf(councilKeys.value, 'Invalid council'),
    councilData: object().json()
})

type Schema = InferType<typeof schema>

const state = reactive({
    name: undefined,
    council: undefined,
    councilData: {}
})

const isSubmitting = ref<boolean>(false);
const toast = useToast();
const onSubmit = (event: FormSubmitEvent<Schema>) => {
    isSubmitting.value = true;
    $fetch('/api/home', {
        method: 'POST',
        body: event.data
    })
        .then(res => {
            toast.add({
                title: 'Home created',
                description: 'The home has been created',
            })
            navigateTo('/home/' + res.id)
        })
        .catch(err => {
            console.error(err)
        })
        .finally(() => {
            isSubmitting.value = false;
        })
}

</script>