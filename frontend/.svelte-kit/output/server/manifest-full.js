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
		client: {start:"_app/immutable/entry/start.B4JD7ar8.js",app:"_app/immutable/entry/app.DJZZEwKQ.js",imports:["_app/immutable/entry/start.B4JD7ar8.js","_app/immutable/chunks/spXS5ly3.js","_app/immutable/chunks/BKZzm82k.js","_app/immutable/chunks/DbyfWEYX.js","_app/immutable/entry/app.DJZZEwKQ.js","_app/immutable/chunks/BKZzm82k.js","_app/immutable/chunks/BDimp7fF.js","_app/immutable/chunks/bgre1PTG.js","_app/immutable/chunks/DbyfWEYX.js","_app/immutable/chunks/Be2-HqVZ.js","_app/immutable/chunks/LWGFU2bj.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
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
