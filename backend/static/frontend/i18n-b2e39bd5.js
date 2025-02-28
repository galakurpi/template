function noop() { }
function assign(tar, src) {
    // @ts-ignore
    for (const k in src)
        tar[k] = src[k];
    return tar;
}
function run(fn) {
    return fn();
}
function blank_object() {
    return Object.create(null);
}
function run_all(fns) {
    fns.forEach(run);
}
function is_function(thing) {
    return typeof thing === 'function';
}
function safe_not_equal(a, b) {
    return a != a ? b == b : a !== b || ((a && typeof a === 'object') || typeof a === 'function');
}
function is_empty(obj) {
    return Object.keys(obj).length === 0;
}
function subscribe(store, ...callbacks) {
    if (store == null) {
        return noop;
    }
    const unsub = store.subscribe(...callbacks);
    return unsub.unsubscribe ? () => unsub.unsubscribe() : unsub;
}
function component_subscribe(component, store, callback) {
    component.$$.on_destroy.push(subscribe(store, callback));
}
function create_slot(definition, ctx, $$scope, fn) {
    if (definition) {
        const slot_ctx = get_slot_context(definition, ctx, $$scope, fn);
        return definition[0](slot_ctx);
    }
}
function get_slot_context(definition, ctx, $$scope, fn) {
    return definition[1] && fn
        ? assign($$scope.ctx.slice(), definition[1](fn(ctx)))
        : $$scope.ctx;
}
function get_slot_changes(definition, $$scope, dirty, fn) {
    if (definition[2] && fn) {
        const lets = definition[2](fn(dirty));
        if ($$scope.dirty === undefined) {
            return lets;
        }
        if (typeof lets === 'object') {
            const merged = [];
            const len = Math.max($$scope.dirty.length, lets.length);
            for (let i = 0; i < len; i += 1) {
                merged[i] = $$scope.dirty[i] | lets[i];
            }
            return merged;
        }
        return $$scope.dirty | lets;
    }
    return $$scope.dirty;
}
function update_slot_base(slot, slot_definition, ctx, $$scope, slot_changes, get_slot_context_fn) {
    if (slot_changes) {
        const slot_context = get_slot_context(slot_definition, ctx, $$scope, get_slot_context_fn);
        slot.p(slot_context, slot_changes);
    }
}
function get_all_dirty_from_scope($$scope) {
    if ($$scope.ctx.length > 32) {
        const dirty = [];
        const length = $$scope.ctx.length / 32;
        for (let i = 0; i < length; i++) {
            dirty[i] = -1;
        }
        return dirty;
    }
    return -1;
}
function exclude_internal_props(props) {
    const result = {};
    for (const k in props)
        if (k[0] !== '$')
            result[k] = props[k];
    return result;
}
function compute_rest_props(props, keys) {
    const rest = {};
    keys = new Set(keys);
    for (const k in props)
        if (!keys.has(k) && k[0] !== '$')
            rest[k] = props[k];
    return rest;
}
function set_store_value(store, ret, value) {
    store.set(value);
    return ret;
}

const globals = (typeof window !== 'undefined'
    ? window
    : typeof globalThis !== 'undefined'
        ? globalThis
        : global);
