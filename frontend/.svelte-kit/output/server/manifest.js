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
		client: {start:"_app/immutable/entry/start.BQ5hTR03.js",app:"_app/immutable/entry/app.BMgQkFU7.js",imports:["_app/immutable/entry/start.BQ5hTR03.js","_app/immutable/chunks/BN9Q3c0b.js","_app/immutable/chunks/KKiNGECp.js","_app/immutable/chunks/ZXQmN4nw.js","_app/immutable/entry/app.BMgQkFU7.js","_app/immutable/chunks/KKiNGECp.js","_app/immutable/chunks/CxMWnzkG.js","_app/immutable/chunks/B5mZLFLJ.js","_app/immutable/chunks/ZXQmN4nw.js","_app/immutable/chunks/BOZlHw2i.js","_app/immutable/chunks/ZEJ93B6U.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js'))
		],
		routes: [
			
		],
		prerendered_routes: new Set(["/","/dashboard","/signup"]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
