<template>
    <UCard class="mt-10">
        <template #header>
            <div class="flex justify-between">
                <h1>When is bins?</h1>
                <ColorScheme><USelect v-model="$colorMode.preference" :options="['system', 'light', 'dark']" /></ColorScheme>
            </div>
        </template>
        <slot />
        <!--      <UButton icon="i-heroicons-book-open" to="https://ui.nuxt.com" target="_blank">Open Nuxt UI Documentation</UButton>-->
    </UCard>
</template>
<script setup lang="ts">
</script>