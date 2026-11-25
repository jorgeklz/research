process.on("unhandledRejection",e=>console.log("UNHANDLED",String(e&&e.stack||e).split("\n").slice(0,3).join(" | ")));process.on("uncaughtException",e=>console.log("UNCAUGHT",String(e&&e.stack||e).split("\n").slice(0,3).join(" | ")));
const fs=require('fs');
const lang=process.argv[2]||'en', id=process.argv[3]||'observaia';
const root=process.cwd();
const mk=()=>new Proxy(function(){}, {get:(t,k)=>{ if(k==='classList') return {add(){},remove(){},toggle(){},contains(){return false}}; if(k==='dataset') return {}; if(k==='style') return {}; if(k==='children'||k==='length') return []; if(k===Symbol.toPrimitive) return ()=>''; return mk();}, apply:()=>mk(), set:()=>true});
let stage={innerHTML:'',panels:[],links:[]};
const doc={head:{appendChild(){}},documentElement:{style:{setProperty(){}},lang, getAttribute:()=>'', setAttribute(){}}, body:{dataset:{page:process.argv[4]}, classList:{add(){},remove(){}}, appendChild(){}},
 querySelector:(s)=> s==='#nothing'?stage:mk(), querySelectorAll:()=>[], getElementById:()=>mk(), createElement:()=>mk(), addEventListener(){}, title:''};
global.document=doc; global.getComputedStyle=()=>({getPropertyValue:()=>'140px'}); global.window=global; global.addEventListener=()=>{}; global.removeEventListener=()=>{}; global.location={search:'?id='+id+'&doi=10.1007%2Fs44163-026-02501-8', pathname:'/x.html', hash:'#proj-team', href:''};
global.localStorage={getItem(){return null},setItem(){}}; global.matchMedia=()=>({matches:false,addEventListener(){}});
global.navigator={}; global.IntersectionObserver=class{observe(){}unobserve(){}disconnect(){}}; global.requestAnimationFrame=()=>{};
global.fetch=(u)=>{ if(!u.includes('/data/')) return Promise.reject(new Error('net'));const f=u.split('/data/')[1].split('?')[0]; const t=fs.readFileSync(root+'/data/'+f,'utf8'); return Promise.resolve({ok:true,json:()=>Promise.resolve(JSON.parse(t)),text:()=>Promise.resolve(t)});};
global.setTimeout=(f)=>0;
const src=fs.readFileSync(root+'/assets/app.js','utf8');
try{ eval(src);}catch(e){console.log('EVAL ERR',e.message)}
setTimeout=global.__st||setTimeout; setImmediate(()=>setImmediate(()=>{ fs.writeFileSync('/tmp/out_'+lang+'_'+id+'.html',stage.innerHTML); console.log(lang,id,'len',stage.innerHTML.length)}));
