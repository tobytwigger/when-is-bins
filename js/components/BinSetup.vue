<script lang="ts" setup>
import type {Bin} from "~/server/utils/drizzle";
import {object, string, type InferType} from 'yup'
import type {FormSubmitEvent} from "#ui/types";

const props = defineProps<{
    position: number,
    options: string[],
    bin: Bin | null,
    homeId: number
}>();

const toast = useToast();

const emit = defineEmits<{
    (event: 'updated'): void
}>();


const schema = object({
    humanName: string().required('Required'),
    option: string().oneOf(props.options, 'Invalid option').required('Required')
})

type Schema = InferType<typeof schema>

const state = ref<Schema>({
    humanName: '',
    option: '',
})

const isSubmitting = ref(false);

const updateBin = () => {
    isSubmitting.value = true;
    $fetch(`/api/home/${props.homeId}/bins/${props.position}`, {
        method: 'POST',
        body: state.value
    })
        .then(() => {
            toast.add({
                title: 'Bin updated',
                description: 'The bin has been updated',
            })
            emit('updated');
        })
        .catch((error) => {
            console.error(error);
        })
        .finally(() => {
            isSubmitting.value = false;
            emit('updated')
        });
}

const isDirty = computed(() => {
    return state.value.humanName !== (props.bin?.name ?? '') || state.value.option !== (props.bin?.council_name ?? '')
})

watch(() => props.bin, () => {
    state.value.humanName = props.bin?.name ?? ''
    state.value.option = props.bin?.council_name ?? ''
}, {immediate: true})

const isDeleting = ref(false);

const del = () => {
    isDeleting.value = true;
    $fetch(`/api/home/${props.homeId}/bins/${props.position}`, {
        method: 'DELETE'
    })
        .then(() => {
            toast.add({
                title: 'Bin cleared',
                description: 'The bin has been cleared',
            })
        })
        .catch((error) => {
            console.error(error);
        })
        .finally(() => {
            isDeleting.value = false;
            emit('updated')
        });
}

</script>

<template>
    <div class="text-center flex flex-col p-2">
    <span>
        Bin {{ position }}
    </span>

        <span>
        <UForm :schema="schema" :state="state" class="space-y-4" @submit="updateBin">
            <UFormGroup label="Name" name="name">
                <UInput v-model="state.humanName"/>
            </UFormGroup>

            <UFormGroup label="Bin" name="bin">
                <USelectMenu
                    v-model="state.option"
                    :options="props.options"
                    class="w-full lg:w-48"
                    placeholder="Select a bin from the council"
                    searchable
                    searchable-placeholder="Search bins..."
                />
            </UFormGroup>

            <div class="flex flex-col space-y-2 w-full justify-center">
                <UButton icon="i-material-symbols-save-outline" class="w-min"
                         v-if="isDirty" :loading="isSubmitting" type="submit"
                        @click="updateBin">
                    Submit
                </UButton>
                <UButton icon="i-heroicons-trash" :loading="isDeleting" @click="del" color="red" class="w-min" v-if="props.bin !== null">
                    Clear
                </UButton>
            </div>

        </UForm>
    </span>
    </div>
</template>

<style scoped>

</style>