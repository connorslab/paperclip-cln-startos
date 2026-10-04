import {sdk} from '../sdk'
import {setDependencies} from '../dependencies'
import {setInterfaces} from '../interfaces'
import {versionGraph} from '../versions'
import {actions,configure} from '../actions'
import {restoreInit} from '../backups'
import {store} from '../fileModels/store'
import {i18n} from '../i18n'
const requireSetup=sdk.setupOnInit(async effects=>{const s=await store.read().const(effects);if(!s?.configuration)await sdk.action.createOwnTask(effects,configure,'critical',{reason:i18n('Configure the backend before starting')})})
export const init=sdk.setupInit(restoreInit,versionGraph,setInterfaces,setDependencies,actions,requireSetup)
export const uninit=sdk.setupUninit(versionGraph)
