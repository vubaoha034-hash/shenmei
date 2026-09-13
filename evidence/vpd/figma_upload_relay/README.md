# VPD Figma Image Upload Relay V1

Purpose: bridge the one missing step in chat-based Figma automation: POSTing local raster bytes to the one-time `upload_assets` submit URL.

## Security model

- Repository may remain public.
- Plain Figma submit URLs and plain image bytes are never committed.
- Each task is a CMS-encrypted `.cms` file encrypted to `relay-cert.pem`.
- The matching private key exists only as the GitHub Actions repository secret `VPD_FIGMA_RELAY_PRIVATE_KEY_B64`.
- Workflow receipts are redacted and never contain the submit URL.
- Submit URLs are additionally validated to `https://mcp.figma.com/mcp/upload/.../submit` before use.

## One-time setup

1. GitHub repository: `vubaoha034-hash/shenmei`.
2. Settings → Secrets and variables → Actions → New repository secret.
3. Name: `VPD_FIGMA_RELAY_PRIVATE_KEY_B64`.
4. Value: the complete one-line content of the separately delivered `VPD_FIGMA_RELAY_PRIVATE_KEY_B64.txt`.
5. Never commit that private-key value or paste it into issues/logs.

## Task creation

After Figma `upload_assets` returns a submit URL and the target PHOTO node is confirmed `locked=false`:

```bash
python scripts/vpd_figma_relay_pack.py \
  --cert evidence/vpd/figma_upload_relay/relay-cert.pem \
  --image /path/to/image.png \
  --submit-url 'https://mcp.figma.com/mcp/upload/.../submit?scaleMode=FILL' \
  --node-id '12:12' \
  --task-id 'P6-DOUFANG-B-20260913' \
  --output evidence/vpd/figma_upload_relay/tasks/P6-DOUFANG-B-20260913.cms
```

Commit only the `.cms` ciphertext. The push-triggered workflow decrypts it, validates SHA-256/size/host/node id, POSTs raw bytes to Figma, writes a redacted receipt, and deletes a successful ciphertext task from the branch.

## Required Figma invariant

`PHOTO_RAW_LOCKED` means **asset identity is frozen**. It must not mean the Figma node property is locked. Before upload:

- semantic asset identity: locked
- Figma node `locked`: `false`
- target fill may be placeholder before upload

## Failure behavior

- Missing secret: workflow stops before decrypt/upload.
- Bad ciphertext, checksum, node id, MIME type, or submit URL host: no upload.
- Upload failure: ciphertext task remains for retry and a redacted failure receipt is persisted.
- No receipt or placeholder/proxy may be treated as final pixel evidence.
