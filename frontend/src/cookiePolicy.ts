import CookiePolicy from './landing/CookiePolicy.svelte';

const cookiePolicy = new CookiePolicy({
  target: document.body,
});

export default cookiePolicy;