import {sdk} from './sdk'
import {i18n} from './i18n'
export const setInterfaces=sdk.setupInterfaces(async({effects})=>{
const receipts=[]
const host9735=sdk.MultiHost.of(effects,'peers');const origin9735=await host9735.bindPort(9735,{protocol:null,preferredExternalPort:39735,addSsl:null,secure:{ssl:false}});receipts.push(await origin9735.export([sdk.createInterface(effects,{id:'peers',name:i18n('Peers'),description:i18n('Peers'),type:'p2p',masked:false,schemeOverride:null,username:null,path:'',query:{}})]))
const host9737=sdk.MultiHost.of(effects,'cln-grpc');const origin9737=await host9737.bindPort(9737,{protocol:null,preferredExternalPort:39737,addSsl:null,secure:{ssl:true}});receipts.push(await origin9737.export([sdk.createInterface(effects,{id:'cln-grpc',name:i18n('CLN gRPC'),description:i18n('CLN gRPC'),type:'api',masked:false,schemeOverride:{ssl:'https',noSsl:'https'},username:null,path:'',query:{}})]))
const host9738=sdk.MultiHost.of(effects,'hold-grpc');const origin9738=await host9738.bindPort(9738,{protocol:null,preferredExternalPort:39738,addSsl:null,secure:{ssl:true}});receipts.push(await origin9738.export([sdk.createInterface(effects,{id:'hold-grpc',name:i18n('Hold gRPC'),description:i18n('Hold gRPC'),type:'api',masked:false,schemeOverride:{ssl:'https',noSsl:'https'},username:null,path:'',query:{}})]))
return receipts
})
