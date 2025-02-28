import svelte from "rollup-plugin-svelte";
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import typescript from '@rollup/plugin-typescript';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import css from 'rollup-plugin-css-only';
import sveltePreprocess from "svelte-preprocess";
import json from '@rollup/plugin-json';

// Determine the directory name
const __dirname = dirname(fileURLToPath(import.meta.url));
const production = !process.env.ROLLUP_WATCH;

// Shared plugins configuration
const sharedPlugins = [
    svelte({
        preprocess: sveltePreprocess({
            sourceMap: !production
        }),
        compilerOptions: {
            dev: !production
        },
        onwarn: (warning, handler) => {
            if (warning.code.startsWith('a11y-')) return;
            handler(warning);
        },
        css: css => {
            css.write('public/build/bundle.css');
        }
    }),
    json(),
    css({ output: 'bundle.css' }),
    resolve({
        browser: true,
        dedupe: ["svelte", "@stripe/stripe-js", "chart.js", "svelte-chartjs"],  // Added chart.js and svelte-chartjs
        exportConditions: ['svelte', 'browser', 'module', 'default'],
        extensions: ['.svelte', '.js', '.ts', '.mjs', '.json', '.node'],
        mainFields: ['browser', 'module', 'main'],
        preferBuiltins: false
    }),
    commonjs({
        include: ['node_modules/**'],
        requireReturnsDefault: 'auto',
        transformMixedEsModules: true
    }),
    typescript({
        sourceMap: true,
        inlineSources: !production,
        tsconfig: './tsconfig.json',
    }),
];

export default {
    input: ["src/login.ts", "src/register.ts",
        "src/landing.ts", "src/landingContact.ts", "src/register.ts", "src/privacyPolicy.ts", 
        "src/cookiePolicy.ts", "src/success.ts", "src/cancel.ts", "src/termsOfService.ts", "src/accountSettings.ts",
    ],
    output: {
        sourcemap: true,
        format: "es",
        dir: join(__dirname, "build/dist/static/frontend"),
    },
    plugins: sharedPlugins,
    external: [],
    preserveEntrySignatures: false,
};