function append(target, node) {
    target.appendChild(node);
}
function insert(target, node, anchor) {
    target.insertBefore(node, anchor || null);
}
function detach(node) {
    if (node.parentNode) {
        node.parentNode.removeChild(node);
    }
}
function destroy_each(iterations, detaching) {
    for (let i = 0; i < iterations.length; i += 1) {
        if (iterations[i])
            iterations[i].d(detaching);
    }
}
function element(name) {
    return document.createElement(name);
}
function svg_element(name) {
    return document.createElementNS('http://www.w3.org/2000/svg', name);
}
function text(data) {
    return document.createTextNode(data);
}
function space() {
    return text(' ');
}
function empty() {
    return text('');
}
function listen(node, event, handler, options) {
    node.addEventListener(event, handler, options);
    return () => node.removeEventListener(event, handler, options);
}
function prevent_default(fn) {
    return function (event) {
        event.preventDefault();
        // @ts-ignore
        return fn.call(this, event);
    };
}
function attr(node, attribute, value) {
    if (value == null)
        node.removeAttribute(attribute);
    else if (node.getAttribute(attribute) !== value)
        node.setAttribute(attribute, value);
}
function set_svg_attributes(node, attributes) {
    for (const key in attributes) {
        attr(node, key, attributes[key]);
    }
}
function children(element) {
    return Array.from(element.childNodes);
}
function set_data(text, data) {
    data = '' + data;
    if (text.data === data)
        return;
    text.data = data;
}
function set_input_value(input, value) {
    input.value = value == null ? '' : value;
}
function set_style(node, key, value, important) {
    if (value == null) {
        node.style.removeProperty(key);
    }
    else {
        node.style.setProperty(key, value, important ? 'important' : '');
    }
}
function select_option(select, value, mounting) {
    for (let i = 0; i < select.options.length; i += 1) {
        const option = select.options[i];
        if (option.__value === value) {
            option.selected = true;
            return;
        }
    }
    if (!mounting || value !== undefined) {
        select.selectedIndex = -1; // no option should be selected
    }
}
function select_value(select) {
    const selected_option = select.querySelector(':checked');
    return selected_option && selected_option.__value;
}
function toggle_class(element, name, toggle) {
    element.classList[toggle ? 'add' : 'remove'](name);
}
function custom_event(type, detail, { bubbles = false, cancelable = false } = {}) {
    const e = document.createEvent('CustomEvent');
    e.initCustomEvent(type, bubbles, cancelable, detail);
    return e;
}

let current_component;
function set_current_component(component) {
    current_component = component;
}
function get_current_component() {
    if (!current_component)
        throw new Error('Function called outside component initialization');
    return current_component;
}
/**
 * The `onMount` function schedules a callback to run as soon as the component has been mounted to the DOM.
 * It must be called during the component's initialisation (but doesn't need to live *inside* the component;
 * it can be called from an external module).
 *
 * `onMount` does not run inside a [server-side component](/docs#run-time-server-side-component-api).
 *
 * https://svelte.dev/docs#run-time-svelte-onmount
 */
function onMount(fn) {
    get_current_component().$$.on_mount.push(fn);
}
/**
 * Creates an event dispatcher that can be used to dispatch [component events](/docs#template-syntax-component-directives-on-eventname).
 * Event dispatchers are functions that can take two arguments: `name` and `detail`.
 *
 * Component events created with `createEventDispatcher` create a
 * [CustomEvent](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent).
 * These events do not [bubble](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events#Event_bubbling_and_capture).
 * The `detail` argument corresponds to the [CustomEvent.detail](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent/detail)
 * property and can contain any type of data.
 *
 * https://svelte.dev/docs#run-time-svelte-createeventdispatcher
 */
function createEventDispatcher() {
    const component = get_current_component();
    return (type, detail, { cancelable = false } = {}) => {
        const callbacks = component.$$.callbacks[type];
        if (callbacks) {
            // TODO are there situations where events could be dispatched
            // in a server (non-DOM) environment?
            const event = custom_event(type, detail, { cancelable });
            callbacks.slice().forEach(fn => {
                fn.call(component, event);
            });
            return !event.defaultPrevented;
        }
        return true;
    };
}

