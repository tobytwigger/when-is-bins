import {eq} from 'drizzle-orm';

export default defineEventHandler(async (event) => {
    const id = getRouterParam(event, 'id')

    return {home: await useDrizzle().select().from(tables.homes).where(eq(tables.homes.id, id)).get()};
});