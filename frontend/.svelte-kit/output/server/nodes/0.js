import * as universal from '../entries/pages/_layout.js';

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/+layout.js";
export const imports = ["_app/immutable/nodes/0.DMmiB9cV.js","_app/immutable/chunks/CO5X12ro.js","_app/immutable/chunks/DZq78Ezw.js"];
export const stylesheets = ["_app/immutable/assets/0.Ck0qZ4Lb.css"];
export const fonts = [];