const dirty_components = [];
const binding_callbacks = [];
let render_callbacks = [];
const flush_callbacks = [];
const resolved_promise = /* @__PURE__ */ Promise.resolve();
let update_scheduled = false;
function schedule_update() {
    if (!update_scheduled) {
        update_scheduled = true;
        resolved_promise.then(flush);
    }
}
function add_render_callback(fn) {
    render_callbacks.push(fn);
}
// flush() calls callbacks in this order:
// 1. All beforeUpdate callbacks, in order: parents before children
// 2. All bind:this callbacks, in reverse order: children before parents.
// 3. All afterUpdate callbacks, in order: parents before children. EXCEPT
//    for afterUpdates called during the initial onMount, which are called in
//    reverse order: children before parents.
// Since callbacks might update component values, which could trigger another
// call to flush(), the following steps guard against this:
// 1. During beforeUpdate, any updated components will be added to the
//    dirty_components array and will cause a reentrant call to flush(). Because
//    the flush index is kept outside the function, the reentrant call will pick
//    up where the earlier call left off and go through all dirty components. The
//    current_component value is saved and restored so that the reentrant call will
//    not interfere with the "parent" flush() call.
// 2. bind:this callbacks cannot trigger new flush() calls.
// 3. During afterUpdate, any updated components will NOT have their afterUpdate
//    callback called a second time; the seen_callbacks set, outside the flush()
//    function, guarantees this behavior.
const seen_callbacks = new Set();
let flushidx = 0; // Do *not* move this inside the flush() function
function flush() {
    // Do not reenter flush while dirty components are updated, as this can
    // result in an infinite loop. Instead, let the inner flush handle it.
    // Reentrancy is ok afterwards for bindings etc.
    if (flushidx !== 0) {
        return;
    }
    const saved_component = current_component;
    do {
        // first, call beforeUpdate functions
        // and update components
        try {
            while (flushidx < dirty_components.length) {
                const component = dirty_components[flushidx];
                flushidx++;
                set_current_component(component);
                update(component.$$);
            }
        }
        catch (e) {
            // reset dirty state to not end up in a deadlocked state and then rethrow
            dirty_components.length = 0;
            flushidx = 0;
            throw e;
        }
        set_current_component(null);
        dirty_components.length = 0;
        flushidx = 0;
        while (binding_callbacks.length)
            binding_callbacks.pop()();
        // then, once components are updated, call
        // afterUpdate functions. This may cause
        // subsequent updates...
        for (let i = 0; i < render_callbacks.length; i += 1) {
            const callback = render_callbacks[i];
            if (!seen_callbacks.has(callback)) {
                // ...so guard against infinite loops
                seen_callbacks.add(callback);
                callback();
            }
        }
        render_callbacks.length = 0;
    } while (dirty_components.length);
    while (flush_callbacks.length) {
        flush_callbacks.pop()();
    }
    update_scheduled = false;
    seen_callbacks.clear();
    set_current_component(saved_component);
}
function update($$) {
    if ($$.fragment !== null) {
        $$.update();
        run_all($$.before_update);
        const dirty = $$.dirty;
        $$.dirty = [-1];
        $$.fragment && $$.fragment.p($$.ctx, dirty);
        $$.after_update.forEach(add_render_callback);
    }
}
/**
 * Useful for example to execute remaining `afterUpdate` callbacks before executing `destroy`.
 */
function flush_render_callbacks(fns) {
    const filtered = [];
    const targets = [];
    render_callbacks.forEach((c) => fns.indexOf(c) === -1 ? filtered.push(c) : targets.push(c));
    targets.forEach((c) => c());
    render_callbacks = filtered;
}
const outroing = new Set();
let outros;
function group_outros() {
    outros = {
        r: 0,
        c: [],
        p: outros // parent group
    };
}
function check_outros() {
    if (!outros.r) {
        run_all(outros.c);
    }
    outros = outros.p;
}
function transition_in(block, local) {
    if (block && block.i) {
        outroing.delete(block);
        block.i(local);
    }
}
function transition_out(block, local, detach, callback) {
    if (block && block.o) {
        if (outroing.has(block))
            return;
        outroing.add(block);
        outros.c.push(() => {
            outroing.delete(block);
            if (callback) {
                if (detach)
                    block.d(1);
                callback();
            }
        });
        block.o(local);
    }
    else if (callback) {
        callback();
    }
}

