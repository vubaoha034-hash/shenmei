// Two actual sequential Figma operations are preserved separately.
// 1. FIGMA_LAYOUT.js: creates a single guarded V8 frame, returns all new IDs.
// 2. FIGMA_WORDMARK_IMPORT.js: imports the sole V8 SVG into those returned nodes.
// Call each separately; update IDs from operation 1 if recovering another draft.
// This index is intentionally not a combined executable or a new design run.
