<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { t } from '../i18n.js';  // Import the translation store
    import { User } from 'lucide-svelte';  // Import the User icon
  
    const dispatch = createEventDispatcher();
  
    export let currentPage: string = 'landing';
    $: isLandingPage = currentPage === 'landing' || currentPage === 'landing-contact';
    $: currentPage = currentPage === 'pricing' || currentPage === 'landing' || currentPage === 'landing-contact' ? currentPage : 'landing';

    function handleLogoClick() {
      window.location.href = "/landing";
    }

    function handleStartNowClick(event: Event) {
      event.preventDefault();
      if (currentPage === 'landing') {
        window.location.href = "/pricing?from=start_now";
      } else {
        window.location.href = "/register";
      }
    }

    function handleAccountSettingsClick() {
      window.location.href = "/account-settings";
    }
</script>
  
<nav>
    <div class="left-section">
      <div class="logo-holder" on:click={handleLogoClick}>
        <img src="/static/icons/YekarLogo.svg" alt="Yekar-Logo" />
      </div>
    </div>
    <div class="right-section">
      <a href="/landing" class="nav-button">{$t.nav?.landing || 'AI Solutions'}</a>
      {#if !isLandingPage}
        <a href="/pricing" class="nav-button">{$t.nav?.pricing || 'Pricing'}</a>
        <a href="/api/login" class="nav-button">{$t.nav?.login || 'Log in'}</a>
        <button on:click={handleAccountSettingsClick} class="account-button" title={$t.nav?.accountSettings || 'Account Settings'}>
          <User size={24} />
        </button>
        <a href="#" class="nav-button highlight" on:click={handleStartNowClick}>
          {$t.nav?.startNow || 'Start now'}
        </a>
      {/if}
    </div>
  </nav>
  
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Proxima+Nova:wght@400;600&display=swap');

    nav {
      background-color: #000000;
      min-height: 4rem;
      height: auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.5rem 2rem;
      color: #e3e3e3;
      font-family: 'Proxima Nova', sans-serif;
      text-transform: uppercase;
      z-index: 1000;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .left-section {
      display: flex;
      align-items: center;
      gap: 1rem;
      flex: 1;
      min-width: 200px;
    }

    .right-section {
      display: flex;
      align-items: center;
      gap: 1rem;
      flex: 1;
      justify-content: flex-end;
      flex-wrap: wrap;
    }

    .logo-holder {
      cursor: pointer;
      display: flex;
      align-items: center;
    }

    .logo-holder img {
      height: 2.5rem;
      width: auto;
      max-width: 100%;
    }

    .nav-button {
      background-color: transparent;
      color: #e3e3e3;
      padding: 0.5rem 1rem;
      cursor: pointer;
      font-size: 1rem;
      border: none;
      text-decoration: none;
      text-transform: uppercase;
      position: relative;
      font-weight: 600;
      min-width: 44px;
      min-height: 44px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .nav-button::after {
      content: "";
      display: block;
      width: 0;
      height: 3px;
      background-color: #efc824;
      position: absolute;
      bottom: -3px;
      left: 0;
      transition: width 0.3s;
    }

    .nav-button:hover::after {
      width: 100%;
    }

    .highlight {
      background-color: #efc824;
      color: #1b1b1b;
      border-radius: 20px;
      padding: 0.5rem 1rem;
      transition: transform 0.3s ease;
    }

    .highlight:hover {
      transform: scale(1.1);
    }

    .highlight::after {
      display: none;
    }

    .account-button {
      background-color: transparent;
      color: #e3e3e3;
      padding: 0.5rem;
      cursor: pointer;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: color 0.3s ease;
      min-width: 44px;
      min-height: 44px;
    }

    .account-button:hover {
      color: #efc824;
    }

    @media (max-width: 768px) {
      nav {
        padding: 0.5rem 1rem;
        gap: 0.5rem;
      }

      .left-section {
        min-width: 150px;
        gap: 0.5rem;
      }

      .right-section {
        gap: 0.5rem;
      }

      .logo-holder img {
        height: 2rem;
      }

      .nav-button {
        font-size: 0.9rem;
        padding: 0.4rem 0.8rem;
      }

      .highlight {
        padding: 0.4rem 0.8rem;
      }
    }

    @media (max-width: 480px) {
      nav {
        padding: 0.5rem;
        justify-content: center;
      }

      .left-section, .right-section {
        flex: 0 1 100%;
        justify-content: center;
        min-width: unset;
      }

      .left-section {
        order: -1;
      }

      .right-section {
        gap: 0.25rem;
      }

      .nav-button {
        font-size: 0.85rem;
        padding: 0.3rem 0.6rem;
      }

      .highlight {
        padding: 0.3rem 0.6rem;
      }
    }
  </style>
