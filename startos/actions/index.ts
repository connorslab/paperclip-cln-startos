import {utils} from '@start9labs/start-sdk'
import {sdk} from '../sdk'
import {store} from '../fileModels/store'
import {i18n} from '../i18n'
const spec=sdk.InputSpec.of({
 rpc_url:sdk.Value.text({name:i18n('Knots RPC URL'),description:i18n('Use http://LAN-IP:RPC-PORT. Docker hostnames and .local names may not resolve inside StartOS.'),required:true,default:''}),
 rpc_user:sdk.Value.text({name:i18n('RPC username'),required:true,default:''}),
 rpc_password:sdk.Value.text({name:i18n('RPC password'),required:true,masked:true,default:''}),
 alias:sdk.Value.text({name:i18n('Lightning node name'),required:true,default:'Paperclip Sideflash Test'}),
 tls_host:sdk.Value.text({name:i18n('TLS hostname or LAN IP'),description:i18n('Must match the address clients use. Keep unchanged after the first successful start.'),required:true,default:'startos.local'}),
 trusted_server_key:sdk.Value.text({name:i18n('Trusted ASP public key (optional)'),description:i18n('Full 66-character ASP public key for Sideflash payments.'),required:false,default:''}),
 regtest:sdk.Value.toggle({name:i18n('Use regtest (advanced)'),description:i18n('Leave off for the Bitcoin main network. Existing funded instances cannot change networks.'),default:false}),
 checkConnection:sdk.Value.toggle({name:i18n('Check node connection before saving'),description:i18n('Checks RPC reachability, credentials and network without moving funds.'),default:true}),
})
export const configure=sdk.Action.withInput('configure',async()=>({name:i18n('Configure test app'),description:i18n('Configure this isolated test instance while stopped.'),warning:i18n('Experimental and unaudited. Back up before changing settings.'),allowedStatuses:'only-stopped',group:null,visibility:'enabled',access:'user'}),spec,async()=>{
 const saved=await store.read().once();const c=saved?.configuration?JSON.parse(saved.configuration):{}
 return {rpc_url:c.rpc_url||'',rpc_user:c.rpc_user||'',rpc_password:c.rpc_password||'',alias:c.alias||'Paperclip Sideflash Test',tls_host:c.tls_host||'startos.local',trusted_server_key:c.trusted_server_key||'',regtest:c.network==='regtest',checkConnection:true}
},async({effects,input})=>{
 const old=await store.read().once()
 const previous=old?.configuration?JSON.parse(old.configuration):{}
 const c={...previous,network:input.regtest?'regtest':'bitcoin',rpc_url:input.rpc_url.trim(),rpc_user:input.rpc_user,rpc_password:input.rpc_password,alias:input.alias.trim(),tls_host:input.tls_host.trim(),trusted_server_key:(input.trusted_server_key||'').trim()}
 const endpoint=new URL(c.rpc_url)
 if(endpoint.protocol!=='http:'||endpoint.username||endpoint.password||endpoint.search||endpoint.hash||!['','/'].includes(endpoint.pathname))throw new Error('Use a private HTTP node RPC URL without embedded credentials or a path.')
 if(JSON.stringify(c).length>65536)throw new Error(i18n('Configuration too large'))
 await sdk.SubContainer.withTemp(effects,{imageId:'app'},sdk.Mounts.of(),'validate-settings',async sub=>{
  await sub.execFail(['python3','/opt/startos/check-settings.py','cln'],{input:JSON.stringify(c)},15000)
  if(input.checkConnection)await sub.execFail(['python3','/opt/startos/check-connection.py'],{input:JSON.stringify(c)},45000)
 })
 await store.merge(effects,{configuration:JSON.stringify(c),token:old?.token||utils.getDefaultString({charset:'0-9,a-f',len:64}),postgres:old?.postgres||utils.getDefaultString({charset:'a-z,A-Z,0-9',len:48})})
 return {version:'1',title:i18n('Configuration saved'),message:i18n('Settings saved. Start the app.'),result:null}
})

const inspect=sdk.Action.withoutInput('connection-info',async()=>({name:i18n('CLN gRPC'),description:i18n('Connection details and funding information'),warning:i18n('Keep these details private'),allowedStatuses:'only-running',group:null,visibility:'enabled',access:'user'}),async({effects})=>{const value=await sdk.SubContainer.withTemp(effects,{imageId:'app'},sdk.Mounts.of().mountVolume({volumeId:'main',subpath:null,mountpoint:'/data',readonly:true}),'connection-info',async sub=>String((await sub.execFail(["python3", "/opt/startos/connection.py"],{},15000)).stdout));return {version:'1',title:i18n('CLN gRPC'),message:i18n('Keep these details private'),result:{type:'single',name:i18n('CLN gRPC'),description:null,value,masked:true,copyable:true,qr:false}}})
const rtlPassword=sdk.Action.withoutInput('rtl-password',async()=>({name:'RTL initial password',description:'Show the generated initial RTL login password. A password changed inside RTL takes precedence.',warning:null,allowedStatuses:'any',group:null,visibility:'enabled',access:'user'}),async()=>{const s=await store.read().once();return {version:'1',title:'RTL initial password',message:'Keep this password private. RTL can manage funds and channels.',result:{type:'single',name:'Password',description:null,value:s?.token||'',masked:true,copyable:true,qr:false}}})
export const actions=sdk.Actions.of().addAction(configure).addAction(inspect).addAction(rtlPassword)
