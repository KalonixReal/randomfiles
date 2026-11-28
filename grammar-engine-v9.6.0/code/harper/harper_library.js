(()=>{var St=Object.create;var ze=Object.defineProperty;var $t=Object.getOwnPropertyDescriptor;var jt=Object.getOwnPropertyNames;var xt=Object.getPrototypeOf,At=Object.prototype.hasOwnProperty;var Lt=(r=>typeof require<"u"?require:typeof Proxy<"u"?new Proxy(r,{get:(n,e)=>(typeof require<"u"?require:n)[e]}):r)(function(r){if(typeof require<"u")return require.apply(this,arguments);throw Error('Dynamic require of "'+r+'" is not supported')});var zt=(r,n,e,t)=>{if(n&&typeof n=="object"||typeof n=="function")for(let i of jt(n))!At.call(r,i)&&i!==e&&ze(r,i,{get:()=>n[i],enumerable:!(t=$t(n,i))||t.enumerable});return r};var Tt=(r,n,e)=>(e=r!=null?St(xt(r)):{},zt(n||!r||!r.__esModule?ze(e,"default",{value:r,enumerable:!0}):e,r));var Wt=Object.defineProperty,Ve=r=>{throw TypeError(r)},Et=(r,n,e)=>n in r?Wt(r,n,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[n]=e,Kn=(r,n,e)=>Et(r,typeof n!="symbol"?n+"":n,e),Pe=(r,n,e)=>n.has(r)||Ve("Cannot "+e),B=(r,n,e)=>(Pe(r,n,"read from private field"),e?e.call(r):n.get(r)),Te=(r,n,e)=>n.has(r)?Ve("Cannot add the same private member more than once"):n instanceof WeakSet?n.add(r):n.set(r,e),Mn=(r,n,e,t)=>(Pe(r,n,"write to private field"),t?t.call(r,e):n.set(r,e),e),on,k,X=Object.freeze({American:0,0:"American",British:1,1:"British",Australian:2,2:"Australian",Canadian:3,3:"Canadian",Indian:4,4:"Indian"}),fn=Object.freeze({Plain:0,0:"Plain",Markdown:1,1:"Markdown",Typst:2,2:"Typst"}),Q=class On{static __wrap(n){let e=Object.create(On.prototype);return e.__wbg_ptr=n,We.register(e,e.__wbg_ptr,e),e}static __unwrap(n){return n instanceof On?n.__destroy_into_raw():0}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,We.unregister(this),n}free(){let n=this.__destroy_into_raw();s.__wbg_lint_free(n,0)}static from_json(n){let e=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),t=m,i=s.lint_from_json(e,t);if(i[2])throw C(i[1]);return On.__wrap(i[0])}get_problem_text(){let n,e;try{let t=s.lint_get_problem_text(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}lint_kind(){let n,e;try{let t=s.lint_lint_kind(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}lint_kind_pretty(){let n,e;try{let t=s.lint_lint_kind_pretty(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}message(){let n,e;try{let t=s.lint_message(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}message_html(){let n,e;try{let t=s.lint_message_html(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}span(){let n=s.lint_span(this.__wbg_ptr);return Un.__wrap(n)}suggestion_count(){return s.lint_suggestion_count(this.__wbg_ptr)>>>0}suggestions(){let n=s.lint_suggestions(this.__wbg_ptr);var e=Sn(n[0],n[1]);return s.__wbindgen_free(n[0],n[1]*4,4),e}to_json(){let n,e;try{let t=s.lint_to_json(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}};Symbol.dispose&&(Q.prototype[Symbol.dispose]=Q.prototype.free);var te=class re{static __wrap(n){let e=Object.create(re.prototype);return e.__wbg_ptr=n,Ee.register(e,e.__wbg_ptr,e),e}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,Ee.unregister(this),n}free(){let n=this.__destroy_into_raw();s.__wbg_linter_free(n,0)}apply_suggestion(n,e,t){let i,_;try{let g=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),d=m;Zn(e,Q),Zn(t,An);let f=s.linter_apply_suggestion(this.__wbg_ptr,g,d,e.__wbg_ptr,t.__wbg_ptr);var o=f[0],l=f[1];if(f[3])throw o=0,l=0,C(f[2]);return i=o,_=l,p(o,l)}finally{s.__wbindgen_free(i,_,1)}}clear_ignored_lints(){s.linter_clear_ignored_lints(this.__wbg_ptr)}clear_words(){s.linter_clear_words(this.__wbg_ptr)}context_hash(n,e){let t=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),i=m;Zn(e,Q);let _=s.linter_context_hash(this.__wbg_ptr,t,i,e.__wbg_ptr);return BigInt.asUintN(64,_)}export_ignored_lints(){let n,e;try{let t=s.linter_export_ignored_lints(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}export_words(){let n=s.linter_export_words(this.__wbg_ptr);var e=Sn(n[0],n[1]);return s.__wbindgen_free(n[0],n[1]*4,4),e}generate_stats_file(){let n,e;try{let t=s.linter_generate_stats_file(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}get_dialect(){return s.linter_get_dialect(this.__wbg_ptr)}get_lint_config_as_json(){let n,e;try{let t=s.linter_get_lint_config_as_json(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}get_lint_config_as_object(){return s.linter_get_lint_config_as_object(this.__wbg_ptr)}get_lint_descriptions_as_json(){let n,e;try{let t=s.linter_get_lint_descriptions_as_json(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}get_lint_descriptions_as_object(){return s.linter_get_lint_descriptions_as_object(this.__wbg_ptr)}get_lint_descriptions_html_as_json(){let n,e;try{let t=s.linter_get_lint_descriptions_html_as_json(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}get_lint_descriptions_html_as_object(){return s.linter_get_lint_descriptions_html_as_object(this.__wbg_ptr)}get_structured_lint_config_as_json(){let n,e;try{let t=s.linter_get_structured_lint_config_as_json(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}get_structured_lint_config_as_object(){return s.linter_get_structured_lint_config_as_object(this.__wbg_ptr)}ignore_hashes(n){let e=Ct(n,s.__wbindgen_malloc),t=m;s.linter_ignore_hashes(this.__wbg_ptr,e,t)}ignore_lints(n,e){let t=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),i=m,_=ae(e,s.__wbindgen_malloc),o=m;s.linter_ignore_lints(this.__wbg_ptr,t,i,_,o)}import_ignored_lints(n){let e=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),t=m,i=s.linter_import_ignored_lints(this.__wbg_ptr,e,t);if(i[1])throw C(i[0])}import_stats_file(n){let e=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),t=m,i=s.linter_import_stats_file(this.__wbg_ptr,e,t);if(i[1])throw C(i[0])}import_weirpack(n){let e=Nt(n,s.__wbindgen_malloc),t=m,i=s.linter_import_weirpack(this.__wbg_ptr,e,t);if(i[2])throw C(i[1]);return C(i[0])}import_words(n){let e=ae(n,s.__wbindgen_malloc),t=m;s.linter_import_words(this.__wbg_ptr,e,t)}is_likely_english(n){let e=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),t=m;return s.linter_is_likely_english(this.__wbg_ptr,e,t)!==0}isolate_english(n){let e,t;try{let i=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),_=m,o=s.linter_isolate_english(this.__wbg_ptr,i,_);return e=o[0],t=o[1],p(o[0],o[1])}finally{s.__wbindgen_free(e,t,1)}}lint(n,e,t,i,_,o){let l=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),g=m;var d=D(i)?0:v(i,s.__wbindgen_malloc,s.__wbindgen_realloc),f=m;let c=s.linter_lint(this.__wbg_ptr,l,g,e,t,d,f,_,o);var u=Sn(c[0],c[1]);return s.__wbindgen_free(c[0],c[1]*4,4),u}static new(n){let e=s.linter_new(n);return re.__wrap(e)}organized_lints(n,e,t,i,_,o){let l=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),g=m;var d=D(i)?0:v(i,s.__wbindgen_malloc,s.__wbindgen_realloc),f=m;let c=s.linter_organized_lints(this.__wbg_ptr,l,g,e,t,d,f,_,o);var u=Sn(c[0],c[1]);return s.__wbindgen_free(c[0],c[1]*4,4),u}set_lint_config_from_json(n){let e=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),t=m,i=s.linter_set_lint_config_from_json(this.__wbg_ptr,e,t);if(i[1])throw C(i[0])}set_lint_config_from_object(n){let e=s.linter_set_lint_config_from_object(this.__wbg_ptr,n);if(e[1])throw C(e[0])}summarize_stats(n,e){return s.linter_summarize_stats(this.__wbg_ptr,!D(n),D(n)?BigInt(0):n,!D(e),D(e)?BigInt(0):e)}};Symbol.dispose&&(te.prototype[Symbol.dispose]=te.prototype.free);var Dn=class Ge{static __wrap(n){let e=Object.create(Ge.prototype);return e.__wbg_ptr=n,Fe.register(e,e.__wbg_ptr,e),e}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,Fe.unregister(this),n}free(){let n=this.__destroy_into_raw();s.__wbg_organizedgroup_free(n,0)}get group(){let n,e;try{let t=s.__wbg_get_organizedgroup_group(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}get lints(){let n=s.__wbg_get_organizedgroup_lints(this.__wbg_ptr);var e=Sn(n[0],n[1]);return s.__wbindgen_free(n[0],n[1]*4,4),e}set group(n){let e=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),t=m;s.__wbg_set_organizedgroup_group(this.__wbg_ptr,e,t)}set lints(n){let e=ae(n,s.__wbindgen_malloc),t=m;s.__wbg_set_organizedgroup_lints(this.__wbg_ptr,e,t)}};Symbol.dispose&&(Dn.prototype[Symbol.dispose]=Dn.prototype.free);var Un=class kn{static __wrap(n){let e=Object.create(kn.prototype);return e.__wbg_ptr=n,Me.register(e,e.__wbg_ptr,e),e}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,Me.unregister(this),n}free(){let n=this.__destroy_into_raw();s.__wbg_span_free(n,0)}get end(){return s.__wbg_get_span_end(this.__wbg_ptr)>>>0}get start(){return s.__wbg_get_span_start(this.__wbg_ptr)>>>0}set end(n){s.__wbg_set_span_end(this.__wbg_ptr,n)}set start(n){s.__wbg_set_span_start(this.__wbg_ptr,n)}static from_json(n){let e=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),t=m,i=s.span_from_json(e,t);if(i[2])throw C(i[1]);return kn.__wrap(i[0])}is_empty(){return s.span_is_empty(this.__wbg_ptr)!==0}len(){return s.span_len(this.__wbg_ptr)>>>0}static new(n,e){let t=s.span_new(n,e);return kn.__wrap(t)}to_json(){let n,e;try{let t=s.span_to_json(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}};Symbol.dispose&&(Un.prototype[Symbol.dispose]=Un.prototype.free);var An=class ie{static __wrap(n){let e=Object.create(ie.prototype);return e.__wbg_ptr=n,Oe.register(e,e.__wbg_ptr,e),e}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,Oe.unregister(this),n}free(){let n=this.__destroy_into_raw();s.__wbg_suggestion_free(n,0)}static from_json(n){let e=v(n,s.__wbindgen_malloc,s.__wbindgen_realloc),t=m,i=s.suggestion_from_json(e,t);if(i[2])throw C(i[1]);return ie.__wrap(i[0])}get_replacement_text(){let n,e;try{let t=s.suggestion_get_replacement_text(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}kind(){return s.suggestion_kind(this.__wbg_ptr)}to_json(){let n,e;try{let t=s.suggestion_to_json(this.__wbg_ptr);return n=t[0],e=t[1],p(t[0],t[1])}finally{s.__wbindgen_free(n,e,1)}}};Symbol.dispose&&(An.prototype[Symbol.dispose]=An.prototype.free);var zn=Object.freeze({Replace:0,0:"Replace",Remove:1,1:"Remove",InsertAfter:2,2:"InsertAfter"});function Ft(){return s.get_default_lint_config()}function Mt(){let r,n;try{let e=s.get_default_lint_config_as_json();return r=e[0],n=e[1],p(e[0],e[1])}finally{s.__wbindgen_free(r,n,1)}}function Ot(){s.setup()}function kt(r){let n,e;try{let t=v(r,s.__wbindgen_malloc,s.__wbindgen_realloc),i=m,_=s.to_title_case(t,i);return n=_[0],e=_[1],p(_[0],_[1])}finally{s.__wbindgen_free(n,e,1)}}function Je(){return{__proto__:null,"./harper_wasm_slim_bg.js":{__proto__:null,__wbg_Error_30c8987f7c2ed4e2:function(n,e){return Error(p(n,e))},__wbg_String_8564e559799eccda:function(n,e){let t=String(e),i=v(t,s.__wbindgen_malloc,s.__wbindgen_realloc),_=m;F().setInt32(n+4,_,!0),F().setInt32(n+0,i,!0)},__wbg___wbindgen_boolean_get_5b446f51afd21013:function(n){let e=n,t=typeof e=="boolean"?e:void 0;return D(t)?16777215:t?1:0},__wbg___wbindgen_debug_string_4687d8d8c2017d52:function(n,e){let t=se(e),i=v(t,s.__wbindgen_malloc,s.__wbindgen_realloc),_=m;F().setInt32(n+4,_,!0),F().setInt32(n+0,i,!0)},__wbg___wbindgen_is_function_1f9d30630b8b1d3d:function(n){return typeof n=="function"},__wbg___wbindgen_is_object_3c45d4f2dde4e749:function(n){let e=n;return typeof e=="object"&&e!==null},__wbg___wbindgen_is_string_90b56bc79aad6f6c:function(n){return typeof n=="string"},__wbg___wbindgen_jsval_loose_eq_677f21e468d6b461:function(n,e){return n==e},__wbg___wbindgen_number_get_2e0e7dee9f701a71:function(n,e){let t=e,i=typeof t=="number"?t:void 0;F().setFloat64(n+8,D(i)?0:i,!0),F().setInt32(n+0,!D(i),!0)},__wbg___wbindgen_string_get_0380ccaa2f57f0d9:function(n,e){let t=e,i=typeof t=="string"?t:void 0;var _=D(i)?0:v(i,s.__wbindgen_malloc,s.__wbindgen_realloc),o=m;F().setInt32(n+4,o,!0),F().setInt32(n+0,_,!0)},__wbg___wbindgen_throw_41e9ee4f547fc59a:function(n,e){throw new Error(p(n,e))},__wbg_call_6137034ef55c9d0f:function(){return sn(function(n,e){return n.call(e)},arguments)},__wbg_done_b41a1d26cdb37fb6:function(n){return n.done},__wbg_entries_fb6397112b1de25f:function(n){return Object.entries(n)},__wbg_error_757e9472f8410341:function(n,e){let t,i;try{t=n,i=e,console.error(p(n,e))}finally{s.__wbindgen_free(t,i,1)}},__wbg_getRandomValues_973dabfb0ad1769f:function(){return sn(function(n,e){globalThis.crypto.getRandomValues(Qn(n,e))},arguments)},__wbg_getRandomValues_a608c4436c19407a:function(){return sn(function(n,e){globalThis.crypto.getRandomValues(Qn(n,e))},arguments)},__wbg_getTime_f5a55efff2585d5d:function(n){return n.getTime()},__wbg_get_658f6698067d9515:function(){return sn(function(n,e){return Reflect.get(n,e)},arguments)},__wbg_get_6c896e0571ddae51:function(n,e){return n[e>>>0]},__wbg_get_unchecked_288889d017702237:function(n,e){return n[e>>>0]},__wbg_instanceof_ArrayBuffer_a99f175873e5d9b8:function(n){let e;try{e=n instanceof ArrayBuffer}catch{e=!1}return e},__wbg_instanceof_Uint8Array_828cef2aaacafc31:function(n){let e;try{e=n instanceof Uint8Array}catch{e=!1}return e},__wbg_iterator_e3c31c892080e444:function(){return Symbol.iterator},__wbg_length_7f3c00c40364105e:function(n){return n.length},__wbg_length_d4bdea10311bd9cf:function(n){return n.length},__wbg_lint_new:function(n){return Q.__wrap(n)},__wbg_lint_unwrap:function(n){return Q.__unwrap(n)},__wbg_log_1f8cbb01c83d06c2:function(n,e,t,i,_,o,l,g){let d,f;try{d=n,f=e,console.log(p(n,e),p(t,i),p(_,o),p(l,g))}finally{s.__wbindgen_free(d,f,1)}},__wbg_log_a54ca6b45e09078a:function(n,e){let t,i;try{t=n,i=e,console.log(p(n,e))}finally{s.__wbindgen_free(t,i,1)}},__wbg_mark_6b7f03786f5e4d61:function(n,e){performance.mark(p(n,e))},__wbg_measure_0e21b33a1c6e3a29:function(){return sn(function(n,e,t,i){let _,o,l,g;try{_=n,o=e,l=t,g=i,performance.measure(p(n,e),p(t,i))}finally{s.__wbindgen_free(_,o,1),s.__wbindgen_free(l,g,1)}},arguments)},__wbg_new_0_72d020f0c63443d4:function(){return new Date},__wbg_new_1dbf7428bba60a42:function(n){return new Uint8Array(n)},__wbg_new_227d7c05414eb861:function(){return new Error},__wbg_new_28744009d011f847:function(){return new Map},__wbg_new_617a8cdb8bb1130e:function(){return new Object},__wbg_new_ee2291f50781bf1d:function(){return new Array},__wbg_next_33784799010f1bbe:function(n){return n.next},__wbg_next_f4aac29c42af995c:function(){return sn(function(n){return n.next()},arguments)},__wbg_organizedgroup_new:function(n){return Dn.__wrap(n)},__wbg_prototypesetcall_bc27214492979395:function(n,e,t){Uint8Array.prototype.set.call(Qn(n,e),t)},__wbg_set_6ae97e73113c4f0b:function(n,e,t){return n.set(e,t)},__wbg_set_6be42768c690e380:function(n,e,t){n[e]=t},__wbg_set_bea140a88be9b277:function(n,e,t){n[e>>>0]=t},__wbg_stack_3b0d974bbf31e44f:function(n,e){let t=e.stack,i=v(t,s.__wbindgen_malloc,s.__wbindgen_realloc),_=m;F().setInt32(n+4,_,!0),F().setInt32(n+0,i,!0)},__wbg_suggestion_new:function(n){return An.__wrap(n)},__wbg_value_f3c585ee8f5ba40c:function(n){return n.value},__wbindgen_generic_0000000000000001:function(n){return n},__wbindgen_generic_0000000000000002:function(n,e){return p(n,e)},__wbindgen_init_externref_table:function(){let n=s.__wbindgen_externrefs,e=n.grow(4);n.set(0,void 0),n.set(e+0,void 0),n.set(e+1,null),n.set(e+2,!0),n.set(e+3,!1)}}}}var We=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>s.__wbg_lint_free(r,1)),Ee=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>s.__wbg_linter_free(r,1)),Fe=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>s.__wbg_organizedgroup_free(r,1)),Me=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>s.__wbg_span_free(r,1)),Oe=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>s.__wbg_suggestion_free(r,1));function qe(r){let n=s.__externref_table_alloc();return s.__wbindgen_externrefs.set(n,r),n}function Zn(r,n){if(!(r instanceof n))throw new Error(`expected instance of ${n.name}`)}function se(r){let n=typeof r;if(n=="number"||n=="boolean"||r==null)return`${r}`;if(n=="string")return`"${r}"`;if(n=="symbol"){let i=r.description;return i==null?"Symbol":`Symbol(${i})`}if(n=="function"){let i=r.name;return typeof i=="string"&&i.length>0?`Function(${i})`:"Function"}if(Array.isArray(r)){let i=r.length,_="[";i>0&&(_+=se(r[0]));for(let o=1;o<i;o++)_+=", "+se(r[o]);return _+="]",_}let e=/\[object ([^\]]+)\]/.exec(toString.call(r)),t;if(e&&e.length>1)t=e[1];else return toString.call(r);if(t=="Object")try{return"Object("+JSON.stringify(r)+")"}catch{return"Object"}return r instanceof Error?`${r.name}: ${r.message}
${r.stack}`:t}function Sn(r,n){r=r>>>0;let e=F(),t=[];for(let i=r;i<r+4*n;i+=4)t.push(s.__wbindgen_externrefs.get(e.getUint32(i,!0)));return s.__externref_drop_slice(r,n),t}function Qn(r,n){return r=r>>>0,_n().subarray(r/1,r/1+n)}var hn=null;function Rt(){return(hn===null||hn.byteLength===0)&&(hn=new BigUint64Array(s.memory.buffer)),hn}var K=null;function F(){return(K===null||K.buffer.detached===!0||K.buffer.detached===void 0&&K.buffer!==s.memory.buffer)&&(K=new DataView(s.memory.buffer)),K}function p(r,n){return Ut(r>>>0,n)}var bn=null;function _n(){return(bn===null||bn.byteLength===0)&&(bn=new Uint8Array(s.memory.buffer)),bn}function sn(r,n){try{return r.apply(this,n)}catch(e){let t=qe(e);s.__wbindgen_exn_store(t)}}function D(r){return r==null}function Ct(r,n){let e=n(r.length*8,8)>>>0;return Rt().set(r,e/8),m=r.length,e}function Nt(r,n){let e=n(r.length*1,1)>>>0;return _n().set(r,e/1),m=r.length,e}function ae(r,n){let e=n(r.length*4,4)>>>0;for(let t=0;t<r.length;t++){let i=qe(r[t]);F().setUint32(e+4*t,i,!0)}return m=r.length,e}function v(r,n,e){if(e===void 0){let l=$n.encode(r),g=n(l.length,1)>>>0;return _n().subarray(g,g+l.length).set(l),m=l.length,g}let t=r.length,i=n(t,1)>>>0,_=_n(),o=0;for(;o<t;o++){let l=r.charCodeAt(o);if(l>127)break;_[i+o]=l}if(o!==t){o!==0&&(r=r.slice(o)),i=e(i,t,t=o+r.length*3,1)>>>0;let l=_n().subarray(i+o,i+t),g=$n.encodeInto(r,l);o+=g.written,i=e(i,t,o,1)>>>0}return m=o,i}function C(r){let n=s.__wbindgen_externrefs.get(r);return s.__externref_table_dealloc(r),n}var Rn=new TextDecoder("utf-8",{ignoreBOM:!0,fatal:!0});Rn.decode();var Dt=2146435072,Yn=0;function Ut(r,n){return Yn+=n,Yn>=Dt&&(Rn=new TextDecoder("utf-8",{ignoreBOM:!0,fatal:!0}),Rn.decode(),Yn=n),Rn.decode(_n().subarray(r,r+n))}var $n=new TextEncoder;"encodeInto"in $n||($n.encodeInto=function(r,n){let e=$n.encode(r);return n.set(e),{read:r.length,written:e.length}});var m=0,s;function He(r,n){return s=r.exports,hn=null,K=null,bn=null,s.__wbindgen_start(),s}async function It(r,n){if(typeof Response=="function"&&r instanceof Response){if(!r.ok)throw new Error(`failed to fetch Wasm: ${r.status} ${r.statusText} fetching '${r.url}'`);if(typeof WebAssembly.instantiateStreaming=="function")try{return await WebAssembly.instantiateStreaming(r,n)}catch(i){if(e(r.type)&&r.headers.get("Content-Type")!=="application/wasm")console.warn("`WebAssembly.instantiateStreaming` failed because your server does not serve Wasm with `application/wasm` MIME type. Falling back to `WebAssembly.instantiate` which is slower. Original error:\n",i);else throw i}let t=await r.arrayBuffer();return await WebAssembly.instantiate(t,n)}else{let t=await WebAssembly.instantiate(r,n);return t instanceof WebAssembly.Instance?{instance:t,module:r}:t}function e(t){switch(t){case"basic":case"cors":case"default":return!0}return!1}}function Bt(r){if(s!==void 0)return s;r!==void 0&&(Object.getPrototypeOf(r)===Object.prototype?{module:r}=r:console.warn("using deprecated parameters for `initSync()`; pass a single object instead"));let n=Je();r instanceof WebAssembly.Module||(r=new WebAssembly.Module(r));let e=new WebAssembly.Instance(r,n);return He(e)}async function Ke(r){if(s!==void 0)return s;r!==void 0&&(Object.getPrototypeOf(r)===Object.prototype?{module_or_path:r}=r:console.warn("using deprecated parameters for the initialization function; pass a single object instead")),r===void 0&&(r=new URL);let n=Je();(typeof r=="string"||typeof Request=="function"&&r instanceof Request||typeof URL=="function"&&r instanceof URL)&&(r=fetch(r));let{instance:e}=await It(await r,n);return He(e)}var Vt=Object.freeze(Object.defineProperty({__proto__:null,Dialect:X,Language:fn,Lint:Q,Linter:te,OrganizedGroup:Dn,Span:Un,Suggestion:An,SuggestionKind:zn,default:Ke,get_default_lint_config:Ft,get_default_lint_config_as_json:Mt,initSync:Bt,setup:Ot,to_title_case:kt},Symbol.toStringTag,{value:"Module"})),Pt=Object.freeze({American:0,0:"American",British:1,1:"British",Australian:2,2:"Australian",Canadian:3,3:"Canadian",Indian:4,4:"Indian"}),Gt=Object.freeze({Plain:0,0:"Plain",Markdown:1,1:"Markdown",Typst:2,2:"Typst"}),V=class r{static __wrap(n){let e=Object.create(r.prototype);return e.__wbg_ptr=n,ke.register(e,e.__wbg_ptr,e),e}static __unwrap(n){return n instanceof r?n.__destroy_into_raw():0}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,ke.unregister(this),n}free(){let n=this.__destroy_into_raw();a.__wbg_lint_free(n,0)}static from_json(n){let e=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),t=h,i=a.lint_from_json(e,t);if(i[2])throw N(i[1]);return r.__wrap(i[0])}get_problem_text(){let n,e;try{let t=a.lint_get_problem_text(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}lint_kind(){let n,e;try{let t=a.lint_lint_kind(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}lint_kind_pretty(){let n,e;try{let t=a.lint_lint_kind_pretty(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}message(){let n,e;try{let t=a.lint_message(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}message_html(){let n,e;try{let t=a.lint_message_html(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}span(){let n=a.lint_span(this.__wbg_ptr);return gn.__wrap(n)}suggestion_count(){return a.lint_suggestion_count(this.__wbg_ptr)>>>0}suggestions(){let n=a.lint_suggestions(this.__wbg_ptr);var e=jn(n[0],n[1]);return a.__wbindgen_free(n[0],n[1]*4,4),e}to_json(){let n,e;try{let t=a.lint_to_json(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}};Symbol.dispose&&(V.prototype[Symbol.dispose]=V.prototype.free);var Ln=class r{static __wrap(n){let e=Object.create(r.prototype);return e.__wbg_ptr=n,Re.register(e,e.__wbg_ptr,e),e}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,Re.unregister(this),n}free(){let n=this.__destroy_into_raw();a.__wbg_linter_free(n,0)}apply_suggestion(n,e,t){let i,_;try{let g=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),d=h;Xn(e,V),Xn(t,Y);let f=a.linter_apply_suggestion(this.__wbg_ptr,g,d,e.__wbg_ptr,t.__wbg_ptr);var o=f[0],l=f[1];if(f[3])throw o=0,l=0,N(f[2]);return i=o,_=l,w(o,l)}finally{a.__wbindgen_free(i,_,1)}}clear_ignored_lints(){a.linter_clear_ignored_lints(this.__wbg_ptr)}clear_words(){a.linter_clear_words(this.__wbg_ptr)}context_hash(n,e){let t=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),i=h;Xn(e,V);let _=a.linter_context_hash(this.__wbg_ptr,t,i,e.__wbg_ptr);return BigInt.asUintN(64,_)}export_ignored_lints(){let n,e;try{let t=a.linter_export_ignored_lints(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}export_words(){let n=a.linter_export_words(this.__wbg_ptr);var e=jn(n[0],n[1]);return a.__wbindgen_free(n[0],n[1]*4,4),e}generate_stats_file(){let n,e;try{let t=a.linter_generate_stats_file(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}get_dialect(){return a.linter_get_dialect(this.__wbg_ptr)}get_lint_config_as_json(){let n,e;try{let t=a.linter_get_lint_config_as_json(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}get_lint_config_as_object(){return a.linter_get_lint_config_as_object(this.__wbg_ptr)}get_lint_descriptions_as_json(){let n,e;try{let t=a.linter_get_lint_descriptions_as_json(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}get_lint_descriptions_as_object(){return a.linter_get_lint_descriptions_as_object(this.__wbg_ptr)}get_lint_descriptions_html_as_json(){let n,e;try{let t=a.linter_get_lint_descriptions_html_as_json(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}get_lint_descriptions_html_as_object(){return a.linter_get_lint_descriptions_html_as_object(this.__wbg_ptr)}get_structured_lint_config_as_json(){let n,e;try{let t=a.linter_get_structured_lint_config_as_json(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}get_structured_lint_config_as_object(){return a.linter_get_structured_lint_config_as_object(this.__wbg_ptr)}ignore_hashes(n){let e=Yt(n,a.__wbindgen_malloc),t=h;a.linter_ignore_hashes(this.__wbg_ptr,e,t)}ignore_lints(n,e){let t=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),i=h,_=_e(e,a.__wbindgen_malloc),o=h;a.linter_ignore_lints(this.__wbg_ptr,t,i,_,o)}import_ignored_lints(n){let e=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),t=h,i=a.linter_import_ignored_lints(this.__wbg_ptr,e,t);if(i[1])throw N(i[0])}import_stats_file(n){let e=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),t=h,i=a.linter_import_stats_file(this.__wbg_ptr,e,t);if(i[1])throw N(i[0])}import_weirpack(n){let e=Xt(n,a.__wbindgen_malloc),t=h,i=a.linter_import_weirpack(this.__wbg_ptr,e,t);if(i[2])throw N(i[1]);return N(i[0])}import_words(n){let e=_e(n,a.__wbindgen_malloc),t=h;a.linter_import_words(this.__wbg_ptr,e,t)}is_likely_english(n){let e=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),t=h;return a.linter_is_likely_english(this.__wbg_ptr,e,t)!==0}isolate_english(n){let e,t;try{let i=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),_=h,o=a.linter_isolate_english(this.__wbg_ptr,i,_);return e=o[0],t=o[1],w(o[0],o[1])}finally{a.__wbindgen_free(e,t,1)}}lint(n,e,t,i,_,o){let l=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),g=h;var d=U(i)?0:S(i,a.__wbindgen_malloc,a.__wbindgen_realloc),f=h;let c=a.linter_lint(this.__wbg_ptr,l,g,e,t,d,f,_,o);var u=jn(c[0],c[1]);return a.__wbindgen_free(c[0],c[1]*4,4),u}static new(n){let e=a.linter_new(n);return r.__wrap(e)}organized_lints(n,e,t,i,_,o){let l=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),g=h;var d=U(i)?0:S(i,a.__wbindgen_malloc,a.__wbindgen_realloc),f=h;let c=a.linter_organized_lints(this.__wbg_ptr,l,g,e,t,d,f,_,o);var u=jn(c[0],c[1]);return a.__wbindgen_free(c[0],c[1]*4,4),u}set_lint_config_from_json(n){let e=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),t=h,i=a.linter_set_lint_config_from_json(this.__wbg_ptr,e,t);if(i[1])throw N(i[0])}set_lint_config_from_object(n){let e=a.linter_set_lint_config_from_object(this.__wbg_ptr,n);if(e[1])throw N(e[0])}summarize_stats(n,e){return a.linter_summarize_stats(this.__wbg_ptr,!U(n),U(n)?BigInt(0):n,!U(e),U(e)?BigInt(0):e)}};Symbol.dispose&&(Ln.prototype[Symbol.dispose]=Ln.prototype.free);var cn=class r{static __wrap(n){let e=Object.create(r.prototype);return e.__wbg_ptr=n,Ce.register(e,e.__wbg_ptr,e),e}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,Ce.unregister(this),n}free(){let n=this.__destroy_into_raw();a.__wbg_organizedgroup_free(n,0)}get group(){let n,e;try{let t=a.__wbg_get_organizedgroup_group(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}get lints(){let n=a.__wbg_get_organizedgroup_lints(this.__wbg_ptr);var e=jn(n[0],n[1]);return a.__wbindgen_free(n[0],n[1]*4,4),e}set group(n){let e=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),t=h;a.__wbg_set_organizedgroup_group(this.__wbg_ptr,e,t)}set lints(n){let e=_e(n,a.__wbindgen_malloc),t=h;a.__wbg_set_organizedgroup_lints(this.__wbg_ptr,e,t)}};Symbol.dispose&&(cn.prototype[Symbol.dispose]=cn.prototype.free);var gn=class r{static __wrap(n){let e=Object.create(r.prototype);return e.__wbg_ptr=n,Ne.register(e,e.__wbg_ptr,e),e}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,Ne.unregister(this),n}free(){let n=this.__destroy_into_raw();a.__wbg_span_free(n,0)}get end(){return a.__wbg_get_span_end(this.__wbg_ptr)>>>0}get start(){return a.__wbg_get_span_start(this.__wbg_ptr)>>>0}set end(n){a.__wbg_set_span_end(this.__wbg_ptr,n)}set start(n){a.__wbg_set_span_start(this.__wbg_ptr,n)}static from_json(n){let e=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),t=h,i=a.span_from_json(e,t);if(i[2])throw N(i[1]);return r.__wrap(i[0])}is_empty(){return a.span_is_empty(this.__wbg_ptr)!==0}len(){return a.span_len(this.__wbg_ptr)>>>0}static new(n,e){let t=a.span_new(n,e);return r.__wrap(t)}to_json(){let n,e;try{let t=a.span_to_json(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}};Symbol.dispose&&(gn.prototype[Symbol.dispose]=gn.prototype.free);var Y=class r{static __wrap(n){let e=Object.create(r.prototype);return e.__wbg_ptr=n,De.register(e,e.__wbg_ptr,e),e}__destroy_into_raw(){let n=this.__wbg_ptr;return this.__wbg_ptr=0,De.unregister(this),n}free(){let n=this.__destroy_into_raw();a.__wbg_suggestion_free(n,0)}static from_json(n){let e=S(n,a.__wbindgen_malloc,a.__wbindgen_realloc),t=h,i=a.suggestion_from_json(e,t);if(i[2])throw N(i[1]);return r.__wrap(i[0])}get_replacement_text(){let n,e;try{let t=a.suggestion_get_replacement_text(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}kind(){return a.suggestion_kind(this.__wbg_ptr)}to_json(){let n,e;try{let t=a.suggestion_to_json(this.__wbg_ptr);return n=t[0],e=t[1],w(t[0],t[1])}finally{a.__wbindgen_free(n,e,1)}}};Symbol.dispose&&(Y.prototype[Symbol.dispose]=Y.prototype.free);var Jt=Object.freeze({Replace:0,0:"Replace",Remove:1,1:"Remove",InsertAfter:2,2:"InsertAfter"});function qt(){return a.get_default_lint_config()}function Ht(){let r,n;try{let e=a.get_default_lint_config_as_json();return r=e[0],n=e[1],w(e[0],e[1])}finally{a.__wbindgen_free(r,n,1)}}function Kt(){a.setup()}function Zt(r){let n,e;try{let t=S(r,a.__wbindgen_malloc,a.__wbindgen_realloc),i=h,_=a.to_title_case(t,i);return n=_[0],e=_[1],w(_[0],_[1])}finally{a.__wbindgen_free(n,e,1)}}function Ze(){return{__proto__:null,"./harper_wasm_bg.js":{__proto__:null,__wbg_Error_30c8987f7c2ed4e2:function(n,e){return Error(w(n,e))},__wbg_String_8564e559799eccda:function(n,e){let t=String(e),i=S(t,a.__wbindgen_malloc,a.__wbindgen_realloc),_=h;M().setInt32(n+4,_,!0),M().setInt32(n+0,i,!0)},__wbg___wbindgen_boolean_get_5b446f51afd21013:function(n){let e=n,t=typeof e=="boolean"?e:void 0;return U(t)?16777215:t?1:0},__wbg___wbindgen_debug_string_4687d8d8c2017d52:function(n,e){let t=oe(e),i=S(t,a.__wbindgen_malloc,a.__wbindgen_realloc),_=h;M().setInt32(n+4,_,!0),M().setInt32(n+0,i,!0)},__wbg___wbindgen_is_function_1f9d30630b8b1d3d:function(n){return typeof n=="function"},__wbg___wbindgen_is_object_3c45d4f2dde4e749:function(n){let e=n;return typeof e=="object"&&e!==null},__wbg___wbindgen_is_string_90b56bc79aad6f6c:function(n){return typeof n=="string"},__wbg___wbindgen_jsval_loose_eq_677f21e468d6b461:function(n,e){return n==e},__wbg___wbindgen_number_get_2e0e7dee9f701a71:function(n,e){let t=e,i=typeof t=="number"?t:void 0;M().setFloat64(n+8,U(i)?0:i,!0),M().setInt32(n+0,!U(i),!0)},__wbg___wbindgen_string_get_0380ccaa2f57f0d9:function(n,e){let t=e,i=typeof t=="string"?t:void 0;var _=U(i)?0:S(i,a.__wbindgen_malloc,a.__wbindgen_realloc),o=h;M().setInt32(n+4,o,!0),M().setInt32(n+0,_,!0)},__wbg___wbindgen_throw_41e9ee4f547fc59a:function(n,e){throw new Error(w(n,e))},__wbg_call_6137034ef55c9d0f:function(){return an(function(n,e){return n.call(e)},arguments)},__wbg_done_b41a1d26cdb37fb6:function(n){return n.done},__wbg_entries_fb6397112b1de25f:function(n){return Object.entries(n)},__wbg_error_757e9472f8410341:function(n,e){let t,i;try{t=n,i=e,console.error(w(n,e))}finally{a.__wbindgen_free(t,i,1)}},__wbg_getRandomValues_973dabfb0ad1769f:function(){return an(function(n,e){globalThis.crypto.getRandomValues(ne(n,e))},arguments)},__wbg_getRandomValues_a608c4436c19407a:function(){return an(function(n,e){globalThis.crypto.getRandomValues(ne(n,e))},arguments)},__wbg_getTime_f5a55efff2585d5d:function(n){return n.getTime()},__wbg_get_658f6698067d9515:function(){return an(function(n,e){return Reflect.get(n,e)},arguments)},__wbg_get_6c896e0571ddae51:function(n,e){return n[e>>>0]},__wbg_get_unchecked_288889d017702237:function(n,e){return n[e>>>0]},__wbg_instanceof_ArrayBuffer_a99f175873e5d9b8:function(n){let e;try{e=n instanceof ArrayBuffer}catch{e=!1}return e},__wbg_instanceof_Uint8Array_828cef2aaacafc31:function(n){let e;try{e=n instanceof Uint8Array}catch{e=!1}return e},__wbg_iterator_e3c31c892080e444:function(){return Symbol.iterator},__wbg_length_7f3c00c40364105e:function(n){return n.length},__wbg_length_d4bdea10311bd9cf:function(n){return n.length},__wbg_lint_new:function(n){return V.__wrap(n)},__wbg_lint_unwrap:function(n){return V.__unwrap(n)},__wbg_log_1f8cbb01c83d06c2:function(n,e,t,i,_,o,l,g){let d,f;try{d=n,f=e,console.log(w(n,e),w(t,i),w(_,o),w(l,g))}finally{a.__wbindgen_free(d,f,1)}},__wbg_log_a54ca6b45e09078a:function(n,e){let t,i;try{t=n,i=e,console.log(w(n,e))}finally{a.__wbindgen_free(t,i,1)}},__wbg_mark_6b7f03786f5e4d61:function(n,e){performance.mark(w(n,e))},__wbg_measure_0e21b33a1c6e3a29:function(){return an(function(n,e,t,i){let _,o,l,g;try{_=n,o=e,l=t,g=i,performance.measure(w(n,e),w(t,i))}finally{a.__wbindgen_free(_,o,1),a.__wbindgen_free(l,g,1)}},arguments)},__wbg_new_0_72d020f0c63443d4:function(){return new Date},__wbg_new_1dbf7428bba60a42:function(n){return new Uint8Array(n)},__wbg_new_227d7c05414eb861:function(){return new Error},__wbg_new_28744009d011f847:function(){return new Map},__wbg_new_617a8cdb8bb1130e:function(){return new Object},__wbg_new_ee2291f50781bf1d:function(){return new Array},__wbg_next_33784799010f1bbe:function(n){return n.next},__wbg_next_f4aac29c42af995c:function(){return an(function(n){return n.next()},arguments)},__wbg_organizedgroup_new:function(n){return cn.__wrap(n)},__wbg_prototypesetcall_bc27214492979395:function(n,e,t){Uint8Array.prototype.set.call(ne(n,e),t)},__wbg_set_6ae97e73113c4f0b:function(n,e,t){return n.set(e,t)},__wbg_set_6be42768c690e380:function(n,e,t){n[e]=t},__wbg_set_bea140a88be9b277:function(n,e,t){n[e>>>0]=t},__wbg_stack_3b0d974bbf31e44f:function(n,e){let t=e.stack,i=S(t,a.__wbindgen_malloc,a.__wbindgen_realloc),_=h;M().setInt32(n+4,_,!0),M().setInt32(n+0,i,!0)},__wbg_suggestion_new:function(n){return Y.__wrap(n)},__wbg_value_f3c585ee8f5ba40c:function(n){return n.value},__wbindgen_generic_0000000000000001:function(n){return n},__wbindgen_generic_0000000000000002:function(n,e){return w(n,e)},__wbindgen_init_externref_table:function(){let n=a.__wbindgen_externrefs,e=n.grow(4);n.set(0,void 0),n.set(e+0,void 0),n.set(e+1,null),n.set(e+2,!0),n.set(e+3,!1)}}}}var ke=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>a.__wbg_lint_free(r,1)),Re=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>a.__wbg_linter_free(r,1)),Ce=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>a.__wbg_organizedgroup_free(r,1)),Ne=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>a.__wbg_span_free(r,1)),De=typeof FinalizationRegistry>"u"?{register:()=>{},unregister:()=>{}}:new FinalizationRegistry(r=>a.__wbg_suggestion_free(r,1));function Qe(r){let n=a.__externref_table_alloc();return a.__wbindgen_externrefs.set(n,r),n}function Xn(r,n){if(!(r instanceof n))throw new Error(`expected instance of ${n.name}`)}function oe(r){let n=typeof r;if(n=="number"||n=="boolean"||r==null)return`${r}`;if(n=="string")return`"${r}"`;if(n=="symbol"){let i=r.description;return i==null?"Symbol":`Symbol(${i})`}if(n=="function"){let i=r.name;return typeof i=="string"&&i.length>0?`Function(${i})`:"Function"}if(Array.isArray(r)){let i=r.length,_="[";i>0&&(_+=oe(r[0]));for(let o=1;o<i;o++)_+=", "+oe(r[o]);return _+="]",_}let e=/\[object ([^\]]+)\]/.exec(toString.call(r)),t;if(e&&e.length>1)t=e[1];else return toString.call(r);if(t=="Object")try{return"Object("+JSON.stringify(r)+")"}catch{return"Object"}return r instanceof Error?`${r.name}: ${r.message}
${r.stack}`:t}function jn(r,n){r=r>>>0;let e=M(),t=[];for(let i=r;i<r+4*n;i+=4)t.push(a.__wbindgen_externrefs.get(e.getUint32(i,!0)));return a.__externref_drop_slice(r,n),t}function ne(r,n){return r=r>>>0,ln().subarray(r/1,r/1+n)}var yn=null;function Qt(){return(yn===null||yn.byteLength===0)&&(yn=new BigUint64Array(a.memory.buffer)),yn}var Z=null;function M(){return(Z===null||Z.buffer.detached===!0||Z.buffer.detached===void 0&&Z.buffer!==a.memory.buffer)&&(Z=new DataView(a.memory.buffer)),Z}function w(r,n){return er(r>>>0,n)}var vn=null;function ln(){return(vn===null||vn.byteLength===0)&&(vn=new Uint8Array(a.memory.buffer)),vn}function an(r,n){try{return r.apply(this,n)}catch(e){let t=Qe(e);a.__wbindgen_exn_store(t)}}function U(r){return r==null}function Yt(r,n){let e=n(r.length*8,8)>>>0;return Qt().set(r,e/8),h=r.length,e}function Xt(r,n){let e=n(r.length*1,1)>>>0;return ln().set(r,e/1),h=r.length,e}function _e(r,n){let e=n(r.length*4,4)>>>0;for(let t=0;t<r.length;t++){let i=Qe(r[t]);M().setUint32(e+4*t,i,!0)}return h=r.length,e}function S(r,n,e){if(e===void 0){let l=xn.encode(r),g=n(l.length,1)>>>0;return ln().subarray(g,g+l.length).set(l),h=l.length,g}let t=r.length,i=n(t,1)>>>0,_=ln(),o=0;for(;o<t;o++){let l=r.charCodeAt(o);if(l>127)break;_[i+o]=l}if(o!==t){o!==0&&(r=r.slice(o)),i=e(i,t,t=o+r.length*3,1)>>>0;let l=ln().subarray(i+o,i+t),g=xn.encodeInto(r,l);o+=g.written,i=e(i,t,o,1)>>>0}return h=o,i}function N(r){let n=a.__wbindgen_externrefs.get(r);return a.__externref_table_dealloc(r),n}var Cn=new TextDecoder("utf-8",{ignoreBOM:!0,fatal:!0});Cn.decode();var nr=2146435072,ee=0;function er(r,n){return ee+=n,ee>=nr&&(Cn=new TextDecoder("utf-8",{ignoreBOM:!0,fatal:!0}),Cn.decode(),ee=n),Cn.decode(ln().subarray(r,r+n))}var xn=new TextEncoder;"encodeInto"in xn||(xn.encodeInto=function(r,n){let e=xn.encode(r);return n.set(e),{read:r.length,written:e.length}});var h=0,a;function Ye(r,n){return a=r.exports,yn=null,Z=null,vn=null,a.__wbindgen_start(),a}async function tr(r,n){if(typeof Response=="function"&&r instanceof Response){if(!r.ok)throw new Error(`failed to fetch Wasm: ${r.status} ${r.statusText} fetching '${r.url}'`);if(typeof WebAssembly.instantiateStreaming=="function")try{return await WebAssembly.instantiateStreaming(r,n)}catch(i){if(e(r.type)&&r.headers.get("Content-Type")!=="application/wasm")console.warn("`WebAssembly.instantiateStreaming` failed because your server does not serve Wasm with `application/wasm` MIME type. Falling back to `WebAssembly.instantiate` which is slower. Original error:\n",i);else throw i}let t=await r.arrayBuffer();return await WebAssembly.instantiate(t,n)}else{let t=await WebAssembly.instantiate(r,n);return t instanceof WebAssembly.Instance?{instance:t,module:r}:t}function e(t){switch(t){case"basic":case"cors":case"default":return!0}return!1}}function rr(r){if(a!==void 0)return a;r!==void 0&&(Object.getPrototypeOf(r)===Object.prototype?{module:r}=r:console.warn("using deprecated parameters for `initSync()`; pass a single object instead"));let n=Ze();r instanceof WebAssembly.Module||(r=new WebAssembly.Module(r));let e=new WebAssembly.Instance(r,n);return Ye(e)}async function ir(r){if(a!==void 0)return a;r!==void 0&&(Object.getPrototypeOf(r)===Object.prototype?{module_or_path:r}=r:console.warn("using deprecated parameters for the initialization function; pass a single object instead")),r===void 0&&(r=new URL);let n=Ze();(typeof r=="string"||typeof Request=="function"&&r instanceof Request||typeof URL=="function"&&r instanceof URL)&&(r=fetch(r));let{instance:e}=await tr(await r,n);return Ye(e)}var sr=Object.freeze(Object.defineProperty({__proto__:null,Dialect:Pt,Language:Gt,Lint:V,Linter:Ln,OrganizedGroup:cn,Span:gn,Suggestion:Y,SuggestionKind:Jt,default:ir,get_default_lint_config:qt,get_default_lint_config_as_json:Ht,initSync:rr,setup:Kt,to_title_case:Zt},Symbol.toStringTag,{value:"Module"})),ar=class Nn extends Promise{constructor(n){super(e=>{e()}),Te(this,on),Te(this,k),Mn(this,on,n)}static from(n){return new Nn(e=>{e(n())})}static resolve(n){return new Nn(e=>{e(n)})}static reject(n){return new Nn((e,t)=>{t(n)})}then(n,e){return B(this,k)??Mn(this,k,new Promise(B(this,on))),B(this,k).then(n,e)}catch(n){return B(this,k)??Mn(this,k,new Promise(B(this,on))),B(this,k).catch(n)}finally(n){return B(this,k)??Mn(this,k,new Promise(B(this,on))),B(this,k).finally(n)}};on=new WeakMap;k=new WeakMap;var Bn=ar,or=(r,n,e,t)=>{if(e==="length"||e==="prototype"||e==="arguments"||e==="caller")return;let i=Object.getOwnPropertyDescriptor(r,e),_=Object.getOwnPropertyDescriptor(n,e);!_r(i,_)&&t||Object.defineProperty(r,e,_)},_r=function(r,n){return r===void 0||r.configurable||r.writable===n.writable&&r.enumerable===n.enumerable&&r.configurable===n.configurable&&(r.writable||r.value===n.value)},lr=(r,n)=>{let e=Object.getPrototypeOf(n);e!==Object.getPrototypeOf(r)&&Object.setPrototypeOf(r,e)},cr=(r,n)=>`/* Wrapped ${r}*/
${n}`,gr=Object.getOwnPropertyDescriptor(Function.prototype,"toString"),fr=Object.getOwnPropertyDescriptor(Function.prototype.toString,"name"),ur=(r,n,e)=>{let t=e===""?"":`with ${e.trim()}() `,i=cr.bind(null,t,n.toString());Object.defineProperty(i,"name",fr),Object.defineProperty(r,"toString",{...gr,value:i})};function dr(r,n,{ignoreNonConfigurable:e=!1}={}){let{name:t}=r;for(let i of Reflect.ownKeys(n))or(r,n,i,e);return lr(r,n),ur(r,n,t),r}var pr=new WeakMap;function Ue(r,{cacheKey:n=([t])=>t,cache:e=new Map}={}){let t=new Map,i=function(..._){let o=n(_);if(t.has(o))return t.get(o);let l=(async()=>{try{if(e&&await e.has(o))return await e.get(o);let d=await r.apply(this,_);try{return d}finally{e&&await e.set(o,d)}}finally{t.delete(o)}})();return t.set(o,l),l};return dr(i,r,{ignoreNonConfigurable:!0}),pr.set(i,e),i}function wr(r){return r.includes("harper_wasm_slim")?"slim":"full"}function mr(r){return r==="slim"?Vt:sr}function hr(r,n){return n==="slim"?r:r.includes("harper_wasm_bg.wasm")?r.replace("harper_wasm_bg.wasm","harper_wasm_slim_bg.wasm"):null}function Ie(r){return typeof process<"u"&&r.startsWith("file://")?import("fs").then(n=>new Promise((e,t)=>{n.readFile(new URL(r).pathname,(i,_)=>{i&&t(i),e(_)})})):r}async function Be(r,n){let e=mr(n),t=hr(r,n);if(t!=null)try{await Ke({module_or_path:Ie(t)})}catch(i){if(n==="slim")throw i}return await e.default({module_or_path:Ie(r)}),e}var br={full:Ue(r=>Be(r,"full")),slim:Ue(r=>Be(r,"slim"))};function Xe(r,n){return br[n](r)}function ce(r,n){return In.create(r,n)}var In=class{constructor(){Kn(this,"url",""),Kn(this,"glueFlavor","full"),Kn(this,"inner",null)}static create(n,e){let t=new le;return t.url=n,t.glueFlavor=e??wr(typeof n=="string"?n:n.href),t.inner=Bn.from(()=>Xe(typeof t.url=="string"?t.url:t.url.href,t.glueFlavor)),t}async getDefaultLintConfigAsJSON(){return(await this.inner).get_default_lint_config_as_json()}async getDefaultLintConfig(){return(await this.inner).get_default_lint_config()}async toTitleCase(n){return(await this.inner).to_title_case(n)}async setup(){(await this.inner).setup()}},le=class extends In{async createLinter(n){return(await this.getBinaryModule()).Linter.new(n??X.American)}async getBinaryModule(){return await Bn.from(()=>Xe(typeof this.url=="string"?this.url:this.url.href,this.glueFlavor))}};var yr=Object.defineProperty,vr=(r,n,e)=>n in r?yr(r,n,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[n]=e,ge=(r,n,e)=>vr(r,typeof n!="symbol"?n+"":n,e);function Sr(r){switch(r){case"plaintext":return fn.Plain;case"typst":return fn.Typst;case"markdown":case void 0:return fn.Markdown;default:return console.warn(`Unknown Harper language '${String(r)}'; using markdown.`),fn.Markdown}}function nt(r,n){return[r,Sr(n?.language),n?.forceAllHeadings??!1,n?.regex_mask,n?.dedup??!0,n?.isolateEnglish??!1]}var Vn=class{constructor(n){ge(this,"binary"),ge(this,"inner"),ge(this,"disposed",!1),this.binary=n.binary,this.binary.setup(),this.inner=this.createInner(n.dialect)}createInner(n){return Bn.from(async()=>(await this.binary.setup(),this.binary.createLinter(n)))}async setup(){await this.lint("",{language:"plaintext"});let n=await this.exportIgnoredLints();await this.importIgnoredLints(n)}async lint(n,e){return(await this.inner).lint(...nt(n,e))}async organizedLints(n,e){let i=(await this.inner).organized_lints(...nt(n,e)),_={};for(let o of i)_[o.group]=o.lints,o.free();return _}async applySuggestion(n,e,t){return(await this.inner).apply_suggestion(n,e,t)}async isLikelyEnglish(n){return(await this.inner).is_likely_english(n)}async isolateEnglish(n){return(await this.inner).isolate_english(n)}async getLintConfig(){return(await this.inner).get_lint_config_as_object()}async getDefaultLintConfigAsJSON(){return await this.binary.getDefaultLintConfigAsJSON()}async getDefaultLintConfig(){return await this.binary.getDefaultLintConfig()}async getStructuredLintConfig(){return(await this.inner).get_structured_lint_config_as_object()}async getStructuredLintConfigJSON(){return(await this.inner).get_structured_lint_config_as_json()}async setLintConfig(n){(await this.inner).set_lint_config_from_object(n)}async getLintConfigAsJSON(){return(await this.inner).get_lint_config_as_json()}async setLintConfigWithJSON(n){(await this.inner).set_lint_config_from_json(n)}async toTitleCase(n){return await this.binary.toTitleCase(n)}async getLintDescriptions(){return(await this.inner).get_lint_descriptions_as_object()}async getLintDescriptionsAsJSON(){return(await this.inner).get_lint_descriptions_as_json()}async getLintDescriptionsHTML(){return(await this.inner).get_lint_descriptions_html_as_object()}async getLintDescriptionsHTMLAsJSON(){return(await this.inner).get_lint_descriptions_html_as_json()}async ignoreLint(n,e){return await this.ignoreLints(n,[e])}async ignoreLints(n,e){(await this.inner).ignore_lints(n,e)}async ignoreLintHash(n){(await this.inner).ignore_hashes(new BigUint64Array([n]))}async exportIgnoredLints(){return(await this.inner).export_ignored_lints()}async importIgnoredLints(n){(await this.inner).import_ignored_lints(n)}async contextHash(n,e){return(await this.inner).context_hash(n,e)}async clearIgnoredLints(){(await this.inner).clear_ignored_lints()}async clearWords(){return(await this.inner).clear_words()}async importWords(n){return(await this.inner).import_words(n)}async exportWords(){return(await this.inner).export_words()}async getDialect(){return(await this.inner).get_dialect()}async setDialect(n){let e=await this.inner;return e.get_dialect()!==n&&(e.free(),this.inner=this.createInner(n)),Promise.resolve()}async summarizeStats(n,e){return(await this.inner).summarize_stats(n,e)}async generateStatsFile(){return(await this.inner).generate_stats_file()}async importStatsFile(n){return(await this.inner).import_stats_file(n)}async loadWeirpackFromBlob(n){let e=new Uint8Array(await n.arrayBuffer());return this.loadWeirpackFromBytes(e)}async loadWeirpackFromBytes(n){let e=await this.inner,t=n instanceof Uint8Array?n:Uint8Array.from(n);return e.import_weirpack(t)}async dispose(){if(this.disposed)return;this.disposed=!0,(await this.inner).free()}};var $r=`var __defProp = Object.defineProperty;
var __typeError = (msg) => {
  throw TypeError(msg);
};
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __publicField = (obj, key, value) => __defNormalProp(obj, typeof key !== "symbol" ? key + "" : key, value);
var __accessCheck = (obj, member, msg) => member.has(obj) || __typeError("Cannot " + msg);
var __privateGet = (obj, member, getter) => (__accessCheck(obj, member, "read from private field"), getter ? getter.call(obj) : member.get(obj));
var __privateAdd = (obj, member, value) => member.has(obj) ? __typeError("Cannot add the same private member more than once") : member instanceof WeakSet ? member.add(obj) : member.set(obj, value);
var __privateSet = (obj, member, value, setter) => (__accessCheck(obj, member, "write to private field"), setter ? setter.call(obj, value) : member.set(obj, value), value);
var _executor, _promise;
const Dialect$1 = Object.freeze({
  American: 0,
  "0": "American",
  British: 1,
  "1": "British",
  Australian: 2,
  "2": "Australian",
  Canadian: 3,
  "3": "Canadian",
  Indian: 4,
  "4": "Indian"
});
const Language$1 = Object.freeze({
  Plain: 0,
  "0": "Plain",
  Markdown: 1,
  "1": "Markdown",
  Typst: 2,
  "2": "Typst"
});
let Lint$1 = class Lint {
  static __wrap(ptr) {
    const obj = Object.create(Lint.prototype);
    obj.__wbg_ptr = ptr;
    LintFinalization$1.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  static __unwrap(jsValue) {
    if (!(jsValue instanceof Lint)) {
      return 0;
    }
    return jsValue.__destroy_into_raw();
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    LintFinalization$1.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm$1.__wbg_lint_free(ptr, 0);
  }
  /**
   * @param {string} json
   * @returns {Lint}
   */
  static from_json(json) {
    const ptr0 = passStringToWasm0$1(json, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.lint_from_json(ptr0, len0);
    if (ret[2]) {
      throw takeFromExternrefTable0$1(ret[1]);
    }
    return Lint.__wrap(ret[0]);
  }
  /**
   * Get the content of the source material pointed to by [\`Self::span\`]
   * @returns {string}
   */
  get_problem_text() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.lint_get_problem_text(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a string representing the general category of the lint.
   * @returns {string}
   */
  lint_kind() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.lint_lint_kind(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a string representing the general category of the lint.
   * @returns {string}
   */
  lint_kind_pretty() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.lint_lint_kind_pretty(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a description of the error.
   * @returns {string}
   */
  message() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.lint_message(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a description of the error as HTML.
   * @returns {string}
   */
  message_html() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.lint_message_html(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get the location of the problematic text.
   * @returns {Span}
   */
  span() {
    const ret = wasm$1.lint_span(this.__wbg_ptr);
    return Span$1.__wrap(ret);
  }
  /**
   * Equivalent to calling \`.length\` on the result of \`suggestions()\`.
   * @returns {number}
   */
  suggestion_count() {
    const ret = wasm$1.lint_suggestion_count(this.__wbg_ptr);
    return ret >>> 0;
  }
  /**
   * Get an array of any suggestions that may resolve the issue.
   * @returns {Suggestion[]}
   */
  suggestions() {
    const ret = wasm$1.lint_suggestions(this.__wbg_ptr);
    var v1 = getArrayJsValueFromWasm0$1(ret[0], ret[1]);
    wasm$1.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v1;
  }
  /**
   * @returns {string}
   */
  to_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.lint_to_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
};
if (Symbol.dispose) Lint$1.prototype[Symbol.dispose] = Lint$1.prototype.free;
let Linter$1 = class Linter {
  static __wrap(ptr) {
    const obj = Object.create(Linter.prototype);
    obj.__wbg_ptr = ptr;
    LinterFinalization$1.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    LinterFinalization$1.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm$1.__wbg_linter_free(ptr, 0);
  }
  /**
   * Apply a suggestion from a given lint.
   * This action will be logged to the Linter's statistics.
   * @param {string} source_text
   * @param {Lint} lint
   * @param {Suggestion} suggestion
   * @returns {string}
   */
  apply_suggestion(source_text, lint, suggestion) {
    let deferred3_0;
    let deferred3_1;
    try {
      const ptr0 = passStringToWasm0$1(source_text, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
      const len0 = WASM_VECTOR_LEN$1;
      _assertClass$1(lint, Lint$1);
      _assertClass$1(suggestion, Suggestion$1);
      const ret = wasm$1.linter_apply_suggestion(this.__wbg_ptr, ptr0, len0, lint.__wbg_ptr, suggestion.__wbg_ptr);
      var ptr2 = ret[0];
      var len2 = ret[1];
      if (ret[3]) {
        ptr2 = 0;
        len2 = 0;
        throw takeFromExternrefTable0$1(ret[2]);
      }
      deferred3_0 = ptr2;
      deferred3_1 = len2;
      return getStringFromWasm0$1(ptr2, len2);
    } finally {
      wasm$1.__wbindgen_free(deferred3_0, deferred3_1, 1);
    }
  }
  clear_ignored_lints() {
    wasm$1.linter_clear_ignored_lints(this.__wbg_ptr);
  }
  /**
   * Clear the user dictionary.
   */
  clear_words() {
    wasm$1.linter_clear_words(this.__wbg_ptr);
  }
  /**
   * Compute the context hash of a given lint.
   * @param {string} source_text
   * @param {Lint} lint
   * @returns {bigint}
   */
  context_hash(source_text, lint) {
    const ptr0 = passStringToWasm0$1(source_text, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    _assertClass$1(lint, Lint$1);
    const ret = wasm$1.linter_context_hash(this.__wbg_ptr, ptr0, len0, lint.__wbg_ptr);
    return BigInt.asUintN(64, ret);
  }
  /**
   * Export the linter's ignored lints as a privacy-respecting JSON list of hashes.
   * @returns {string}
   */
  export_ignored_lints() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.linter_export_ignored_lints(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Export words from the dictionary.
   * Note: this will only return words previously added by [\`Self::import_words\`].
   * @returns {string[]}
   */
  export_words() {
    const ret = wasm$1.linter_export_words(this.__wbg_ptr);
    var v1 = getArrayJsValueFromWasm0$1(ret[0], ret[1]);
    wasm$1.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v1;
  }
  /**
   * @returns {string}
   */
  generate_stats_file() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.linter_generate_stats_file(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get the dialect this struct was constructed for.
   * @returns {Dialect}
   */
  get_dialect() {
    const ret = wasm$1.linter_get_dialect(this.__wbg_ptr);
    return ret;
  }
  /**
   * @returns {string}
   */
  get_lint_config_as_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.linter_get_lint_config_as_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * @returns {any}
   */
  get_lint_config_as_object() {
    const ret = wasm$1.linter_get_lint_config_as_object(this.__wbg_ptr);
    return ret;
  }
  /**
   * Get a JSON map containing the descriptions of all the linting rules, formatted as Markdown.
   * @returns {string}
   */
  get_lint_descriptions_as_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.linter_get_lint_descriptions_as_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a Record containing the descriptions of all the linting rules, formatted as Markdown.
   * @returns {any}
   */
  get_lint_descriptions_as_object() {
    const ret = wasm$1.linter_get_lint_descriptions_as_object(this.__wbg_ptr);
    return ret;
  }
  /**
   * Get a JSON map containing the descriptions of all the linting rules, formatted as HTML.
   * @returns {string}
   */
  get_lint_descriptions_html_as_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.linter_get_lint_descriptions_html_as_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a Record containing the descriptions of all the linting rules, formatted as HTML.
   * @returns {any}
   */
  get_lint_descriptions_html_as_object() {
    const ret = wasm$1.linter_get_lint_descriptions_html_as_object(this.__wbg_ptr);
    return ret;
  }
  /**
   * @returns {string}
   */
  get_structured_lint_config_as_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.linter_get_structured_lint_config_as_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * @returns {any}
   */
  get_structured_lint_config_as_object() {
    const ret = wasm$1.linter_get_structured_lint_config_as_object(this.__wbg_ptr);
    return ret;
  }
  /**
   * Add a specific context hash to the ignored lints list.
   * @param {BigUint64Array} hashes
   */
  ignore_hashes(hashes) {
    const ptr0 = passArray64ToWasm0$1(hashes, wasm$1.__wbindgen_malloc);
    const len0 = WASM_VECTOR_LEN$1;
    wasm$1.linter_ignore_hashes(this.__wbg_ptr, ptr0, len0);
  }
  /**
   * @param {string} source_text
   * @param {Lint[]} lints
   */
  ignore_lints(source_text, lints) {
    const ptr0 = passStringToWasm0$1(source_text, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ptr1 = passArrayJsValueToWasm0$1(lints, wasm$1.__wbindgen_malloc);
    const len1 = WASM_VECTOR_LEN$1;
    wasm$1.linter_ignore_lints(this.__wbg_ptr, ptr0, len0, ptr1, len1);
  }
  /**
   * Import into the linter's ignored lints from a privacy-respecting JSON list of hashes.
   * @param {string} json
   */
  import_ignored_lints(json) {
    const ptr0 = passStringToWasm0$1(json, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.linter_import_ignored_lints(this.__wbg_ptr, ptr0, len0);
    if (ret[1]) {
      throw takeFromExternrefTable0$1(ret[0]);
    }
  }
  /**
   * @param {string} file
   */
  import_stats_file(file) {
    const ptr0 = passStringToWasm0$1(file, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.linter_import_stats_file(this.__wbg_ptr, ptr0, len0);
    if (ret[1]) {
      throw takeFromExternrefTable0$1(ret[0]);
    }
  }
  /**
   * Load a Weirpack from raw bytes, merging its rules into the current linter.
   * Returns test failures if any are found, and does not import in that case.
   * @param {Uint8Array} bytes
   * @returns {any}
   */
  import_weirpack(bytes) {
    const ptr0 = passArray8ToWasm0$1(bytes, wasm$1.__wbindgen_malloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.linter_import_weirpack(this.__wbg_ptr, ptr0, len0);
    if (ret[2]) {
      throw takeFromExternrefTable0$1(ret[1]);
    }
    return takeFromExternrefTable0$1(ret[0]);
  }
  /**
   * Import words into the dictionary.
   * @param {string[]} additional_words
   */
  import_words(additional_words) {
    const ptr0 = passArrayJsValueToWasm0$1(additional_words, wasm$1.__wbindgen_malloc);
    const len0 = WASM_VECTOR_LEN$1;
    wasm$1.linter_import_words(this.__wbg_ptr, ptr0, len0);
  }
  /**
   * Helper method to quickly check if a plain string is likely intended to be English
   * @param {string} text
   * @returns {boolean}
   */
  is_likely_english(text) {
    const ptr0 = passStringToWasm0$1(text, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.linter_is_likely_english(this.__wbg_ptr, ptr0, len0);
    return ret !== 0;
  }
  /**
   * Helper method to remove non-English text from a plain English document.
   * @param {string} text
   * @returns {string}
   */
  isolate_english(text) {
    let deferred2_0;
    let deferred2_1;
    try {
      const ptr0 = passStringToWasm0$1(text, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
      const len0 = WASM_VECTOR_LEN$1;
      const ret = wasm$1.linter_isolate_english(this.__wbg_ptr, ptr0, len0);
      deferred2_0 = ret[0];
      deferred2_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred2_0, deferred2_1, 1);
    }
  }
  /**
   * Perform the configured linting on the provided text.
   *
   * If the provided regex mask cannot be parsed, this method will return an empty array.
   * @param {string} text
   * @param {Language} language
   * @param {boolean} all_headings
   * @param {string | null | undefined} regex_mask
   * @param {boolean} dedup
   * @param {boolean} isolate_english
   * @returns {Lint[]}
   */
  lint(text, language, all_headings, regex_mask, dedup, isolate_english) {
    const ptr0 = passStringToWasm0$1(text, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    var ptr1 = isLikeNone$1(regex_mask) ? 0 : passStringToWasm0$1(regex_mask, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    var len1 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.linter_lint(this.__wbg_ptr, ptr0, len0, language, all_headings, ptr1, len1, dedup, isolate_english);
    var v3 = getArrayJsValueFromWasm0$1(ret[0], ret[1]);
    wasm$1.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v3;
  }
  /**
   * Construct a new \`Linter\`.
   * Note that this can mean constructing the curated dictionary, which is the most expensive operation
   * in Harper.
   * @param {Dialect} dialect
   * @returns {Linter}
   */
  static new(dialect) {
    const ret = wasm$1.linter_new(dialect);
    return Linter.__wrap(ret);
  }
  /**
   * @param {string} text
   * @param {Language} language
   * @param {boolean} all_headings
   * @param {string | null | undefined} regex_mask
   * @param {boolean} dedup
   * @param {boolean} isolate_english
   * @returns {OrganizedGroup[]}
   */
  organized_lints(text, language, all_headings, regex_mask, dedup, isolate_english) {
    const ptr0 = passStringToWasm0$1(text, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    var ptr1 = isLikeNone$1(regex_mask) ? 0 : passStringToWasm0$1(regex_mask, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    var len1 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.linter_organized_lints(this.__wbg_ptr, ptr0, len0, language, all_headings, ptr1, len1, dedup, isolate_english);
    var v3 = getArrayJsValueFromWasm0$1(ret[0], ret[1]);
    wasm$1.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v3;
  }
  /**
   * @param {string} json
   */
  set_lint_config_from_json(json) {
    const ptr0 = passStringToWasm0$1(json, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.linter_set_lint_config_from_json(this.__wbg_ptr, ptr0, len0);
    if (ret[1]) {
      throw takeFromExternrefTable0$1(ret[0]);
    }
  }
  /**
   * @param {any} object
   */
  set_lint_config_from_object(object) {
    const ret = wasm$1.linter_set_lint_config_from_object(this.__wbg_ptr, object);
    if (ret[1]) {
      throw takeFromExternrefTable0$1(ret[0]);
    }
  }
  /**
   * @param {bigint | null} [start_time]
   * @param {bigint | null} [end_time]
   * @returns {any}
   */
  summarize_stats(start_time, end_time) {
    const ret = wasm$1.linter_summarize_stats(this.__wbg_ptr, !isLikeNone$1(start_time), isLikeNone$1(start_time) ? BigInt(0) : start_time, !isLikeNone$1(end_time), isLikeNone$1(end_time) ? BigInt(0) : end_time);
    return ret;
  }
};
if (Symbol.dispose) Linter$1.prototype[Symbol.dispose] = Linter$1.prototype.free;
let OrganizedGroup$1 = class OrganizedGroup {
  static __wrap(ptr) {
    const obj = Object.create(OrganizedGroup.prototype);
    obj.__wbg_ptr = ptr;
    OrganizedGroupFinalization$1.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    OrganizedGroupFinalization$1.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm$1.__wbg_organizedgroup_free(ptr, 0);
  }
  /**
   * @returns {string}
   */
  get group() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.__wbg_get_organizedgroup_group(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * @returns {Lint[]}
   */
  get lints() {
    const ret = wasm$1.__wbg_get_organizedgroup_lints(this.__wbg_ptr);
    var v1 = getArrayJsValueFromWasm0$1(ret[0], ret[1]);
    wasm$1.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v1;
  }
  /**
   * @param {string} arg0
   */
  set group(arg0) {
    const ptr0 = passStringToWasm0$1(arg0, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    wasm$1.__wbg_set_organizedgroup_group(this.__wbg_ptr, ptr0, len0);
  }
  /**
   * @param {Lint[]} arg0
   */
  set lints(arg0) {
    const ptr0 = passArrayJsValueToWasm0$1(arg0, wasm$1.__wbindgen_malloc);
    const len0 = WASM_VECTOR_LEN$1;
    wasm$1.__wbg_set_organizedgroup_lints(this.__wbg_ptr, ptr0, len0);
  }
};
if (Symbol.dispose) OrganizedGroup$1.prototype[Symbol.dispose] = OrganizedGroup$1.prototype.free;
let Span$1 = class Span {
  static __wrap(ptr) {
    const obj = Object.create(Span.prototype);
    obj.__wbg_ptr = ptr;
    SpanFinalization$1.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    SpanFinalization$1.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm$1.__wbg_span_free(ptr, 0);
  }
  /**
   * @returns {number}
   */
  get end() {
    const ret = wasm$1.__wbg_get_span_end(this.__wbg_ptr);
    return ret >>> 0;
  }
  /**
   * @returns {number}
   */
  get start() {
    const ret = wasm$1.__wbg_get_span_start(this.__wbg_ptr);
    return ret >>> 0;
  }
  /**
   * @param {number} arg0
   */
  set end(arg0) {
    wasm$1.__wbg_set_span_end(this.__wbg_ptr, arg0);
  }
  /**
   * @param {number} arg0
   */
  set start(arg0) {
    wasm$1.__wbg_set_span_start(this.__wbg_ptr, arg0);
  }
  /**
   * @param {string} json
   * @returns {Span}
   */
  static from_json(json) {
    const ptr0 = passStringToWasm0$1(json, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.span_from_json(ptr0, len0);
    if (ret[2]) {
      throw takeFromExternrefTable0$1(ret[1]);
    }
    return Span.__wrap(ret[0]);
  }
  /**
   * @returns {boolean}
   */
  is_empty() {
    const ret = wasm$1.span_is_empty(this.__wbg_ptr);
    return ret !== 0;
  }
  /**
   * @returns {number}
   */
  len() {
    const ret = wasm$1.span_len(this.__wbg_ptr);
    return ret >>> 0;
  }
  /**
   * @param {number} start
   * @param {number} end
   * @returns {Span}
   */
  static new(start, end) {
    const ret = wasm$1.span_new(start, end);
    return Span.__wrap(ret);
  }
  /**
   * @returns {string}
   */
  to_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.span_to_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
};
if (Symbol.dispose) Span$1.prototype[Symbol.dispose] = Span$1.prototype.free;
let Suggestion$1 = class Suggestion {
  static __wrap(ptr) {
    const obj = Object.create(Suggestion.prototype);
    obj.__wbg_ptr = ptr;
    SuggestionFinalization$1.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    SuggestionFinalization$1.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm$1.__wbg_suggestion_free(ptr, 0);
  }
  /**
   * @param {string} json
   * @returns {Suggestion}
   */
  static from_json(json) {
    const ptr0 = passStringToWasm0$1(json, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.suggestion_from_json(ptr0, len0);
    if (ret[2]) {
      throw takeFromExternrefTable0$1(ret[1]);
    }
    return Suggestion.__wrap(ret[0]);
  }
  /**
   * Get the text that is going to replace the problematic section.
   * If [\`Self::kind\`] is \`SuggestionKind::Remove\`, this will return an empty
   * string.
   * @returns {string}
   */
  get_replacement_text() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.suggestion_get_replacement_text(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * @returns {SuggestionKind}
   */
  kind() {
    const ret = wasm$1.suggestion_kind(this.__wbg_ptr);
    return ret;
  }
  /**
   * @returns {string}
   */
  to_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm$1.suggestion_to_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0$1(ret[0], ret[1]);
    } finally {
      wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
};
if (Symbol.dispose) Suggestion$1.prototype[Symbol.dispose] = Suggestion$1.prototype.free;
const SuggestionKind$1 = Object.freeze({
  /**
   * Replace the problematic text.
   */
  Replace: 0,
  "0": "Replace",
  /**
   * Remove the problematic text.
   */
  Remove: 1,
  "1": "Remove",
  /**
   * Insert additional text after the error.
   */
  InsertAfter: 2,
  "2": "InsertAfter"
});
function get_default_lint_config$1() {
  const ret = wasm$1.get_default_lint_config();
  return ret;
}
function get_default_lint_config_as_json$1() {
  let deferred1_0;
  let deferred1_1;
  try {
    const ret = wasm$1.get_default_lint_config_as_json();
    deferred1_0 = ret[0];
    deferred1_1 = ret[1];
    return getStringFromWasm0$1(ret[0], ret[1]);
  } finally {
    wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
  }
}
function setup$1() {
  wasm$1.setup();
}
function to_title_case$1(text) {
  let deferred2_0;
  let deferred2_1;
  try {
    const ptr0 = passStringToWasm0$1(text, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN$1;
    const ret = wasm$1.to_title_case(ptr0, len0);
    deferred2_0 = ret[0];
    deferred2_1 = ret[1];
    return getStringFromWasm0$1(ret[0], ret[1]);
  } finally {
    wasm$1.__wbindgen_free(deferred2_0, deferred2_1, 1);
  }
}
function __wbg_get_imports$1() {
  const import0 = {
    __proto__: null,
    __wbg_Error_30c8987f7c2ed4e2: function(arg0, arg1) {
      const ret = Error(getStringFromWasm0$1(arg0, arg1));
      return ret;
    },
    __wbg_String_8564e559799eccda: function(arg0, arg1) {
      const ret = String(arg1);
      const ptr1 = passStringToWasm0$1(ret, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
      const len1 = WASM_VECTOR_LEN$1;
      getDataViewMemory0$1().setInt32(arg0 + 4 * 1, len1, true);
      getDataViewMemory0$1().setInt32(arg0 + 4 * 0, ptr1, true);
    },
    __wbg___wbindgen_boolean_get_5b446f51afd21013: function(arg0) {
      const v = arg0;
      const ret = typeof v === "boolean" ? v : void 0;
      return isLikeNone$1(ret) ? 16777215 : ret ? 1 : 0;
    },
    __wbg___wbindgen_debug_string_4687d8d8c2017d52: function(arg0, arg1) {
      const ret = debugString$1(arg1);
      const ptr1 = passStringToWasm0$1(ret, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
      const len1 = WASM_VECTOR_LEN$1;
      getDataViewMemory0$1().setInt32(arg0 + 4 * 1, len1, true);
      getDataViewMemory0$1().setInt32(arg0 + 4 * 0, ptr1, true);
    },
    __wbg___wbindgen_is_function_1f9d30630b8b1d3d: function(arg0) {
      const ret = typeof arg0 === "function";
      return ret;
    },
    __wbg___wbindgen_is_object_3c45d4f2dde4e749: function(arg0) {
      const val = arg0;
      const ret = typeof val === "object" && val !== null;
      return ret;
    },
    __wbg___wbindgen_is_string_90b56bc79aad6f6c: function(arg0) {
      const ret = typeof arg0 === "string";
      return ret;
    },
    __wbg___wbindgen_jsval_loose_eq_677f21e468d6b461: function(arg0, arg1) {
      const ret = arg0 == arg1;
      return ret;
    },
    __wbg___wbindgen_number_get_2e0e7dee9f701a71: function(arg0, arg1) {
      const obj = arg1;
      const ret = typeof obj === "number" ? obj : void 0;
      getDataViewMemory0$1().setFloat64(arg0 + 8 * 1, isLikeNone$1(ret) ? 0 : ret, true);
      getDataViewMemory0$1().setInt32(arg0 + 4 * 0, !isLikeNone$1(ret), true);
    },
    __wbg___wbindgen_string_get_0380ccaa2f57f0d9: function(arg0, arg1) {
      const obj = arg1;
      const ret = typeof obj === "string" ? obj : void 0;
      var ptr1 = isLikeNone$1(ret) ? 0 : passStringToWasm0$1(ret, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
      var len1 = WASM_VECTOR_LEN$1;
      getDataViewMemory0$1().setInt32(arg0 + 4 * 1, len1, true);
      getDataViewMemory0$1().setInt32(arg0 + 4 * 0, ptr1, true);
    },
    __wbg___wbindgen_throw_41e9ee4f547fc59a: function(arg0, arg1) {
      throw new Error(getStringFromWasm0$1(arg0, arg1));
    },
    __wbg_call_6137034ef55c9d0f: function() {
      return handleError$1(function(arg0, arg1) {
        const ret = arg0.call(arg1);
        return ret;
      }, arguments);
    },
    __wbg_done_b41a1d26cdb37fb6: function(arg0) {
      const ret = arg0.done;
      return ret;
    },
    __wbg_entries_fb6397112b1de25f: function(arg0) {
      const ret = Object.entries(arg0);
      return ret;
    },
    __wbg_error_757e9472f8410341: function(arg0, arg1) {
      let deferred0_0;
      let deferred0_1;
      try {
        deferred0_0 = arg0;
        deferred0_1 = arg1;
        console.error(getStringFromWasm0$1(arg0, arg1));
      } finally {
        wasm$1.__wbindgen_free(deferred0_0, deferred0_1, 1);
      }
    },
    __wbg_getRandomValues_973dabfb0ad1769f: function() {
      return handleError$1(function(arg0, arg1) {
        globalThis.crypto.getRandomValues(getArrayU8FromWasm0$1(arg0, arg1));
      }, arguments);
    },
    __wbg_getRandomValues_a608c4436c19407a: function() {
      return handleError$1(function(arg0, arg1) {
        globalThis.crypto.getRandomValues(getArrayU8FromWasm0$1(arg0, arg1));
      }, arguments);
    },
    __wbg_getTime_f5a55efff2585d5d: function(arg0) {
      const ret = arg0.getTime();
      return ret;
    },
    __wbg_get_658f6698067d9515: function() {
      return handleError$1(function(arg0, arg1) {
        const ret = Reflect.get(arg0, arg1);
        return ret;
      }, arguments);
    },
    __wbg_get_6c896e0571ddae51: function(arg0, arg1) {
      const ret = arg0[arg1 >>> 0];
      return ret;
    },
    __wbg_get_unchecked_288889d017702237: function(arg0, arg1) {
      const ret = arg0[arg1 >>> 0];
      return ret;
    },
    __wbg_instanceof_ArrayBuffer_a99f175873e5d9b8: function(arg0) {
      let result;
      try {
        result = arg0 instanceof ArrayBuffer;
      } catch (_) {
        result = false;
      }
      const ret = result;
      return ret;
    },
    __wbg_instanceof_Uint8Array_828cef2aaacafc31: function(arg0) {
      let result;
      try {
        result = arg0 instanceof Uint8Array;
      } catch (_) {
        result = false;
      }
      const ret = result;
      return ret;
    },
    __wbg_iterator_e3c31c892080e444: function() {
      const ret = Symbol.iterator;
      return ret;
    },
    __wbg_length_7f3c00c40364105e: function(arg0) {
      const ret = arg0.length;
      return ret;
    },
    __wbg_length_d4bdea10311bd9cf: function(arg0) {
      const ret = arg0.length;
      return ret;
    },
    __wbg_lint_new: function(arg0) {
      const ret = Lint$1.__wrap(arg0);
      return ret;
    },
    __wbg_lint_unwrap: function(arg0) {
      const ret = Lint$1.__unwrap(arg0);
      return ret;
    },
    __wbg_log_1f8cbb01c83d06c2: function(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7) {
      let deferred0_0;
      let deferred0_1;
      try {
        deferred0_0 = arg0;
        deferred0_1 = arg1;
        console.log(getStringFromWasm0$1(arg0, arg1), getStringFromWasm0$1(arg2, arg3), getStringFromWasm0$1(arg4, arg5), getStringFromWasm0$1(arg6, arg7));
      } finally {
        wasm$1.__wbindgen_free(deferred0_0, deferred0_1, 1);
      }
    },
    __wbg_log_a54ca6b45e09078a: function(arg0, arg1) {
      let deferred0_0;
      let deferred0_1;
      try {
        deferred0_0 = arg0;
        deferred0_1 = arg1;
        console.log(getStringFromWasm0$1(arg0, arg1));
      } finally {
        wasm$1.__wbindgen_free(deferred0_0, deferred0_1, 1);
      }
    },
    __wbg_mark_6b7f03786f5e4d61: function(arg0, arg1) {
      performance.mark(getStringFromWasm0$1(arg0, arg1));
    },
    __wbg_measure_0e21b33a1c6e3a29: function() {
      return handleError$1(function(arg0, arg1, arg2, arg3) {
        let deferred0_0;
        let deferred0_1;
        let deferred1_0;
        let deferred1_1;
        try {
          deferred0_0 = arg0;
          deferred0_1 = arg1;
          deferred1_0 = arg2;
          deferred1_1 = arg3;
          performance.measure(getStringFromWasm0$1(arg0, arg1), getStringFromWasm0$1(arg2, arg3));
        } finally {
          wasm$1.__wbindgen_free(deferred0_0, deferred0_1, 1);
          wasm$1.__wbindgen_free(deferred1_0, deferred1_1, 1);
        }
      }, arguments);
    },
    __wbg_new_0_72d020f0c63443d4: function() {
      const ret = /* @__PURE__ */ new Date();
      return ret;
    },
    __wbg_new_1dbf7428bba60a42: function(arg0) {
      const ret = new Uint8Array(arg0);
      return ret;
    },
    __wbg_new_227d7c05414eb861: function() {
      const ret = new Error();
      return ret;
    },
    __wbg_new_28744009d011f847: function() {
      const ret = /* @__PURE__ */ new Map();
      return ret;
    },
    __wbg_new_617a8cdb8bb1130e: function() {
      const ret = new Object();
      return ret;
    },
    __wbg_new_ee2291f50781bf1d: function() {
      const ret = new Array();
      return ret;
    },
    __wbg_next_33784799010f1bbe: function(arg0) {
      const ret = arg0.next;
      return ret;
    },
    __wbg_next_f4aac29c42af995c: function() {
      return handleError$1(function(arg0) {
        const ret = arg0.next();
        return ret;
      }, arguments);
    },
    __wbg_organizedgroup_new: function(arg0) {
      const ret = OrganizedGroup$1.__wrap(arg0);
      return ret;
    },
    __wbg_prototypesetcall_bc27214492979395: function(arg0, arg1, arg2) {
      Uint8Array.prototype.set.call(getArrayU8FromWasm0$1(arg0, arg1), arg2);
    },
    __wbg_set_6ae97e73113c4f0b: function(arg0, arg1, arg2) {
      const ret = arg0.set(arg1, arg2);
      return ret;
    },
    __wbg_set_6be42768c690e380: function(arg0, arg1, arg2) {
      arg0[arg1] = arg2;
    },
    __wbg_set_bea140a88be9b277: function(arg0, arg1, arg2) {
      arg0[arg1 >>> 0] = arg2;
    },
    __wbg_stack_3b0d974bbf31e44f: function(arg0, arg1) {
      const ret = arg1.stack;
      const ptr1 = passStringToWasm0$1(ret, wasm$1.__wbindgen_malloc, wasm$1.__wbindgen_realloc);
      const len1 = WASM_VECTOR_LEN$1;
      getDataViewMemory0$1().setInt32(arg0 + 4 * 1, len1, true);
      getDataViewMemory0$1().setInt32(arg0 + 4 * 0, ptr1, true);
    },
    __wbg_suggestion_new: function(arg0) {
      const ret = Suggestion$1.__wrap(arg0);
      return ret;
    },
    __wbg_value_f3c585ee8f5ba40c: function(arg0) {
      const ret = arg0.value;
      return ret;
    },
    __wbindgen_generic_0000000000000001: function(arg0) {
      const ret = arg0;
      return ret;
    },
    __wbindgen_generic_0000000000000002: function(arg0, arg1) {
      const ret = getStringFromWasm0$1(arg0, arg1);
      return ret;
    },
    __wbindgen_init_externref_table: function() {
      const table = wasm$1.__wbindgen_externrefs;
      const offset = table.grow(4);
      table.set(0, void 0);
      table.set(offset + 0, void 0);
      table.set(offset + 1, null);
      table.set(offset + 2, true);
      table.set(offset + 3, false);
    }
  };
  return {
    __proto__: null,
    "./harper_wasm_slim_bg.js": import0
  };
}
const LintFinalization$1 = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm$1.__wbg_lint_free(ptr, 1));
const LinterFinalization$1 = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm$1.__wbg_linter_free(ptr, 1));
const OrganizedGroupFinalization$1 = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm$1.__wbg_organizedgroup_free(ptr, 1));
const SpanFinalization$1 = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm$1.__wbg_span_free(ptr, 1));
const SuggestionFinalization$1 = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm$1.__wbg_suggestion_free(ptr, 1));
function addToExternrefTable0$1(obj) {
  const idx = wasm$1.__externref_table_alloc();
  wasm$1.__wbindgen_externrefs.set(idx, obj);
  return idx;
}
function _assertClass$1(instance, klass) {
  if (!(instance instanceof klass)) {
    throw new Error(\`expected instance of \${klass.name}\`);
  }
}
function debugString$1(val) {
  const type = typeof val;
  if (type == "number" || type == "boolean" || val == null) {
    return \`\${val}\`;
  }
  if (type == "string") {
    return \`"\${val}"\`;
  }
  if (type == "symbol") {
    const description = val.description;
    if (description == null) {
      return "Symbol";
    } else {
      return \`Symbol(\${description})\`;
    }
  }
  if (type == "function") {
    const name = val.name;
    if (typeof name == "string" && name.length > 0) {
      return \`Function(\${name})\`;
    } else {
      return "Function";
    }
  }
  if (Array.isArray(val)) {
    const length = val.length;
    let debug = "[";
    if (length > 0) {
      debug += debugString$1(val[0]);
    }
    for (let i = 1; i < length; i++) {
      debug += ", " + debugString$1(val[i]);
    }
    debug += "]";
    return debug;
  }
  const builtInMatches = /\\[object ([^\\]]+)\\]/.exec(toString.call(val));
  let className;
  if (builtInMatches && builtInMatches.length > 1) {
    className = builtInMatches[1];
  } else {
    return toString.call(val);
  }
  if (className == "Object") {
    try {
      return "Object(" + JSON.stringify(val) + ")";
    } catch (_) {
      return "Object";
    }
  }
  if (val instanceof Error) {
    return \`\${val.name}: \${val.message}
\${val.stack}\`;
  }
  return className;
}
function getArrayJsValueFromWasm0$1(ptr, len) {
  ptr = ptr >>> 0;
  const mem = getDataViewMemory0$1();
  const result = [];
  for (let i = ptr; i < ptr + 4 * len; i += 4) {
    result.push(wasm$1.__wbindgen_externrefs.get(mem.getUint32(i, true)));
  }
  wasm$1.__externref_drop_slice(ptr, len);
  return result;
}
function getArrayU8FromWasm0$1(ptr, len) {
  ptr = ptr >>> 0;
  return getUint8ArrayMemory0$1().subarray(ptr / 1, ptr / 1 + len);
}
let cachedBigUint64ArrayMemory0$1 = null;
function getBigUint64ArrayMemory0$1() {
  if (cachedBigUint64ArrayMemory0$1 === null || cachedBigUint64ArrayMemory0$1.byteLength === 0) {
    cachedBigUint64ArrayMemory0$1 = new BigUint64Array(wasm$1.memory.buffer);
  }
  return cachedBigUint64ArrayMemory0$1;
}
let cachedDataViewMemory0$1 = null;
function getDataViewMemory0$1() {
  if (cachedDataViewMemory0$1 === null || cachedDataViewMemory0$1.buffer.detached === true || cachedDataViewMemory0$1.buffer.detached === void 0 && cachedDataViewMemory0$1.buffer !== wasm$1.memory.buffer) {
    cachedDataViewMemory0$1 = new DataView(wasm$1.memory.buffer);
  }
  return cachedDataViewMemory0$1;
}
function getStringFromWasm0$1(ptr, len) {
  return decodeText$1(ptr >>> 0, len);
}
let cachedUint8ArrayMemory0$1 = null;
function getUint8ArrayMemory0$1() {
  if (cachedUint8ArrayMemory0$1 === null || cachedUint8ArrayMemory0$1.byteLength === 0) {
    cachedUint8ArrayMemory0$1 = new Uint8Array(wasm$1.memory.buffer);
  }
  return cachedUint8ArrayMemory0$1;
}
function handleError$1(f, args) {
  try {
    return f.apply(this, args);
  } catch (e) {
    const idx = addToExternrefTable0$1(e);
    wasm$1.__wbindgen_exn_store(idx);
  }
}
function isLikeNone$1(x) {
  return x === void 0 || x === null;
}
function passArray64ToWasm0$1(arg, malloc) {
  const ptr = malloc(arg.length * 8, 8) >>> 0;
  getBigUint64ArrayMemory0$1().set(arg, ptr / 8);
  WASM_VECTOR_LEN$1 = arg.length;
  return ptr;
}
function passArray8ToWasm0$1(arg, malloc) {
  const ptr = malloc(arg.length * 1, 1) >>> 0;
  getUint8ArrayMemory0$1().set(arg, ptr / 1);
  WASM_VECTOR_LEN$1 = arg.length;
  return ptr;
}
function passArrayJsValueToWasm0$1(array, malloc) {
  const ptr = malloc(array.length * 4, 4) >>> 0;
  for (let i = 0; i < array.length; i++) {
    const add = addToExternrefTable0$1(array[i]);
    getDataViewMemory0$1().setUint32(ptr + 4 * i, add, true);
  }
  WASM_VECTOR_LEN$1 = array.length;
  return ptr;
}
function passStringToWasm0$1(arg, malloc, realloc) {
  if (realloc === void 0) {
    const buf = cachedTextEncoder$1.encode(arg);
    const ptr2 = malloc(buf.length, 1) >>> 0;
    getUint8ArrayMemory0$1().subarray(ptr2, ptr2 + buf.length).set(buf);
    WASM_VECTOR_LEN$1 = buf.length;
    return ptr2;
  }
  let len = arg.length;
  let ptr = malloc(len, 1) >>> 0;
  const mem = getUint8ArrayMemory0$1();
  let offset = 0;
  for (; offset < len; offset++) {
    const code = arg.charCodeAt(offset);
    if (code > 127) break;
    mem[ptr + offset] = code;
  }
  if (offset !== len) {
    if (offset !== 0) {
      arg = arg.slice(offset);
    }
    ptr = realloc(ptr, len, len = offset + arg.length * 3, 1) >>> 0;
    const view = getUint8ArrayMemory0$1().subarray(ptr + offset, ptr + len);
    const ret = cachedTextEncoder$1.encodeInto(arg, view);
    offset += ret.written;
    ptr = realloc(ptr, len, offset, 1) >>> 0;
  }
  WASM_VECTOR_LEN$1 = offset;
  return ptr;
}
function takeFromExternrefTable0$1(idx) {
  const value = wasm$1.__wbindgen_externrefs.get(idx);
  wasm$1.__externref_table_dealloc(idx);
  return value;
}
let cachedTextDecoder$1 = new TextDecoder("utf-8", { ignoreBOM: true, fatal: true });
cachedTextDecoder$1.decode();
const MAX_SAFARI_DECODE_BYTES$1 = 2146435072;
let numBytesDecoded$1 = 0;
function decodeText$1(ptr, len) {
  numBytesDecoded$1 += len;
  if (numBytesDecoded$1 >= MAX_SAFARI_DECODE_BYTES$1) {
    cachedTextDecoder$1 = new TextDecoder("utf-8", { ignoreBOM: true, fatal: true });
    cachedTextDecoder$1.decode();
    numBytesDecoded$1 = len;
  }
  return cachedTextDecoder$1.decode(getUint8ArrayMemory0$1().subarray(ptr, ptr + len));
}
const cachedTextEncoder$1 = new TextEncoder();
if (!("encodeInto" in cachedTextEncoder$1)) {
  cachedTextEncoder$1.encodeInto = function(arg, view) {
    const buf = cachedTextEncoder$1.encode(arg);
    view.set(buf);
    return {
      read: arg.length,
      written: buf.length
    };
  };
}
let WASM_VECTOR_LEN$1 = 0;
let wasm$1;
function __wbg_finalize_init$1(instance, module) {
  wasm$1 = instance.exports;
  cachedBigUint64ArrayMemory0$1 = null;
  cachedDataViewMemory0$1 = null;
  cachedUint8ArrayMemory0$1 = null;
  wasm$1.__wbindgen_start();
  return wasm$1;
}
async function __wbg_load$1(module, imports) {
  if (typeof Response === "function" && module instanceof Response) {
    if (!module.ok) {
      throw new Error(\`failed to fetch Wasm: \${module.status} \${module.statusText} fetching '\${module.url}'\`);
    }
    if (typeof WebAssembly.instantiateStreaming === "function") {
      try {
        return await WebAssembly.instantiateStreaming(module, imports);
      } catch (e) {
        const validResponse = expectedResponseType(module.type);
        if (validResponse && module.headers.get("Content-Type") !== "application/wasm") {
          console.warn("\`WebAssembly.instantiateStreaming\` failed because your server does not serve Wasm with \`application/wasm\` MIME type. Falling back to \`WebAssembly.instantiate\` which is slower. Original error:\\n", e);
        } else {
          throw e;
        }
      }
    }
    const bytes = await module.arrayBuffer();
    return await WebAssembly.instantiate(bytes, imports);
  } else {
    const instance = await WebAssembly.instantiate(module, imports);
    if (instance instanceof WebAssembly.Instance) {
      return { instance, module };
    } else {
      return instance;
    }
  }
  function expectedResponseType(type) {
    switch (type) {
      case "basic":
      case "cors":
      case "default":
        return true;
    }
    return false;
  }
}
function initSync$1(module) {
  if (wasm$1 !== void 0) return wasm$1;
  if (module !== void 0) {
    if (Object.getPrototypeOf(module) === Object.prototype) {
      ({ module } = module);
    } else {
      console.warn("using deprecated parameters for \`initSync()\`; pass a single object instead");
    }
  }
  const imports = __wbg_get_imports$1();
  if (!(module instanceof WebAssembly.Module)) {
    module = new WebAssembly.Module(module);
  }
  const instance = new WebAssembly.Instance(module, imports);
  return __wbg_finalize_init$1(instance);
}
async function __wbg_init$1(module_or_path) {
  if (wasm$1 !== void 0) return wasm$1;
  if (module_or_path !== void 0) {
    if (Object.getPrototypeOf(module_or_path) === Object.prototype) {
      ({ module_or_path } = module_or_path);
    } else {
      console.warn("using deprecated parameters for the initialization function; pass a single object instead");
    }
  }
  if (module_or_path === void 0) {
    module_or_path = new URL();
  }
  const imports = __wbg_get_imports$1();
  if (typeof module_or_path === "string" || typeof Request === "function" && module_or_path instanceof Request || typeof URL === "function" && module_or_path instanceof URL) {
    module_or_path = fetch(module_or_path);
  }
  const { instance, module } = await __wbg_load$1(await module_or_path, imports);
  return __wbg_finalize_init$1(instance);
}
var defaultGlue = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  Dialect: Dialect$1,
  Language: Language$1,
  Lint: Lint$1,
  Linter: Linter$1,
  OrganizedGroup: OrganizedGroup$1,
  Span: Span$1,
  Suggestion: Suggestion$1,
  SuggestionKind: SuggestionKind$1,
  default: __wbg_init$1,
  get_default_lint_config: get_default_lint_config$1,
  get_default_lint_config_as_json: get_default_lint_config_as_json$1,
  initSync: initSync$1,
  setup: setup$1,
  to_title_case: to_title_case$1
});
const Dialect = Object.freeze({
  American: 0,
  "0": "American",
  British: 1,
  "1": "British",
  Australian: 2,
  "2": "Australian",
  Canadian: 3,
  "3": "Canadian",
  Indian: 4,
  "4": "Indian"
});
const Language = Object.freeze({
  Plain: 0,
  "0": "Plain",
  Markdown: 1,
  "1": "Markdown",
  Typst: 2,
  "2": "Typst"
});
class Lint2 {
  static __wrap(ptr) {
    const obj = Object.create(Lint2.prototype);
    obj.__wbg_ptr = ptr;
    LintFinalization.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  static __unwrap(jsValue) {
    if (!(jsValue instanceof Lint2)) {
      return 0;
    }
    return jsValue.__destroy_into_raw();
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    LintFinalization.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm.__wbg_lint_free(ptr, 0);
  }
  /**
   * @param {string} json
   * @returns {Lint}
   */
  static from_json(json) {
    const ptr0 = passStringToWasm0(json, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    const ret = wasm.lint_from_json(ptr0, len0);
    if (ret[2]) {
      throw takeFromExternrefTable0(ret[1]);
    }
    return Lint2.__wrap(ret[0]);
  }
  /**
   * Get the content of the source material pointed to by [\`Self::span\`]
   * @returns {string}
   */
  get_problem_text() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.lint_get_problem_text(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a string representing the general category of the lint.
   * @returns {string}
   */
  lint_kind() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.lint_lint_kind(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a string representing the general category of the lint.
   * @returns {string}
   */
  lint_kind_pretty() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.lint_lint_kind_pretty(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a description of the error.
   * @returns {string}
   */
  message() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.lint_message(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a description of the error as HTML.
   * @returns {string}
   */
  message_html() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.lint_message_html(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get the location of the problematic text.
   * @returns {Span}
   */
  span() {
    const ret = wasm.lint_span(this.__wbg_ptr);
    return Span2.__wrap(ret);
  }
  /**
   * Equivalent to calling \`.length\` on the result of \`suggestions()\`.
   * @returns {number}
   */
  suggestion_count() {
    const ret = wasm.lint_suggestion_count(this.__wbg_ptr);
    return ret >>> 0;
  }
  /**
   * Get an array of any suggestions that may resolve the issue.
   * @returns {Suggestion[]}
   */
  suggestions() {
    const ret = wasm.lint_suggestions(this.__wbg_ptr);
    var v1 = getArrayJsValueFromWasm0(ret[0], ret[1]);
    wasm.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v1;
  }
  /**
   * @returns {string}
   */
  to_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.lint_to_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
}
if (Symbol.dispose) Lint2.prototype[Symbol.dispose] = Lint2.prototype.free;
class Linter2 {
  static __wrap(ptr) {
    const obj = Object.create(Linter2.prototype);
    obj.__wbg_ptr = ptr;
    LinterFinalization.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    LinterFinalization.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm.__wbg_linter_free(ptr, 0);
  }
  /**
   * Apply a suggestion from a given lint.
   * This action will be logged to the Linter's statistics.
   * @param {string} source_text
   * @param {Lint} lint
   * @param {Suggestion} suggestion
   * @returns {string}
   */
  apply_suggestion(source_text, lint, suggestion) {
    let deferred3_0;
    let deferred3_1;
    try {
      const ptr0 = passStringToWasm0(source_text, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
      const len0 = WASM_VECTOR_LEN;
      _assertClass(lint, Lint2);
      _assertClass(suggestion, Suggestion2);
      const ret = wasm.linter_apply_suggestion(this.__wbg_ptr, ptr0, len0, lint.__wbg_ptr, suggestion.__wbg_ptr);
      var ptr2 = ret[0];
      var len2 = ret[1];
      if (ret[3]) {
        ptr2 = 0;
        len2 = 0;
        throw takeFromExternrefTable0(ret[2]);
      }
      deferred3_0 = ptr2;
      deferred3_1 = len2;
      return getStringFromWasm0(ptr2, len2);
    } finally {
      wasm.__wbindgen_free(deferred3_0, deferred3_1, 1);
    }
  }
  clear_ignored_lints() {
    wasm.linter_clear_ignored_lints(this.__wbg_ptr);
  }
  /**
   * Clear the user dictionary.
   */
  clear_words() {
    wasm.linter_clear_words(this.__wbg_ptr);
  }
  /**
   * Compute the context hash of a given lint.
   * @param {string} source_text
   * @param {Lint} lint
   * @returns {bigint}
   */
  context_hash(source_text, lint) {
    const ptr0 = passStringToWasm0(source_text, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    _assertClass(lint, Lint2);
    const ret = wasm.linter_context_hash(this.__wbg_ptr, ptr0, len0, lint.__wbg_ptr);
    return BigInt.asUintN(64, ret);
  }
  /**
   * Export the linter's ignored lints as a privacy-respecting JSON list of hashes.
   * @returns {string}
   */
  export_ignored_lints() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.linter_export_ignored_lints(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Export words from the dictionary.
   * Note: this will only return words previously added by [\`Self::import_words\`].
   * @returns {string[]}
   */
  export_words() {
    const ret = wasm.linter_export_words(this.__wbg_ptr);
    var v1 = getArrayJsValueFromWasm0(ret[0], ret[1]);
    wasm.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v1;
  }
  /**
   * @returns {string}
   */
  generate_stats_file() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.linter_generate_stats_file(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get the dialect this struct was constructed for.
   * @returns {Dialect}
   */
  get_dialect() {
    const ret = wasm.linter_get_dialect(this.__wbg_ptr);
    return ret;
  }
  /**
   * @returns {string}
   */
  get_lint_config_as_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.linter_get_lint_config_as_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * @returns {any}
   */
  get_lint_config_as_object() {
    const ret = wasm.linter_get_lint_config_as_object(this.__wbg_ptr);
    return ret;
  }
  /**
   * Get a JSON map containing the descriptions of all the linting rules, formatted as Markdown.
   * @returns {string}
   */
  get_lint_descriptions_as_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.linter_get_lint_descriptions_as_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a Record containing the descriptions of all the linting rules, formatted as Markdown.
   * @returns {any}
   */
  get_lint_descriptions_as_object() {
    const ret = wasm.linter_get_lint_descriptions_as_object(this.__wbg_ptr);
    return ret;
  }
  /**
   * Get a JSON map containing the descriptions of all the linting rules, formatted as HTML.
   * @returns {string}
   */
  get_lint_descriptions_html_as_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.linter_get_lint_descriptions_html_as_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * Get a Record containing the descriptions of all the linting rules, formatted as HTML.
   * @returns {any}
   */
  get_lint_descriptions_html_as_object() {
    const ret = wasm.linter_get_lint_descriptions_html_as_object(this.__wbg_ptr);
    return ret;
  }
  /**
   * @returns {string}
   */
  get_structured_lint_config_as_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.linter_get_structured_lint_config_as_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * @returns {any}
   */
  get_structured_lint_config_as_object() {
    const ret = wasm.linter_get_structured_lint_config_as_object(this.__wbg_ptr);
    return ret;
  }
  /**
   * Add a specific context hash to the ignored lints list.
   * @param {BigUint64Array} hashes
   */
  ignore_hashes(hashes) {
    const ptr0 = passArray64ToWasm0(hashes, wasm.__wbindgen_malloc);
    const len0 = WASM_VECTOR_LEN;
    wasm.linter_ignore_hashes(this.__wbg_ptr, ptr0, len0);
  }
  /**
   * @param {string} source_text
   * @param {Lint[]} lints
   */
  ignore_lints(source_text, lints) {
    const ptr0 = passStringToWasm0(source_text, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    const ptr1 = passArrayJsValueToWasm0(lints, wasm.__wbindgen_malloc);
    const len1 = WASM_VECTOR_LEN;
    wasm.linter_ignore_lints(this.__wbg_ptr, ptr0, len0, ptr1, len1);
  }
  /**
   * Import into the linter's ignored lints from a privacy-respecting JSON list of hashes.
   * @param {string} json
   */
  import_ignored_lints(json) {
    const ptr0 = passStringToWasm0(json, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    const ret = wasm.linter_import_ignored_lints(this.__wbg_ptr, ptr0, len0);
    if (ret[1]) {
      throw takeFromExternrefTable0(ret[0]);
    }
  }
  /**
   * @param {string} file
   */
  import_stats_file(file) {
    const ptr0 = passStringToWasm0(file, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    const ret = wasm.linter_import_stats_file(this.__wbg_ptr, ptr0, len0);
    if (ret[1]) {
      throw takeFromExternrefTable0(ret[0]);
    }
  }
  /**
   * Load a Weirpack from raw bytes, merging its rules into the current linter.
   * Returns test failures if any are found, and does not import in that case.
   * @param {Uint8Array} bytes
   * @returns {any}
   */
  import_weirpack(bytes) {
    const ptr0 = passArray8ToWasm0(bytes, wasm.__wbindgen_malloc);
    const len0 = WASM_VECTOR_LEN;
    const ret = wasm.linter_import_weirpack(this.__wbg_ptr, ptr0, len0);
    if (ret[2]) {
      throw takeFromExternrefTable0(ret[1]);
    }
    return takeFromExternrefTable0(ret[0]);
  }
  /**
   * Import words into the dictionary.
   * @param {string[]} additional_words
   */
  import_words(additional_words) {
    const ptr0 = passArrayJsValueToWasm0(additional_words, wasm.__wbindgen_malloc);
    const len0 = WASM_VECTOR_LEN;
    wasm.linter_import_words(this.__wbg_ptr, ptr0, len0);
  }
  /**
   * Helper method to quickly check if a plain string is likely intended to be English
   * @param {string} text
   * @returns {boolean}
   */
  is_likely_english(text) {
    const ptr0 = passStringToWasm0(text, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    const ret = wasm.linter_is_likely_english(this.__wbg_ptr, ptr0, len0);
    return ret !== 0;
  }
  /**
   * Helper method to remove non-English text from a plain English document.
   * @param {string} text
   * @returns {string}
   */
  isolate_english(text) {
    let deferred2_0;
    let deferred2_1;
    try {
      const ptr0 = passStringToWasm0(text, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
      const len0 = WASM_VECTOR_LEN;
      const ret = wasm.linter_isolate_english(this.__wbg_ptr, ptr0, len0);
      deferred2_0 = ret[0];
      deferred2_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred2_0, deferred2_1, 1);
    }
  }
  /**
   * Perform the configured linting on the provided text.
   *
   * If the provided regex mask cannot be parsed, this method will return an empty array.
   * @param {string} text
   * @param {Language} language
   * @param {boolean} all_headings
   * @param {string | null | undefined} regex_mask
   * @param {boolean} dedup
   * @param {boolean} isolate_english
   * @returns {Lint[]}
   */
  lint(text, language, all_headings, regex_mask, dedup, isolate_english) {
    const ptr0 = passStringToWasm0(text, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    var ptr1 = isLikeNone(regex_mask) ? 0 : passStringToWasm0(regex_mask, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    var len1 = WASM_VECTOR_LEN;
    const ret = wasm.linter_lint(this.__wbg_ptr, ptr0, len0, language, all_headings, ptr1, len1, dedup, isolate_english);
    var v3 = getArrayJsValueFromWasm0(ret[0], ret[1]);
    wasm.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v3;
  }
  /**
   * Construct a new \`Linter\`.
   * Note that this can mean constructing the curated dictionary, which is the most expensive operation
   * in Harper.
   * @param {Dialect} dialect
   * @returns {Linter}
   */
  static new(dialect) {
    const ret = wasm.linter_new(dialect);
    return Linter2.__wrap(ret);
  }
  /**
   * @param {string} text
   * @param {Language} language
   * @param {boolean} all_headings
   * @param {string | null | undefined} regex_mask
   * @param {boolean} dedup
   * @param {boolean} isolate_english
   * @returns {OrganizedGroup[]}
   */
  organized_lints(text, language, all_headings, regex_mask, dedup, isolate_english) {
    const ptr0 = passStringToWasm0(text, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    var ptr1 = isLikeNone(regex_mask) ? 0 : passStringToWasm0(regex_mask, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    var len1 = WASM_VECTOR_LEN;
    const ret = wasm.linter_organized_lints(this.__wbg_ptr, ptr0, len0, language, all_headings, ptr1, len1, dedup, isolate_english);
    var v3 = getArrayJsValueFromWasm0(ret[0], ret[1]);
    wasm.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v3;
  }
  /**
   * @param {string} json
   */
  set_lint_config_from_json(json) {
    const ptr0 = passStringToWasm0(json, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    const ret = wasm.linter_set_lint_config_from_json(this.__wbg_ptr, ptr0, len0);
    if (ret[1]) {
      throw takeFromExternrefTable0(ret[0]);
    }
  }
  /**
   * @param {any} object
   */
  set_lint_config_from_object(object) {
    const ret = wasm.linter_set_lint_config_from_object(this.__wbg_ptr, object);
    if (ret[1]) {
      throw takeFromExternrefTable0(ret[0]);
    }
  }
  /**
   * @param {bigint | null} [start_time]
   * @param {bigint | null} [end_time]
   * @returns {any}
   */
  summarize_stats(start_time, end_time) {
    const ret = wasm.linter_summarize_stats(this.__wbg_ptr, !isLikeNone(start_time), isLikeNone(start_time) ? BigInt(0) : start_time, !isLikeNone(end_time), isLikeNone(end_time) ? BigInt(0) : end_time);
    return ret;
  }
}
if (Symbol.dispose) Linter2.prototype[Symbol.dispose] = Linter2.prototype.free;
class OrganizedGroup2 {
  static __wrap(ptr) {
    const obj = Object.create(OrganizedGroup2.prototype);
    obj.__wbg_ptr = ptr;
    OrganizedGroupFinalization.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    OrganizedGroupFinalization.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm.__wbg_organizedgroup_free(ptr, 0);
  }
  /**
   * @returns {string}
   */
  get group() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.__wbg_get_organizedgroup_group(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * @returns {Lint[]}
   */
  get lints() {
    const ret = wasm.__wbg_get_organizedgroup_lints(this.__wbg_ptr);
    var v1 = getArrayJsValueFromWasm0(ret[0], ret[1]);
    wasm.__wbindgen_free(ret[0], ret[1] * 4, 4);
    return v1;
  }
  /**
   * @param {string} arg0
   */
  set group(arg0) {
    const ptr0 = passStringToWasm0(arg0, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    wasm.__wbg_set_organizedgroup_group(this.__wbg_ptr, ptr0, len0);
  }
  /**
   * @param {Lint[]} arg0
   */
  set lints(arg0) {
    const ptr0 = passArrayJsValueToWasm0(arg0, wasm.__wbindgen_malloc);
    const len0 = WASM_VECTOR_LEN;
    wasm.__wbg_set_organizedgroup_lints(this.__wbg_ptr, ptr0, len0);
  }
}
if (Symbol.dispose) OrganizedGroup2.prototype[Symbol.dispose] = OrganizedGroup2.prototype.free;
class Span2 {
  static __wrap(ptr) {
    const obj = Object.create(Span2.prototype);
    obj.__wbg_ptr = ptr;
    SpanFinalization.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    SpanFinalization.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm.__wbg_span_free(ptr, 0);
  }
  /**
   * @returns {number}
   */
  get end() {
    const ret = wasm.__wbg_get_span_end(this.__wbg_ptr);
    return ret >>> 0;
  }
  /**
   * @returns {number}
   */
  get start() {
    const ret = wasm.__wbg_get_span_start(this.__wbg_ptr);
    return ret >>> 0;
  }
  /**
   * @param {number} arg0
   */
  set end(arg0) {
    wasm.__wbg_set_span_end(this.__wbg_ptr, arg0);
  }
  /**
   * @param {number} arg0
   */
  set start(arg0) {
    wasm.__wbg_set_span_start(this.__wbg_ptr, arg0);
  }
  /**
   * @param {string} json
   * @returns {Span}
   */
  static from_json(json) {
    const ptr0 = passStringToWasm0(json, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    const ret = wasm.span_from_json(ptr0, len0);
    if (ret[2]) {
      throw takeFromExternrefTable0(ret[1]);
    }
    return Span2.__wrap(ret[0]);
  }
  /**
   * @returns {boolean}
   */
  is_empty() {
    const ret = wasm.span_is_empty(this.__wbg_ptr);
    return ret !== 0;
  }
  /**
   * @returns {number}
   */
  len() {
    const ret = wasm.span_len(this.__wbg_ptr);
    return ret >>> 0;
  }
  /**
   * @param {number} start
   * @param {number} end
   * @returns {Span}
   */
  static new(start, end) {
    const ret = wasm.span_new(start, end);
    return Span2.__wrap(ret);
  }
  /**
   * @returns {string}
   */
  to_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.span_to_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
}
if (Symbol.dispose) Span2.prototype[Symbol.dispose] = Span2.prototype.free;
class Suggestion2 {
  static __wrap(ptr) {
    const obj = Object.create(Suggestion2.prototype);
    obj.__wbg_ptr = ptr;
    SuggestionFinalization.register(obj, obj.__wbg_ptr, obj);
    return obj;
  }
  __destroy_into_raw() {
    const ptr = this.__wbg_ptr;
    this.__wbg_ptr = 0;
    SuggestionFinalization.unregister(this);
    return ptr;
  }
  free() {
    const ptr = this.__destroy_into_raw();
    wasm.__wbg_suggestion_free(ptr, 0);
  }
  /**
   * @param {string} json
   * @returns {Suggestion}
   */
  static from_json(json) {
    const ptr0 = passStringToWasm0(json, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    const ret = wasm.suggestion_from_json(ptr0, len0);
    if (ret[2]) {
      throw takeFromExternrefTable0(ret[1]);
    }
    return Suggestion2.__wrap(ret[0]);
  }
  /**
   * Get the text that is going to replace the problematic section.
   * If [\`Self::kind\`] is \`SuggestionKind::Remove\`, this will return an empty
   * string.
   * @returns {string}
   */
  get_replacement_text() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.suggestion_get_replacement_text(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
  /**
   * @returns {SuggestionKind}
   */
  kind() {
    const ret = wasm.suggestion_kind(this.__wbg_ptr);
    return ret;
  }
  /**
   * @returns {string}
   */
  to_json() {
    let deferred1_0;
    let deferred1_1;
    try {
      const ret = wasm.suggestion_to_json(this.__wbg_ptr);
      deferred1_0 = ret[0];
      deferred1_1 = ret[1];
      return getStringFromWasm0(ret[0], ret[1]);
    } finally {
      wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
    }
  }
}
if (Symbol.dispose) Suggestion2.prototype[Symbol.dispose] = Suggestion2.prototype.free;
const SuggestionKind = Object.freeze({
  /**
   * Replace the problematic text.
   */
  Replace: 0,
  "0": "Replace",
  /**
   * Remove the problematic text.
   */
  Remove: 1,
  "1": "Remove",
  /**
   * Insert additional text after the error.
   */
  InsertAfter: 2,
  "2": "InsertAfter"
});
function get_default_lint_config() {
  const ret = wasm.get_default_lint_config();
  return ret;
}
function get_default_lint_config_as_json() {
  let deferred1_0;
  let deferred1_1;
  try {
    const ret = wasm.get_default_lint_config_as_json();
    deferred1_0 = ret[0];
    deferred1_1 = ret[1];
    return getStringFromWasm0(ret[0], ret[1]);
  } finally {
    wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
  }
}
function setup() {
  wasm.setup();
}
function to_title_case(text) {
  let deferred2_0;
  let deferred2_1;
  try {
    const ptr0 = passStringToWasm0(text, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len0 = WASM_VECTOR_LEN;
    const ret = wasm.to_title_case(ptr0, len0);
    deferred2_0 = ret[0];
    deferred2_1 = ret[1];
    return getStringFromWasm0(ret[0], ret[1]);
  } finally {
    wasm.__wbindgen_free(deferred2_0, deferred2_1, 1);
  }
}
function __wbg_get_imports() {
  const import0 = {
    __proto__: null,
    __wbg_Error_30c8987f7c2ed4e2: function(arg0, arg1) {
      const ret = Error(getStringFromWasm0(arg0, arg1));
      return ret;
    },
    __wbg_String_8564e559799eccda: function(arg0, arg1) {
      const ret = String(arg1);
      const ptr1 = passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
      const len1 = WASM_VECTOR_LEN;
      getDataViewMemory0().setInt32(arg0 + 4 * 1, len1, true);
      getDataViewMemory0().setInt32(arg0 + 4 * 0, ptr1, true);
    },
    __wbg___wbindgen_boolean_get_5b446f51afd21013: function(arg0) {
      const v = arg0;
      const ret = typeof v === "boolean" ? v : void 0;
      return isLikeNone(ret) ? 16777215 : ret ? 1 : 0;
    },
    __wbg___wbindgen_debug_string_4687d8d8c2017d52: function(arg0, arg1) {
      const ret = debugString(arg1);
      const ptr1 = passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
      const len1 = WASM_VECTOR_LEN;
      getDataViewMemory0().setInt32(arg0 + 4 * 1, len1, true);
      getDataViewMemory0().setInt32(arg0 + 4 * 0, ptr1, true);
    },
    __wbg___wbindgen_is_function_1f9d30630b8b1d3d: function(arg0) {
      const ret = typeof arg0 === "function";
      return ret;
    },
    __wbg___wbindgen_is_object_3c45d4f2dde4e749: function(arg0) {
      const val = arg0;
      const ret = typeof val === "object" && val !== null;
      return ret;
    },
    __wbg___wbindgen_is_string_90b56bc79aad6f6c: function(arg0) {
      const ret = typeof arg0 === "string";
      return ret;
    },
    __wbg___wbindgen_jsval_loose_eq_677f21e468d6b461: function(arg0, arg1) {
      const ret = arg0 == arg1;
      return ret;
    },
    __wbg___wbindgen_number_get_2e0e7dee9f701a71: function(arg0, arg1) {
      const obj = arg1;
      const ret = typeof obj === "number" ? obj : void 0;
      getDataViewMemory0().setFloat64(arg0 + 8 * 1, isLikeNone(ret) ? 0 : ret, true);
      getDataViewMemory0().setInt32(arg0 + 4 * 0, !isLikeNone(ret), true);
    },
    __wbg___wbindgen_string_get_0380ccaa2f57f0d9: function(arg0, arg1) {
      const obj = arg1;
      const ret = typeof obj === "string" ? obj : void 0;
      var ptr1 = isLikeNone(ret) ? 0 : passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
      var len1 = WASM_VECTOR_LEN;
      getDataViewMemory0().setInt32(arg0 + 4 * 1, len1, true);
      getDataViewMemory0().setInt32(arg0 + 4 * 0, ptr1, true);
    },
    __wbg___wbindgen_throw_41e9ee4f547fc59a: function(arg0, arg1) {
      throw new Error(getStringFromWasm0(arg0, arg1));
    },
    __wbg_call_6137034ef55c9d0f: function() {
      return handleError(function(arg0, arg1) {
        const ret = arg0.call(arg1);
        return ret;
      }, arguments);
    },
    __wbg_done_b41a1d26cdb37fb6: function(arg0) {
      const ret = arg0.done;
      return ret;
    },
    __wbg_entries_fb6397112b1de25f: function(arg0) {
      const ret = Object.entries(arg0);
      return ret;
    },
    __wbg_error_757e9472f8410341: function(arg0, arg1) {
      let deferred0_0;
      let deferred0_1;
      try {
        deferred0_0 = arg0;
        deferred0_1 = arg1;
        console.error(getStringFromWasm0(arg0, arg1));
      } finally {
        wasm.__wbindgen_free(deferred0_0, deferred0_1, 1);
      }
    },
    __wbg_getRandomValues_973dabfb0ad1769f: function() {
      return handleError(function(arg0, arg1) {
        globalThis.crypto.getRandomValues(getArrayU8FromWasm0(arg0, arg1));
      }, arguments);
    },
    __wbg_getRandomValues_a608c4436c19407a: function() {
      return handleError(function(arg0, arg1) {
        globalThis.crypto.getRandomValues(getArrayU8FromWasm0(arg0, arg1));
      }, arguments);
    },
    __wbg_getTime_f5a55efff2585d5d: function(arg0) {
      const ret = arg0.getTime();
      return ret;
    },
    __wbg_get_658f6698067d9515: function() {
      return handleError(function(arg0, arg1) {
        const ret = Reflect.get(arg0, arg1);
        return ret;
      }, arguments);
    },
    __wbg_get_6c896e0571ddae51: function(arg0, arg1) {
      const ret = arg0[arg1 >>> 0];
      return ret;
    },
    __wbg_get_unchecked_288889d017702237: function(arg0, arg1) {
      const ret = arg0[arg1 >>> 0];
      return ret;
    },
    __wbg_instanceof_ArrayBuffer_a99f175873e5d9b8: function(arg0) {
      let result;
      try {
        result = arg0 instanceof ArrayBuffer;
      } catch (_) {
        result = false;
      }
      const ret = result;
      return ret;
    },
    __wbg_instanceof_Uint8Array_828cef2aaacafc31: function(arg0) {
      let result;
      try {
        result = arg0 instanceof Uint8Array;
      } catch (_) {
        result = false;
      }
      const ret = result;
      return ret;
    },
    __wbg_iterator_e3c31c892080e444: function() {
      const ret = Symbol.iterator;
      return ret;
    },
    __wbg_length_7f3c00c40364105e: function(arg0) {
      const ret = arg0.length;
      return ret;
    },
    __wbg_length_d4bdea10311bd9cf: function(arg0) {
      const ret = arg0.length;
      return ret;
    },
    __wbg_lint_new: function(arg0) {
      const ret = Lint2.__wrap(arg0);
      return ret;
    },
    __wbg_lint_unwrap: function(arg0) {
      const ret = Lint2.__unwrap(arg0);
      return ret;
    },
    __wbg_log_1f8cbb01c83d06c2: function(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7) {
      let deferred0_0;
      let deferred0_1;
      try {
        deferred0_0 = arg0;
        deferred0_1 = arg1;
        console.log(getStringFromWasm0(arg0, arg1), getStringFromWasm0(arg2, arg3), getStringFromWasm0(arg4, arg5), getStringFromWasm0(arg6, arg7));
      } finally {
        wasm.__wbindgen_free(deferred0_0, deferred0_1, 1);
      }
    },
    __wbg_log_a54ca6b45e09078a: function(arg0, arg1) {
      let deferred0_0;
      let deferred0_1;
      try {
        deferred0_0 = arg0;
        deferred0_1 = arg1;
        console.log(getStringFromWasm0(arg0, arg1));
      } finally {
        wasm.__wbindgen_free(deferred0_0, deferred0_1, 1);
      }
    },
    __wbg_mark_6b7f03786f5e4d61: function(arg0, arg1) {
      performance.mark(getStringFromWasm0(arg0, arg1));
    },
    __wbg_measure_0e21b33a1c6e3a29: function() {
      return handleError(function(arg0, arg1, arg2, arg3) {
        let deferred0_0;
        let deferred0_1;
        let deferred1_0;
        let deferred1_1;
        try {
          deferred0_0 = arg0;
          deferred0_1 = arg1;
          deferred1_0 = arg2;
          deferred1_1 = arg3;
          performance.measure(getStringFromWasm0(arg0, arg1), getStringFromWasm0(arg2, arg3));
        } finally {
          wasm.__wbindgen_free(deferred0_0, deferred0_1, 1);
          wasm.__wbindgen_free(deferred1_0, deferred1_1, 1);
        }
      }, arguments);
    },
    __wbg_new_0_72d020f0c63443d4: function() {
      const ret = /* @__PURE__ */ new Date();
      return ret;
    },
    __wbg_new_1dbf7428bba60a42: function(arg0) {
      const ret = new Uint8Array(arg0);
      return ret;
    },
    __wbg_new_227d7c05414eb861: function() {
      const ret = new Error();
      return ret;
    },
    __wbg_new_28744009d011f847: function() {
      const ret = /* @__PURE__ */ new Map();
      return ret;
    },
    __wbg_new_617a8cdb8bb1130e: function() {
      const ret = new Object();
      return ret;
    },
    __wbg_new_ee2291f50781bf1d: function() {
      const ret = new Array();
      return ret;
    },
    __wbg_next_33784799010f1bbe: function(arg0) {
      const ret = arg0.next;
      return ret;
    },
    __wbg_next_f4aac29c42af995c: function() {
      return handleError(function(arg0) {
        const ret = arg0.next();
        return ret;
      }, arguments);
    },
    __wbg_organizedgroup_new: function(arg0) {
      const ret = OrganizedGroup2.__wrap(arg0);
      return ret;
    },
    __wbg_prototypesetcall_bc27214492979395: function(arg0, arg1, arg2) {
      Uint8Array.prototype.set.call(getArrayU8FromWasm0(arg0, arg1), arg2);
    },
    __wbg_set_6ae97e73113c4f0b: function(arg0, arg1, arg2) {
      const ret = arg0.set(arg1, arg2);
      return ret;
    },
    __wbg_set_6be42768c690e380: function(arg0, arg1, arg2) {
      arg0[arg1] = arg2;
    },
    __wbg_set_bea140a88be9b277: function(arg0, arg1, arg2) {
      arg0[arg1 >>> 0] = arg2;
    },
    __wbg_stack_3b0d974bbf31e44f: function(arg0, arg1) {
      const ret = arg1.stack;
      const ptr1 = passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
      const len1 = WASM_VECTOR_LEN;
      getDataViewMemory0().setInt32(arg0 + 4 * 1, len1, true);
      getDataViewMemory0().setInt32(arg0 + 4 * 0, ptr1, true);
    },
    __wbg_suggestion_new: function(arg0) {
      const ret = Suggestion2.__wrap(arg0);
      return ret;
    },
    __wbg_value_f3c585ee8f5ba40c: function(arg0) {
      const ret = arg0.value;
      return ret;
    },
    __wbindgen_generic_0000000000000001: function(arg0) {
      const ret = arg0;
      return ret;
    },
    __wbindgen_generic_0000000000000002: function(arg0, arg1) {
      const ret = getStringFromWasm0(arg0, arg1);
      return ret;
    },
    __wbindgen_init_externref_table: function() {
      const table = wasm.__wbindgen_externrefs;
      const offset = table.grow(4);
      table.set(0, void 0);
      table.set(offset + 0, void 0);
      table.set(offset + 1, null);
      table.set(offset + 2, true);
      table.set(offset + 3, false);
    }
  };
  return {
    __proto__: null,
    "./harper_wasm_bg.js": import0
  };
}
const LintFinalization = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm.__wbg_lint_free(ptr, 1));
const LinterFinalization = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm.__wbg_linter_free(ptr, 1));
const OrganizedGroupFinalization = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm.__wbg_organizedgroup_free(ptr, 1));
const SpanFinalization = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm.__wbg_span_free(ptr, 1));
const SuggestionFinalization = typeof FinalizationRegistry === "undefined" ? { register: () => {
}, unregister: () => {
} } : new FinalizationRegistry((ptr) => wasm.__wbg_suggestion_free(ptr, 1));
function addToExternrefTable0(obj) {
  const idx = wasm.__externref_table_alloc();
  wasm.__wbindgen_externrefs.set(idx, obj);
  return idx;
}
function _assertClass(instance, klass) {
  if (!(instance instanceof klass)) {
    throw new Error(\`expected instance of \${klass.name}\`);
  }
}
function debugString(val) {
  const type = typeof val;
  if (type == "number" || type == "boolean" || val == null) {
    return \`\${val}\`;
  }
  if (type == "string") {
    return \`"\${val}"\`;
  }
  if (type == "symbol") {
    const description = val.description;
    if (description == null) {
      return "Symbol";
    } else {
      return \`Symbol(\${description})\`;
    }
  }
  if (type == "function") {
    const name = val.name;
    if (typeof name == "string" && name.length > 0) {
      return \`Function(\${name})\`;
    } else {
      return "Function";
    }
  }
  if (Array.isArray(val)) {
    const length = val.length;
    let debug = "[";
    if (length > 0) {
      debug += debugString(val[0]);
    }
    for (let i = 1; i < length; i++) {
      debug += ", " + debugString(val[i]);
    }
    debug += "]";
    return debug;
  }
  const builtInMatches = /\\[object ([^\\]]+)\\]/.exec(toString.call(val));
  let className;
  if (builtInMatches && builtInMatches.length > 1) {
    className = builtInMatches[1];
  } else {
    return toString.call(val);
  }
  if (className == "Object") {
    try {
      return "Object(" + JSON.stringify(val) + ")";
    } catch (_) {
      return "Object";
    }
  }
  if (val instanceof Error) {
    return \`\${val.name}: \${val.message}
\${val.stack}\`;
  }
  return className;
}
function getArrayJsValueFromWasm0(ptr, len) {
  ptr = ptr >>> 0;
  const mem = getDataViewMemory0();
  const result = [];
  for (let i = ptr; i < ptr + 4 * len; i += 4) {
    result.push(wasm.__wbindgen_externrefs.get(mem.getUint32(i, true)));
  }
  wasm.__externref_drop_slice(ptr, len);
  return result;
}
function getArrayU8FromWasm0(ptr, len) {
  ptr = ptr >>> 0;
  return getUint8ArrayMemory0().subarray(ptr / 1, ptr / 1 + len);
}
let cachedBigUint64ArrayMemory0 = null;
function getBigUint64ArrayMemory0() {
  if (cachedBigUint64ArrayMemory0 === null || cachedBigUint64ArrayMemory0.byteLength === 0) {
    cachedBigUint64ArrayMemory0 = new BigUint64Array(wasm.memory.buffer);
  }
  return cachedBigUint64ArrayMemory0;
}
let cachedDataViewMemory0 = null;
function getDataViewMemory0() {
  if (cachedDataViewMemory0 === null || cachedDataViewMemory0.buffer.detached === true || cachedDataViewMemory0.buffer.detached === void 0 && cachedDataViewMemory0.buffer !== wasm.memory.buffer) {
    cachedDataViewMemory0 = new DataView(wasm.memory.buffer);
  }
  return cachedDataViewMemory0;
}
function getStringFromWasm0(ptr, len) {
  return decodeText(ptr >>> 0, len);
}
let cachedUint8ArrayMemory0 = null;
function getUint8ArrayMemory0() {
  if (cachedUint8ArrayMemory0 === null || cachedUint8ArrayMemory0.byteLength === 0) {
    cachedUint8ArrayMemory0 = new Uint8Array(wasm.memory.buffer);
  }
  return cachedUint8ArrayMemory0;
}
function handleError(f, args) {
  try {
    return f.apply(this, args);
  } catch (e) {
    const idx = addToExternrefTable0(e);
    wasm.__wbindgen_exn_store(idx);
  }
}
function isLikeNone(x) {
  return x === void 0 || x === null;
}
function passArray64ToWasm0(arg, malloc) {
  const ptr = malloc(arg.length * 8, 8) >>> 0;
  getBigUint64ArrayMemory0().set(arg, ptr / 8);
  WASM_VECTOR_LEN = arg.length;
  return ptr;
}
function passArray8ToWasm0(arg, malloc) {
  const ptr = malloc(arg.length * 1, 1) >>> 0;
  getUint8ArrayMemory0().set(arg, ptr / 1);
  WASM_VECTOR_LEN = arg.length;
  return ptr;
}
function passArrayJsValueToWasm0(array, malloc) {
  const ptr = malloc(array.length * 4, 4) >>> 0;
  for (let i = 0; i < array.length; i++) {
    const add = addToExternrefTable0(array[i]);
    getDataViewMemory0().setUint32(ptr + 4 * i, add, true);
  }
  WASM_VECTOR_LEN = array.length;
  return ptr;
}
function passStringToWasm0(arg, malloc, realloc) {
  if (realloc === void 0) {
    const buf = cachedTextEncoder.encode(arg);
    const ptr2 = malloc(buf.length, 1) >>> 0;
    getUint8ArrayMemory0().subarray(ptr2, ptr2 + buf.length).set(buf);
    WASM_VECTOR_LEN = buf.length;
    return ptr2;
  }
  let len = arg.length;
  let ptr = malloc(len, 1) >>> 0;
  const mem = getUint8ArrayMemory0();
  let offset = 0;
  for (; offset < len; offset++) {
    const code = arg.charCodeAt(offset);
    if (code > 127) break;
    mem[ptr + offset] = code;
  }
  if (offset !== len) {
    if (offset !== 0) {
      arg = arg.slice(offset);
    }
    ptr = realloc(ptr, len, len = offset + arg.length * 3, 1) >>> 0;
    const view = getUint8ArrayMemory0().subarray(ptr + offset, ptr + len);
    const ret = cachedTextEncoder.encodeInto(arg, view);
    offset += ret.written;
    ptr = realloc(ptr, len, offset, 1) >>> 0;
  }
  WASM_VECTOR_LEN = offset;
  return ptr;
}
function takeFromExternrefTable0(idx) {
  const value = wasm.__wbindgen_externrefs.get(idx);
  wasm.__externref_table_dealloc(idx);
  return value;
}
let cachedTextDecoder = new TextDecoder("utf-8", { ignoreBOM: true, fatal: true });
cachedTextDecoder.decode();
const MAX_SAFARI_DECODE_BYTES = 2146435072;
let numBytesDecoded = 0;
function decodeText(ptr, len) {
  numBytesDecoded += len;
  if (numBytesDecoded >= MAX_SAFARI_DECODE_BYTES) {
    cachedTextDecoder = new TextDecoder("utf-8", { ignoreBOM: true, fatal: true });
    cachedTextDecoder.decode();
    numBytesDecoded = len;
  }
  return cachedTextDecoder.decode(getUint8ArrayMemory0().subarray(ptr, ptr + len));
}
const cachedTextEncoder = new TextEncoder();
if (!("encodeInto" in cachedTextEncoder)) {
  cachedTextEncoder.encodeInto = function(arg, view) {
    const buf = cachedTextEncoder.encode(arg);
    view.set(buf);
    return {
      read: arg.length,
      written: buf.length
    };
  };
}
let WASM_VECTOR_LEN = 0;
let wasm;
function __wbg_finalize_init(instance, module) {
  wasm = instance.exports;
  cachedBigUint64ArrayMemory0 = null;
  cachedDataViewMemory0 = null;
  cachedUint8ArrayMemory0 = null;
  wasm.__wbindgen_start();
  return wasm;
}
async function __wbg_load(module, imports) {
  if (typeof Response === "function" && module instanceof Response) {
    if (!module.ok) {
      throw new Error(\`failed to fetch Wasm: \${module.status} \${module.statusText} fetching '\${module.url}'\`);
    }
    if (typeof WebAssembly.instantiateStreaming === "function") {
      try {
        return await WebAssembly.instantiateStreaming(module, imports);
      } catch (e) {
        const validResponse = expectedResponseType(module.type);
        if (validResponse && module.headers.get("Content-Type") !== "application/wasm") {
          console.warn("\`WebAssembly.instantiateStreaming\` failed because your server does not serve Wasm with \`application/wasm\` MIME type. Falling back to \`WebAssembly.instantiate\` which is slower. Original error:\\n", e);
        } else {
          throw e;
        }
      }
    }
    const bytes = await module.arrayBuffer();
    return await WebAssembly.instantiate(bytes, imports);
  } else {
    const instance = await WebAssembly.instantiate(module, imports);
    if (instance instanceof WebAssembly.Instance) {
      return { instance, module };
    } else {
      return instance;
    }
  }
  function expectedResponseType(type) {
    switch (type) {
      case "basic":
      case "cors":
      case "default":
        return true;
    }
    return false;
  }
}
function initSync(module) {
  if (wasm !== void 0) return wasm;
  if (module !== void 0) {
    if (Object.getPrototypeOf(module) === Object.prototype) {
      ({ module } = module);
    } else {
      console.warn("using deprecated parameters for \`initSync()\`; pass a single object instead");
    }
  }
  const imports = __wbg_get_imports();
  if (!(module instanceof WebAssembly.Module)) {
    module = new WebAssembly.Module(module);
  }
  const instance = new WebAssembly.Instance(module, imports);
  return __wbg_finalize_init(instance);
}
async function __wbg_init(module_or_path) {
  if (wasm !== void 0) return wasm;
  if (module_or_path !== void 0) {
    if (Object.getPrototypeOf(module_or_path) === Object.prototype) {
      ({ module_or_path } = module_or_path);
    } else {
      console.warn("using deprecated parameters for the initialization function; pass a single object instead");
    }
  }
  if (module_or_path === void 0) {
    module_or_path = new URL();
  }
  const imports = __wbg_get_imports();
  if (typeof module_or_path === "string" || typeof Request === "function" && module_or_path instanceof Request || typeof URL === "function" && module_or_path instanceof URL) {
    module_or_path = fetch(module_or_path);
  }
  const { instance, module } = await __wbg_load(await module_or_path, imports);
  return __wbg_finalize_init(instance);
}
var fullGlue = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  Dialect,
  Language,
  Lint: Lint2,
  Linter: Linter2,
  OrganizedGroup: OrganizedGroup2,
  Span: Span2,
  Suggestion: Suggestion2,
  SuggestionKind,
  default: __wbg_init,
  get_default_lint_config,
  get_default_lint_config_as_json,
  initSync,
  setup,
  to_title_case
});
const _PLazy = class _PLazy extends Promise {
  constructor(executor) {
    super((resolve) => {
      resolve();
    });
    __privateAdd(this, _executor);
    __privateAdd(this, _promise);
    __privateSet(this, _executor, executor);
  }
  static from(function_) {
    return new _PLazy((resolve) => {
      resolve(function_());
    });
  }
  static resolve(value) {
    return new _PLazy((resolve) => {
      resolve(value);
    });
  }
  static reject(error) {
    return new _PLazy((resolve, reject) => {
      reject(error);
    });
  }
  then(onFulfilled, onRejected) {
    __privateGet(this, _promise) ?? __privateSet(this, _promise, new Promise(__privateGet(this, _executor)));
    return __privateGet(this, _promise).then(onFulfilled, onRejected);
  }
  catch(onRejected) {
    __privateGet(this, _promise) ?? __privateSet(this, _promise, new Promise(__privateGet(this, _executor)));
    return __privateGet(this, _promise).catch(onRejected);
  }
  finally(onFinally) {
    __privateGet(this, _promise) ?? __privateSet(this, _promise, new Promise(__privateGet(this, _executor)));
    return __privateGet(this, _promise).finally(onFinally);
  }
};
_executor = new WeakMap();
_promise = new WeakMap();
let PLazy = _PLazy;
const copyProperty = (to, from, property, ignoreNonConfigurable) => {
  if (property === "length" || property === "prototype") {
    return;
  }
  if (property === "arguments" || property === "caller") {
    return;
  }
  const toDescriptor = Object.getOwnPropertyDescriptor(to, property);
  const fromDescriptor = Object.getOwnPropertyDescriptor(from, property);
  if (!canCopyProperty(toDescriptor, fromDescriptor) && ignoreNonConfigurable) {
    return;
  }
  Object.defineProperty(to, property, fromDescriptor);
};
const canCopyProperty = function(toDescriptor, fromDescriptor) {
  return toDescriptor === void 0 || toDescriptor.configurable || toDescriptor.writable === fromDescriptor.writable && toDescriptor.enumerable === fromDescriptor.enumerable && toDescriptor.configurable === fromDescriptor.configurable && (toDescriptor.writable || toDescriptor.value === fromDescriptor.value);
};
const changePrototype = (to, from) => {
  const fromPrototype = Object.getPrototypeOf(from);
  if (fromPrototype === Object.getPrototypeOf(to)) {
    return;
  }
  Object.setPrototypeOf(to, fromPrototype);
};
const wrappedToString = (withName, fromBody) => \`/* Wrapped \${withName}*/
\${fromBody}\`;
const toStringDescriptor = Object.getOwnPropertyDescriptor(Function.prototype, "toString");
const toStringName = Object.getOwnPropertyDescriptor(Function.prototype.toString, "name");
const changeToString = (to, from, name) => {
  const withName = name === "" ? "" : \`with \${name.trim()}() \`;
  const newToString = wrappedToString.bind(null, withName, from.toString());
  Object.defineProperty(newToString, "name", toStringName);
  Object.defineProperty(to, "toString", { ...toStringDescriptor, value: newToString });
};
function mimicFunction(to, from, { ignoreNonConfigurable = false } = {}) {
  const { name } = to;
  for (const property of Reflect.ownKeys(from)) {
    copyProperty(to, from, property, ignoreNonConfigurable);
  }
  changePrototype(to, from);
  changeToString(to, from, name);
  return to;
}
const cacheStore = /* @__PURE__ */ new WeakMap();
function pMemoize(fn, { cacheKey = ([firstArgument]) => firstArgument, cache = /* @__PURE__ */ new Map() } = {}) {
  const promiseCache = /* @__PURE__ */ new Map();
  const memoized = function(...arguments_) {
    const key = cacheKey(arguments_);
    if (promiseCache.has(key)) {
      return promiseCache.get(key);
    }
    const promise = (async () => {
      try {
        if (cache && await cache.has(key)) {
          return await cache.get(key);
        }
        const promise2 = fn.apply(this, arguments_);
        const result = await promise2;
        try {
          return result;
        } finally {
          if (cache) {
            await cache.set(key, result);
          }
        }
      } finally {
        promiseCache.delete(key);
      }
    })();
    promiseCache.set(key, promise);
    return promise;
  };
  mimicFunction(memoized, fn, {
    ignoreNonConfigurable: true
  });
  cacheStore.set(memoized, cache);
  return memoized;
}
function inferGlueFlavor(binary) {
  return binary.includes("harper_wasm_slim") ? "slim" : "full";
}
function loadGlue(glueFlavor) {
  if (glueFlavor === "slim") {
    return defaultGlue;
  }
  return fullGlue;
}
function getDefaultGlueBinary(binary, glueFlavor) {
  if (glueFlavor === "slim") {
    return binary;
  }
  if (binary.includes("harper_wasm_bg.wasm")) {
    return binary.replace("harper_wasm_bg.wasm", "harper_wasm_slim_bg.wasm");
  }
  return null;
}
function getInitInput(binary) {
  if (typeof process !== "undefined" && binary.startsWith("file://")) {
    return Promise.resolve().then(function() {
      return __viteBrowserExternal$1;
    }).then(
      (fs) => new Promise((resolve, reject) => {
        fs.readFile(new URL(binary).pathname, (err, data) => {
          if (err) reject(err);
          resolve(data);
        });
      })
    );
  }
  return binary;
}
async function loadBinaryUncached(binary, glueFlavor) {
  const exports = loadGlue(glueFlavor);
  const defaultGlueBinary = getDefaultGlueBinary(binary, glueFlavor);
  if (defaultGlueBinary != null) {
    try {
      await __wbg_init$1({ module_or_path: getInitInput(defaultGlueBinary) });
    } catch (err) {
      if (glueFlavor === "slim") {
        throw err;
      }
    }
  }
  await exports.default({ module_or_path: getInitInput(binary) });
  return exports;
}
const loadBinaryByFlavor = {
  full: pMemoize((binary) => loadBinaryUncached(binary, "full")),
  slim: pMemoize((binary) => loadBinaryUncached(binary, "slim"))
};
function loadBinary(binary, glueFlavor) {
  return loadBinaryByFlavor[glueFlavor](binary);
}
class BinaryModuleImpl {
  constructor() {
    __publicField(this, "url", "");
    __publicField(this, "glueFlavor", "full");
    __publicField(this, "inner", null);
  }
  /** Load a binary from a specified URL. This is the only recommended way to construct this type. */
  static create(url, glueFlavor) {
    const module = new SuperBinaryModule();
    module.url = url;
    module.glueFlavor = glueFlavor ?? inferGlueFlavor(typeof url === "string" ? url : url.href);
    module.inner = PLazy.from(
      () => loadBinary(typeof module.url === "string" ? module.url : module.url.href, module.glueFlavor)
    );
    return module;
  }
  async getDefaultLintConfigAsJSON() {
    const exported = await this.inner;
    return exported.get_default_lint_config_as_json();
  }
  async getDefaultLintConfig() {
    const exported = await this.inner;
    return exported.get_default_lint_config();
  }
  async toTitleCase(text) {
    const exported = await this.inner;
    return exported.to_title_case(text);
  }
  async setup() {
    const exported = await this.inner;
    exported.setup();
  }
}
class SuperBinaryModule extends BinaryModuleImpl {
  async createLinter(dialect) {
    const exported = await this.getBinaryModule();
    return exported.Linter.new(dialect ?? Dialect$1.American);
  }
  async getBinaryModule() {
    return await PLazy.from(
      () => loadBinary(typeof this.url === "string" ? this.url : this.url.href, this.glueFlavor)
    );
  }
}
function toWasmLanguage(language) {
  switch (language) {
    case "plaintext":
      return Language$1.Plain;
    case "typst":
      return Language$1.Typst;
    case "markdown":
    case void 0:
      return Language$1.Markdown;
    default:
      console.warn(\`Unknown Harper language '\${String(language)}'; using markdown.\`);
      return Language$1.Markdown;
  }
}
function toWasmLintArgs(text, options) {
  return [
    text,
    toWasmLanguage(options == null ? void 0 : options.language),
    (options == null ? void 0 : options.forceAllHeadings) ?? false,
    options == null ? void 0 : options.regex_mask,
    (options == null ? void 0 : options.dedup) ?? true,
    (options == null ? void 0 : options.isolateEnglish) ?? false
  ];
}
class LocalLinter {
  constructor(init) {
    __publicField(this, "binary");
    __publicField(this, "inner");
    __publicField(this, "disposed", false);
    this.binary = init.binary;
    this.binary.setup();
    this.inner = this.createInner(init.dialect);
  }
  createInner(dialect) {
    return PLazy.from(async () => {
      await this.binary.setup();
      return this.binary.createLinter(dialect);
    });
  }
  async setup() {
    await this.lint("", { language: "plaintext" });
    const exported = await this.exportIgnoredLints();
    await this.importIgnoredLints(exported);
  }
  async lint(text, options) {
    const inner = await this.inner;
    return inner.lint(...toWasmLintArgs(text, options));
  }
  async organizedLints(text, options) {
    const inner = await this.inner;
    const lintGroups = inner.organized_lints(...toWasmLintArgs(text, options));
    const output = {};
    for (const group of lintGroups) {
      output[group.group] = group.lints;
      group.free();
    }
    return output;
  }
  async applySuggestion(text, lint, suggestion) {
    const inner = await this.inner;
    return inner.apply_suggestion(text, lint, suggestion);
  }
  async isLikelyEnglish(text) {
    const inner = await this.inner;
    return inner.is_likely_english(text);
  }
  async isolateEnglish(text) {
    const inner = await this.inner;
    return inner.isolate_english(text);
  }
  async getLintConfig() {
    const inner = await this.inner;
    return inner.get_lint_config_as_object();
  }
  async getDefaultLintConfigAsJSON() {
    return await this.binary.getDefaultLintConfigAsJSON();
  }
  async getDefaultLintConfig() {
    return await this.binary.getDefaultLintConfig();
  }
  async getStructuredLintConfig() {
    const inner = await this.inner;
    return inner.get_structured_lint_config_as_object();
  }
  async getStructuredLintConfigJSON() {
    const inner = await this.inner;
    return inner.get_structured_lint_config_as_json();
  }
  async setLintConfig(config) {
    const inner = await this.inner;
    inner.set_lint_config_from_object(config);
  }
  async getLintConfigAsJSON() {
    const inner = await this.inner;
    return inner.get_lint_config_as_json();
  }
  async setLintConfigWithJSON(config) {
    const inner = await this.inner;
    inner.set_lint_config_from_json(config);
  }
  async toTitleCase(text) {
    return await this.binary.toTitleCase(text);
  }
  async getLintDescriptions() {
    const inner = await this.inner;
    return inner.get_lint_descriptions_as_object();
  }
  async getLintDescriptionsAsJSON() {
    const inner = await this.inner;
    return inner.get_lint_descriptions_as_json();
  }
  async getLintDescriptionsHTML() {
    const inner = await this.inner;
    return inner.get_lint_descriptions_html_as_object();
  }
  async getLintDescriptionsHTMLAsJSON() {
    const inner = await this.inner;
    return inner.get_lint_descriptions_html_as_json();
  }
  async ignoreLint(source, lint) {
    return await this.ignoreLints(source, [lint]);
  }
  async ignoreLints(source, lints) {
    const inner = await this.inner;
    inner.ignore_lints(source, lints);
  }
  async ignoreLintHash(hash) {
    const inner = await this.inner;
    inner.ignore_hashes(new BigUint64Array([hash]));
  }
  async exportIgnoredLints() {
    const inner = await this.inner;
    return inner.export_ignored_lints();
  }
  async importIgnoredLints(json) {
    const inner = await this.inner;
    inner.import_ignored_lints(json);
  }
  async contextHash(source, lint) {
    const inner = await this.inner;
    return inner.context_hash(source, lint);
  }
  async clearIgnoredLints() {
    const inner = await this.inner;
    inner.clear_ignored_lints();
  }
  async clearWords() {
    const inner = await this.inner;
    return inner.clear_words();
  }
  async importWords(words) {
    const inner = await this.inner;
    return inner.import_words(words);
  }
  async exportWords() {
    const inner = await this.inner;
    return inner.export_words();
  }
  async getDialect() {
    const inner = await this.inner;
    return inner.get_dialect();
  }
  async setDialect(dialect) {
    const inner = await this.inner;
    if (inner.get_dialect() !== dialect) {
      inner.free();
      this.inner = this.createInner(dialect);
    }
    return Promise.resolve();
  }
  async summarizeStats(start, end) {
    const inner = await this.inner;
    return inner.summarize_stats(start, end);
  }
  async generateStatsFile() {
    const inner = await this.inner;
    return inner.generate_stats_file();
  }
  async importStatsFile(statsFile) {
    const inner = await this.inner;
    return inner.import_stats_file(statsFile);
  }
  /**
   * Load a Weirpack from a Blob.
   *
   * Returns \`undefined\` if tests pass and rules are imported, otherwise returns
   * the Weirpack test failures.
   */
  async loadWeirpackFromBlob(blob) {
    const bytes = new Uint8Array(await blob.arrayBuffer());
    return this.loadWeirpackFromBytes(bytes);
  }
  /**
   * Load a Weirpack from a byte array.
   *
   * Returns \`undefined\` if tests pass and rules are imported, otherwise returns
   * the Weirpack test failures.
   */
  async loadWeirpackFromBytes(bytes) {
    const inner = await this.inner;
    const data = bytes instanceof Uint8Array ? bytes : Uint8Array.from(bytes);
    const result = inner.import_weirpack(data);
    return result;
  }
  async dispose() {
    if (this.disposed) {
      return;
    }
    this.disposed = true;
    const inner = await this.inner;
    inner.free();
  }
}
function assert(condition, message) {
  if (!condition) {
    throw new Error("Assertion failed");
  }
}
function isSerializedRequest(v) {
  return typeof v === "object" && v !== null && "procName" in v && "args" in v;
}
class Serializer {
  constructor(binary) {
    __publicField(this, "binary");
    this.binary = binary;
    this.binary.setup();
  }
  async serializeArg(arg) {
    var _a;
    const { Lint: Lint3, Span: Span3, Suggestion: Suggestion3 } = await this.binary.getBinaryModule();
    if (Array.isArray(arg)) {
      return {
        json: JSON.stringify(await Promise.all(arg.map((a) => this.serializeArg(a)))),
        type: "Array"
      };
    }
    const argType = typeof arg;
    switch (argType) {
      case "string":
      case "number":
      case "boolean":
      case "undefined":
        return { json: JSON.stringify(arg), type: argType };
      case "bigint":
        return { json: arg.toString(), type: argType };
    }
    if (arg.to_json !== void 0) {
      const json = arg.to_json();
      let type;
      const constructorName = (_a = arg.constructor) == null ? void 0 : _a.name;
      if (arg instanceof Lint3 || constructorName === "Lint") {
        type = "Lint";
      } else if (arg instanceof Suggestion3 || constructorName === "Suggestion") {
        type = "Suggestion";
      } else if (arg instanceof Span3 || constructorName === "Span") {
        type = "Span";
      }
      if (type === void 0) {
        throw new Error("Unhandled case: type undefined");
      }
      return { json, type };
    }
    if (argType == "object") {
      return {
        json: JSON.stringify(
          await Promise.all(
            Object.entries(arg).map(([key, value]) => this.serializeArg([key, value]))
          )
        ),
        type: "object"
      };
    }
    throw new Error(\`Unhandled case: \${arg}\`);
  }
  async serialize(req) {
    return {
      procName: req.procName,
      args: await Promise.all(req.args.map((arg) => this.serializeArg(arg)))
    };
  }
  async deserializeArg(requestArg) {
    const { Lint: Lint3, Span: Span3, Suggestion: Suggestion3 } = await this.binary.getBinaryModule();
    switch (requestArg.type) {
      case "bigint":
        return BigInt(requestArg.json);
      case "undefined":
        return void 0;
      case "boolean":
      case "number":
      case "string":
        return JSON.parse(requestArg.json);
      case "Suggestion":
        return Suggestion3.from_json(requestArg.json);
      case "Lint":
        return Lint3.from_json(requestArg.json);
      case "Span":
        return Span3.from_json(requestArg.json);
      case "Array": {
        const parsed = JSON.parse(requestArg.json);
        assert(Array.isArray(parsed));
        return await Promise.all(parsed.map((arg) => this.deserializeArg(arg)));
      }
      case "object": {
        const parsed = JSON.parse(requestArg.json);
        return Object.fromEntries(
          await Promise.all(parsed.map((val) => this.deserializeArg(val)))
        );
      }
      default:
        throw new Error(\`Unhandled case: \${requestArg.type}\`);
    }
  }
  async deserialize(request) {
    return {
      procName: request.procName,
      args: await Promise.all(request.args.map((arg) => this.deserializeArg(arg)))
    };
  }
}
self.postMessage("ready");
self.onmessage = (e) => {
  const [binaryUrl, dialect, glueFlavor] = e.data;
  if (typeof binaryUrl !== "string") {
    throw new TypeError(\`Expected binary to be a string of url but got \${typeof binaryUrl}.\`);
  }
  if (glueFlavor !== void 0 && glueFlavor !== "full" && glueFlavor !== "slim") {
    throw new TypeError(\`Expected glue flavor to be "full" or "slim" but got \${glueFlavor}.\`);
  }
  const binary = SuperBinaryModule.create(binaryUrl, glueFlavor);
  const serializer = new Serializer(binary);
  const linter = new LocalLinter({ binary, dialect });
  async function processRequest(v) {
    const { procName, args } = await serializer.deserialize(v);
    if (procName in linter) {
      const res = await linter[procName](...args);
      postMessage(await serializer.serializeArg(res));
    }
  }
  self.onmessage = (e2) => {
    if (isSerializedRequest(e2.data)) {
      processRequest(e2.data);
    }
  };
};
var __viteBrowserExternal = {};
var __viteBrowserExternal$1 = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  default: __viteBrowserExternal
});
`,si=typeof self<"u"&&self.Blob&&new Blob(["URL.revokeObjectURL(import.meta.url);",$r],{type:"text/javascript;charset=utf-8"});var un=Uint8Array,et=Uint16Array,jr=Int32Array,xr=new un([0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0,0,0,0]),Ar=new un([0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,0,0]),ai=new un([16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15]),tt=function(r,n){for(var e=new et(31),t=0;t<31;++t)e[t]=n+=1<<r[t-1];for(var i=new jr(e[30]),t=1;t<30;++t)for(var _=e[t];_<e[t+1];++_)i[_]=_-e[t]<<5|t;return{b:e,r:i}},rt=tt(xr,2),Lr=rt.b,zr=rt.r;Lr[28]=258,zr[258]=28;var it=tt(Ar,0),oi=it.b,_i=it.r,Tr=new et(32768);for(b=0;b<32768;++b)P=(b&43690)>>1|(b&21845)<<1,P=(P&52428)>>2|(P&13107)<<2,P=(P&61680)>>4|(P&3855)<<4,Tr[b]=((P&65280)>>8|(P&255)<<8)>>1;var P,b;var Pn=new un(288);for(b=0;b<144;++b)Pn[b]=8;var b;for(b=144;b<256;++b)Pn[b]=9;var b;for(b=256;b<280;++b)Pn[b]=7;var b;for(b=280;b<288;++b)Pn[b]=8;var b,Wr=new un(32);for(b=0;b<32;++b)Wr[b]=5;var b;var Er=new un(0);var Fr=typeof TextDecoder<"u"&&new TextDecoder,Mr=0;try{Fr.decode(Er,{stream:!0}),Mr=1}catch{}var T=Uint8Array,dn=Uint16Array,Or=Int32Array,st=new T([0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0,0,0,0]),at=new T([0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,0,0]),kr=new T([16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15]),ot=function(r,n){for(var e=new dn(31),t=0;t<31;++t)e[t]=n+=1<<r[t-1];for(var i=new Or(e[30]),t=1;t<30;++t)for(var _=e[t];_<e[t+1];++_)i[_]=_-e[t]<<5|t;return{b:e,r:i}},_t=ot(st,2),lt=_t.b,Rr=_t.r;lt[28]=258,Rr[258]=28;var ct=ot(at,0),Cr=ct.b,ci=ct.r,pe=new dn(32768);for(y=0;y<32768;++y)G=(y&43690)>>1|(y&21845)<<1,G=(G&52428)>>2|(G&13107)<<2,G=(G&61680)>>4|(G&3855)<<4,pe[y]=((G&65280)>>8|(G&255)<<8)>>1;var G,y,Tn=(function(r,n,e){for(var t=r.length,i=0,_=new dn(n);i<t;++i)r[i]&&++_[r[i]-1];var o=new dn(n);for(i=1;i<n;++i)o[i]=o[i-1]+_[i-1]<<1;var l;if(e){l=new dn(1<<n);var g=15-n;for(i=0;i<t;++i)if(r[i])for(var d=i<<4|r[i],f=n-r[i],c=o[r[i]-1]++<<f,u=c|(1<<f)-1;c<=u;++c)l[pe[c]>>g]=d}else for(l=new dn(t),i=0;i<t;++i)r[i]&&(l[i]=pe[o[r[i]-1]++]>>15-r[i]);return l}),Wn=new T(288);for(y=0;y<144;++y)Wn[y]=8;var y;for(y=144;y<256;++y)Wn[y]=9;var y;for(y=256;y<280;++y)Wn[y]=7;var y;for(y=280;y<288;++y)Wn[y]=8;var y,gt=new T(32);for(y=0;y<32;++y)gt[y]=5;var y;var Nr=Tn(Wn,9,1);var Dr=Tn(gt,5,1),fe=function(r){for(var n=r[0],e=1;e<r.length;++e)r[e]>n&&(n=r[e]);return n},R=function(r,n,e){var t=n/8|0;return(r[t]|r[t+1]<<8)>>(n&7)&e},ue=function(r,n){var e=n/8|0;return(r[e]|r[e+1]<<8|r[e+2]<<16)>>(n&7)},Ur=function(r){return(r+7)/8|0},me=function(r,n,e){return(n==null||n<0)&&(n=0),(e==null||e>r.length)&&(e=r.length),new T(r.subarray(n,e))};var Ir=["unexpected EOF","invalid block type","invalid length/literal","invalid distance","stream finished","no stream handler",,"no callback","invalid UTF-8 data","extra field too long","date not in range 1980-2099","filename too long","stream finishing","invalid zip data"],z=function(r,n,e){var t=new Error(n||Ir[r]);if(t.code=r,Error.captureStackTrace&&Error.captureStackTrace(t,z),!e)throw t;return t},Br=function(r,n,e,t){var i=r.length,_=t?t.length:0;if(!i||n.f&&!n.l)return e||new T(0);var o=!e,l=o||n.i!=2,g=n.i;o&&(e=new T(i*3));var d=function(xe){var Ae=e.length;if(xe>Ae){var Le=new T(Math.max(Ae*2,xe));Le.set(e),e=Le}},f=n.f||0,c=n.p||0,u=n.b||0,$=n.l,j=n.d,A=n.m,L=n.n,x=i*8;do{if(!$){f=R(r,c,1);var En=R(r,c+1,3);if(c+=3,En)if(En==1)$=Nr,j=Dr,A=9,L=5;else if(En==2){var en=R(r,c,31)+257,pn=R(r,c+10,15)+4,he=en+R(r,c+5,31)+1;c+=14;for(var wn=new T(he),Gn=new T(19),E=0;E<pn;++E)Gn[kr[E]]=R(r,c+E*3,7);c+=pn*3;for(var be=fe(Gn),mt=(1<<be)-1,ht=Tn(Gn,be,1),E=0;E<he;){var ye=ht[R(r,c,mt)];c+=ye&15;var W=ye>>4;if(W<16)wn[E++]=W;else{var tn=0,Fn=0;for(W==16?(Fn=3+R(r,c,3),c+=2,tn=wn[E-1]):W==17?(Fn=3+R(r,c,7),c+=3):W==18&&(Fn=11+R(r,c,127),c+=7);Fn--;)wn[E++]=tn}}var ve=wn.subarray(0,en),H=wn.subarray(en);A=fe(ve),L=fe(H),$=Tn(ve,A,1),j=Tn(H,L,1)}else z(1);else{var W=Ur(c)+4,J=r[W-4]|r[W-3]<<8,q=W+J;if(q>i){g&&z(0);break}l&&d(u+J),e.set(r.subarray(W,q),u),n.b=u+=J,n.p=c=q*8,n.f=f;continue}if(c>x){g&&z(0);break}}l&&d(u+131072);for(var bt=(1<<A)-1,yt=(1<<L)-1,Jn=c;;Jn=c){var tn=$[ue(r,c)&bt],rn=tn>>4;if(c+=tn&15,c>x){g&&z(0);break}if(tn||z(2),rn<256)e[u++]=rn;else if(rn==256){Jn=c,$=null;break}else{var Se=rn-254;if(rn>264){var E=rn-257,mn=st[E];Se=R(r,c,(1<<mn)-1)+lt[E],c+=mn}var qn=j[ue(r,c)&yt],Hn=qn>>4;qn||z(3),c+=qn&15;var H=Cr[Hn];if(Hn>3){var mn=at[Hn];H+=ue(r,c)&(1<<mn)-1,c+=mn}if(c>x){g&&z(0);break}l&&d(u+131072);var $e=u+Se;if(u<H){var je=_-H,vt=Math.min(H,$e);for(je+u<0&&z(3);u<vt;++u)e[u]=t[je+u]}for(;u<$e;++u)e[u]=e[u-H]}}n.l=$,n.p=Jn,n.b=u,n.f=f,$&&(f=1,n.m=A,n.d=j,n.n=L)}while(!f);return u!=e.length&&o?me(e,0,u):e.subarray(0,u)};var Vr=new T(0);var I=function(r,n){return r[n]|r[n+1]<<8},O=function(r,n){return(r[n]|r[n+1]<<8|r[n+2]<<16|r[n+3]<<24)>>>0},de=function(r,n){return O(r,n)+O(r,n+4)*4294967296};function Pr(r,n){return Br(r,{i:2},n&&n.out,n&&n.dictionary)}var we=typeof TextDecoder<"u"&&new TextDecoder,Gr=0;try{we.decode(Vr,{stream:!0}),Gr=1}catch{}var Jr=function(r){for(var n="",e=0;;){var t=r[e++],i=(t>127)+(t>223)+(t>239);if(e+i>r.length)return{s:n,r:me(r,e-1)};i?i==3?(t=((t&15)<<18|(r[e++]&63)<<12|(r[e++]&63)<<6|r[e++]&63)-65536,n+=String.fromCharCode(55296|t>>10,56320|t&1023)):i&1?n+=String.fromCharCode((t&31)<<6|r[e++]&63):n+=String.fromCharCode((t&15)<<12|(r[e++]&63)<<6|r[e++]&63):n+=String.fromCharCode(t)}};function qr(r,n){if(n){for(var e="",t=0;t<r.length;t+=16384)e+=String.fromCharCode.apply(null,r.subarray(t,t+16384));return e}else{if(we)return we.decode(r);var i=Jr(r),_=i.s,e=i.r;return e.length&&z(8),_}}var Hr=function(r,n){return n+30+I(r,n+26)+I(r,n+28)},Kr=function(r,n,e){var t=I(r,n+28),i=I(r,n+30),_=qr(r.subarray(n+46,n+46+t),!(I(r,n+8)&2048)),o=n+46+t,l=Zr(r,o,i,e,O(r,n+20),O(r,n+24),O(r,n+42)),g=l[0],d=l[1],f=l[2];return[I(r,n+10),g,d,_,o+i+I(r,n+32),f]},Zr=function(r,n,e,t,i,_,o){var l=i==4294967295,g=_==4294967295,d=o==4294967295,f=n+e,c=l+g+d;if(t&&c){for(;n+4<f;n+=4+I(r,n+2))if(I(r,n)==1)return[l?de(r,n+4+8*g):i,g?de(r,n+4):_,d?de(r,n+4+8*(g+l)):o,1];t<2&&z(13)}return[i,_,o,0]};function ft(r,n){for(var e={},t=r.length-22;O(r,t)!=101010256;--t)(!t||r.length-t>65558)&&z(13);var i=I(r,t+8);if(!i)return{};var _=O(r,t+16),o=O(r,t-20)==117853008;if(o){var l=O(r,t-12);o=O(r,l)==101075792,o&&(i=O(r,l+32),_=O(r,l+48))}for(var g=n&&n.filter,d=0;d<i;++d){var f=Kr(r,_,o),c=f[0],u=f[1],$=f[2],j=f[3],A=f[4],L=f[5],x=Hr(r,L);_=A,(!g||g({name:j,size:u,originalSize:$,compression:c}))&&(c?c==8?e[j]=Pr(r.subarray(x,x+u),{out:new T($)}):z(14,"unknown compression type "+c):e[j]=me(r,x,x+u))}return e}var nn=null,ut=null,dt="",pt=null,wt=Promise.resolve();function Qr(r){let n=[0];for(let e of r)n.push(n.at(-1)+e.length);return n}function Yr(r,n){for(let e of r.matchAll(/(?:^\s*|[.!?]\s+|\n[\t ]*)(?:he|she|it)[\t ]+(don['’]t)\b/giu)){let t=e[1],i=e.index+e[0].length,_=i-t.length;if(n.some(l=>l.start<i&&l.end>_))continue;let o="doesn"+t[3]+"t";t===t.toUpperCase()?o=o.toUpperCase():t[0]==="D"&&(o="D"+o.slice(1)),n.push({start:_,end:i,problem:t,kind:"Grammar",message:"Use \u201Cdoesn\u2019t\u201D with he, she or it in standard English.",rule:"NotepadSubjectContraction",suggestions:[o]})}}async function Xr(r){let{id:n,type:e,text:t="",language:i="US",personal:_=[]}=r;try{if(e==="init"){let c=atob(r.archive),u=Uint8Array.from(c,j=>j.charCodeAt(0)),$=ft(u)["engine.wasm"];ut=URL.createObjectURL(new Blob([$],{type:"application/wasm"})),nn=new Vn({binary:ce(ut),dialect:X.American}),await nn.setup(),postMessage({id:n,result:{ready:!0,version:"2.13.0"}});return}if(!nn)throw Error("Language engine is not ready");let o=i==="GB"?X.British:X.American;o!==pt&&(await nn.setDialect(o),pt=o);let l=JSON.stringify(_);l!==dt&&(await nn.clearWords(),_.length&&await nn.importWords(_),dt=l);let g=Qr(t),d=await nn.organizedLints(t,{language:"plaintext"}),f=[];for(let[c,u]of Object.entries(d))for(let $ of u)try{let j=$.span(),A=$.get_problem_text(),L=j.start,x=j.end;if(t.slice(L,x)!==A&&(L=g[j.start],x=g[j.end]),j.free(),!Number.isInteger(L)||!Number.isInteger(x)||t.slice(L,x)!==A)continue;let En=A,W=$.suggestions(),J=[];for(let q of W){let en=q.kind(),pn=en===zn.Remove?"":en===zn.InsertAfter?A+q.get_replacement_text():q.get_replacement_text();J.length<8&&!J.includes(pn)&&J.push(pn),q.free()}f.push({start:L,end:x,problem:A,kind:$.lint_kind(),message:$.message(),rule:c,suggestions:J})}finally{$.free()}e==="lint"&&Yr(t,f),postMessage({id:n,result:e==="word"?{correct:!f.some(c=>["spelling","typo"].includes(c.kind.toLowerCase())),suggestions:f.filter(c=>["spelling","typo"].includes(c.kind.toLowerCase())).flatMap(c=>c.suggestions)}:f})}catch(o){postMessage({id:n,error:o.message||String(o)})}}self.onmessage=r=>{wt=wt.catch(()=>{}).then(()=>Xr(r.data))};})();
