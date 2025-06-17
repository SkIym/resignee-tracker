import * as server from '../entries/pages/_page.server.js';

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/+page.server.js";
export const imports = ["_app/immutable/nodes/2.i_FqB79G.js","_app/immutable/chunks/B5mZLFLJ.js","_app/immutable/chunks/KKiNGECp.js","_app/immutable/chunks/D6vZkVq1.js","_app/immutable/chunks/CxMWnzkG.js","_app/immutable/chunks/BOZlHw2i.js","_app/immutable/chunks/DX3MR-9l.js","_app/immutable/chunks/DgfLiGhn.js","_app/immutable/chunks/ZXQmN4nw.js"];
export const stylesheets = [];
export const fonts = [];
