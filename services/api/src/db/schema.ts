import {
  pgTable,
  text,
  timestamp,
  decimal,
  primaryKey,
} from "drizzle-orm/pg-core";

export const currencyRate = pgTable(
  "currency_rate",
  {
    baseCurrency: text("base_currency").notNull(),
    quoteCurrency: text("quote_currency").notNull(),
    date: timestamp("date", { precision: 3, mode: "date" }).notNull(),
    rate: decimal("rate").notNull(),
    createdAt: timestamp("created_at", { precision: 3, mode: "date" })
      .defaultNow()
      .notNull(),
  },
  (table) => {
    return {
      pk: primaryKey({
        columns: [table.baseCurrency, table.quoteCurrency, table.date],
      }),
    };
  }
);
