import { drizzle } from 'drizzle-orm/libsql'
export { sql, eq, and, or } from 'drizzle-orm'

import * as schema from '../database/schema'

export const tables = schema

export function useDrizzle() {
    return drizzle(process.env.DATABASE_PATH!, { schema })
}

export type Home = typeof schema.homes.$inferSelect

export type Bin = typeof schema.bins.$inferSelect