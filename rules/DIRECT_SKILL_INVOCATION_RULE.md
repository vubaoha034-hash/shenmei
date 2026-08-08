# DIRECT SKILL INVOCATION RULE

状态：`MANDATORY`

当用户明确说“直接用 Skill”“使用某个 Skill”“按这个 Skill 生成”，或以 `$skill-name` 点名调用时：

1. **先执行该 Skill，而不是进入自由提示词创作模式。**
2. 不得用助手自行写的一套新风格说明、艺术指导或长 Prompt 替代 Skill 的 Prompt Compiler。
3. 不得因为输出不满意，就未经用户要求擅自改写 Skill、增加视觉规则、改名、重构或新建派生版本。
4. 如果 Skill 本身规定了 Prompt Compiler，最终 Prompt 必须由该 Compiler 产生；助手只能填写它要求的变量或做 Skill 明确允许的适配。
5. 如果用户提供的是图片，优先把图片作为该 Skill 规定的输入素材；不得默认把其他上下文图片混入同一次生成。
6. 若结果不满意，先诊断：
   - Skill 是否真正被读取；
   - 调用链是否绕过了 Skill；
   - 最终 Prompt 是否由 Skill Compiler 产生；
   - 是否混入了助手自创的风格词 / 文案 / 参考图；
   - 图像生成器是否未按 Skill 预期响应。
7. 在完成上述诊断前，不得把问题归咎于 Skill 本身，也不得自动进入“我重新给你写提示词”的模式。
8. 只有用户明确要求“改 Skill”“重写 Prompt”“另做一个版本”时，才允许离开直接执行路径。

核心原则：

> **用户点名 Skill = 执行 Skill，不是借 Skill 名义自由发挥。**
