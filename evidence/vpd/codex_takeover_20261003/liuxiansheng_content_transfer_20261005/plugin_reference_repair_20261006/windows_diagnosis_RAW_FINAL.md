诊断已解决：`diagnosis_resolved=true`，`plan_frozen=true`。下一阶段交给 PRIMARY 实现薄包装，FAST 核验产物；本次未修改任何文件。

**根因与反证**

- 默认 `bash` 解析到 `C:\Windows\System32\bash.exe`，首轮是缺失 WSL。
- 显式 Git Bash 执行 `--version` 与 `--noprofile --norc -c ...` 均在执行脚本前失败：
  `NtCreateDirectoryObject(\BaseNamedObjects\msys-2.0S5-1888ae32e00d56aa): 0xC0000022`。
- 因此第二轮属于当前受限环境中的 MSYS 启动访问拒绝。Node PATH、反斜杠、项目源码均不能解释 `--version` 也失败。底层具体 ACL 来源尚未区分，但不影响恢复决策。
- 原生 Node `v24.19.0`、Windows `bsdtar 3.8.8` 正常。使用精确中文项目路径，在内存中完成 gzip 打包与列表读取：退出码 0、gzip magic `1f8b08`、`gunzip` 成功，没有落盘。
- 当前 Git clean，HEAD 为 `535a61558e3154b644f60b7b643566a94f1ea86f`。已确认 `.sites-runtime/` 被忽略。

**PRIMARY 的固定实现范围**

1. 使用父任务提出的 `.sites-runtime/native-package-v012-20261006`。检查路径在所选 Site 内、祖先没有链接或重解析点、目标 `dist` 尚不存在，并且位于输入 `Site/dist` 外。不得复用或删除已有目录。
2. 通过绝对 Node 路径调用未修改的官方 `prepare-site-build.cjs`，参数为 `[project, stage/dist]`；要求退出码 0、输出 `worker`。
3. 准确复现 [package-site.sh](C:/Users/Administrator/.codex/plugins/cache/openai-curated-remote/sites/0.1.75/skills/sites-hosting/scripts/package-site.sh:17) 的 manifest 处理：
   - 使用源 hosting；同时存在且不同的 `artifact_metadata` 必须报错，比较用 `isDeepStrictEqual`。
   - built attribution 优先于 source attribution。
   - 写入 `JSON.stringify(staged,null,2) + "\n"`。
4. 将源 `drizzle/` 的**内容**复制至 `stage/dist/.openai/drizzle/`。
5. 使用已验证的 `C:/Windows/System32/tar.exe`，参数数组：
   `['-C', stage, '-czf', archive, 'dist']`。
   不需要 Python 打包依赖。保留 `dist/server/index.js` 与 `dist/server/core.mjs` 的目录位置。
6. 记录这是原生恢复包装，不能将之前官方 workflow 的失败改写为成功。发布继续由 Site owner 使用既有 project、已推送 commit 和验证后的 archive 完成。

**FAST 验收**

读取 gzip/tar 成员并直接计算内容哈希，无须解压。普通文件应恰好六个：

| 归档成员 | SHA-256 |
|---|---|
| `dist/server/core.mjs` | `9e34b09f74ea937f73f311b14a74d6781bbbb818988a5b93bea94ca0b57828e8` |
| `dist/server/index.js` | `32b3badaa81cfaa7567c0a7eda07cbf1d7e6da18d27a337c54bb6e9e97ea5dc8` |
| `dist/.openai/hosting.json` | `60eb1ca5af7f6b6f46576c78bb7725b8b441fec7687fa0f7cb365747787c90a1` |
| `dist/.openai/drizzle/0000_yellow_clint_barton.sql` | `d45ec4315b7852ac015378d73df73199da4b1a5362a8a87ad60d1d5f42fc330a` |
| `dist/.openai/drizzle/meta/0000_snapshot.json` | `2e490c841cd58c9656a612f9b78d2552f908c89253a63df7f51416f29fc919ff` |
| `dist/.openai/drizzle/meta/_journal.json` | `c494a3041c3089af128a795a7dd63d51709b85a6ef07e8858c568a94c0838749` |

源 hosting 仍须保持冻结哈希 `bd112c8d960dd2af7dfdf9010d3c4713308dae84f9615aa8cc22e4eaf457e7e2`。官方格式化会将它从 118 字节改为归档内的 126 字节，所以上表归档哈希不同是预期行为；JSON 内容必须相同。

同时检查：无重复成员、绝对路径、`..`、链接或特殊文件；所有成员在 `dist/` 下；Git HEAD、clean 状态及冻结源哈希未变；归档哈希在上传前后保持一致。

**可证伪预测与剩余边界**

该方案预测官方 helper 返回 `worker`，归档六个文件均符合上表。任一步失败或出现额外成员，应保留真实失败并重新开启诊断，不调整验收。完整落盘包装和云端部署尚未执行，因此当前结论不构成部署成功证明。
