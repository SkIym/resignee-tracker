export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {start:"_app/immutable/entry/start.DjME1cfX.js",app:"_app/immutable/entry/app.CdFiu4DG.js",imports:["_app/immutable/entry/start.DjME1cfX.js","_app/immutable/chunks/CBEX_6va.js","_app/immutable/chunks/KKiNGECp.js","_app/immutable/chunks/ZXQmN4nw.js","_app/immutable/entry/app.CdFiu4DG.js","_app/immutable/chunks/KKiNGECp.js","_app/immutable/chunks/CxMWnzkG.js","_app/immutable/chunks/B5mZLFLJ.js","_app/immutable/chunks/ZXQmN4nw.js","_app/immutable/chunks/BOZlHw2i.js","_app/immutable/chunks/ZEJ93B6U.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js')),
			__memo(() => import('./nodes/3.js')),
			__memo(() => import('./nodes/4.js'))
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			},
			{
				id: "/dashboard",
				pattern: /^\/dashboard\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
				endpoint: null
			},
			{
				id: "/signup",
				pattern: /^\/signup\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 4 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
