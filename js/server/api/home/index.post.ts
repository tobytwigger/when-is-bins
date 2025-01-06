export default defineEventHandler(async (event) => {
    const {
        name,
        council,
        councilData
    } = await readBody(event).catch(() => {})

    const home = await useDrizzle().insert(tables.homes).values({
        name,
        council,
        council_data: councilData
    }).returning().get()

    return home;
})