function get_spread_update(levels, updates) {
    const update = {};
    const to_null_out = {};
    const accounted_for = { $$scope: 1 };
    let i = levels.length;
    while (i--) {
        const o = levels[i];
        const n = updates[i];
        if (n) {
            for (const key in o) {
                if (!(key in n))
                    to_null_out[key] = 1;
            }
            for (const key in n) {
                if (!accounted_for[key]) {
                    update[key] = n[key];
                    accounted_for[key] = 1;
                }
            }
            levels[i] = n;
        }
        else {
            for (const key in o) {
                accounted_for[key] = 1;
            }
        }
    }
    for (const key in to_null_out) {
        if (!(key in update))
            update[key] = undefined;
    }
    return update;
}
function get_spread_object(spread_props) {
    return typeof spread_props === 'object' && spread_props !== null ? spread_props : {};
}
function create_component(block) {
    block && block.c();
}
function mount_component(component, target, anchor, customElement) {
    const { fragment, after_update } = component.$$;
    fragment && fragment.m(target, anchor);
    if (!customElement) {
        // onMount happens before the initial afterUpdate
        add_render_callback(() => {
            const new_on_destroy = component.$$.on_mount.map(run).filter(is_function);
            // if the component was destroyed immediately
            // it will update the `$$.on_destroy` reference to `null`.
            // the destructured on_destroy may still reference to the old array
            if (component.$$.on_destroy) {
                component.$$.on_destroy.push(...new_on_destroy);
            }
            else {
                // Edge case - component was destroyed immediately,
                // most likely as a result of a binding initialising
                run_all(new_on_destroy);
            }
            component.$$.on_mount = [];
        });
    }
    after_update.forEach(add_render_callback);
}
function destroy_component(component, detaching) {
    const $$ = component.$$;
    if ($$.fragment !== null) {
        flush_render_callbacks($$.after_update);
        run_all($$.on_destroy);
        $$.fragment && $$.fragment.d(detaching);
        // TODO null out other refs, including component.$$ (but need to
        // preserve final state?)
        $$.on_destroy = $$.fragment = null;
        $$.ctx = [];
    }
}
function make_dirty(component, i) {
    if (component.$$.dirty[0] === -1) {
        dirty_components.push(component);
        schedule_update();
        component.$$.dirty.fill(0);
    }
    component.$$.dirty[(i / 31) | 0] |= (1 << (i % 31));
}
function init(component, options, instance, create_fragment, not_equal, props, append_styles, dirty = [-1]) {
    const parent_component = current_component;
    set_current_component(component);
    const $$ = component.$$ = {
        fragment: null,
        ctx: [],
        // state
        props,
        update: noop,
        not_equal,
        bound: blank_object(),
        // lifecycle
        on_mount: [],
        on_destroy: [],
        on_disconnect: [],
        before_update: [],
        after_update: [],
        context: new Map(options.context || (parent_component ? parent_component.$$.context : [])),
        // everything else
        callbacks: blank_object(),
        dirty,
        skip_bound: false,
        root: options.target || parent_component.$$.root
    };
    append_styles && append_styles($$.root);
    let ready = false;
    $$.ctx = instance
        ? instance(component, options.props || {}, (i, ret, ...rest) => {
            const value = rest.length ? rest[0] : ret;
            if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
                if (!$$.skip_bound && $$.bound[i])
                    $$.bound[i](value);
                if (ready)
                    make_dirty(component, i);
            }
            return ret;
        })
        : [];
    $$.update();
    ready = true;
    run_all($$.before_update);
    // `false` as a special case of no DOM component
    $$.fragment = create_fragment ? create_fragment($$.ctx) : false;
    if (options.target) {
        if (options.hydrate) {
            const nodes = children(options.target);
            // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
            $$.fragment && $$.fragment.l(nodes);
            nodes.forEach(detach);
        }
        else {
            // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
            $$.fragment && $$.fragment.c();
        }
        if (options.intro)
            transition_in(component.$$.fragment);
        mount_component(component, options.target, options.anchor, options.customElement);
        flush();
    }
    set_current_component(parent_component);
}
/**
 * Base class for Svelte components. Used when dev=false.
 */
class SvelteComponent {
    $destroy() {
        destroy_component(this, 1);
        this.$destroy = noop;
    }
    $on(type, callback) {
        if (!is_function(callback)) {
            return noop;
        }
        const callbacks = (this.$$.callbacks[type] || (this.$$.callbacks[type] = []));
        callbacks.push(callback);
        return () => {
            const index = callbacks.indexOf(callback);
            if (index !== -1)
                callbacks.splice(index, 1);
        };
    }
    $set($$props) {
        if (this.$$set && !is_empty($$props)) {
            this.$$.skip_bound = true;
            this.$$set($$props);
            this.$$.skip_bound = false;
        }
    }
}

const subscriber_queue = [];
/**
 * Create a `Writable` store that allows both updating and reading by subscription.
 * @param {*=}value initial value
 * @param {StartStopNotifier=} start
 */
function writable(value, start = noop) {
    let stop;
    const subscribers = new Set();
    function set(new_value) {
        if (safe_not_equal(value, new_value)) {
            value = new_value;
            if (stop) { // store is ready
                const run_queue = !subscriber_queue.length;
                for (const subscriber of subscribers) {
                    subscriber[1]();
                    subscriber_queue.push(subscriber, value);
                }
                if (run_queue) {
                    for (let i = 0; i < subscriber_queue.length; i += 2) {
                        subscriber_queue[i][0](subscriber_queue[i + 1]);
                    }
                    subscriber_queue.length = 0;
                }
            }
        }
    }
    function update(fn) {
        set(fn(value));
    }
    function subscribe(run, invalidate = noop) {
        const subscriber = [run, invalidate];
        subscribers.add(subscriber);
        if (subscribers.size === 1) {
            stop = start(set) || noop;
        }
        run(value);
        return () => {
            subscribers.delete(subscriber);
            if (subscribers.size === 0 && stop) {
                stop();
                stop = null;
            }
        };
    }
    return { set, update, subscribe };
}

