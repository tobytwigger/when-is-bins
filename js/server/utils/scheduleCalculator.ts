export async function calculateSchedule(schedule: Schedule) {

    // Calculate the schedule for the next 6 months.

    // First, we clear all current schedule entries for this schedule.
    await useDrizzle().delete(tables.bin_days)
        .where(eq(tables.bin_days.schedule_id, schedule.id))

    const start = new Date(schedule.start)

    const dates: Date[] = [new Date(schedule.start)]
    // We will calculate the schedule for the next 6 months.

    // We finish the schedule either when it ends, or in 6 months time.
    const finish = schedule.end ? new Date(schedule.end) : new Date(start.getTime() + 6 * 30 * 24 * 60 * 60 * 1000)

    const currentDate = start

    while (currentDate < finish) {
        // We calculate the next date.
        currentDate.setDate(currentDate.getDate() + 7 * schedule.repeat_weeks)
        dates.push(new Date(currentDate))
    }

    const bins = await useDrizzle().select().from(tables.bin_schedules)
        .where(eq(tables.bin_schedules.schedule_id, schedule.id))
        .all()

    // For each date, we save the bin days
    for (const date of dates) {
        for (const bin of bins) {
            await useDrizzle().insert(tables.bin_days).values({
                bin_id: bin.bin_id,
                schedule_id: schedule.id,
                home_id: schedule.home_id,
                date
            })
        }
    }

}