import fs from 'node:fs';
import {spawn} from 'node:child_process';
process.umask(0o077);
fs.mkdirSync('/rtl-data/db',{recursive:true});
for(let i=0;!fs.existsSync('/rtl-auth/access.rune');i++){
 if(i>=150)throw new Error('CLN credentials are not ready. Check CLN startup.');
 await new Promise(r=>setTimeout(r,1000));
}
const rune=fs.readFileSync('/rtl-auth/access.rune','utf8').trim();
if(!/^[A-Za-z0-9_=-]+$/.test(rune))throw new Error('Invalid local CLN credential');
fs.writeFileSync('/rtl-data/access.rune','LIGHTNING_RUNE='+JSON.stringify(rune)+'\n',{mode:0o600});
const config='/rtl-data/RTL-Config.json';
if(!fs.existsSync(config)){
 if(!process.env.STARTOS_TOKEN)throw new Error('RTL initial password missing');
 fs.writeFileSync(config,JSON.stringify({multiPass:process.env.STARTOS_TOKEN,port:'3000',defaultNodeIndex:1,dbDirectoryPath:'/rtl-data/db',SSO:{rtlSSO:0},nodes:[{index:1,lnNode:'Paperclip Sideflash',lnImplementation:'CLN',authentication:{runePath:'/rtl-data/access.rune'},settings:{userPersona:'OPERATOR',themeMode:'NIGHT',themeColor:'PURPLE',logLevel:'ERROR',lnServerUrl:'http://127.0.0.1:3010',fiatConversion:false,enableOffers:true,unannouncedChannels:true,blockExplorerUrl:'https://mempool.guide'}}]},null,2),{mode:0o600});
}
const env={...process.env,RTL_CONFIG_PATH:'/rtl-data'};delete env.STARTOS_TOKEN;
const child=spawn('node',['rtl.js'],{cwd:'/RTL',env,stdio:'inherit'});
for(const sig of ['SIGTERM','SIGINT'])process.on(sig,()=>child.kill(sig));
child.on('exit',(code)=>process.exit(code??1));
