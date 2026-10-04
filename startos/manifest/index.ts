import { setupManifest } from '@start9labs/start-sdk'
import { long, short } from './i18n'
export const manifest = setupManifest({
  id: 'paperclip-cln-sideflash', title: 'Paperclip CLN Sideflash', license: 'MIT',
  packageRepo: 'https://github.com/connorslab/paperclip-cln-startos',
  upstreamRepo: 'https://github.com/connorslab/lightning',
  marketingUrl: 'https://ark.paperclippool.xyz', donationUrl: null,
  description: {short, long}, volumes: ["main", "startos", "rtl"],
  images: {"rtl": {"source": {"dockerTag": "paperclip-rtl-startos:sideflash-rc3-package"}, "arch": ["x86_64"]},"app": {"source": {"dockerTag": "paperclip-cln-startos:sideflash-20261004-1"}, "arch": ["x86_64"]}}, dependencies: {},
})
