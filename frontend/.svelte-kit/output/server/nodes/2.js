import * as server from '../entries/pages/_page.server.js';

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/+page.server.js";
export const imports = ["_app/immutable/nodes/2.DdAVClIj.js","_app/immutable/chunks/bgre1PTG.js","_app/immutable/chunks/BKZzm82k.js","_app/immutable/chunks/SOPnzMaR.js","_app/immutable/chunks/BDimp7fF.js","_app/immutable/chunks/Be2-HqVZ.js","_app/immutable/chunks/M8bK7g7j.js","_app/immutable/chunks/spXS5ly3.js","_app/immutable/chunks/DbyfWEYX.js"];
export const stylesheets = [];
export const fonts = [];
