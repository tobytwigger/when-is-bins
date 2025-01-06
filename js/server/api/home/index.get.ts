export default defineEventHandler(async (event) => {
    console.log('ss');
    let homes = await useDrizzle().select().from(tables.homes);
    console.log('bb');
    return {homes: homes};
})
