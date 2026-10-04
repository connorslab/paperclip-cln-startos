import {sdk} from './sdk'
import {i18n} from './i18n'
export const {createBackup,restoreInit}=sdk.setupBackups(async({effects})=>sdk.Backups.ofVolumes('main','startos','rtl').setPreBackup(async effects=>{const status=await sdk.getStatus(effects).once();if(status?.started)throw new Error(i18n('Stop the app before backing up its financial state'))}))
