FROM paperclip-rtl-startos:sideflash-rc3
USER root
COPY start.mjs /opt/start.mjs
ENTRYPOINT ["/sbin/tini","-g","--","node","/opt/start.mjs"]
