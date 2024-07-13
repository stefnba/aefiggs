import { Hono } from "hono";
import { db } from "@db";
import { sql } from "drizzle-orm";
import { currencyRate } from "@db/schema";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

const app = new Hono();

app.get("/", (c) => {
  return c.text("Server is running...");
});

app.get(
  "/rates",
  zValidator(
    "query",
    z.object({
      baseCurrency: z.string().optional(),
      quoteCurrency: z.string().optional(),
      limit: z.coerce.number().default(50),
      date: z.union([z.array(z.coerce.date()), z.coerce.date()]).optional(),
      startDate: z.coerce.date().optional(),
      endDate: z.coerce.date().optional(),
    })
  ),
  async (c) => {
    const { baseCurrency, quoteCurrency, limit, date, startDate, endDate } =
      c.req.valid("query");

    if (date && (startDate || endDate)) {
      return c.json(
        {
          message: "Cannot use date with startDate or endDate",
        },
        400
      );
    }

    const rates = await db.query.currencyRate.findMany({
      columns: {
        baseCurrency: true,
        quoteCurrency: true,
        rate: true,
      },
      extras: {
        date: sql`${currencyRate.date}::date`.as("date"),
      },
      where: (fields, { and, eq, inArray, gte, lte }) =>
        and(
          startDate ? gte(fields.date, startDate) : undefined,
          endDate ? lte(fields.date, endDate) : undefined,
          baseCurrency ? eq(fields.baseCurrency, baseCurrency) : undefined,
          quoteCurrency ? eq(fields.quoteCurrency, quoteCurrency) : undefined,
          date
            ? inArray(fields.date, Array.isArray(date) ? date : [date])
            : undefined
        ),
      orderBy: (fields, { desc }) => [desc(fields.date)],
      limit: limit,
    });
    return c.json(rates);
  }
);

export default app;