var meta$1 = {
	title: "AI Automation Solutions for Businesses | Yekar",
	description: "Transform your business operations with our AI automation solutions. Increase efficiency, reduce costs, and improve customer experience with Yekar."
};
var hero$1 = {
	title: "Optimize Your Business with AI",
	subtitle: "We study your business processes in depth and apply solutions to reduce costs and save time.",
	primaryButton: "Contact Us",
	secondaryButton: ""
};
var benefits$1 = {
	title: "How Can We Help You?",
	description: "AI will transform every sector.\nWe ensure this change propels your business forward, not left behind.",
	items: [
		{
			title: "Greater Efficiency",
			description: "We help automate tasks to reduce costs and save time."
		},
		{
			title: "Guaranteed Security",
			description: "We implement solutions with rigorous protocols that protect your data and operations."
		},
		{
			title: "Better Customer Experience",
			description: "Deliver personalized interactions and faster response times.\nBoth in the purchase process and post-purchase."
		},
		{
			title: "Decision Making",
			description: "Leverage your company's data to make better strategic decisions."
		}
	]
};
var process$1 = {
	title: "How We Implement",
	description: "A structured approach that minimizes disruption.",
	steps: [
		{
			number: "01",
			title: "Education",
			description: "We teach you how AI works. The basics and the latest advancements. Also the possible risks and benefits for your business."
		},
		{
			number: "02",
			title: "Assessment",
			description: "We study your processes to identify automations with the highest potential impact.\nWe create an action plan for your business."
		},
		{
			number: "03",
			title: "Development",
			description: "We build customized solutions that integrate into your business context."
		},
		{
			number: "04",
			title: "Tracking",
			description: "We measure the performance of applied solutions to ensure they work.\nWe continuously improve your automations.\nWe keep you updated on the latest AI developments."
		}
	]
};
var caseStudies$1 = {
	title: "Solutions",
	description: "Yekar started as a software product company.\nWe've added internal automations and see the big difference they make.\nWe want to take this change to the world. Here are some of our examples:",
	cases: [
		{
			industry: "Marketing",
			title: "Automated video creation",
			description: "We reduced the time it takes to create a short marketing video from 3 hours to 30 minutes.",
			metrics: [
				"Time saved: 150 minutes per video",
				"6x faster",
				"Consistent quality"
			]
		},
		{
			industry: "Product development",
			title: "Automated internal documentation search",
			description: "We structured our internal documentation and we use AI to find what we need in seconds (primarily related to software development).",
			metrics: [
				"Software development 50% faster",
				"Error reduction",
				"User experience improvement"
			]
		}
	],
	possibilities: {
		title: "Endless Possibilities",
		departments: [
			{
				name: "Marketing",
				description: "Automatic content creation and publishing, refinement based on data analysis."
			},
			{
				name: "Sales",
				description: "Sales automation, outbound lead generation, and customer relationship management."
			},
			{
				name: "Customer Support",
				description: "Ticket management, customer service, and product support."
			},
			{
				name: "HR",
				description: "Recruitment process optimization and talent management."
			},
			{
				name: "Finance",
				description: "Report automation, cost analysis, and predictive analysis."
			},
			{
				name: "Product Development",
				description: "Process optimization and market analysis."
			}
		],
		conclusion: "We have identified and designed specific automations internally that we are now ready to implement in our and other businesses."
	}
};
var cta$1 = {
	title: "Let's talk about your case",
	description: "Schedule a consultation to talk about your company and see how you can leverage AI.",
	primaryButton: "Contact Us",
	secondaryButton: ""
};
var contact$1 = {
	title: "Contact Us - AI Automation Solutions | Yekar",
	description: "Do you have an exciting AI idea, a question, or just want to chat about our work? We're here to listen! Get in touch, and we will be ready to help, guide, or simply share in your enthusiasm. Let's create a memorable AI journey together!",
	heading: "Get in Touch",
	subheading: "Schedule a free consultation to discuss how AI automation can address your specific business challenges",
	nameLabel: "What is your name?",
	namePlaceholder: "Name",
	emailLabel: "What is your email?",
	emailPlaceholder: "Email",
	roleLabel: "What is your role within your organization?",
	rolePlaceholder: "Enter role",
	companyNameLabel: "Company name?",
	companyNamePlaceholder: "Enter company name",
	companyWebsiteLabel: "Company website?",
	companyWebsitePlaceholder: "Enter company website",
	companySizeLabel: "Company size?",
	companySizeOptions: {
		option1: "Less than 20 people",
		option2: "20-50 people",
		option3: "51-200 people",
		option4: "201-500 people",
		option5: "501-1000 people",
		option6: "1001+ people"
	},
	revenueLabel: "Company's annual revenue?",
	revenueOptions: {
		option1: "Less than $100K/month",
		option2: "$100K-$500K/month",
		option3: "$500K-$1M/month",
		option4: "$1M-$5M/month",
		option5: "$5M+/month"
	},
	budgetLabel: "Project budget?",
	budgetOptions: {
		option1: "$0 - $5000",
		option2: "$5000 - $10000",
		option3: "$10000 - $25000",
		option4: "$25000 - $50000",
		option5: "$50000+"
	},
	servicesLabel: "What services are you interested in?",
	servicesOptions: {
		option1: "Developing a custom AI solution",
		option2: "AI integration with existing systems",
		option3: "AI strategy consulting",
		option4: "Data analysis and insights",
		option5: "AI automation",
		option6: "Other"
	},
	messageLabel: "How can we help?",
	messagePlaceholder: "Type your response here...",
	submitButton: "Submit",
	successMessage: "Thank you for your inquiry. We will contact you shortly."
};
var en = {
	meta: meta$1,
	hero: hero$1,
	benefits: benefits$1,
	process: process$1,
	caseStudies: caseStudies$1,
	cta: cta$1,
	contact: contact$1
};

