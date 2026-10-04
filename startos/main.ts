import {sdk} from './sdk'
import {store} from './fileModels/store'
import {i18n} from './i18n'
export const main=sdk.setupMain(async({effects})=>{const saved=await store.read().const(effects);if(!saved?.configuration)throw new Error(i18n('Configure the backend before starting'));
await sdk.volumes.main.writeFile('settings.json',saved.configuration,{mode:0o600});
await sdk.volumes.main.writeFile('rtl/.keep','',{mode:0o600});
let daemons=sdk.Daemons.of(effects)
return daemons.addDaemon('app',{subcontainer:sdk.SubContainer.of(effects,{imageId:'app'},sdk.Mounts.of().mountVolume({volumeId:'main',subpath:null,mountpoint:'/data',readonly:false}),'app'),exec:{command:['/usr/bin/tini','--','python3','/opt/startos/start.py'],user:'root',runAsInit:true,env:{STARTOS_TOKEN:saved.token,APP_PASSWORD:saved.token,POSTGRES_PASSWORD:saved.postgres}},ready:{display:i18n('Service'),fn:()=>sdk.healthCheck.checkPortListening(effects,9737,{successMessage:i18n('Ready'),errorMessage:i18n('Starting')})},requires:[]}).addDaemon('rtl',{subcontainer:sdk.SubContainer.of(effects,{imageId:'rtl'},sdk.Mounts.of().mountVolume({volumeId:'main',subpath:'rtl',mountpoint:'/rtl-auth',readonly:true}).mountVolume({volumeId:'rtl',subpath:null,mountpoint:'/rtl-data',readonly:false}),'rtl'),exec:{command:['/sbin/tini','-g','--','node','/opt/start.mjs'],user:'root',runAsInit:true,env:{STARTOS_TOKEN:saved.token}},ready:{display:'RTL',fn:()=>sdk.healthCheck.checkPortListening(effects,3000,{successMessage:i18n('Ready'),errorMessage:i18n('Starting')})},requires:['app']})
})
