import {mkdirSync,copyFileSync} from 'node:fs';
mkdirSync('dist/server',{recursive:true});
mkdirSync('dist/.openai',{recursive:true});
for(const [source,target] of [
  ['worker.mjs','index.js'],
  ['base-worker.mjs','base-worker.mjs'],
  ['core.mjs','core.mjs'],
  ['delivery-contract.mjs','delivery-contract.mjs'],
  ['exact-contract.mjs','exact-contract.mjs'],
  ['typography-task.mjs','typography-task.mjs']
]) copyFileSync(source,'dist/server/'+target);
copyFileSync('.openai/hosting.json','dist/.openai/hosting.json');
console.log(JSON.stringify({built:true,version:'0.2.0',entry:'dist/server/index.js',mcp:true,persistent_typography_tasks:true}));
