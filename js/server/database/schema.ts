import {sqliteTable, text, integer, unique} from 'drizzle-orm/sqlite-core'

export const homes = sqliteTable('homes', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    name: text('name').notNull().unique(),
    council: text('council').notNull(),
    council_data: text('council_data', {mode: 'json'}),
    active: integer('active', {mode: 'boolean'}).notNull().default(false),
})

export const bins = sqliteTable('bins', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    council_name: text('council_name').notNull(),
    name: text('name').notNull(),
    position: integer('position').notNull(),
    home_id: integer('home_id').notNull().references(() => homes.id),
}, (t) => ({
    unq: unique().on(t.position, t.home_id)
}));