var meta = {
	title: "Soluciones de Automatización con IA para Empresas | Yekar",
	description: "Transforma las operaciones de tu empresa con nuestras soluciones de automatización con IA. Aumenta la eficiencia, reduce costos y mejora la experiencia del cliente con Yekar."
};
var hero = {
	title: "Optimiza tu empresa con IA",
	subtitle: "Estudiamos los procesos de tu empresa a fondo y aplicamos soluciones para reducir costes y ganar tiempo.",
	primaryButton: "Contáctanos",
	secondaryButton: ""
};
var benefits = {
	title: "¿Cómo te podemos ayudar?",
	description: "La IA transformará todos los sectores.\nNos aseguramos de que este cambio no te deje atrás.",
	items: [
		{
			title: "Mayor eficiencia",
			description: "Ayudamos a automatizar tareas para reducir costes y ganar tiempo."
		},
		{
			title: "Seguridad garantizada",
			description: "Implementamos los protocolos necesarios para proteger tus datos y operaciones."
		},
		{
			title: "Mejor experiencia del cliente",
			description: "Ofrece interacciones personalizadas y tiempos de respuesta más rápidos.\nTanto en el proceso de compra como en el post-venta."
		},
		{
			title: "Toma de decisiones",
			description: "Aprovecha los datos de tu empresa para tomar mejores decisiones estratégicas."
		}
	]
};
var process = {
	title: "Cómo Implementamos",
	description: "Un enfoque estructurado que minimiza la interrupción.",
	steps: [
		{
			number: "01",
			title: "Actualización",
			description: "Te actualizamos con cuáles son los últimos desarrollos de la IA y los mayores riesgos y ventajas para tu empresa."
		},
		{
			number: "02",
			title: "Evaluación",
			description: "Estudiamos tus procesos para identificar automatizaciones con el mayor potencial de impacto. Creamos un plan de acción para tu empresa."
		},
		{
			number: "03",
			title: "Desarrollo",
			description: "Construimos soluciones personalizadas que se integran en el contexto de tu empresa."
		},
		{
			number: "04",
			title: "Seguimiento",
			description: "Medimos el rendimiento de las soluciones aplicadas para asegurarnos de que funcionan de verdad.\nAñadimos mejoras continuas a tus automatizaciones.\nTe mantenemos actualizado sobre las últimas novedades de la IA."
		}
	]
};
var caseStudies = {
	title: "Soluciones",
	description: "Yekar comenzó como una empresa de software.\nHemos añadido automatizaciones internamente y vemos la gran diferencia que suponen.\nQueremos llevar este cambio a todo el mundo. Estos son algunos de nuestros ejemplos:",
	cases: [
		{
			industry: "Marketing",
			title: "Creación automática de videos",
			description: "Hemos creado un sistema que crea ideas y guiones de vídeos y los narra automáticamente con IA.\nReducimos el tiempo que se tarda en crear un video de marketing de 3 horas a 30 minutos.",
			metrics: [
				"Tiempo ahorrado: 150 minutos por video",
				"6 veces más rápido",
				"Calidad consistente"
			]
		},
		{
			industry: "Desarrollo de producto",
			title: "Búsqueda automática de documentación interna",
			description: "Estructuramos nuestra documentación interna y utilizamos la IA para encontrar lo que necesitamos en segundos (principalmente relacionado al desarrollo de software).",
			metrics: [
				"Desarrollo de software 50% más rápido",
				"Reducción de errores",
				"Mejora de la experiencia del usuario"
			]
		}
	],
	possibilities: {
		title: "Posibilidades infinitas",
		departments: [
			{
				name: "Marketing",
				description: "Creación de contenido automática y publicación, refinamiento basado en el análisis de datos."
			},
			{
				name: "Ventas",
				description: "Automatización de ventas, generación de leads outbound y gestión de relaciones con clientes."
			},
			{
				name: "Soporte al cliente",
				description: "Gestión de tickets, servicio al cliente y soporte del producto."
			},
			{
				name: "RRHH",
				description: "Optimización del proceso de contratación y gestión del talento."
			},
			{
				name: "Finanzas",
				description: "Automatización de informes, análisis de costes y análisis predictivo."
			},
			{
				name: "Desarrollo de producto",
				description: "Optimización de procesos y análisis de mercado."
			}
		],
		conclusion: "Hemos identificado y diseñado automatizaciones específicas internamente que ahora estamos listos para implementar en nuestra empresa y en otras."
	}
};
var cta = {
	title: "Hablemos de tu caso",
	description: "Programa una consulta para hablar de tu empresa y ver cómo puedes aprovechar la IA.",
	primaryButton: "Contáctanos",
	secondaryButton: ""
};
var contact = {
	title: "Contáctanos - Soluciones de Automatización con IA | Yekar",
	description: "¿Tienes una idea interesante de IA, una pregunta o simplemente quieres hablar de nuestro trabajo? Estamos aquí para escucharte. Ponte en contacto y estaremos listos para ayudarte, guiarte o simplemente compartir tu entusiasmo. ¡Vamos a crear una experiencia de IA memorable juntos!",
	heading: "Ponte en Contacto",
	subheading: "Programa una consulta gratuita para discutir cómo la automatización con IA puede abordar tus desafíos empresariales específicos.",
	nameLabel: "¿Cuál es tu nombre?",
	namePlaceholder: "Nombre",
	emailLabel: "¿Cuál es tu correo electrónico?",
	emailPlaceholder: "Correo electrónico",
	roleLabel: "¿Cuál es tu rol dentro de tu organización?",
	rolePlaceholder: "Ingresa tu rol",
	companyNameLabel: "¿Nombre de la empresa?",
	companyNamePlaceholder: "Ingresa el nombre de la empresa",
	companyWebsiteLabel: "¿Sitio web de la empresa?",
	companyWebsitePlaceholder: "Ingresa el sitio web de la empresa",
	companySizeLabel: "¿Tamaño de la empresa?",
	companySizeOptions: {
		option1: "Menos de 20 personas",
		option2: "20-50 personas",
		option3: "51-200 personas",
		option4: "201-500 personas",
		option5: "501-1000 personas",
		option6: "Más de 1000 personas"
	},
	revenueLabel: "¿Ingresos anuales de la empresa?",
	revenueOptions: {
		option1: "Menos de 100.000€/mes",
		option2: "100.000€-500.000€/mes",
		option3: "500.000€-1.000.000€/mes",
		option4: "1.000.000€-5.000.000€/mes",
		option5: "Más de 5.000.000€/mes"
	},
	budgetLabel: "¿Presupuesto del proyecto?",
	budgetOptions: {
		option1: "0 - 5.000€",
		option2: "5.000€ - 10.000€",
		option3: "10.000€ - 25.000€",
		option4: "25.000€ - 50.000€",
		option5: "Más de 50.000€"
	},
	servicesLabel: "¿Qué servicios te interesan?",
	servicesOptions: {
		option1: "Desarrollo de una solución de IA personalizada",
		option2: "Integración de IA con sistemas existentes",
		option3: "Consultoría de estrategia de IA",
		option4: "Análisis de datos e insights",
		option5: "Automatización con IA",
		option6: "Otro"
	},
	messageLabel: "¿Cómo podemos ayudarte?",
	messagePlaceholder: "Escribe tu mensaje aquí...",
	submitButton: "Enviar",
	successMessage: "Gracias por tu consulta. Nos pondremos en contacto contigo pronto."
};
var es = {
	meta: meta,
	hero: hero,
	benefits: benefits,
	process: process,
	caseStudies: caseStudies,
	cta: cta,
	contact: contact
};

