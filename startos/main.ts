import {sdk} from './sdk'
import {store} from './fileModels/store'
import {i18n} from './i18n'
export const main=sdk.setupMain(async({effects})=>{const saved=await store.read().const(effects);if(!saved?.configuration)throw new Error(i18n('Configure the backend before starting'));
await sdk.volumes.main.writeFile('settings.json',saved.configuration,{mode:0o600});
let daemons=sdk.Daemons.of(effects)
return daemons.addDaemon('app',{subcontainer:sdk.SubContainer.of(effects,{imageId:'app'},sdk.Mounts.of().mountVolume({volumeId:'main',subpath:null,mountpoint:'/data',readonly:false}),'app'),exec:{command:['/usr/bin/tini','--','python3','/opt/startos/start.py'],user:'root',runAsInit:true,env:{STARTOS_TOKEN:saved.token,APP_PASSWORD:saved.token,POSTGRES_PASSWORD:saved.postgres}},ready:{display:i18n('Service'),fn:()=>sdk.healthCheck.checkPortListening(effects,9737,{successMessage:i18n('Ready'),errorMessage:i18n('Starting')})},requires:[]})
})
