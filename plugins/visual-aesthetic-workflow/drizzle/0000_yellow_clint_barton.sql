CREATE TABLE `feedback_intakes` (
	`actor_id` text NOT NULL,
	`idempotency_key` text NOT NULL,
	`content_sha256` text NOT NULL,
	`payload` text NOT NULL,
	`recorded_at` text NOT NULL,
	PRIMARY KEY(`actor_id`, `idempotency_key`)
);
