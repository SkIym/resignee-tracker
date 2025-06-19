import * as server from '../entries/pages/_page.server.js';

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/+page.server.js";
export const imports = ["_app/immutable/nodes/2.DyL2rTxY.js","_app/immutable/chunks/CO5X12ro.js","_app/immutable/chunks/DZq78Ezw.js","_app/immutable/chunks/BhebSDih.js","_app/immutable/chunks/sKjDUr9k.js","_app/immutable/chunks/BQGRK2Qk.js","_app/immutable/chunks/CdqjsRcG.js","_app/immutable/chunks/CBaeDeQn.js","_app/immutable/chunks/hoQZN_2d.js"];
export const stylesheets = [];
export const fonts = [];
