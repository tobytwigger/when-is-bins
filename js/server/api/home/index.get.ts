export default defineEventHandler(async (event) => {
    return {homes: await useDrizzle().select().from(tables.homes)};
})
