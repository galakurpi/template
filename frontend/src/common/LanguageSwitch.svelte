<script lang="ts">
  import { locale } from '../i18n.js';
  import { t } from '../i18n.js';
  import { onMount } from 'svelte';

  let currentLocale: string;

  onMount(() => {
    // Initialize with the stored locale
    currentLocale = localStorage.getItem('locale') || 'en';
  });

  function setLanguage(lang: 'en' | 'es') {
    currentLocale = lang;
    $locale = lang;
  }
</script>

<div class="language-switch">
  <button 
    on:click={() => setLanguage('es')} 
    class="language-button" 
    class:active={$locale === 'es'}
    aria-label={$t.languageSwitch?.spanishLabel || "Switch to Spanish"}
  >
    {$t.languageSwitch?.spanish || "ESP"}
  </button>
  <button 
    on:click={() => setLanguage('en')} 
    class="language-button" 
    class:active={$locale === 'en'}
    aria-label={$t.languageSwitch?.englishLabel || "Switch to English"}
  >
    {$t.languageSwitch?.english || "ENG"}
  </button>
</div>

<style>
  .language-switch {
    display: flex;
    background-color: #2f2f2f;
    border-radius: 20px;
    overflow: hidden;
  }

  .language-button {
    background-color: transparent;
    color: #e3e3e3;
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-size: 0.9rem;
    border: none;
    text-transform: uppercase;
    font-weight: 600;
    transition: background-color 0.3s, color 0.3s;
  }

  .language-button:hover {
    background-color: rgba(239, 200, 36, 0.2);
  }

  .language-button.active {
    background-color: #efc824;
    color: #000000;
  }
</style>