const aiBusinessTranslations = {
    en,
    es
};

const featureTranslations = {
    aiBusiness: aiBusinessTranslations
};

const translations = {
    en: () => import('./en-086b5dc2.js'),
    es: () => import('./es-d8e1eb69.js'),
};
// Helper function to get browser language
const getBrowserLanguage = () => {
    if (typeof window !== 'undefined') {
        // Get browser language
        const browserLang = navigator.language.toLowerCase();
        // Check if it starts with any of our supported languages
        if (browserLang.startsWith('es')) {
            return 'es';
        }
        // Default to English for all other languages
        return 'en';
    }
    return 'en';
};
// Get initial locale from localStorage, browser language, or default to 'en'
const getInitialLocale = () => {
    if (typeof window !== 'undefined') {
        // First check localStorage for user's previous preference
        const savedLocale = localStorage.getItem('locale');
        if (savedLocale === 'es' || savedLocale === 'en') {
            return savedLocale;
        }
        // If no saved preference, use browser language
        return getBrowserLanguage();
    }
    return 'en';
};
const locale = writable(getInitialLocale());
function createTranslationStore() {
    const { subscribe, set } = writable({});
    return {
        subscribe,
        init: async (currentLocale) => {
            try {
                console.log(`Loading translations for ${currentLocale}`);
                const module = await translations[currentLocale]();
                // Merge main translations with feature translations
                const mainTranslations = module.default || module;
                const localeFeatureTranslations = {};
                // Add feature translations
                Object.keys(featureTranslations).forEach((feature) => {
                    const typedFeatureTranslations = featureTranslations;
                    if (typedFeatureTranslations[feature] && typedFeatureTranslations[feature][currentLocale]) {
                        localeFeatureTranslations[feature] = typedFeatureTranslations[feature][currentLocale];
                    }
                });
                // Merge translations
                const mergedTranslations = {
                    ...mainTranslations,
                    features: {
                        ...mainTranslations.features, // Preserve original features including title
                        ...localeFeatureTranslations // Add feature-specific translations
                    }
                };
                set(mergedTranslations);
                // Save locale preference to localStorage
                if (typeof window !== 'undefined') {
                    localStorage.setItem('locale', currentLocale);
                }
            }
            catch (error) {
                console.error(`Error loading translations for ${currentLocale}:`, error);
                // Fallback to English if there's an error
                if (currentLocale !== 'en') {
                    console.log('Falling back to English translations');
                    const enModule = await translations.en();
                    set(enModule.default || enModule);
                    if (typeof window !== 'undefined') {
                        localStorage.setItem('locale', 'en');
                    }
                }
            }
        },
    };
}
const t = createTranslationStore();
locale.subscribe(($locale) => {
    t.init($locale);
});

export { set_style as A, globals as B, binding_callbacks as C, destroy_each as D, select_option as E, prevent_default as F, select_value as G, assign as H, get_spread_update as I, get_spread_object as J, exclude_internal_props as K, create_slot as L, update_slot_base as M, get_all_dirty_from_scope as N, get_slot_changes as O, check_outros as P, group_outros as Q, svg_element as R, SvelteComponent as S, empty as T, set_svg_attributes as U, compute_rest_props as V, createEventDispatcher as W, space as a, attr as b, insert as c, append as d, element as e, detach as f, component_subscribe as g, set_input_value as h, init as i, set_data as j, t as k, listen as l, toggle_class as m, noop as n, locale as o, onMount as p, set_store_value as q, run_all as r, safe_not_equal as s, text as t, create_component as u, mount_component as v, transition_in as w, transition_out as x, destroy_component as y, add_render_callback as z };
//# sourceMappingURL=i18n-b2e39bd5.js.map
