import {rmSync,mkdirSync,copyFileSync} from 'node:fs';
rmSync('dist',{recursive:true,force:true});
mkdirSync('dist/server',{recursive:true});
mkdirSync('dist/.openai',{recursive:true});
for(const name of ['index.js','base-worker.mjs','core.mjs','delivery-contract.mjs','exact-contract.mjs','typography-task.mjs']) copyFileSync('server/'+name,'dist/server/'+name);
copyFileSync('.openai/hosting.json','dist/.openai/hosting.json');
console.log(JSON.stringify({built:true,version:'0.3.0',entry:'dist/server/index.js',mcp:true}));
