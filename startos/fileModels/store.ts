import {FileHelper,z} from '@start9labs/start-sdk'
import {sdk} from '../sdk'
export const store = FileHelper.json({base:sdk.volumes.startos,subpath:'store.json'},z.object({configuration:z.string().catch(''),token:z.string().catch(''),postgres:z.string().catch('')}))
