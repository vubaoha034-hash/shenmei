import {mkdirSync,copyFileSync,readFileSync} from 'node:fs';
mkdirSync('dist/server',{recursive:true});
mkdirSync('dist/.openai',{recursive:true});
for(const [source,target] of [['worker.mjs','index.js'],['core.mjs','core.mjs'],['exact-contract.mjs','exact-contract.mjs'],['delivery-contract.mjs','delivery-contract.mjs']])copyFileSync(source,'dist/server/'+target);
copyFileSync('.openai/hosting.json','dist/.openai/hosting.json');
const hosting=JSON.parse(readFileSync('dist/.openai/hosting.json','utf8'));
if(!hosting.project_id || !hosting.capabilities.includes('mcp') || hosting.d1!=='DB')throw Error('Invalid hosting manifest');
console.log(JSON.stringify({built:true,entry:'dist/server/index.js',mcp:true,feedback_only_d1:true}));
