import { migrate } from 'drizzle-orm/libsql/migrator'

export default defineNitroPlugin(async (nitroApp) => {
    const db = useDrizzle();
    	try {
		await migrate(db, { migrationsFolder: '/home/toby/when-is-bins/js/server/database/migrations' })
		console.log('Migration completed ✅')
	} catch (error) {
		console.error('Migration failed 🚨:', error)
	}
})