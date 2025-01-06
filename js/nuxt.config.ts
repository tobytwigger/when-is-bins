// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    devtools: {enabled: true},
    modules: ["@nuxt/ui"],
    compatibilityDate: "2025-01-05",
    nitro: {
        experimental: {
            database: true
        },
        database: {
            default: {
                connector: 'sqlite',
                options: {
                    cwd: './../../',
                    name: 'database.sqlite',
                }
            },
        }
    }
})
