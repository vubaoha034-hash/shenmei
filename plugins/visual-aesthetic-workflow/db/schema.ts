import {sqliteTable,text,primaryKey} from 'drizzle-orm/sqlite-core';
export const feedbackIntakes=sqliteTable('feedback_intakes',{
  actorId:text('actor_id').notNull(),
  idempotencyKey:text('idempotency_key').notNull(),
  contentSha256:text('content_sha256').notNull(),
  payload:text('payload').notNull(),
  recordedAt:text('recorded_at').notNull(),
},t=>[primaryKey({columns:[t.actorId,t.idempotencyKey]})]);
