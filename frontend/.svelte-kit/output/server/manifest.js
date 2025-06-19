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
		client: {start:"_app/immutable/entry/start.Dzg1sKja.js",app:"_app/immutable/entry/app.C7sPxRCU.js",imports:["_app/immutable/entry/start.Dzg1sKja.js","_app/immutable/chunks/CBaeDeQn.js","_app/immutable/chunks/DZq78Ezw.js","_app/immutable/chunks/hoQZN_2d.js","_app/immutable/entry/app.C7sPxRCU.js","_app/immutable/chunks/DZq78Ezw.js","_app/immutable/chunks/sKjDUr9k.js","_app/immutable/chunks/CO5X12ro.js","_app/immutable/chunks/hoQZN_2d.js","_app/immutable/chunks/BQGRK2Qk.js","_app/immutable/chunks/BgZpowm-.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
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
