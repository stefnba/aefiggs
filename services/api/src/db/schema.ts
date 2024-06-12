import { pgTable, text, timestamp, decimal, index } from "drizzle-orm/pg-core";

export const currencyRate = pgTable(
  "currency_rate",
  {
    transactionCurrency: text("transactionCurrency").notNull(),
    baseCurrency: text("baseCurrency").notNull(),
    date: timestamp("date", { precision: 3, mode: "date" }).notNull(),
    rate: decimal("rate").notNull(),
    createdAt: timestamp("createdAt", { precision: 3, mode: "date" })
      .defaultNow()
      .notNull(),
  },
  (table) => {
    return {
      transactionCurrency: index("transactionCurrency_idx").on(
        table.transactionCurrency
      ),
      baseCurrency: index("baseCurrency_idx").on(table.baseCurrency),
      date: index("date_idx").on(table.date),
    };
  }
);
