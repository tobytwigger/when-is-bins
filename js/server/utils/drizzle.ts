import { drizzle } from 'drizzle-orm/libsql'
export { sql, eq, and, or } from 'drizzle-orm'
import path from 'path'
import * as schema from '../database/schema'

export const tables = schema

export function useDrizzle() {
    const databasePath = path.resolve(__dirname, './../../../../database.sqlite');
    console.log('Absolute Path to the Database:', databasePath);
    return drizzle('file:./../../../../database.sqlite', { schema })
}

export type Home = typeof schema.homes.$inferSelect

export type Bin = typeof schema.bins.$inferSelect