CREATE TABLE IF NOT EXISTS "currency_rate" (
	"transactionCurrency" text NOT NULL,
	"baseCurrency" text NOT NULL,
	"date" timestamp (3) NOT NULL,
	"rate" numeric NOT NULL,
	"createdAt" timestamp (3) DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS "transactionCurrency_idx" ON "currency_rate" USING btree ("transactionCurrency");--> statement-breakpoint
CREATE INDEX IF NOT EXISTS "baseCurrency_idx" ON "currency_rate" USING btree ("baseCurrency");--> statement-breakpoint
CREATE INDEX IF NOT EXISTS "date_idx" ON "currency_rate" USING btree ("date");